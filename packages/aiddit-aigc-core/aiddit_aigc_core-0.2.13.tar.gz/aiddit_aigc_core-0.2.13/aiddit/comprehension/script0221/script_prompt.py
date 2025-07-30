import aiddit.model.google_genai as google_genai


def image_description(image):
    prompt = f'''
请充分必要描述以下图片

要求：
- 输出为中文；
- 请只描述客观事实，不要加入任何```主观```评价性语言；
    - 关于人物的描述，需要包括性别、年龄、肤色、发型、穿着等信息；
    - 关于物品的描述，需要包括颜色、形状、大小、材质等信息；
    - 关于动物的描述，需要包括种类、颜色、大小、特征等信息；
    - 关于场景的描述，需要包括地点、时间、气氛、人物动作等信息；
    - 关于食物的描述，需要包括种类、颜色、形状、味道等信息；
    - 关于建筑的描述，需要包括风格、材质、颜色、大小等信息；
    - 如果图片存在拼接，需要描述拼接的方式、拼接的部分等信息；
    - 关于构图的描述，需要包括主体、背景、前景、对比等信息；
    - 关于排版的描述，需要包括文字的位置、字体、颜色、大小等信息；
    - 等等其他信息，需要充分描述；
    - 禁止出现'氛围'、'和谐'、'视觉呈现','美学'等指代无不明确的用词
- 要求描述详细，信息量丰富；字数300字以上；
- 直接输出描述结果，不要有任何多余的解释；
'''
    ans = google_genai.google_genai(prompt, model_name="gemini-2.0-flash", images=[image], temperature=0,
                                    response_mime_type=None)
    return ans


def note_script_from_image_description(note, image_description_results):
    cover = image_description_results[0]
    gallery = image_description_results[1:]

    gallery_description = "\n".join([f"【图{index + 2}】：\n{r.get('description')}\n" for index, r in
                                     enumerate(gallery)])

    prompt = f'''
我会给出小红书的帖子信息：

帖子的标题如下：
"""
{note['title']}
"""

帖子正文如下：
"""
{note['body_text']}
"""

我会给你一共{len(image_description_results)}张图片的描述，其中第一张图片是封面图片，其他图片是图集图片。
封面图片如下：
【图1】：
{cover.get('description')}

图集图片如下：
{gallery_description}

以上就是我提供的全部内容。

请你从内容创作的角度，根据我给出的内容，完成以下任务：
- 从内容创作的角度，对这条小红书的帖子进行创作脚本的拆解；
    - 拆解出来的创作脚本是能够完整的从脚本来还原创作复刻这条帖子的内容；
    - 拆解出来的创作脚本是对帖子内容的一个完整的解读；从【结构化】、【逻辑】的层面来进行拆解；
    - 请思考创作是如何去表现作者想要表达的主题；
    - 创作脚本是类似于电影的剧本，但是我现在要对一个小红书的图文帖子进行创作脚本的拆解；
    - 请不要以第三人称的方式去描述，而是站在第一人称视角去给出结果，假设是你的内容，你当时的创作过程脚本；
    - 我会给你以下几个方面的提示可以帮助你去思考，并给我结果：
        - 整体规划
            - 指的是对这个帖子的创作，整体层面的规划；
            - 标题、正文、图片之间的关系如何？如何环环相扣从而产生一个好内容？
            - 内容侧重与图片还是文字？还是图文都重要？为什么？
            - 为了表达内容的主题，整体规划是怎么样的？
            - 比如角色设置、服装设置、场景设置、拍摄、等等其他信息
            - 比如场景设置、拍摄、等等其他信息
            - 等等其他信息
        - 标题
            - 标题的吸引点如何构建？
            - 核心主题怎么体现？
            - 写作逻辑如何？
            - 等等其他信息
        - 正文
            - 正文的结构如何？
            - 写作技巧、手法、方式如何？
            - 内容的逻辑如何？
            - 等等其他信息；
        - 图片
            - 封面(dict)
                - 封面的选取逻辑（dict）: 为什么选取了这张图片作为封面？其背后的逻辑是什么？
                - 封面和内容主题的关系(dict)：图片是如何表现内容主题或者亮点的？
                - 其他重要信息（dict）
                - index(int):对应上面的图片序号
                - 图片要点(str): 结合当前内容的主题，给出图片的重要信息
            - 图集(dict)
                - 图集中图片规划（dict）
                    - 图集图片总数(index)
                    - 图集段落划分逻辑（dict）
                - 图集的数量规划逻辑（dict）
                - 图集和内容主题的关系(dict)：图片是如何表现内容主题或者亮点的？
                - 图集中图片的排列/顺序逻辑（dict）
                    - 图集之间的顺序怎么安排？排序的逻辑、依据是什么？
                - 图集图片列表（list(dict），每一张图片都包含以下信息：
                    - index(int): 对应上面的图片序号
                    - 图片要点(str): 结合当前内容的主题，给出图片的重要信息
            - 封面和图集的关联关系(dict)
            - 封面和图集的通用信息(dict)
    - 请参考（包含但不限于）上述提示，output in JSON format with keys:
        - 整体规划(dict)
        - 标题(dict)
        - 正文(dict)
        - 图片(dict):
            - 封面(dict)
            - 图集(dict)
            - 封面和图集的关联关系(dict)
要求：
- 输出为中文；
- 请只描述客观事实，不要加入任何```主观```评价性语言；
- 请不要只进行概括性的描述
    - 比如：标题很吸引人，正文很有趣，图片很好看，构图简洁明了，这样是不允许的；
    - 禁止出现'氛围'、'和谐'、'视觉呈现','美学'等指代无不明确的用词
- 输出为JSON，不要有除了JSON格式之外的其他输出；
'''
    print(prompt)

    ans = google_genai.google_genai(prompt, model_name="gemini-2.0-flash", temperature=0)

    print(ans)
    return ans


