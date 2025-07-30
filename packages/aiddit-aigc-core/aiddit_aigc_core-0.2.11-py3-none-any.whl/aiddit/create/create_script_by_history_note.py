import json
import os
import aiddit.xhs.keyword_search as keyword_search
import aiddit.model.google_genai as google_genai
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
import aiddit.utils as utils
from aiddit.create.prompts.create_script_by_history_note import (
    NOTE_PROVIDER_PROMPT,
    SAME_TOPIC_FIND_PROMPT,
    RENSHE_SCRIPT_MODE_AND_SEARCH_NOTE_SCRIPT_GENERATE_PROMPT,
    FIND_BEST_SCRIPT_NOTE_FROM_HISTORY_NOTE_PROMPT,
    NOTE_PROMPT,
    HISTORY_NOTE_AND_SEARCH_GENERATE_PROMPT,
    SCRIPT_ALIGN_MATERIALS_PROMPT,
    HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_GENERATE_PROMPT,
    HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_GENERATE_PROMPT,
    HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_AND_SCREENPLAY_GENERATE_PROMPT,
    TOPIC_TYPE_MATCH_PROMPT,
    OPTIMIZE_SCRIPT_PROMPT
)
from tenacity import retry, stop_after_attempt, wait_fixed
import aiddit.create.create_screenplay_by_history_note as create_screenplay_by_history_note
import aiddit.comprehension.script0221.script_compehension as script_comprehension
import aiddit.comprehension.script0221.script_prompt as script_prompt
import aiddit.create.script_pipeline as script_pipeline

TOPIC_SCRIPT_KNOWLEDGE = {
    "故事叙事性选题": "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/小红书_故事叙事性_图文脚本构建指南.pdf",
    "产品测评与推荐": "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/小红书_产品测评与推荐_图文脚本构建指南.pdf",
    "教程与指南": "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/小红书_教程与指南_图文脚本构建指南.pdf",
    "经验分享与生活记录": "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/小红书_经验分享与生活记录_图文脚本构建指南_.pdf",
    "清单与合集": "",
    "热点追踪与话题讨论": "",
    "对比与选择": "",
}

DEFAULT_SCRIPT_KNOWLEDGE = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/xhs_script_0415.pdf"


def _search_estimate(process_result, xuanti_result):
    result = {}

    final_xuanti = xuanti_result.get("选题")

    keyword = final_xuanti
    keyword_search_result_dir = keyword_search.key_word_search_without_oss_save(keyword)

    search_result_list = [json.load(open(os.path.join(keyword_search_result_dir, i), "r")) for i in
                          os.listdir(keyword_search_result_dir) if i.endswith(".json")]
    search_result_map = {note["channel_content_id"]: note for note in search_result_list}
    print(f"search {keyword} success, result count {len(search_result_list)}")

    ask_result = _ask_gemini(search_result_list, final_xuanti)

    ask_note_result_list = ask_result if type(ask_result) is list else ask_result.get("判断结果", [])
    print(f"_search_estimate input {len(search_result_list)} 个帖子， 模型判断了 {len(ask_note_result_list)} 个帖子")

    has_same_topic = any(note.get("same_topic") is True for note in ask_note_result_list)

    for i in ask_note_result_list:
        note = search_result_map.get(i.get("note_id"))
        if note is not None:
            note["same_topic"] = i.get("same_topic")
            note["score"] = i.get("score")
            note["explain"] = i.get("explain")

    result["搜索关键词"] = keyword
    result["是否有相同选题"] = has_same_topic
    result["搜索结果"] = search_result_map
    result["搜索是否完成"] = True

    # result["质量是否通过"] = _quality_estimate([note for note in search_result_list if note.get("same_topic") is True])
    result["质量是否通过"] = has_same_topic

    process_result.update(result)
    utils.save(process_result, process_result["save_path"])


def _same_topic_note_script_comprehension(process_result):
    """理解单帖脚本"""
    same_topic_notes = [note for note in process_result.get("搜索结果").values() if
                        note.get("same_topic") is True and note.get("script") is None]
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(script_comprehension.note_script, note) for note in same_topic_notes]
        for future, note in zip(concurrent.futures.as_completed(futures), same_topic_notes):
            note["script"] = future.result()

    utils.save(process_result, process_result["save_path"])


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


