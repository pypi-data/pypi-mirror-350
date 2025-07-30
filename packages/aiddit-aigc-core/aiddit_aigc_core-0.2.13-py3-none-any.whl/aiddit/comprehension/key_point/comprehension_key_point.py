from image_analyzer.lib.chat import try_chat_with_data, get_client
from image_article_comprehension.aiddit.model import gemini


def pack_image_content(note, img_num=100):
    image_content = []
    image_url_set = set([])
    for image_url in note['images'][:img_num]:
        if image_url not in image_url_set:
            image_content.append({"type": "image_url", "image_url": {"detail": "low", "url": image_url}})
            image_url_set.add(image_url)
    return image_content


def distinct_image_content(note, img_num=100):
    distinct_image_url = []
    image_url_set = set([])
    for image_url in note['images'][:img_num]:
        if image_url not in image_url_set:
            distinct_image_url.append(image_url)
            image_url_set.add(image_url)

    return distinct_image_url


def analysis_key_point_v1(note, model='claude-3-5-sonnet-20241022', client=None, max_tokens=4096, seed=None,
                          temperature=0.0):
    # if client is None:
    #     client = get_client(model=model)
    # image_content = pack_image_content(note, img_num=10)
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

请你从内容创作的角度，根据我给出的内容，按照以下步骤找到内容的所有`亮点`，每一个`亮点`应该遵循以下步骤得出：

1. 找到`内容亮点的角度`：
     - 首先`内容亮点的角度`需要结合内容整体的主题；与主题无关紧要的可以忽略；
     - `内容亮点的角度`指的是你认为这个内容最吸引人的地方：可能是内容的创意、内容的视觉表达、内容的反差、内容的玩梗等等；
     - 严格去挑选，平庸且常见的不应该成为内容的亮点，你需要找到内容中最具最最有吸引力或者最有代表性的地方；

2. 从`内容亮点的角度`出发发现内容的创作'亮点`：
     - `亮点`一定要能够反映内容中最独特、最具有吸引力的，比如：女性的身材或颜值、创意、搞怪、玩梗、视觉等等；
     - 亮点可能存在于图片中、也可能存在标题和正文的文本中，你需要结合图片和文字，判断真正的亮点来源；
     - 确定亮点的专业领域，用专业领域的相关词汇表达亮点；要求用词精准拿捏，专业性强、无歧义；
     - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
     - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
     - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；

3. 亮点的组成描述：
     - 请结构化的描述以上亮点的详细组成部分，比如：亮点的主体、亮点的背景、亮点的细节等等；
     - 目的是为了在二次创作的时候还原以上亮点，所以这也是AIGC基于亮点去二次创作需要充分必要的生成材料；
     - 亮点的组成描述要求用词精准拿捏，专业性强、无歧义；
     
4. 亮点保持依赖的组成：
    - 为了能够精准的还原亮点，从`亮点组成`(Dict)`给出需要严格依赖的组成部分；
    
        
要求：
- 输出为中文；
- 请只描述客观事实，不要加入任何'主观'评价性语言；
- 语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；
- 请直接输出JSON格式，避免JSON Value中出现`"`，因为这会导致解析失败，确保输出能够被JSON语法正确解析，不要有除了JSON格式之外的其他输出；
- 确保直接输出JSON数组，直接输出的结果不是JSON对象；
- direct output in JSONArray[] format , array with each JSONObject has keys:
  - `内容亮点的角度`(str) 
  - `亮点 `(str)
  - `亮点组成`(Dict)
  - `亮点依赖的组成`(List) , each value is a str
    '''.strip()
    # note_data = image_content + [{"text": prompt, "type": "text"}]
    # ans = try_chat_with_data(
    #     note_data,
    #     client=client,
    #     model=model,
    #     max_tokens=max_tokens,
    #     seed=seed,
    #     temperature=temperature
    # )

    # ans = claude35(prompt, image_list=note.get("images", []))

    print(prompt)
    ans = gemini(prompt, images=note.get("images", []))
    return ans


def analysis_key_point_segment(note, model='claude-3-5-sonnet-20241022', client=None, max_tokens=4096, seed=None,
                               temperature=0.0):
    if client is None:
        client = get_client(model=model)
    image_content = pack_image_content(note)
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

请你从内容创作的角度，根据我给出的内容，按照以下步骤找到内容的所有`亮点`，每一个`亮点`应该遵循以下步骤得出：

1. 找到`内容亮点的角度`：
     - 首先`内容亮点的角度`需要结合内容整体的主题；与主题无关紧要的可以忽略；
     - `内容亮点的角度`指的是你认为这个内容最吸引人的地方：可能是内容的创意、内容的视觉表达、内容的反差、内容的玩梗等等；
     - 严格去挑选，平庸且常见的不应该成为内容的亮点，你需要找到内容中最具最最有吸引力或者最有代表性的地方；

2. 从`内容亮点的角度`出发发现内容的创作'亮点`：
     - `亮点`一定要能够反映内容中最独特、最具有吸引力的，比如：女性的身材或颜值、创意、搞怪、玩梗、视觉等等；
     - 亮点可能存在于图片中、也可能存在标题和正文的文本中，你需要结合图片和文字，判断真正的亮点来源；
     - 确定亮点的专业领域，用专业领域的相关词汇表达亮点；要求用词精准拿捏，专业性强、无歧义；
     - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
     - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
     - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；

3. 亮点的组成描述：
     - 请结构化的描述以上亮点的详细组成部分，比如：亮点的主体、亮点的背景、亮点的细节等等；
     - 目的是为了在二次创作的时候还原以上亮点，所以这也是AIGC基于亮点去二次创作需要充分必要的生成材料；
     - 如果亮点是纯视觉相关：
        - 请给出最具代表性的视觉来源的图片segment；
        - 在输出`亮点组成`(Dict)第一层中用字段`image_vision`(List)表示，image_vision中的每一个元素是一个Dict，包含以下字段：
            - image_index(int)：表示我给你的第几张图片；
            - image_width(int)：表示图片的宽度；
            - image_height(int)：表示图片的高度；
            - segment_position(List): 亮点视觉的在图片中的位置，top,left,right,bottom四个方向在图片中的坐标；
     - 亮点的组成描述要求用词精准拿捏，专业性强、无歧义；


要求：
- 输出为中文；
- 请只描述客观事实，不要加入任何`主观`评价性语言；
- 语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSONArray format , each JSONObject with keys:
  - `内容亮点的角度`(str) 
  - `亮点 `(str)
  - `亮点组成`(Dict)
    '''.strip()
    note_data = image_content + [{"text": prompt, "type": "text"}]
    ans = try_chat_with_data(
        note_data,
        client=client,
        model=model,
        max_tokens=max_tokens,
        seed=seed,
        temperature=temperature
    )
    return ans


