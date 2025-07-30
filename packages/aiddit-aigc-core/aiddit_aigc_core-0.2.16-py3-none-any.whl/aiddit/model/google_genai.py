import logging

from google import genai as google_genai
from google.genai import types
import aiddit.model.gemini_upload_file as gemini_upload_file
import aiddit.utils as utils
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_fixed
import os
import json
from tqdm import tqdm
import concurrent.futures
from dotenv import load_dotenv
from aiddit.model.gemini_available_mime_types import AVAILABLE_MIME_TYPES

load_dotenv()

api_key = os.getenv("google_genai_api_key")
cache_dir = os.getenv("google_genai_upload_file_cache_dir")
generate_image_save_dir_path = os.getenv("google_genai_generated_image_save_dir")

google_genai_client = google_genai.Client(api_key=api_key)


# google 升级的SDK https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn

class MaxTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"MaxTokenException: {self.message}"


MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_5_PRO_EXPT_0325 = "gemini-2.5-pro-preview-05-06"
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash-preview-05-20"
# MODEL_GEMINI_2_5_PRO_EXPT_0325 = "gemini-2.5-pro-exp-03-25"
MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION = "gemini-2.0-flash-exp-image-generation"


def google_genai(prompt, model_name=MODEL_GEMINI_2_0_FLASH, response_mime_type="application/json", images=None,
                 temperature=0, max_output_tokens=8192):
    contents = []
    if images is not None and len(images) > 0:
        seen = set()
        unique_image_urls = [url for url in images if not (url in seen or seen.add(url))]
        for image in tqdm(unique_image_urls):
            path = gemini_upload_file.handle_file_path(image)
            try:
                # image_content = Image.open(path)
                image_content = upload_file(image)
            except Exception as e:
                utils.delete_file(path)
                print(f"Image.open Error {image} , {path} error {str(e)}")
                raise e

            contents.append(image_content)

    contents.append(prompt)
    response = google_genai_client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type=response_mime_type,
            max_output_tokens=max_output_tokens,
            temperature=temperature
        )
    )

    if response.candidates[0].finish_reason == types.FinishReason.MAX_TOKENS:
        raise MaxTokenException(f"reached max tokens {max_output_tokens}")

    return response.text


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def upload_file(image_url):
    image_local_path = gemini_upload_file.handle_file_path(image_url)
    return __do_file_upload_and_cache(image_local_path)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def upload_file_from_local(image_local_path):
    return __do_file_upload_and_cache(image_local_path)