def _quality_estimate(same_topic_notes: list):
    """质量评估"""
    quality_pass = False
    for note in same_topic_notes:
        if note.get("like_count") > 100 or note.get("collect_count") > 100:
            quality_pass = True
            break

    return quality_pass


def _ask_gemini(search_result_list, final_xuanti: str):
    """从搜索的结果中找同题的帖子"""
    history_messages = _build_note_prompt(search_result_list, each_note_image_count=3)

    ask_prompt = SAME_TOPIC_FIND_PROMPT.format(note_count=len(search_result_list), final_xuanti=final_xuanti)
    ask_message = GenaiConversationMessage("user", [GenaiMessagePart(MessageType.TEXT, ask_prompt)])
    gemini_result = google_genai.google_genai_output_images_and_text(ask_message,
                                                                     model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                     history_messages=history_messages,
                                                                     response_mime_type="application/json")
    response_content = gemini_result.content[0].value
    print(response_content)
    return utils.try_remove_markdown_tag_and_to_json(response_content)


def _process(xuanti_result, renshe_info, renshe_path, use_script_mode=False):
    xuanti_creation = xuanti_result.get("topic").get("选题结果")
    final_xuanti = xuanti_creation.get("选题")

    log_file_name = final_xuanti + ".json"

    # force update save path
    save_path = os.path.join(log_file_dir, log_file_name)

    process_result = json.load(open(save_path, "r")) if os.path.exists(save_path) else {
        "xuanti_creation": xuanti_creation,
        "reference_note": xuanti_result.get("reference_note"),
        "renshe_path": renshe_path,
        "save_path": save_path,
        "use_script_mode": use_script_mode
    }

    process_result["save_path"] = save_path

    if process_result.get("选题类型结果") is None:
        topic_type_result = _get_topic_type_and_script_knowledge(final_xuanti)
        process_result["选题类型结果"] = topic_type_result
        utils.save(process_result, process_result["save_path"])

    topic_type = process_result.get("选题类型结果").get("选题类型")
    need_generate_screenplay = topic_type == "故事叙事性选题"
    script_knowledge_path = TOPIC_SCRIPT_KNOWLEDGE.get(topic_type)
    if script_knowledge_path is None or script_knowledge_path == "":
        script_knowledge_path = DEFAULT_SCRIPT_KNOWLEDGE

    # 选题关键词搜索
    if process_result.get("搜索是否完成", False) is False:
        _search_estimate(process_result, xuanti_creation)

    # 参考历史帖子的脚本 生成新脚本
    _generate_script_by_history_note(process_result,
                                     script_mode=renshe_info.get("脚本模式"),
                                     history_note_dir_path=renshe_info.get("history_note_dir_path"),
                                     account_name=renshe_info.get("account_info").get("account_name"),
                                     account_description=renshe_info.get("account_info").get("description"),
                                     final_xuanti=final_xuanti,
                                     need_generate_screenplay=need_generate_screenplay,
                                     script_knowledge_path=script_knowledge_path)


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