def analysis_xuanti_v7(note, img_num=1, model='claude-3-5-sonnet-20241022', client=None, max_tokens=4096, seed=None,
                       temperature=0.0):
    # if client is None:
    #     client = get_client(model=model)
    # image_content = pack_image_content(note, img_num)
    prompt = f'''
你是一名资深内容创作者，你擅长：

我会给出图片和以下小红书的帖子信息：
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
1. 仔细阅读内容，确定该出内容所属的创作领域，你将会以该`领域(内容创作)专家`完成接下来的关于内容创作有关的任务；
     - 确定创作者创作的内容的所属领域；
     - `领域专家`拥有极其精准的专业性语言、词汇、视角、经验；
2. 以`领域专家`的身份找出内容的`内容选题`：
     - 用专业领域的视角表达内容选题；要求用词精准拿捏，专业性强、无歧义；
     - 禁止出现`氛围`、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
     - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
     - 内容中真正的亮点，`内容选题`一定要能够反映此条内容中最独特、最具有吸引力的，比如：女性的身材或颜值、创意、搞怪、玩梗、视觉、独特性等等；
     - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
3. 结合`内容选题`给出'内容选题描述'：
    - `内容选题描述`指的是`内容选题`在这条内容中的独特性描述，重点在于对关键点的含义进行深刻的描述，其他无关的内容不应出现；
    - 请只描述客观事实，不要加入任何`主观、`评价性'语言；
    - 必须具体到帖子中的的具体内容，必须客观、言之有物、言之有理；避免出现'氛围'、'视觉效果','和谐'等模糊的词汇；
    - 禁止在描述的末尾加入任何总结性的语言；比如'有趣'应该替换为具体的'什么什么有趣'；
4. 结合`内容选题`给出`文本`和`标题`的描述：
    - 请述`文本`和`标题`的特点，突出`内容选题`的独特性；
    - 用词准确具体客观，不要笼统；

要求：
- `领域专家`文字语言表达风格：严谨专业、诗经、曹雪芹红楼梦、诗化语言、象征隐喻、骈文
- 语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；
- 深入思考内容其背后创作者，在创作内容时，考虑并突出与普通内容的区别
- 输出为中文；
- 请只描述客观事实，不要加入任何```主观```评价性语言；
- 请严格控制输出的内容能够被正确解析为JSON，避免JSON Value中出现`"`，因为这会导致解析失败；
- output in JSON format with keys:
    - `内容所属领域`(str)
    - `内容选题`(str) 
    - `内容选题描述`(str)
    - `文本和标题描述`(str)
    '''.strip()
    # note_data = image_content + [{"text": prompt, "type": "text"}]
    # ans = try_chat_with_data(
    #     note_data,
    #     client=client,
    #     model=model,
    #     max_tokens=max_tokens,
    #     seed=seed,
    #     temperature=temperature
    # )

    # ans = claude35(prompt, image_list=note.get("images", []))

    print(prompt)
    ans = gemini(prompt, images=note.get("images", []))
    return ans
