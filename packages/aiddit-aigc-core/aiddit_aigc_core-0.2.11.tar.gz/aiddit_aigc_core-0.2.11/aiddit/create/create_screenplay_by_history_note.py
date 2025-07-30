import json
import os
from aiddit.create.prompts.create_screenplay_prompt import (
    HISTORY_NOTE_SCREENPLAY_GENERATE_PROMPT
)
from aiddit.create.prompts.create_topic_by_history_note_prompt import NOTE_PROMPT
import aiddit.utils as utils
import aiddit.model.google_genai as google_genai
from tqdm import tqdm


def generate_screenplay(topic, history_note_list):
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

    # 知识库研究报告
    knowledge_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/knowledge/剧本创作：叙事选题与情节_ (1).pdf"
    knowledge_conversation_message = google_genai.GenaiConversationMessage.text_and_images(
        "这是剧本创作(研究报告)",
        knowledge_path)

    history_message.append(knowledge_conversation_message)
    # 生成剧本
    history_note_screenplay_generate_prompt = HISTORY_NOTE_SCREENPLAY_GENERATE_PROMPT.format(
        note_count=len(history_note_list),
        topic=topic)

    ask_message_conversation = google_genai.GenaiConversationMessage.one("user",
                                                                         history_note_screenplay_generate_prompt)

    ask_response_conversation = google_genai.google_genai_output_images_and_text(ask_message_conversation,
                                                                                 model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                                 history_messages=history_message,
                                                                                 response_mime_type="application/json")
    print(ask_response_conversation.content[0].value)

    screenplay_result =  utils.try_remove_markdown_tag_and_to_json(ask_response_conversation.content[0].value)

    if type(screenplay_result) is list:
        return screenplay_result[0]

    return screenplay_result


if __name__ == "__main__":
    renshe_info = json.load(open(
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_comprehension/account_摸鱼阿希_617a100c000000001f03f0b9.json",
        "r"))
    history_note_dir_path = renshe_info.get("history_note_dir_path")

    hnl = utils.load_from_json_dir(history_note_dir_path)

    r = generate_screenplay("同事误入前卫舞蹈现场，这肢体动作是在模仿上班状态吗？", hnl)

    print(r.get("剧本结果").get("剧本故事情节"))
    pass
