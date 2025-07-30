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


class GenaiConversationMessage:
    def __init__(self, role, content: list[GenaiMessagePart]):
        self.role = role
        self.content = content

    def __str__(self):
        break_line = "\n"
        return f"role: {self.role}, content: [\n{break_line.join(str(part) for part in self.content)}]"

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
                                        system_instruction_prompt : str = None,
                                        response_mime_type="text/plain",
                                        max_output_tokens: int = 8192*2,
                                        temperature: float = 1,
                                        print_messages: bool = True) -> GenaiConversationMessage:
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
            print(chunk.text, end = "")

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

    if text_response_content is not None and len(text_response_content) > 0:
        response_content.append(GenaiMessagePart(MessageType.TEXT, text_response_content))

    response_conversation_message =  GenaiConversationMessage("model", response_content)

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
    # google_genai_conversation()

    #     prompt_list = ["""你将要帮我生成一组图片，下面是图片中的通用信息：
    # {
    # "阿希": "年轻男性，身穿休闲办公服装，发型简单利落的短发，体型中等。表情生动丰富，能展现出从兴奋到生无可恋的多种状态。坐姿自然随意，符合年轻打工人特征。",
    # "办公室工位": "标准的开放式办公工位，配备灰色办公桌和黑色办公椅，桌面上有显示器、键盘、鼠标等基础办公设备。工位四周有矮隔板，背景是其他同事的工位。",
    # "打工人/生活用品": "办公桌面上摆放着工牌、便利贴、水杯、手机、计算器等办公必需品，以及外卖盒、零食包装等生活用品，呈现出真实的办公环境。",
    # "搞怪表情": "夸张的面部表情，包括瞪大眼睛、嘴角上扬的兴奋表情，以及眼神空洞、面无表情的呆滞状态，体现出强烈的情绪反差。",
    # "摸鱼状态": "瘫坐在办公椅上，身体前倾或后仰，双手无力下垂，眼神放空，整个人呈现出精神涣散的状态。"
    # }
    # 如果你听明白了，请回复 好的。""",
    #                    "在标准的开放式办公工位上，年轻男性阿希身穿休闲办公服装，看到手机补贴新闻，兴奋地举起手机，脸上露出夸张的瞪眼笑容，背景是摆满办公用品和生活物品的工位。",
    #                    "年轻男性阿希在开放式办公工位上，打开计算器，认真计算工资，桌面上整齐摆放着工牌、便利贴等办公用品，表情严肃认真",
    #                    "年轻男性阿希在办公工位上，掰着手指头，计算各项支出，嘴里念念有词，眉头紧锁，似乎在为钱发愁",
    #                    "年轻男性阿希在办公工位上，看着计算器上的余额，表情逐渐凝固，眼神空洞呆滞，面部表情夸张地显示出震惊，似乎发现了什么可怕的事情",
    #                    "年轻男性阿希瘫坐在办公工位的椅子上，身体无力下垂，眼神放空，桌面上散落着办公用品和生活物品，整个人呈现出生无可恋的状态"]
    # prompt_list = ["解释马太效应，越详细越好"]
    #
    # hms = []
    #
    # for prompt in prompt_list:
    #     ml: list[GenaiMessagePart] = []
    #     ml.append(GenaiMessagePart(MessageType.TEXT, prompt))
    #     mess = GenaiConversationMessage("user", ml)
    #
    #     res = google_genai_output_images_and_text(mess, history_messages=hms, max_output_tokens=200)
    #     hms.append(mess)
    #     hms.append(res)
    #     print(res)

    # print(types.BlockedReason.BLOCKED_REASON_UNSPECIFIED.value== "11BLOCKED_REASON_UNSPECIFIED")
    #
    # print("对单张或多张图片进行分析，并根据问题进行回答；\n\nArgs:\n    image_url_list: 需要分析的图片URL列表，支持单张或多张图片同时分析\n    question: 需要分析的问题（最好一次只问一个问题）\n")

    # ans =  google_genai(prompt="描述这张图片", images=["http://res.cybertogether.net/crawler/image/9e9db9930ad678316454a5e3a75be389.webp"])
    # print(ans)

    # r = utils.try_remove_markdown_tag_and_to_json("[{\"title\": \"骑手们别太搞笑了哈哈哈\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g008314s5modg1e4g5nmh0ctg8u6ns1atnho?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"哥们，你越界了啊\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg31d2ukbad106g5obcvu4gjv8bkscj3kg?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"他是不是有一点点可爱\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg31ev441vn6sdg5n2hc5e4592ttlt3688?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"老板下班兼职送外卖\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg30tr7esnj50505n8pm605huvn0ni9apg?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"关于老板为了给我们发工资去\"送外卖\"这件事\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg31avrpndvng7040uh3kdkqufr38nev6o?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"老板开始重操旧业做起外卖小哥\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g0083134ajmdomq6g5n8pm605huvnoq12448?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"段子果然都来源于现实\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg31dscbjt3gu705oidecr41suf2f73478?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"谁的老板还在一线奋斗！\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/notes_pre_post/1040g3k031ghs92jjjo5g4buk8cgqvcop69df0k0?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"东子亲自送外卖，这波操作太圈粉了！\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/1040g2sg31gis1hfj3ujg5opgatuovno8eab7ieo?imageView2/2/w/1080/format/webp\"]}, {\"title\": \"千亿总裁送外卖！\", \"body_text\": \"\", \"image_url_list\": [\"https://ci.xiaohongshu.com/notes_pre_post/1040g3k831gj51r4f3qeg5nf78n808hf2qdqi6tg?imageView2/2/w/1080/format/webp\"]}]")
    #
    # print(json.dumps(r, ensure_ascii=False, indent=4))

    print("[\n  {\n    \"title\": \"上班要明白的道理\",\n    \"body_text\": \"无论在任何地方上班，\\n只要公司不开除你，那你就先干着\\n同事对你指指点点的时候，你就笑笑\\n领导批评你的时候，你就听听就好，不要太在意。\\n#被文字治愈[话题]# #治愈系漫画[话题]# #看淡一切烦恼[话题]# #好好活在当下[话题]# #人间清醒[话题]# #人生不必太多焦虑[话题]# #上班为了什么[话题]# #打工人也是人[话题]# #对工作的态度[话题]# #女生必看[话题]#\",\n    \"image_url_list\": [\"http://res.cybertogether.net/crawler/image/5565693591ab874a9955f5791c942f86.webp\"]\n  },\n  {\n    \"title\": \"永远会被阳光治愈🌞\",\n    \"body_text\": \"今日开窗时分在下午，本以为可以静静等天黑，却迎来了阳光返场，突然就想到一句诗：\\n\"柳暗花明又一村\"。\\n真像梦一样，美好到不真实。\\n#好好生活大赛[话题]# #年度旷野时分[话题]# #浪漫生活的记录者[话题]#  #冬日好好宅[话题]# #小红书居家趋势[话题]# #20分钟家效应[话题]# #独居女孩[话题]# #记录吧就现在[话题]# #家有艺术感[话题]# #边生活边艺术[话题]# @VLOG薯 @家居薯\",\n    \"image_url_list\": [\"http://res.cybertogether.net/crawler/image/b0976a71d24ca0e6b06db02bf1c810e7.jpeg\"]\n  },\n  {\n    \"title\": \"地铁上活捉一只打工人...\",\n    \"body_text\": \"《希老师打工人颜艺合集》\\n什么时候才放大长假啊啊啊啊啊!!!\\n最近公司周六也加班...\\n本打工人真的有点撑不住了...[哭惹R][哭惹R][哭惹R]\\n\\t\\n#打工人日常[话题]# #打工人[话题]# #搞笑的日常[话题]# #沙雕搞笑[话题]# #奇葩同事[话题]# #打工人日常[话题]# #打工人精神状态[话题]#\",\n    \"image_url_list\": [\"http://res.cybertogether.net/crawler/image/0de587fd37a9d8eeb05548103845c39a.webp\"]\n  },\n  {\n    \"title\": \"打工人：你好，吃派吗？\",\n    \"body_text\": \"《摸鱼打工人的精神状态》\\n拜托阿希去摸鱼的时候打包个肯德基...\\n摸到肯德基疯狂吃派活动，爽歪歪...[doge]\\n结果拿了个晾衣架去打包...[汗颜R]\\n这是得多怕同事吃上热乎的呀...[捂脸R][捂脸R]\\n\\t\\n奶黄风味派绵密顺滑，微甜不腻的港式奶黄流心！\\n一口爆浆的浓郁奶香~[萌萌哒R]\\n白桃风味派酸甜爆汁，大颗京十四白桃果肉！\\n一口清爽春回~[哇R]\\n红豆派经典饱满有层次，颗粒扎实的红豆酱！\\n尊嘟好吃！爱了！！[害羞R][害羞R]\\n\\t\\n#搞笑的日常[话题]# #摸鱼[话题]# #别惹打工人[话题]# #当代年轻人打工精神状态[话题]#\",\n    \"image_url_list\": [\"http://res.cybertogether.net/crawler/image/6c1a48cd0513ed898d9df91fdea097ac.jpeg\"]\n  }\n]")
    pass
