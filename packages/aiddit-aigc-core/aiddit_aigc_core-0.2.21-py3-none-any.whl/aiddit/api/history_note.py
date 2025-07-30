import aiddit.utils as utils
import aiddit.model.google_genai as google_genai

NOTE_PROVIDER_PROMPT = """这是人设账号中中的第{index}个帖子
标题：{title}
正文: {body_text}
还有如下{media_count}个{content_type_description}：
"""


def build_history_note_messages(history_notes):
    build_history_note_messages = []

    for index, h_note in enumerate(history_notes):
        # 历史参考帖子
        if h_note.get("content_type") == "video" and h_note.get("video", {}).get("video_url") is not None:
            reference_note_medias = [h_note.get("video", {}).get("video_url")]
            content_type_description = "视频"
        else:
            reference_note_medias = [utils.oss_resize_image(i) for i in
                                     utils.remove_duplicates(h_note.get("images"))]
            content_type_description = "图片"

        history_note_prompt = NOTE_PROVIDER_PROMPT.format(
            index=index + 1,
            title=h_note.get("title"),
            body_text=h_note.get("body_text"),
            media_count=len(reference_note_medias),
            content_type_description=content_type_description)
        history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            history_note_prompt, reference_note_medias)
        build_history_note_messages.append(history_note_conversation_user_message)

    return build_history_note_messages
