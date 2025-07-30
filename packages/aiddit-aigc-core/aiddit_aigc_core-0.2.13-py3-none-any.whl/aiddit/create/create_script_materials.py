import json
import os.path

import aiddit.utils as utils
from aiddit.create.prompts.create_script_materials_prompt import (
    SCRIPT_ALIGN_MATERIALS_PROMPT,
    SEARCH_KEYWORD_PROMPT,
    EXTRACT_MATERIAL_FROM_SEARCH_NOTES_PROMPT
)
from aiddit.create.prompts.create_script_by_history_note import NOTE_PROMPT
import aiddit.model.google_genai as google_genai
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
from aiddit.xhs import keyword_search


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


def script_materials_build(script, history_notes):
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325

    history_message = []

    for index, h_note in enumerate(history_notes):
        # 历史参考帖子
        h_note_images = utils.remove_duplicates(h_note.get("images"))
        history_note_prompt = NOTE_PROMPT.format(note_description=f"【历史创作帖子{index + 1}】",
                                                 channel_content_id=h_note.get("channel_content_id"),
                                                 title=h_note.get("title"), body_text=h_note.get("body_text"),
                                                 image_count=len(h_note_images))
        history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            history_note_prompt, h_note_images)
        history_message.append(history_note_conversation_user_message)

    same_topic_note = script.get("reference_note")
    # 参考的同选题帖子
    same_topic_note_prompt = NOTE_PROMPT.format(note_description="【参考的同选题帖子】",
                                                channel_content_id=same_topic_note.get("channel_content_id"),
                                                title=same_topic_note.get("title"),
                                                body_text=same_topic_note.get("body_text"),
                                                image_count=len(same_topic_note.get("images")))
    same_topic_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
        same_topic_note_prompt, utils.remove_duplicates(same_topic_note.get("images")))
    history_message.append(same_topic_note_conversation_user_message)

    # 脚本
    script_userMessage = GenaiConversationMessage.one("user",
                                                      f"【脚本的图集描述】\n{json.dumps(script.get('script').get('创作的脚本').get('图集描述'), ensure_ascii=False, indent=4)}")
    history_message.append(script_userMessage)

    script_align_materials_model_message = google_genai.google_genai_output_images_and_text(
        GenaiConversationMessage.one("user", SCRIPT_ALIGN_MATERIALS_PROMPT),
        model=model,
        history_messages=history_message,
        response_mime_type="application/json")

    script_align_materials_content = script_align_materials_model_message.content[0].value
    script_with_materials = utils.try_remove_markdown_tag_and_to_json(script_align_materials_content)

    source_notes = history_notes + [same_topic_note]
    generated_materials = script_with_materials if type(script_with_materials) is list else script_with_materials.get(
        "材料", [])
    for materials in generated_materials:
        for sources in materials.get("材料来源", []):
            image = _find_material_image(source_notes, sources.get("note_id"), sources.get("image_index"))
            sources["image"] = image

    print(json.dumps(script_with_materials, ensure_ascii=False, indent=4))

    return script_with_materials


def search_materials(script, script_with_materials, save_callback):
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325
    for m in [i for i in script_with_materials if len(i.get("材料来源")) == 0]:
        material_name = m.get("材料名")
        material_description = m.get("材料描述")

        search_keyword = m.get("search_keyword", None)
        if search_keyword is None:
            search_keyword_prompt = SEARCH_KEYWORD_PROMPT.format(
                script=json.dumps(script, ensure_ascii=False, indent=4),
                name=material_name,
                description=material_description)
            search_keyword = google_genai.google_genai(search_keyword_prompt,
                                                       model_name=model,
                                                       response_mime_type=None)
            m["search_keyword"] = search_keyword
            save_callback()

        print(f"材料名：{material_name}，材料描述：{material_description}")
        print(f"搜索关键词：{search_keyword}")

        search_notes = utils.load_from_json_dir(keyword_search.key_word_search(search_keyword))

        history_message = []
        for index, h_note in enumerate(search_notes):
            # 历史参考帖子
            h_note_images = utils.remove_duplicates(h_note.get("images"))
            history_note_prompt = NOTE_PROMPT.format(note_description=f"【材料搜索的帖子{index + 1}】",
                                                     channel_content_id=h_note.get("channel_content_id"),
                                                     title=h_note.get("title"), body_text=h_note.get("body_text"),
                                                     image_count=len(h_note_images))
            history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
                history_note_prompt, h_note_images)
            history_message.append(history_note_conversation_user_message)

        extract_material_from_search_notes_prompt = EXTRACT_MATERIAL_FROM_SEARCH_NOTES_PROMPT.format(name=material_name,
                                                                                                     description=material_description)

        extract_material_from_search_model_message = google_genai.google_genai_output_images_and_text(
            GenaiConversationMessage.one("user", extract_material_from_search_notes_prompt),
            model=model,
            history_messages=history_message,
            response_mime_type="application/json")

        extract_material_from_search_content = extract_material_from_search_model_message.content[0].value
        print(extract_material_from_search_content)

        material_sources = utils.try_remove_markdown_tag_and_to_json(extract_material_from_search_content)
        if type(material_sources) is list:
            for source in material_sources:
                if type(source) is dict:
                    source_note_id = source.get("note_id")
                    source_image_index = source.get("image_index")
                    source["note"] = next((n for n in search_notes if n.get("channel_content_id") == source_note_id), None)
                    image = _find_material_image(search_notes, source_note_id, source_image_index)
                    if image is not None:
                        source["image"] = image
        m["材料来源"] = material_sources
        save_callback()

    return False


if __name__ == "__main__":
    script_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/materials/猫咪穿上新中式旗袍的生活记录.json"
    script_data = json.load(open(script_path, "r"))
    generated_script = next(
        (script_data[key] for key in script_data.keys() if key.startswith("script_generate_result")), None)

    history_note_data = utils.load_from_json_dir(
        json.load(open(script_data.get("renshe_path"), "r")).get("history_note_dir_path"))

    script_materials_save_path = os.path.dirname(script_path) + "/materials_" + os.path.basename(script_path)

    script_materials_result = None

    if os.path.exists(script_materials_save_path):
        script_materials_result = json.load(open(script_materials_save_path, "r"))
    else:
        script_materials_result = {
            "script": generated_script
        }

    script_materials = script_materials_result.get("script_materials", None)

    if script_materials is None:
        script_materials = script_materials_build(generated_script, history_note_data)
        script_materials_result["script_materials"] = script_materials
        utils.save(script_materials_result, script_materials_save_path)

    if not script_materials_result.get("search_finished"):
        script_materials_result["finished"] = search_materials(generated_script, script_materials,
                                                               save_callback=lambda: utils.save(script_materials_result,
                                                                                                script_materials_save_path))
        utils.save(script_materials_result, script_materials_save_path)
    pass