def _generate_script_by_history_note(process_result, script_mode, history_note_dir_path, account_name,
                                     account_description,
                                     final_xuanti, need_generate_screenplay, script_knowledge_path):
    # 搜索出来的同题帖子
    same_topic_notes = [note for note in process_result.get("搜索结果").values() if note.get("same_topic") is True]
    if len(same_topic_notes) == 0:
        same_topic_notes = [note for note in process_result.get("搜索结果").values()]

    # same_topic_notes 同题排序
    same_topic_notes = sorted(same_topic_notes, key=lambda x: x.get("score", 0), reverse=True)

    #  gemini-2.5-pro-exp-03-25
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325

    for same_topic_note in [same_topic_notes[0]]:
        generated_key = f"script_generate_result_{same_topic_note.get('channel_content_id')}"
        if process_result.get(generated_key) is not None:
            generate_script_result = process_result.get(generated_key)
        else:
            generate_script_result = {
                "reference_note": same_topic_note
            }
            process_result[generated_key] = generate_script_result

        if generate_script_result.get("history_note") is None:
            # 参考历史帖子中的 脚本 & 风格
            history_notes = _find_best_script_note_from_history_note(final_xuanti, history_note_dir_path)
            generate_script_result["history_note"] = history_notes
            utils.save(process_result, process_result["save_path"])
            if len(history_notes) is None:
                print("没有找到历史帖子")
                continue
        else:
            history_notes = generate_script_result.get("history_note")

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

        # 搜索同题帖子
        same_topic_note_prompt = NOTE_PROMPT.format(note_description="【参考的同选题帖子】",
                                                    channel_content_id=same_topic_note.get("channel_content_id"),
                                                    title=same_topic_note.get("title"),
                                                    body_text=same_topic_note.get("body_text"),
                                                    image_count=len(same_topic_note.get("images")))
        same_topic_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            same_topic_note_prompt, utils.remove_duplicates(same_topic_note.get("images")))
        history_message.append(same_topic_note_conversation_user_message)

        screenplay_result = None
        if need_generate_screenplay:
            ## 剧本生成
            if generate_script_result.get("screenplay_result") is None:
                screenplay_result = create_screenplay_by_history_note.generate_screenplay(final_xuanti,
                                                                                          utils.load_from_json_dir(
                                                                                              history_note_dir_path))
                generate_script_result["screenplay_result"] = screenplay_result
                utils.save(process_result, process_result["save_path"])
            else:
                screenplay_result = generate_script_result.get("screenplay_result")

        ## 脚本知识库
        script_knowledge_file_name = os.path.basename(script_knowledge_path)
        knowledge_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            f"这是小红书图文内容脚本创作专业指南：{script_knowledge_file_name}",
            script_knowledge_path)
        history_message.append(knowledge_conversation_user_message)

        if need_generate_screenplay and screenplay_result is not None:
            ## 默认带脚本模式生成
            history_note_and_search_generate_prompt = HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_AND_SCREENPLAY_GENERATE_PROMPT.format(
                final_xuanti=final_xuanti,
                screenplay=screenplay_result.get("剧本结果").get("剧本故事情节"),
                screenplay_keypoint=screenplay_result.get("剧本结果").get("剧本关键点"),
                images_script_mode=script_mode.get("图集模式"),
                script_knowledge_file_name=script_knowledge_file_name,
                account_name=account_name,
                account_description=account_description)
        else:
            history_note_and_search_generate_prompt = HISTORY_NOTE_AND_SEARCH_AND_SCRIPT_MODE_AND_KNOWLEDGE_GENERATE_PROMPT.format(
                final_xuanti=final_xuanti,
                images_script_mode=script_mode.get("图集模式"),
                script_knowledge_file_name=script_knowledge_file_name,
                account_name=account_name,
                account_description=account_description)

        script_generate_conversation_user_message = GenaiConversationMessage.one("user",
                                                                                 history_note_and_search_generate_prompt)
        if generate_script_result.get("script") is None:
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

            generate_script_result["script"] = script_ans
            utils.save(process_result, process_result["save_path"])
        else:
            history_message.append(script_generate_conversation_user_message)
            script_ans = generate_script_result.get("script")
            history_message.append(google_genai.GenaiConversationMessage.one("model",
                                                                             json.dumps(script_ans, ensure_ascii=False,
                                                                                        indent=4)))

        # optimize_script_prompt = OPTIMIZE_SCRIPT_PROMPT
        # optimize_script_conversation_user_message = GenaiConversationMessage.one("user",optimize_script_prompt)
        #
        # if generate_script_result.get("optimize_script") is None:
        #     optimize_script_ans_conversation_model_message = google_genai.google_genai_output_images_and_text(
        #         optimize_script_conversation_user_message,
        #         model=model,
        #         history_messages=history_message,
        #         response_mime_type="application/json")
        #     history_message.append(optimize_script_conversation_user_message)
        #     optimize_script_ans_content = optimize_script_ans_conversation_model_message.content[0].value
        #     optimize_script_ans = utils.try_remove_markdown_tag_and_to_json(optimize_script_ans_content)
        #     generate_script_result["optimize_script"] = optimize_script_ans
        #     utils.save(process_result, process_result["save_path"])
        # else:
        #     history_message.append(optimize_script_conversation_user_message)
        #     optimize_script_ans = generate_script_result.get("optimize_script")
        #     history_message.append(google_genai.GenaiConversationMessage.one("model",
        #                                                                      json.dumps(optimize_script_ans, ensure_ascii=False,
        #                                                                                 indent=4)))

        # 材料构建
        if generate_script_result.get("script_with_materials") is None:
            script_align_materials_prompt_message = google_genai.google_genai_output_images_and_text(
                GenaiConversationMessage.one("user", SCRIPT_ALIGN_MATERIALS_PROMPT),
                model=model,
                history_messages=history_message,
                response_mime_type="application/json")
            script_align_materials_content = script_align_materials_prompt_message.content[0].value
            print(script_align_materials_content)
            script_with_materials = utils.try_remove_markdown_tag_and_to_json(script_align_materials_content)
            for materials in script_with_materials.get("带材料的脚本").get("材料", []):
                target_notes = history_notes + [same_topic_note]
                image = _find_material_image(target_notes, materials.get("note_id"), materials.get("image_index"))
                materials["image"] = image

            generate_script_result["script_with_materials"] = script_with_materials
            utils.save(process_result, process_result["save_path"])

        # if generate_script_result.get("generated_images") is None:
        #     # history_message 中移除knowledge_conversation_message ，avoid 'The input token count (32811) exceeds the maximum number of tokens allowed (32768)
        #     history_message.remove(knowledge_conversation_user_message)
        #
        #     script_image_description_list = script_ans.get("创作的脚本", []).get("图集描述", [])
        #     """根据脚本描述生成图片"""
        #     for i in script_image_description_list:
        #         # 图片生成
        #         image_generate_conversation = GenaiConversationMessage.one("user",
        #                                                                    f"参考【历史创作帖子】以及历史生成结果，保持风格的一致性，请根据下述图片描述完成图片生成：\n\n{i}")
        #         image_generation_conversation_message = google_genai.google_genai_output_images_and_text(
        #             image_generate_conversation,
        #             model=google_genai.MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION,
        #             history_messages=history_message)
        #         history_message.append(image_generate_conversation)
        #         history_message.append(image_generation_conversation_message)
        #     generated_images = google_genai.get_generated_images(history_message)
        #     print(generated_images)
        #     generate_script_result["generated_images"] = generated_images

        """保存结果"""
        utils.save(process_result, process_result["save_path"])

        print(f"{final_xuanti} 生成脚本完成")


