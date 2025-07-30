import os
import traceback

import json
import aiddit.utils as utils
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
from aiddit.api.script.prompt import (
    TOPIC_TYPE_MATCH_PROMPT,
    HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_AND_SCREENPLAY_GENERATE_PROMPT,
    NOTE_PROMPT,
    HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_GENERATE_PROMPT,
    SCRIPT_ALIGN_MATERIALS_PROMPT,
    NOTE_PROVIDER_PROMPT,
    FIND_BEST_SCRIPT_NOTE_FROM_HISTORY_NOTE_PROMPT,
    SCRIPT_OPTIMIZE_PROMPT
)
import aiddit.model.google_genai as google_genai
import aiddit.create.create_renshe_comprehension as create_renshe_comprehension
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
import aiddit.create.create_screenplay_by_history_note as create_screenplay_by_history_note
from aiddit.api.xhs_api import _get_xhs_account_info, _get_xhs_account_note_list

load_dotenv()

xhs_cache_dir = os.getenv("xhs_cache_dir")

DEFAULT_SCRIPT_KNOWLEDGE = os.getenv("script_knowledge_base")


def script(xhs_user_id: str, topic):
    print(topic)
    # prepare renshe info
    account_info = _get_xhs_account_info(xhs_user_id)
    account_history_note_path = _get_xhs_account_note_list(xhs_user_id)
    script_mode = _get_xhs_account_script_mode(xhs_user_id)

    # 知识库
    topic_script_knowledge = {
        "故事叙事性选题": os.getenv("script_knowledge_narrative_story"),
        "产品测评与推荐": os.getenv("script_knowledge_product_review"),
        "教程与指南": os.getenv("script_knowledge_tutorial_guide"),
        "经验分享与生活记录": os.getenv("script_knowledge_experience_sharing")
    }

    topic_type = _get_topic_type_and_script_knowledge(topic).get("选题类型结果", {}).get("选题类型", "")
    need_generate_screenplay = topic_type == "故事叙事性选题"
    script_knowledge_path = topic_script_knowledge.get(topic_type, None)
    if script_knowledge_path is None or script_knowledge_path == "":
        script_knowledge_path = DEFAULT_SCRIPT_KNOWLEDGE

    # 脚本生成
    return _generate_script_by_history_note(script_mode=script_mode,
                                            history_note_dir_path=account_history_note_path,
                                            account_name=account_info.get("account_name"),
                                            account_description=account_info.get("description"),
                                            final_xuanti=topic,
                                            need_generate_screenplay=need_generate_screenplay,
                                            script_knowledge_path=script_knowledge_path)