def __do_file_upload_and_cache(local_image_path):
    cache_file_path = os.path.join(cache_dir, utils.md5_str(local_image_path) + ".json")

    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'r') as file:
            file_ref_dict = json.load(file)
            file_ref = types.File()
            file_ref.name = file_ref_dict.get("name")
            file_ref.mime_type = file_ref_dict.get("mime_type")
            file_ref.size_bytes = file_ref_dict.get("size_bytes")
            file_ref.create_time = datetime.strptime(file_ref_dict.get("create_time"), '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                tzinfo=timezone.utc)
            file_ref.expiration_time = datetime.strptime(file_ref_dict.get("expiration_time"),
                                                         '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            file_ref.update_time = file_ref_dict.get("update_time")
            file_ref.sha256_hash = file_ref_dict.get("sha256_hash")
            file_ref.uri = file_ref_dict.get("uri")
            file_ref.state = file_ref_dict.get("state")
            file_ref.source = file_ref_dict.get("source")

            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            if current_time < file_ref.expiration_time:
                # print("cache hint")
                return file_ref

    file_ref = google_genai_client.files.upload(file=local_image_path)
    # print(f"real uploading to google {local_image_path}")
    os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
    with open(cache_file_path, 'w') as file:
        json.dump(file_ref.to_json_dict(), file)
    return file_ref


def google_genai_conversation(history_messages, prompt, response_mime_type=None):
    history = []
    for message in history_messages:
        # role  Must be either 'user' or  'model'
        part = types.Part.from_text(text=message.get("content", ""))
        # 创建一个 Content 实例
        content = types.Content(parts=[part], role="user" if message.get("role") == "user" else "model", )
        history.append(content)

    chat = google_genai_client.chats.create(model=MODEL_GEMINI_2_0_FLASH, history=history)
    response = chat.send_message(prompt, config=types.GenerateContentConfig(
        max_output_tokens=1000 * 20,
        temperature=0,
        response_mime_type=response_mime_type
    ))

    return response.text


from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    LOCAL_IMAGE = "local_image"
    URL_IMAGE = "url_image"


class GenaiMessagePart:
    def __init__(self, message_type: MessageType, value: str):
        self.message_type = message_type
        self.value = value

    def __str__(self):
        return f"message_type: {self.message_type}, value: {self.value}"

    @staticmethod
    def image(image_url):
        message_type = MessageType.URL_IMAGE if image_url.startswith("http") else MessageType.LOCAL_IMAGE
        return GenaiMessagePart(message_type, image_url)


class UsageMetadata:
    def __init__(self, model, usage: types.UsageMetadata):
        self.model = model
        self.usage = usage

    def __str__(self):
        return f"UsageMetadata(model = {self.model}, usage={self.usage})"


class GenaiConversationMessage:
    def __init__(self, role, content: list[GenaiMessagePart], usage_metadata: types.UsageMetadata = None):
        self.role = role
        self.content = content
        self.usage_metadata = usage_metadata

    def __str__(self):
        break_line = "\n"
        return f"role: {self.role}\ncontent: [\n{break_line.join(str(part) for part in self.content)}]\nusage_metadata = {str(self.usage_metadata)}"

    @staticmethod
    def one(role, value, message_type=MessageType.TEXT):
        return GenaiConversationMessage(role, [GenaiMessagePart(message_type, value)])

    @staticmethod
    def text_and_images(text, images):
        content = [GenaiMessagePart(MessageType.TEXT, text)]

        if type(images) is str:
            content.append(GenaiMessagePart.image(images))
        elif type(images) is list:
            for image in images:
                content.append(GenaiMessagePart.image(image))

        return GenaiConversationMessage("user", content)

    def is_empty(self):
        return len(self.content) == 0


def save_binary_file(file_name, data):
    if os.path.exists(generate_image_save_dir_path) is False:
        os.makedirs(generate_image_save_dir_path)

    save_path = os.path.join(generate_image_save_dir_path, file_name)
    f = open(save_path, "wb")
    f.write(data)
    f.close()
    return save_path


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _prepare_message_for_request(index, conversation_message):
    parts = []
    for gemini_message_part in conversation_message.content:
        if gemini_message_part.message_type == MessageType.TEXT:
            parts.append(types.Part.from_text(text=gemini_message_part.value))
        elif gemini_message_part.message_type == MessageType.URL_IMAGE:
            f = upload_file(gemini_message_part.value)
            if f.mime_type in AVAILABLE_MIME_TYPES:
                parts.append(types.Part.from_uri(file_uri=f.uri, mime_type=f.mime_type))
            else:
                print(f"Unsupported mime type: {f.mime_type} , MessageType.URL = {gemini_message_part.value}")
        elif gemini_message_part.message_type == MessageType.LOCAL_IMAGE:
            if gemini_message_part.value == "image safety":
                parts.append(types.Part.from_text(text="because image safety , cannot generate image"))
            else:
                f = upload_file_from_local(gemini_message_part.value)
                if f.mime_type in AVAILABLE_MIME_TYPES:
                    parts.append(types.Part.from_uri(file_uri=f.uri, mime_type=f.mime_type))
                else:
                    print(f"Unsupported mime type: {f.mime_type} , MessageType.LOCAL = {gemini_message_part.value}")

    if len(parts) == 0:
        raise Exception(f"parts is empty：{str(conversation_message)}")

    return index, types.Content(parts=parts,
                                role=conversation_message.role if conversation_message.role == "user" else "model", )


"""
response_mime_type : application/json text/plain
"""


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def google_genai_output_images_and_text(new_message: GenaiConversationMessage,
                                        model=MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION,
                                        history_messages: list[GenaiConversationMessage] | None = None,
                                        system_instruction_prompt: str = None,
                                        response_mime_type="text/plain",
                                        max_output_tokens: int = 8192 * 2,
                                        temperature: float = 1,
                                        print_messages: bool = True,
                                        usage_meta_history: list = None) -> GenaiConversationMessage:
    global chunk
    if print_messages:
        if history_messages is not None:
            for hm in history_messages:
                print(hm)
        print(new_message)

    prepared_message = []
    prepared_message_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(_prepare_message_for_request, index, message) for index, message in
                   enumerate((history_messages or []) + [new_message])]
        print(f"\n-------preparing conversation 0 / {len(futures)}----------\n")
        for future in concurrent.futures.as_completed(futures):
            try:
                idx, result = future.result()
                prepared_message.append({
                    "index": idx,
                    "content": result
                })
                prepared_message_count += 1
                print(f"\rprepare message success : {prepared_message_count} / {len(futures)}")
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"prepare message failed, {str(e)}")

    prepared_message.sort(key=lambda x: x["index"])
    contents = [item["content"] for item in prepared_message]

    response_modalities = ["image", "text"] if model == MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION else None

    system_instruction = None if system_instruction_prompt is None else [
        types.Part.from_text(text=system_instruction_prompt),
    ],

    generate_content_config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=0.95,
        top_k=40,
        system_instruction=system_instruction_prompt,
        max_output_tokens=max_output_tokens,
        response_modalities=response_modalities,
        response_mime_type=response_mime_type,
    )

    response_content: list[GenaiMessagePart] = []

    print("\n-------conversation prepared , waiting response ----------\n")

    text_response_content = ""
    for chunk in google_genai_client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].inline_data:
            file_name = f"{utils.generate_uuid_datetime()}.png"
            image_save_path = save_binary_file(
                file_name, chunk.candidates[0].content.parts[0].inline_data.data
            )
            print(
                "File of mime type"
                f" {chunk.candidates[0].content.parts[0].inline_data.mime_type} saved"
                f"to: {image_save_path}"
            )
            response_content.append(GenaiMessagePart(MessageType.LOCAL_IMAGE, image_save_path))
        else:
            text_response_content += chunk.text
            print(chunk.text, end="")

    if chunk and chunk.candidates and chunk.candidates[0].finish_reason:
        if chunk.candidates[0].finish_reason == types.FinishReason.MAX_TOKENS:
            raise MaxTokenException(f"reached max tokens {max_output_tokens}")

        # if chunk.candidates[0].finish_reason != types.FinishReason.STOP:
        #     raise Exception("Unexpected Finish Reason: " + chunk.candidates[0].finish_reason)

    if chunk and chunk.prompt_feedback and chunk.prompt_feedback.block_reason:
        if chunk.prompt_feedback.block_reason == "IMAGE_SAFETY":
            response_content.append(GenaiMessagePart(MessageType.LOCAL_IMAGE, "image safety"))
        else:
            raise Exception("Prompt Feedback Block Reason: " + chunk.prompt_feedback.block_reason)

    usage_metadata = None
    if chunk and chunk.usage_metadata:
        try:
            print(f"model={model} , Usage Metadata:{chunk.usage_metadata}")
            usage_metadata = UsageMetadata(model, chunk.usage_metadata)
        except Exception as e:
            print(f"Error parsing usage metadata: {str(e)}")

    if text_response_content is not None and len(text_response_content) > 0:
        response_content.append(GenaiMessagePart(MessageType.TEXT, text_response_content))

    if usage_meta_history is not None:
        usage_meta_history.append(usage_metadata)

    response_conversation_message = GenaiConversationMessage("model", response_content, usage_metadata=usage_metadata)

    if response_conversation_message.is_empty():
        raise Exception("response_conversation_message is empty")

    return response_conversation_message


def get_generated_images(all_messages):
    generated_images = []

    for msg in all_messages:
        if msg.role == "model":
            for gemini_message_part in msg.content:
                if gemini_message_part.message_type == MessageType.LOCAL_IMAGE:
                    generated_images.append(gemini_message_part.value)

    return generated_images


if __name__ == "__main__":
    gemini_result = google_genai_output_images_and_text(
        GenaiConversationMessage.one("user", "你好，给我将一个200个字的笑话"), model="gemini-2.0-flash",
        history_messages=[],
        response_mime_type="text/plain", )

    print(gemini_result)
    print(gemini_result.usage_metadata)
    pass
