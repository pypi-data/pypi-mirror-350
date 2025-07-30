import google.generativeai as generativeai
import os
import json
from tqdm import tqdm
from image_article_comprehension.aiddit.model import upload_file, handle_file_path
from google.ai.generativelanguage_v1beta.types import content
import time

os.environ['http_proxy'] = 'http://127.0.0.1:8118'
os.environ['https_proxy'] = 'http://127.0.0.1:8118'
os.environ['all_proxy'] = 'socks5://127.0.0.1:8119'

generativeai.configure(api_key="AIzaSyDP8v6Q_vIYH9dZIPqSShB0GNVx21RAV4Q")

def distinct_image_content(note, img_num=100):
    distinct_image_url = []
    image_url_set = set([])
    for image_url in note['images'][:img_num]:
        if image_url not in image_url_set:
            distinct_image_url.append(image_url)
            image_url_set.add(image_url)

    return distinct_image_url


def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
    should probably employ a more sophisticated approach.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = generativeai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = generativeai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()


## response_mime_type="application/json、 text/plain"
def start_chat(prompt, model_name="gemini-2.0-flash-exp", response_mime_type="application/json", images=None,
               temperature=0):
    # Create the model
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": response_mime_type,
    }

    files = []
    if images is not None and len(images) > 0:
        seen = set()
        unique_image_urls = [url for url in images if not (url in seen or seen.add(url))]
        for file in tqdm(unique_image_urls):
            r = upload_file(file, generativeai)
            if r is not None:
                files.append(r)

    model = generativeai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config
    )

    history = []
    if len(files) > 0:
        if images is not None and any("mp4" in image for image in images):
            wait_for_files_active(files)
        history = [
            {
                "role": "user",
                "parts": files
            },
        ]

    chat_session = model.start_chat(history=history)

    response = chat_session.send_message(prompt)

    return response.text


def translate_to_mj_prompt(text):
    # Create the model
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = generativeai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="你是一位Midjourney Prompt工程师",
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(
        f"""请将以下描述翻译成英文，请遵循以下规则：
-注意不要有Midjourney的banned word：
    ALLOWED
    Safe For Work (SFW) content.
    Respectful or light-hearted parodies, satire, andcaricatures using real images.
    Fictional or exaggerated scenarios, includingabsurd or humorous situations.
    NOT ALLOWED
    Content that disrespects, harms, or misleadsabout public figures or events.
    Hate speech, explicit or real-world violence.Nudity or overtly sexualized images.Imagery that might be considered culturallyinsensitive.
-在避免banned word的基础上，应该详细、准确的还原中文意思;
-请直接输出指令的英文结果，不要有任何解释以及命令;
-输出结果应该去掉json标记;

描述如下：{text}
""")

    return response.text


def translate_to_english(text):
    # Create the model
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = generativeai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="你是一名中文翻译英文的翻译专家",
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(
        f"将以下内容翻译成英文，直接原文保持格式输出翻译结果，不要有任何多余的解释：\n{text}")

    return response.text


def translate_to_chinese(text):
    # Create the model
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = generativeai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="你是一名英文翻译中文的翻译专家",
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(
        f"将以下内容翻译成中文，直接原文保持格式输出翻译结果，不要有任何多余的解释：\n{text}")

    return response.text


def gemini_script_section(note):
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = generativeai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    images = distinct_image_content(note, 100)

    files = []

    for file in tqdm(images):
        r = upload_file(file, generativeai)
        if r is not None:
            files.append(r)
        else:
            raise Exception(f"图片上传失败 : {file}")

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": files
            },
        ]
    )

    prompt = f'''
我会给出图片和以下小红书的帖子信息；
帖子的标题如下：
"""
{note['title']}
"""
帖子正文如下：
"""
{note['body_text']}
"""

以上就是我提供的全部内容。

请你从内容创作的角度，根据我给出的内容，按照以下步骤完成我给出的任务：
1. 整体先理解图片，将我给出的所有图片按照一定的规则进行分组；
    - 分组规则可能是根据图片的内容、风格、色调、主题、故事性、活动和动作等进行分组;
    - 分组规则也可以类似于电影中的镜头/脚本；
    - 从第一张图片开始【依次】往后找，按照分组规则找到一组`图片序号连续`的图片，这些图片就是一个分组；
    - 严格按照：【每一个分组中的图片序号必须是连续的】：
       - 比如一共5张图片；将会分成 1-2-3-4-5 或者 1-2-3 和 4-5；不能出现 1-2-5 或者 3-4；
2. 描述每个分组的主题思想：
    - 直接描述分组中的主要内容、场景、思想，不要分别对每张图片中进行描述；
    - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
    - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
    - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
3. 描述每个分组中，属于每个分组的独特，且分组内所有图片的共性内容;
    - 描述尽可能详细，不要遗漏任何细节；
    - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
    - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
    - 包括图片中的光影、色彩、构图、角度、主题、风格、后期处理等等等维度；
    
要求：
- 输出为中文；
- 严格按照分组的规则进行分组；确保每个分组中的图片序号是连续的；
- 请只描述客观事实，不要加入任何'主观'评价性语言；
- 语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format, each JSONObject with  keys:
  - sections(List), each JSONObject with keys:
      - `section_image_index`(List): the index of images in this section, first image index is 0;
      - `section_description `(str): the description of this section;
      - 'section_common'(dict), the common part of this section ， use chinese to define key and value;
                '''.strip()

    response = chat_session.send_message(prompt)

    return response.text


if __name__ == '__main__':
    # Create the model
    # r = translate_to_chinese(
    #     "A young woman with long, dark brown hair and light skin is standing on a stage, holding a golden award statue. She is wearing a dark, sparkly, floor-length gown with a sweetheart neckline and a high slit on the side. The gown appears to be made of a sheer material, allowing some of her legs to be visible. The stage is dark blue, and there is a microphone stand visible to the left of the frame. The background is blurred, but appears to be a large, dark blue screen. The woman is smiling and looking directly at the camera.")
    #
    # print(r)
    # note_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/要点_脚本_材料测试数据/669e5a45000000002701f7bb.json"
    # note = json.load(open(note_path, 'r'))
    # gemini_script_section(note)

    ans = start_chat("描述这个视频", images=[
        "https://www.douyin.com/aweme/v1/play/?video_id=v0d00fg10000cta33p7og65iblol7aig&ratio=1080p&line=0"])
    print(ans)

    pass