def _generate_script_by_history_note(script_mode, history_note_dir_path, account_name,
                                     account_description,
                                     final_xuanti, need_generate_screenplay, script_knowledge_path):
    #  gemini-2.5-pro-exp-03-25
    model = google_genai.MODEL_GEMINI_2_5_FLASH

    # 历史选题相似帖子
    history_notes = _find_best_script_note_from_history_note(final_xuanti, history_note_dir_path)

    history_message = []

    for index, h_note in enumerate(history_notes):
        # 历史参考帖子
        h_note_images = utils.remove_duplicates(h_note.get("images"))
        h_note_images = [utils.oss_resize_image(i) for i in h_note_images]
        history_note_prompt = NOTE_PROMPT.format(note_description=f"【历史创作帖子{index + 1}】",
                                                 channel_content_id=h_note.get("channel_content_id"),
                                                 title=h_note.get("title"), body_text=h_note.get("body_text"),
                                                 image_count=len(h_note_images))
        history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            history_note_prompt, h_note_images)
        history_message.append(history_note_conversation_user_message)

    screenplay_result = None
    if need_generate_screenplay:
        ## 剧本生成
        screenplay_result = create_screenplay_by_history_note.generate_screenplay(final_xuanti,
                                                                                  utils.load_from_json_dir(
                                                                                      history_note_dir_path))
    ## 脚本知识库
    script_knowledge_file_name = None
    if script_knowledge_path is not None and os.path.exists(script_knowledge_path):
        script_knowledge_file_name = os.path.basename(script_knowledge_path)
        knowledge_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            f"这是小红书图文内容脚本创作专业指南：{script_knowledge_file_name}",
            script_knowledge_path)
        history_message.append(knowledge_conversation_user_message)

    if need_generate_screenplay and screenplay_result is not None:
        ## 默认带脚本模式生成
        history_note_and_search_generate_prompt = HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_AND_SCREENPLAY_GENERATE_PROMPT.format(
            final_xuanti=final_xuanti,
            screenplay=screenplay_result.get("剧本结果", {}).get("剧本故事情节", ""),
            screenplay_keypoint=screenplay_result.get("剧本结果", {}).get("剧本关键点", ""),
            images_script_mode=script_mode.get("图集模式", {}),
            script_knowledge_file_name=script_knowledge_file_name,
            account_name=account_name,
            account_description=account_description)
    else:
        history_note_and_search_generate_prompt = HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_GENERATE_PROMPT.format(
            final_xuanti=final_xuanti,
            images_script_mode=script_mode.get("图集模式", {}),
            script_knowledge_file_name=script_knowledge_file_name,
            account_name=account_name,
            account_description=account_description)

    script_generate_conversation_user_message = GenaiConversationMessage.one("user",
                                                                             history_note_and_search_generate_prompt)
    # 生成脚本
    script_ans_conversation_model_message = google_genai.google_genai_output_images_and_text(
        script_generate_conversation_user_message,
        model=model,
        history_messages=history_message,
        response_mime_type="application/json")
    history_message.append(script_ans_conversation_model_message)
    script_ans_content = script_ans_conversation_model_message.content[0].value
    print(script_ans_content)
    script_ans = utils.try_remove_markdown_tag_and_to_json(script_ans_content)

    # 脚本调整
    # script_optimize_conversation_user_message = GenaiConversationMessage.one("user", SCRIPT_OPTIMIZE_PROMPT)
    # script_optimize_conversation_model_message = google_genai.google_genai_output_images_and_text(
    #     script_optimize_conversation_user_message,
    #     model=model,
    #     history_messages=history_message,
    #     response_mime_type="application/json")
    # history_message.append(script_optimize_conversation_model_message)
    # script_ans_content = script_optimize_conversation_model_message.content[0].value
    # print(script_ans_content)
    # script_ans = utils.try_remove_markdown_tag_and_to_json(script_ans_content)

    # 材料构建
    script_align_materials_prompt_message = google_genai.google_genai_output_images_and_text(
        GenaiConversationMessage.one("user", SCRIPT_ALIGN_MATERIALS_PROMPT),
        model=model,
        history_messages=history_message,
        response_mime_type="application/json")
    script_align_materials_content = script_align_materials_prompt_message.content[0].value
    print(script_align_materials_content)
    script_with_materials = utils.try_remove_markdown_tag_and_to_json(script_align_materials_content)

    script_with_materials_data = script_with_materials.get("脚本", {})
    script_with_materials_data = script_with_materials_data if type(script_with_materials_data) is dict  else script_with_materials_data[0]

    for materials in script_with_materials_data.get("图集材料", []):
        target_notes = history_notes
        note_id = materials.get("note_id")
        image = _find_material_image(target_notes, note_id, materials.get("image_index"))
        materials["材料图片"] = image
        # 如果materials有字段 note_id 则删除
        if "note_id" in materials:
            del materials["note_id"]

        if "image_index" in materials:
            del materials["image_index"]

    script_result = script_with_materials

    try:
        created_script_value = script_ans.get("创作的脚本", {})
        created_script = created_script_value[0] if type(created_script_value) is list else created_script_value
        script_result["标题"] = created_script.get("标题", "")
        script_result["正文"] = created_script.get("正文", "")
    except Exception as e:
        traceback.print_exc()
        print(f"获取标题 正文失败 ： {json.dumps(script_ans, indent=4, ensure_ascii=False)}", str(e))

    script_result["选题"] = final_xuanti

    return script_result


def _find_best_script_note_from_history_note(final_xuanti, history_note_dir_path):
    history_note_list = utils.load_from_json_dir(history_note_dir_path)

    if len(history_note_list) == 0:
        raise Exception(f"没有找到历史帖子， 请检查 {history_note_dir_path} 是否存在")

    history_messages = _build_note_prompt(history_note_list)
    find_best_script_note_from_history_note_prompt = FIND_BEST_SCRIPT_NOTE_FROM_HISTORY_NOTE_PROMPT.format(
        final_xuanti=final_xuanti, note_count=len(history_note_list))
    gemini_result = google_genai.google_genai_output_images_and_text(
        GenaiConversationMessage.one("user", find_best_script_note_from_history_note_prompt), model="gemini-2.0-flash",
        history_messages=history_messages,
        response_mime_type="application/json")
    response_content = gemini_result.content[0].value
    print(response_content)

    note_ans = utils.try_remove_markdown_tag_and_to_json(response_content)
    history_reference_note_list = [i.get("帖子id", "") for i in note_ans.get("参考帖子", [])]
    find_notes = []
    for note in history_note_list:
        if note.get("channel_content_id") in history_reference_note_list:
            find_notes.append(note)

    return find_notes


