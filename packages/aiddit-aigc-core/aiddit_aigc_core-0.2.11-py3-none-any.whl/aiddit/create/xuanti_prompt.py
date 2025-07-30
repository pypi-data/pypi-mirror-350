import json
from aiddit.model.chat import claude


def xuanti_creation_20250113(renshe_xuanti_unique, xuanti_mode, note_info):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

你的内容创作灵魂：
{json.dumps(renshe_xuanti_unique.get("创作灵魂", ""), ensure_ascii=False)}

你的创作内容品类：
{json.dumps(renshe_xuanti_unique.get("内容品类", ""), ensure_ascii=False)}

你的内容创作中的选题必要点：
{json.dumps(renshe_xuanti_unique.get("选题必要点", ""), ensure_ascii=False)}

有了上面这些内容创作的基础信息外，对于选题创作，你还有如下模式：
选题模式：
{xuanti_mode.get("选题模式", "")}

选题创作方式:
{xuanti_mode.get("选题创作方式", "")}

选题模式要点:
{json.dumps(xuanti_mode.get("选题模式要点", ""), ensure_ascii=False, indent=4)}

选题模式灵感:
{json.dumps(xuanti_mode.get("选题模式灵感", ""), ensure_ascii=False, indent=4)}


以上就是你所有的`创作人设`，下面你将完成以下任务：
首先你需要根据以下`参考内容`的标题、正文、图片，基于自己的创作方向和关键点，创作出一个新的内容选题：
标题:
{note_info.get("title")}
正文：
{note_info.get("body_text")}

最后严格按照如下流程，产生选题：
- 深刻理解自己的创作灵魂、创作内容品类、选题必要点；
    - 创作灵魂满足其一即可；
    - 内容品类满足其一即可；
    - 选题必要点必须全部满足；
- 深刻理解自己的选题创作模式：
    - 选题模式是指根据参考内容来进行创作的方式；
    - 选题模式灵感是指该模式下的灵感来源，是该模式下的创作灵感，你可以根据灵感来找到选题的参考点；
    - 选题模式要点是指该模式下的关键点，是该模式下的创作重要要点；
- 根据参考内容结合自己的创作人设，找到符合创作人设、创作模式的参考点：
    - 参考点需要结合自己的创作需求来实际产生；
    - 请注意你的参考点：参考点应该是具体的、明确的等等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
    - 参考点一定要结合实际来产生有意义的选题，而不是为了产生选题而产生，如果参考点不够明确，你可以终止创作；
    - 请勿强行、滥用参考点，因为平庸、普通的选题不是你的创作目标；
    - 如果找不到参考点，也比较正常，并不是所有的参考内容都能够与自己的创作相结合；输出原因即可；并终止创作；
- 根据参考内容中的参考点来完成选题创作：
    - 选题要符合自己的创作方向、创作风格；
    - 创作完选题后，务必要对应自己的`创作人设`、`创作模式`，如果不符，你要有自我调整的过程；
    - 选题需要有关键的细节；
    - 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
    - 选题的句式应该为简单句；避免使用复杂句式；
    - 你可以参考你历史创作的优质选题：
{json.dumps(xuanti_mode.get("历史优质选题", ""), ensure_ascii=False, indent=4)}

最后结果输出：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `能否产生选题`(enum[是,否])
    - `不能产生选题的原因`(str) 
    - `最终的选题`(str) 
    - `选题的详细描述信息`(str)
        - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
        - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
    - `选题的参考来源`(str)
    - `选题依赖的关键信息`(dict)   
    '''.strip()

    print(prompt)
    ans = claude(prompt, image_list=note_info.get("images", []), temperature=0.0)

    return ans


def xuanti_estimate_20250113(renshe_xuanti_unique, xuanti_mode, xuanti_creation):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。
你的内容创作灵魂：
{json.dumps(renshe_xuanti_unique.get("创作灵魂", ""), ensure_ascii=False)}

选题模式：
{xuanti_mode.get("选题模式", "")}

选题创作方式:
{xuanti_mode.get("选题创作方式", "")}

选题模式要点:
{json.dumps(xuanti_mode.get("选题模式要点", ""), ensure_ascii=False, indent=4)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation.get("最终的选题", "")}
选题描述：{xuanti_creation.get("选题的详细描述信息", "")}

请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`选题`是否符合以下要求：
     - 选题符合`创作灵魂`；
     - 选题的创作品类在：`{json.dumps(renshe_xuanti_unique.get("内容品类", ""), ensure_ascii=False)}` 中；
     - 选题符合`选题模式`；
     - 内容选题是按照`选题创作方式`的方式进行的创作；
2. 判断'选题描述'是否符合以下要求：
    - 结合`选题`和`选题模式要点`，判断选题描述是否符合要求；
    - 选题描述中必须都包含`选题模式要点`
    - 选题描述必须符合都包含了如下：
{json.dumps(renshe_xuanti_unique.get("选题必要点", ""), ensure_ascii=False, indent=4)}


要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `选题符合是否要求`(enum[是、否]) 
    - `选题解释`(str)
    - `选题描述符合是否要求`(enum[是、否])
    - `选题描述解释`(str)
'''.strip()

    print(prompt)
    ans = claude(prompt)

    return ans
