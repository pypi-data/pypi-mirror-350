from tenacity import retry, stop_after_attempt, wait_fixed

from aiddit.api.xhs_api import _get_xhs_account_info, _get_xhs_account_note_list, _get_note_detail_by_id
import aiddit.api.topic.prompt as prompt
import aiddit.model.google_genai as google_genai
import aiddit.utils as utils
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
import os

def reference_note_available(xhs_user_id: str, reference_note_id: str) -> str:
    account_info = _get_xhs_account_info(xhs_user_id)
    account_history_note_path = _get_xhs_account_note_list(xhs_user_id)

    model = google_genai.MODEL_GEMINI_2_5_FLASH

    reference_note = _get_note_detail_by_id(reference_note_id)

    history_notes = utils.load_from_json_dir(account_history_note_path)

    history_messages = []

    for index, h_note in enumerate(history_notes):
        # 历史参考帖子
        h_note_images = utils.remove_duplicates(h_note.get("images"))
        h_note_images = [utils.oss_resize_image(i) for i in h_note_images]
        history_note_prompt = prompt.NOTE_PROVIDER_PROMPT.format(
            index=index + 1,
            title=h_note.get("title"),
            body_text=h_note.get("body_text"),
            image_count=len(h_note_images))
        history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            history_note_prompt, h_note_images)
        history_messages.append(history_note_conversation_user_message)


    # 参考帖子
    if reference_note.get("content_type") == "video" and reference_note.get("video", {}).get("video_url") is not None:
        reference_note_medias = [reference_note.get("video", {}).get("video_url")]
    else:
        reference_note_medias = [utils.oss_resize_image(i) for i in utils.remove_duplicates(reference_note.get("images"))]
    reference_note_prompt = prompt.REFERENCE_NOTE_PROVIDER_PROMPT.format(
        title=reference_note.get("title"),
        body_text=reference_note.get("body_text"),
        image_count=len(reference_note_medias)
    )
    reference_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(reference_note_prompt,reference_note_medias)
    history_messages.append(reference_note_conversation_user_message)

    # 专家知识
    expert_knowledge_path = "../expert/topic_theory_expert.txt"
    # 获取绝对路径
    expert_knowledge_absolute_path = os.path.abspath(expert_knowledge_path)
    print(expert_knowledge_absolute_path)
    expert_knowledge_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
        f"小红书内容创作的理论基石：基于特定账号人设与参考帖子的选题策略。从中你可以学习 了解小红书内容创作的理论基石，基于特定账号人设与参考帖子的选题策略。", expert_knowledge_absolute_path)
    history_messages.append(expert_knowledge_conversation_user_message)


    # 参考帖子是否能产生选题
    reference_available_prompt = prompt.REFERENCE_NOTE_AVAILABLE_PROMPT.format(account_name=account_info.get("account_name"),
                                                                               account_description=account_info.get("description"),)
    reference_available_conversation_user_message = GenaiConversationMessage.one("user",
                                                                             reference_available_prompt)

    script_ans_conversation_model_message = google_genai.google_genai_output_images_and_text(
        reference_available_conversation_user_message,
        model=model,
        history_messages=history_messages,
        system_instruction_prompt=prompt.SYSTEM_INSTRUCTION_PROMPT)
    ans_content = script_ans_conversation_model_message.content[0].value


    return ans_content


if __name__ == "__main__":
    ans = reference_note_available("62f63a81000000001902dc91 ","6828090000000000220242a0")
    pass
