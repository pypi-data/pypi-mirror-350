import json
import logging
import os.path

from aiddit.create.prompts.create_renshe_comprehension_prompt import (
    NOTE_PROMPT,
    HISTORY_NOTE_TOPIC_MODE_SUMMARY,
    HISTORY_NOTE_SCRIPT_MODE_SUMMARY,
    USER_ACCOUNT_INFO_PROMPT
)
import aiddit.utils as utils
import aiddit.model.google_genai as google_genai
import aiddit.xhs.account_note_list as account_note_list
import aiddit.xhs.note_detail as note_detail


def build_history_messages(history_note_list, account_user_info):
    history_message = []

    user_account_info_prompt = USER_ACCOUNT_INFO_PROMPT.format(account_name=account_user_info.get("account_name"),
                                                               account_description=account_user_info.get("description"),
                                                               note_count=len(history_note_list))
    user_account_info_conversation_message = google_genai.GenaiConversationMessage.text_and_images(
        user_account_info_prompt,
        account_user_info.get("avatar_url"))
    history_message.append(user_account_info_conversation_message)

    for index, h_note in enumerate(history_note_list):
        try:
            # 历史参考帖子
            h_note_images = utils.remove_duplicates(h_note.get("images"))
            h_note_images = [utils.oss_resize_image(i) for i in h_note_images]
            history_note_prompt = NOTE_PROMPT.format(note_index=index + 1,
                                                     channel_content_id=h_note.get("channel_content_id"),
                                                     title=h_note.get("title"), body_text=h_note.get("body_text"),
                                                     image_count=len(h_note_images))
            history_note_conversation_message = google_genai.GenaiConversationMessage.text_and_images(
                history_note_prompt,
                h_note_images)
            history_message.append(history_note_conversation_message)
        except Exception as e:
            print(f"error , str {e}, {json.dumps(h_note, ensure_ascii=False, indent=4)}")

    return history_message


def comprehension_topic_mode(history_note_list, account_user_info):
    history_message = build_history_messages(history_note_list, account_user_info)

    history_note_summary_prompt = HISTORY_NOTE_TOPIC_MODE_SUMMARY.format(note_count=len(history_note_list))
    ask_message_conversation = google_genai.GenaiConversationMessage.one("user", history_note_summary_prompt)
    message_response = google_genai.google_genai_output_images_and_text(ask_message_conversation,
                                                                        model=google_genai.MODEL_GEMINI_2_0_FLASH,
                                                                        temperature=0,
                                                                        history_messages=history_message,
                                                                        response_mime_type="application/json")
    response_content = message_response.content[0].value
    print(response_content)

    return utils.try_remove_markdown_tag_and_to_json(response_content)


def comprehension_script_mode(history_note_list, account_user_info):
    history_message = build_history_messages(history_note_list, account_user_info)

    history_note_script_mode_summary_prompt = HISTORY_NOTE_SCRIPT_MODE_SUMMARY.format(note_count=len(history_note_list))
    ask_message_conversation = google_genai.GenaiConversationMessage.one("user",
                                                                         history_note_script_mode_summary_prompt)
    message_response = google_genai.google_genai_output_images_and_text(ask_message_conversation,
                                                                        model=google_genai.MODEL_GEMINI_2_0_FLASH,
                                                                        temperature=0,
                                                                        history_messages=history_message,
                                                                        response_mime_type="application/json")
    response_content = message_response.content[0].value
    return utils.try_remove_markdown_tag_and_to_json(response_content)


def build_renshe_info(save_dir_path, account_id):
    renshe_info_list = [json.load(open(os.path.join(save_dir_path, i))) for i in os.listdir(save_dir_path) if
                        i.endswith(".json") and account_id in i]

    if len(renshe_info_list) == 0:
        renshe_info = {}
    else:
        renshe_info = renshe_info_list[0]

    if renshe_info.get("account_info") is None:
        account_info = account_note_list.get_account_info(account_id)
        renshe_info["account_info"] = account_info
    else:
        account_info = renshe_info.get("account_info")

    account_name = account_info.get("account_name")

    note_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data"
    # note_dir = f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/comprehension/note_data"
    note_detail_dir = f"{note_dir}/account_{account_name}_{account_id}"

    if not os.path.exists(note_detail_dir) or len(os.listdir(note_detail_dir)) < 5:
        account_note_list.save_account_note(account_id, account_name, note_detail_dir)

    renshe_info["history_note_dir_path"] = note_detail_dir

    note_detail.batch_get_note_detail_with_retries(note_detail_dir)

    save_path = f"{save_dir_path}/account_{account_name}_{account_id}.json"
    utils.save(renshe_info, save_path)

    return renshe_info


if __name__ == "__main__":
    # renshe_dir_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_comprehension/agent_test_account"
    # rs = build_renshe_info(renshe_dir_path,"5c321b93000000000700bbfe")

    renshe_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_comprehension/agent_test_account/account_每天一点心理学_643aadb2000000000d01a5bb.json"
    rs = json.load(open(renshe_path, "r"))
    history_note_dir_path = rs.get("history_note_dir_path")
    account_info = rs.get("account_info")
    note_list = utils.load_from_json_dir(history_note_dir_path)

    if rs.get("选题模式") is None:
        rs["选题模式"] = comprehension_topic_mode(note_list, account_info).get("选题模式")
        utils.save(rs, renshe_path)

    if rs.get("脚本模式") is None:
        rs["脚本模式"] = comprehension_script_mode(note_list, account_info)
        utils.save(rs, renshe_path)