if __name__ == "__main__":
    # 替换 start account_LING_5687a2645e87e702df7b5304 account_山木木简笔画_649da24b000000002b0081a1
    xuanti_output_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/topic_result_0428/脆肚火锅噗噜噗噜"
    renshe_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_comprehension/agent_test_account/account_脆肚火锅噗噜噗噜_5c0aa4ce000000000500b192.json"
    # 替换 end

    result_save_base_dir_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/script_result_0428"
    log_file_dir = os.path.join(result_save_base_dir_path, os.path.basename(xuanti_output_dir))

    renshe_info_data = json.load(open(renshe_path, "r"))

    for result in utils.load_from_json_dir(xuanti_output_dir):
        topic = result.get("topic")
        if type(topic) is list:
            topic = topic[0]
            result['topic'] = topic
            update_path = os.path.join(xuanti_output_dir,
                                       f"{result.get('reference_note').get('channel_content_id')}.json")
            utils.save(result, update_path)

        # _process(result, renshe_info_data, renshe_path, True)

        if result.get("topic").get("选题结果").get(
                "选题") == "Intp's｜阴雨天的精神角落：在屏幕细节里画个迷宫.json".replace(".json", ""):
            _process(result, renshe_info_data, renshe_path, True)
            break
        else:
            print(result.get("topic").get("选题结果").get("选题"))

    pass