from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
import aiddit.utils as utils


def note_script(note):
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325
    history_messages, ask_message = build_note_script_message(note)
    ans_conversation_message = google_genai.google_genai_output_images_and_text(ask_message, model=model,
                                                                                history_messages=history_messages,
                                                                                response_mime_type="application/json",
                                                                                temperature=0)

    return ans_conversation_message.content[0].value


def note_create_style(note):
    images = utils.remove_duplicates(note.get("images", []))
    prompt = "总结这些图片的创作风格"
    ans_conversation_message = google_genai.google_genai_output_images_and_text(GenaiConversationMessage.text_and_images(prompt,images),
                                                                                model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                                response_mime_type="application/json",
                                                                                temperature=0)
    return ans_conversation_message.content[0].value

def build_note_script_message(note):
    images = utils.remove_duplicates(note.get("images", []))

    history_messages = []
    for index, image in enumerate(images):
        if index == 0:
            prompt_message = GenaiMessagePart(MessageType.TEXT, "这是小红书的封面图片 图【1】")
        else:
            prompt_message = GenaiMessagePart(MessageType.TEXT, f"这是小红书的图集图片【图{index + 1}】")

        image_message = GenaiMessagePart(MessageType.URL_IMAGE, utils.oss_resize_image(image))
        contents = [prompt_message, image_message]
        message = GenaiConversationMessage("user", contents)
        history_messages.append(message)

    prompt = f'''
上面就是我给出的所有的小红书图片信息了，一个{len(images)}张，接下来我会给出小红书的帖子信息：

帖子的标题如下：
"""
{note['title']}
"""

帖子正文如下：
"""
{note['body_text']}
"""

以上就是我提供的全部内容。

请你从内容创作的角度，根据我给出的内容，完成以下任务：
- 从内容创作的角度，对这条小红书的帖子进行创作脚本的拆解；
    - 拆解出来的创作脚本是能够完整的从脚本来还原创作复刻这条帖子的内容；
    - 拆解出来的创作脚本是对帖子内容的一个完整的解读；从【结构化】、【逻辑】的层面来进行拆解；
    - 请思考创作是如何去表现作者想要表达的主题；
    - 创作脚本是类似于电影的剧本，但是我现在要对一个小红书的图文帖子进行创作脚本的拆解；
    - 请不要以第三人称的方式去描述，而是站在第一人称视角去给出结果，假设是你的内容，你当时的创作过程脚本；
    - 我会给你以下几个方面的提示可以帮助你去思考，并给我结果：
        - 整体规划
            - 指的是对这个帖子的创作，整体层面的规划；
            - 标题、正文、图片之间的关系如何？如何环环相扣从而产生一个好内容？
            - 内容侧重与图片还是文字？还是图文都重要？为什么？
            - 为了表达内容的主题，整体规划是怎么样的？
            - 比如角色设置、服装设置、场景设置、拍摄、等等其他信息
            - 比如场景设置、拍摄、等等其他信息
            - 等等其他信息
        - 标题
            - 标题的吸引点如何构建？
            - 核心主题怎么体现？
            - 写作逻辑如何？
            - 等等其他信息
        - 正文
            - 正文的结构如何？
            - 写作技巧、手法、方式如何？
            - 内容的逻辑如何？
            - 等等其他信息；
        - 图片
            - 封面(dict)
                - 封面的选取逻辑（dict）: 为什么选取了这张图片作为封面？其背后的逻辑是什么？
                - 封面和内容主题的关系(dict)：图片是如何表现内容主题或者亮点的？
            - 图集(dict)
                - 图集中图片规划（dict）
                    - 图集图片总数(index)
                    - 图集段落划分逻辑（dict）
                - 图集的数量规划逻辑（dict）
                - 图集和内容主题的关系(dict)：图片是如何表现内容主题或者亮点的？
                - 图集中图片的排列/顺序逻辑（dict）
                    - 图集之间的顺序怎么安排？排序的逻辑、依据是什么？
            - 图片表现方式(dict)
                - 图片上运用了什么方式/技巧去呈现内容，从而增加内容的表现力？等等
                - 图片的风格、色调、构图、角度、透视等等
            - 图片中人物表现方式(dict)
                - 呈现方式：一些具体例子，你需要根据实际的图片选择合适的词语，包括但不限于以下几种：
                    - 人物大小：人小景大，人景结合，特写，全身像，半身像等等
                    - 人物位置：居中、黄金分割、边缘、前景、背景等等
                    - 人物姿态：站立、坐着、行走、奔跑、背对镜头、侧身、凝视远方、与他人互动等等
                    - 其他：人物表情、人物动作、人物特点、人物与其他元素的关系等等
                - 人物特点：人物的性别、年龄、肤色、发型、穿着等信息
                - 人物与其他元素的关系：人物与场景、人物与物品、人物与其他人物等等
                - 人物在图集中出现的占比、频率等信息
                - 以及其他关于人物的补充信息
    - 请参考（包含但不限于）上述提示，output in JSON format with keys:
        - 整体规划(dict)
        - 标题(dict)
        - 正文(dict)
        - 图片(dict):
            - 封面(dict)
            - 图集(dict)
            - 图片表现方式(dict)
            - 图片中人物表现方式(dict)
            - 封面和图集的通用信息(dict)
            - 封面和图集的关联关系(dict)
要求：
- 输出为中文；
- 请只描述客观事实，不要加入任何```主观```评价性语言；
- 请不要只进行概括性的描述
    - 比如：标题很吸引人，正文很有趣，图片很好看，构图简洁明了，这样是不允许的；
    - 禁止出现'氛围'、'和谐'、'视觉呈现','美学'等指代无不明确的用词
- 输出为JSON，不要有除了JSON格式之外的其他输出；
    - dict表示为json object格式，请严格控制你的输出格式和类型；
    '''
    # print(prompt)

    ask_message = GenaiConversationMessage("user", [GenaiMessagePart(MessageType.TEXT, prompt)])

    return history_messages, ask_message
