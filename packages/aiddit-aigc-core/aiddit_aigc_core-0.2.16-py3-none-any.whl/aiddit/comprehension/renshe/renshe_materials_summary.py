import image_article_comprehension.aiddit.model.google_genai as genai
from tqdm import tqdm
from google.genai import types
import image_article_comprehension.aiddit.utils as utils
from tenacity import retry, stop_after_attempt, wait_fixed
import json
import os


def append_conversation_message(conversation_list, role, message, images, save_path=None):
    conversation_list.append({
        "role": role,
        "message": {
            "content": message,
            "images": images
        }
    })

    if save_path is not None:
        utils.save(conversation_list, save_path)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_message_with_retry(chat, contents):
    response = chat.send_message(contents, config=types.GenerateContentConfig(
        response_mime_type="application/json",
    ))
    return response


def extract_renshe_constant(account_info, comprehension_note_list, conversation_list_save_path=None):
    conversation_list = []

    chat = genai.google_genai_client.chats.create(model="gemini-2.0-flash")
    avatar_url = account_info.get("avatar_url")
    system_prompt = f"""
有一个小红书的账号：
账号名称：{account_info.get("account_name")}
账号简介：{account_info.get("description")}
以及我会再给你账号的头像图片。

接下来，
我会依次给你小红书的帖子数据
包括标题、正文、封面、图集等信息
第一张图为封面，其余的为图集

我会一个帖子的一个帖子的给你，你需要针对每个新的帖子，以及上个帖子的结果来总结、修正你的结果
你需要帮我完成以下任务：
- 找出帖子中跟账号人设相关的素材，它可以是：
    -  角色
        - 角色如果是人：包括外貌、性别、性格、职业、兴趣爱好等
        - 角色如果是动物：包括外貌、种类、性格、品种等
        - 每个角色应该分别是一个独立的素材，并且结合上下文给出角色的名称作为素材名称
    - 场景
        - 场景的时间、地点、氛围、气氛等
        - 场景的构成元素，比如家具、装饰、道具等
        - 场景的构成元素应该分别是一个独立的素材
    -  视觉风格，包括配色、字体、排版、滤镜等。
        - 每一种应该分别是一个独立的素材
        - 封面和图集要进行区分，因为封面和图集的风格可能不一样；
        - 对封面和图集的创作形式、固定模版、排版结构等形式保持高度的敏感，因为这是一个账号的风格的体现；
        - 如果没有视觉风格，可以不提取；
    -  符合人设身份和风格的常用表达方式、口头禅、标签等。
        - 每一种应该分别是一个独立的素材
    -  创作的通用内容结构和表达方式、固定模版。
        - 创作形式是否存在模版形式：比如封面都是用统一的模版、图集中的图片是否是统一的形式来呈现等等。
        - 每一种应该分别是一个独立的素材
    - 以上维度仅供参考！不要局限于上述维度。如果没有的，可以不提取；
    - 你可以根据你的理解和判断，找到更合适的维度，上面没有的维度直接忽略，不要进行解释；
- 对于图片的描述请严格区分封面和图集；
- 每个素材名称需要简洁明了，符合口语化的表达；严禁复杂的专业术语、结构；进行简化、抽象；
    - 每一种素材都应该拆分最小的颗粒度、最小的单元
    - 可以是名词、动词、形容词、副词等等
- 每个素材要有`出现频率`：1%~100%；你需要根据实际情况+每个帖子的数据来判断；
    - 出现频率是该素材，综合历史数据，在帖子中出现的频率；
    - 素材的出现频率是基于帖子，而不是基于帖子中的图片；
    - 在最后的输出结果中，仅保留`出现频率`大于 50%的素材，在过程中可以暂时保留；
- 素材是为了，再次创作的时候，要保持这些素材，从而使得创作者的风格保持一致；
- 第一个帖子应该是你的初始结果，要求对一个帖子进行充分必要全面的分析和拆解；
- 你需要在后续的帖子中一步一步修正你的结果，最终的结果是取每个帖子中的交集部分；   
    - 每一次给你一个新的帖子都是为了完善和纠正之前的结果；
    - 用帖子的数据是为了让你更好的修正你的结果；
    - 最终的结果是所有帖子中共有的、能代表账号风格的素材；
    - 你的结果需要是一个动态的过程，不是一个静态的结果；

要求如下：
    细致入微：尽可能从各个维度挖掘素材，不放过任何细节。
    客观准确：基于数据本身进行分析，避免主观臆断。
    动态调整：根据新帖子的数据，及时修正和完善之前的分析结果。
    求同存异：最终提取的是所有帖子中共有的、能代表账号风格的素材。
    调整频率：根据新帖子的数据，调整现有素材的“出现频率”。
    修改详情：完善现有素材的细节描述。

- 最终的输出结果为JSON，格式如下：
{{
    素材名称1 : {{
        出现频率(int)
        素材类型(str)
        explanation(str)
        调整过程(str)
        详情(dict)
    }}
    素材名称2,
    ...
    素材名称N,
}}

好的，以上就是我的任务要求，你准备好了吗？
如果准备好了，请回复“准备好了”，并说明你对这个任务的理解。
如果你完成的比较好，我会奖励你一个大鸡腿。
    """

    append_conversation_message(conversation_list, "user", system_prompt, [avatar_url], conversation_list_save_path)

    response = chat.send_message(system_prompt)

    append_conversation_message(conversation_list, "assistant", response.text, None, conversation_list_save_path)

    print(response.text)

    for index, note in enumerate(comprehension_note_list):
        p = ""

        if index == 0:
            p += "第一个帖子，你需要对一个帖子进行充分必要全面的分析和拆解\n"
        elif index == len(comprehension_note_list) - 1:
            p += "这是最后一个帖子，你需要给出完整的结果作为结论了！！！\n"
        else:
            p += f"这是第{index + 1}个帖子，基于新增的这个帖子，请仔细分析和修正你的结果\n"

        p += f"""标题：{note.get("title")}

    正文：{note.get("body_text")}    

    Attention：第一张图为封面，其余的为图集图片！
    """

        images = [utils.oss_resize_image(img) for img in note.get("images", [])]
        append_conversation_message(conversation_list, "user", p, images, conversation_list_save_path)
        contents = []
        if images is not None and len(images) > 0:
            seen = set()
            unique_image_urls = [url for url in images if not (url in seen or seen.add(url))]
            for image in tqdm(unique_image_urls):
                contents.append(genai.upload_file(image))

        contents.append(p)

        response = send_message_with_retry(chat, contents)
        append_conversation_message(conversation_list, "assistant", response.text, None, conversation_list_save_path)
        print(response.text)

    summary_prompt = """最后请根据上述所有的素材，总结并给出所有素材的详细描述：
要求如下：
- 低于出现频率80%的素材不要保留；
- 素材详情的应该详细到具体的细节；
- 每个素材的详情能够支持还原到素材的实际情况；
- 最终的输出结果为JSON，格式如下：
{{
    素材名称1 : {{
        素材类型(str)
        详情(dict)
    }}
    素材名称2,
    ...
    素材名称N,
}}
"""
    append_conversation_message(conversation_list, "user", summary_prompt, None, conversation_list_save_path)
    response = send_message_with_retry(chat, [summary_prompt])
    print(response.text)
    append_conversation_message(conversation_list, "assistant", response.text, None, conversation_list_save_path)

    return response.text


def test():
    renshe_info_path = "/image_article_comprehension/aiddit/comprehension/renshe/result/20250110_摸鱼阿希.json"
    renshe_info = json.loads(open(renshe_info_path, 'r').read())
    note_dir_path = renshe_info.get("comprehension_note_path")
    note_list = [json.load(open(os.path.join(note_dir_path, v), 'r')).get("note_info") for v in
                 os.listdir(note_dir_path) if
                 v.endswith(".json")]
    # comprehension_note_list = random.sample(note_list, min(len(note_list), 5))
    input_note_list = note_list[:15]
    file_name = str(len(input_note_list)) + "_x_" + os.path.basename(renshe_info_path)

    conversation_save_path = f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result/materials/" + file_name

    extract_renshe_constant(renshe_info.get("account_info"), input_note_list, conversation_save_path)


if __name__ == "__main__":
    test()
    pass
