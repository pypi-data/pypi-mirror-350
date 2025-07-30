import json
import os
from prompts.create_topic_by_history_note_prompt import (
    CREATE_TOPIC_BY_HISTORY_NOTE_PROMPT,
    CREATE_TOPIC_BY_HISTORY_NOTE_AND_XUANTI_MODE_PROMPT,
    CREATE_TOPIC_BY_HISTORY_NOTE_ADN_KNOWLEDGE_PROMPT,
    NOTE_PROMPT,
)
import aiddit.utils as utils
import aiddit.model.google_genai as google_genai
from tqdm import tqdm


def create_topic_from_history_note(stimulus_note, history_note_list, xuanti_mode):
    history_message = []
    for index, h_note in enumerate(history_note_list):
        # 历史参考帖子
        h_note_images = utils.remove_duplicates(h_note.get("images"))
        history_note_prompt = NOTE_PROMPT.format(note_index=index + 1,
                                                 channel_content_id=h_note.get("channel_content_id"),
                                                 title=h_note.get("title"), body_text=h_note.get("body_text"),
                                                 image_count=len(h_note_images))
        history_note_conversation_message = google_genai.GenaiConversationMessage.text_and_images(history_note_prompt,
                                                                                                  h_note_images)
        history_message.append(history_note_conversation_message)

    if stimulus_note.get("content_type") == "video":
        medias = [stimulus_note.get("video", {}).get("video_url")]
    else:
        medias = utils.remove_duplicates(stimulus_note.get("images"))

    knowledge_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/xhs_topic.pdf"
    knowledge_conversation_message =  google_genai.GenaiConversationMessage.text_and_images("这是基于账号人设的小红书图文内容选题策略知识库",
                                                          knowledge_path)
    history_message.append(knowledge_conversation_message)
    create_topic_by_history_note_prompt = CREATE_TOPIC_BY_HISTORY_NOTE_ADN_KNOWLEDGE_PROMPT.format(
        note_count=len(history_note_list),
        channel_content_id=stimulus_note.get(
            "channel_content_id"),
        title=stimulus_note.get("title"),
        body_text=stimulus_note.get(
            "body_text"),
        image_count=len(
            medias))

    # if xuanti_mode is not None:
    #     create_topic_by_history_note_prompt = CREATE_TOPIC_BY_HISTORY_NOTE_AND_XUANTI_MODE_PROMPT.format(
    #         note_count=len(history_note_list),
    #         xuanti_mode=json.dumps(xuanti_mode, ensure_ascii=False, indent=4),
    #         channel_content_id=stimulus_note.get(
    #             "channel_content_id"),
    #         title=stimulus_note.get("title"),
    #         body_text=stimulus_note.get(
    #             "body_text"),
    #         image_count=len(
    #             medias))
    # else:
    #     create_topic_by_history_note_prompt = CREATE_TOPIC_BY_HISTORY_NOTE_PROMPT.format(
    #         note_count=len(history_note_list),
    #         channel_content_id=stimulus_note.get(
    #             "channel_content_id"),
    #         title=stimulus_note.get("title"),
    #         body_text=stimulus_note.get(
    #             "body_text"),
    #         image_count=len(
    #             medias))

    ask_message_conversation = google_genai.GenaiConversationMessage.text_and_images(
        create_topic_by_history_note_prompt, medias)
    ask_response_conversation = google_genai.google_genai_output_images_and_text(ask_message_conversation,
                                                                                 model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                                 history_messages=history_message,
                                                                                 response_mime_type="application/json")

    print(ask_response_conversation.content[0].value)

    return utils.try_remove_markdown_tag_and_to_json(ask_response_conversation.content[0].value)


if __name__ == "__main__":
    renshe_info = json.load(open(
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_comprehension/agent_test_account/account_脆肚火锅噗噜噗噜_5c0aa4ce000000000500b192.json",
        "r"))
    history_note_dir_path = renshe_info.get("history_note_dir_path")

    hnl = utils.load_from_json_dir(history_note_dir_path)

    stimulus_note_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/xhs/result/小红书热搜0427"

    save_output_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/topic_result_0428/" + \
                      os.path.basename(history_note_dir_path).split("_")[1]


    stimulus_note_list = utils.load_from_json_dir(stimulus_note_dir)

    import random
    # 打乱stimulus_note_list顺序
    random.shuffle(stimulus_note_list)

    success_cnt = 0

    for stimulus in tqdm(stimulus_note_list):

        try:
            topic_save_path = os.path.join(save_output_dir, stimulus.get("channel_content_id") + ".json")

            if os.path.exists(topic_save_path):
                continue

            topic_result = create_topic_from_history_note(stimulus, hnl, xuanti_mode=None)

            if topic_result.get("选题结果").get("是否能产生新的选题") == "是":
                success_cnt += 1
                result = {
                    "reference_note": stimulus,
                    "topic": topic_result,
                }
                utils.save(result, topic_save_path)

            if success_cnt >= 2:
                break
        except Exception as e:
            print(f"create topic error {stimulus.get('channel_content_id')}, {str(e)}")