def _build_note_prompt(note_list, each_note_image_count=100):
    history_messages = []
    for index, note in enumerate(note_list):
        contents = []
        note_provider_prompt = NOTE_PROVIDER_PROMPT.format(index=index + 1,
                                                           channel_content_id=note.get("channel_content_id"),
                                                           title=note.get("title"),
                                                           body_text=note.get("body_text"))
        text_message = GenaiMessagePart(MessageType.TEXT, note_provider_prompt)
        contents.append(text_message)
        for image in utils.remove_duplicates(note.get("images"))[:each_note_image_count]:
            image_message = GenaiMessagePart(MessageType.URL_IMAGE, utils.oss_resize_image(image))
            contents.append(image_message)

        message = GenaiConversationMessage("user", contents)
        history_messages.append(message)

    return history_messages


def _find_material_image(note_list, note_id, image_index):
    note_map = {note.get("channel_content_id"): note for note in note_list}

    if image_index is None:
        return None

    target_note = note_map.get(note_id)
    if target_note is None:
        return None

    images = utils.remove_duplicates(target_note.get("images"))
    image_index_int = image_index if (type(image_index) is int) else int(image_index)
    real_index = image_index_int - 1
    if real_index in range(0, len(images)):
        return images[real_index]

    return None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _get_topic_type_and_script_knowledge(final_xuanti):
    topic_type_match_prompt = TOPIC_TYPE_MATCH_PROMPT.format(topic=final_xuanti)
    ask_message = GenaiConversationMessage.one("user", topic_type_match_prompt)
    gemini_result = google_genai.google_genai_output_images_and_text(ask_message,
                                                                     model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                     history_messages=None,
                                                                     response_mime_type="application/json")

    response_content = gemini_result.content[0].value
    print(response_content)
    topic_type_result = utils.try_remove_markdown_tag_and_to_json(response_content)
    if topic_type_result.get("选题类型") is None:
        raise Exception(f"没有找到选题类型， 请检查 {response_content}")

    return topic_type_result


def _get_xhs_account_script_mode(xhs_user_id):
    account_info = _get_xhs_account_info(xhs_user_id)
    history_note_list_path = _get_xhs_account_note_list(xhs_user_id)

    if account_info.get('script_mode') is None:
        xhs_cache_account_info = os.path.join(xhs_cache_dir, "account_info")
        account_user_info_path = os.path.join(xhs_cache_account_info, f"{xhs_user_id}.json")

        script_mode = create_renshe_comprehension.comprehension_script_mode(
            utils.load_from_json_dir(history_note_list_path), account_info)
        account_info["script_mode"] = script_mode
        utils.save(account_info, account_user_info_path)

    return account_info.get("script_mode")


if __name__ == "__main__":
    user_id = "58eee4af82ec39634ba1f420"

    act_info = _get_xhs_account_info(user_id)
    print(json.dumps(act_info, indent=4, ensure_ascii=False))
    account_save_path = _get_xhs_account_note_list(user_id)
    print(account_save_path)

    sr = script(user_id, """把空气炸锅烤粽子加入小葵家宴，6位小姐姐全被这神仙口感征服\n\n选题的详细说明：\n这个选题完美融合了用户的\"小葵家宴\"系列和刺激源中的创新美食方法，将空气炸锅烤粽子这一新奇吃法作为家宴的一道特色创意美食。选题不仅保留了用户分享美食的核心人设，还结合了社交元素和故事性，通过记录6位小姐姐品尝这道意外美食时的反应和互动，增加内容的趣味性和情感深度。选题也巧妙地融入了用户的潮汕背景，可以选择使用当地特色粽子，展示个人文化特色，同时借助端午节的时令话题增加内容的相关性和传播性。\n\n选题创作中的关键点：\n1. 系列延续：保持\"小葵家宴\"这一核心系列，维持账号一致性\n2. 创新与传统结合：将现代烹饪方法（空气炸锅）与传统食物（粽子）结合，创造惊喜感\n3. 社交元素：通过记录小姐姐们的反应和评价，增强社交分享维度\n4. 地域特色：可融入潮汕/顺德的粽子特色，突出个人地域标签\n5. 仪式感：结合端午节的时令，增加内容的时效性和文化深度\n6. 口感对比：重点突出\"神仙口感\"（外酥里嫩）这一最大卖点\n7. 真实性：延续用户一贯的真实、热情、生活化的表达风格
""")

    print(json.dumps(sr, ensure_ascii=False, indent=4))
