import json
from image_article_comprehension.aiddit.model import claude


def xuanti_generate(renshe_topic, renshe_keypoint, reference_note_keypoint, xuanti_reference):
    xuanti_reference_description = "\n\n".join(xuanti_reference)
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于的创作风格和灵感，基于参考内容创作出高质量的内容

你的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

你的【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}

现在，你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
2. 判断选题是否合理：
    - 注意：选题一定要符合创作方向，而不是强行将创作方向和参考内容的关键信息拼凑在一起，这是产生选题最基本的标准和原则；
    - 请参考历史完整的选题和描述，确保选题不会有太大的偏差：
{xuanti_reference_description}
    - 并不是每个【参考内容的关键信息】都能够和自己的创作方向和关键点匹配，请严格按照以下标准来评估选题，在JSON中输出为 `选题判断`(dict)：
         - 内容选题符合自己的创作方向和关键点；
         - 内容选题结合了参考内容中的亮点、关键点
         - 内容用专业领域的视角来表达；用词精准拿捏，专业性强、无歧义；
         - 禁止出现`氛围`、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
         - 内容中真正的亮点，`内容选题`一定要能够反映此条内容中最独特、最具有吸引力的，比如：女性的身材或颜值、创意、搞怪、玩梗、视觉、独特性等等；
         - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
         - 你需要严格判断选题是否可以和自己的创作方向和关键点匹配；没有明确意义的选题不应该被选中；
3. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
        - `选题判断`(dict)
            - `是否可行`(enum[是、否])
            - `explanation`(str)
'''.strip()

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_generate_20240103(renshe_topic, renshe_keypoint, reference_note_keypoint):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于的创作风格和灵感，基于参考内容创作出高质量的内容

你的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

你的【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}

现在，你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
2. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
'''.strip()

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_generate_20240104(renshe_topic, renshe_keypoint, reference_note_keypoint):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

然后仔细思考【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}

现在，你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
    - 选题需要有关键的细节；
        - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
    - 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - 选题的句式应该为简单句；避免使用复杂句式；
        - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
'''.strip()

    print(prompt)
    ans = claude(prompt, temperature=1.0)

    return ans


def xuanti_generate_20240106(renshe_topic, renshe_keypoint, reference_note_keypoint, renshe_unique_point):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

并且保持自己的创作灵魂：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

再保持结合自己创作中的重要关键点：
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

并且你常见的创作方式特征如下：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

然后仔细思考【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}

以上就是我给出的创作方向、创作灵魂、重要关键点和创作特征。
现在，你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
    - 选题需要有关键的细节；
        - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
    - 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - 选题的句式应该为简单句；避免使用复杂句式；
        - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
'''.strip()

    print(prompt)
    ans = claude(prompt, temperature=0.0)

    return ans


def xuanti_generate_20240107(renshe_keypoint, reference_note_keypoint, renshe_unique_point):
    history_xuanti = "\n".join(renshe_unique_point.get("优质选题详情", []))
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的【创作方向】：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

再保持结合自己创作中的重要关键点：
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

并且你常见的创作方式特征如下：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

然后仔细自己思考【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}

再满足以上要求的同时，也要参考自己过往的历史优秀选题：
{history_xuanti}

以上就是我给出的所有信息，下面你将完成以下任务：
你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
    - 选题需要有关键的细节；
        - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
    - 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - 选题的句式应该为简单句；避免使用复杂句式；
        - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
'''.strip()

    print(prompt)
    ans = claude(prompt, temperature=0.0)

    return ans


def xuanti_generate_20240108(base_topic, renshe_keypoint, renshe_keypoint_with_xuanti, reference_note_keypoint,
                             renshe_unique_point):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的【创作方向】：
{json.dumps(base_topic, ensure_ascii=False)}

并且保持自己的创作灵魂：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

再保持结合自己创作中的重要关键点：
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

并且你常见的创作方式特征如下：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

然后仔细自己思考【创作内容中的关键点】：
{json.dumps(renshe_keypoint, ensure_ascii=False)}
{json.dumps(renshe_keypoint_with_xuanti, ensure_ascii=False)}

以上就是我给出的所有信息，下面你将完成以下任务：
你需要根据以下【参考内容的关键信息】，基于自己的创作方向和关键点，创作出一个新的内容选题：
{json.dumps(reference_note_keypoint, ensure_ascii=False)}

要求如下：
1. 产生选题：
    - 新的内容选题需要符合你的创作方向和关键点；
        - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
        - 选题要符合自己的创作方向、创作风格；
        - 内容选题可以包括但不限于`创作内容中的关键点`；
    - 新的内容选题也需要保留参考`参考内容的关键信息`中的关键信息；
        - 请注意完整的保留`参考内容的关键信息`中的`亮点`，亮点应该是具体的'创意'、'行为'等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
        - 优先保留完整的`亮点`；
        - 如果无法保留完整的`亮点`，请保留其中的关键信息；
    - 新的内容选题需要保持高质量的内容创作水准；
    - 选题需要有关键的细节；
        - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
    - 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - 选题的句式应该为简单句；避免使用复杂句式；
        - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
    - 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
    - output in JSON format , with keys:
        - `最终的选题`(str) 
        - `选题的详细描述信息`(str)
            - 禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图','趣味性'等指代无不明确的用词；
            - 禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
        - `选题的参考来源`(str)
        - `选题依赖的关键信息`(dict)   
'''.strip()

    print(prompt)
    ans = claude(prompt, temperature=0.0)

    return ans


def xuanti_generate_by_note(base_topic, renshe_keypoint, renshe_keypoint_with_xuanti, renshe_unique_point, note_info):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的 创作方向：
{json.dumps(base_topic, ensure_ascii=False)}

并且保持自己的 创作灵魂：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

再保持结合自己创作中的 重要关键点：
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

并且你常见的 创作特征：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

然后仔细思考自己创作中的 关键点：
{json.dumps(renshe_keypoint, ensure_ascii=False)}
{json.dumps(renshe_keypoint_with_xuanti, ensure_ascii=False)}

以上就是你所有的`创作人设`，下面你将完成以下任务：
你需要根据以下参考内容的标题、正文、图片，基于自己的创作方向和关键点，创作出一个新的内容选题：
标题:
{note_info.get("title")}
正文：
{note_info.get("body_text")}

要求如下：
1. 产生选题：
- 新的内容选题需要符合你`创作人设`；
    - 首先最重要的事情就是：你要深刻白自己的创作人设；
    - 你新产生的选题必须符合自己的创作人设，如果偏离了自己的创作人设，那是一个非常糟糕的选题；
    - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
    - 选题要符合自己的创作方向、创作风格；
    - 内容选题可以包括但不限于`重要关键点`；
- 新的内容选题需要结合参考内容；
    - 请注意结合自己的`创作人设`，结合参考内容的标题、正文、图片，创作出一个新的内容选题；
    - 你需要从参考内容找到符合自己创作人设的关键带你，然后结合自己的创作人设，创作出一个新的内容选题；
    - 请注意你的参考点，亮点应该是具体的、明确的等等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
- 新的内容选题需要保持高质量的内容创作水准；
    - 创作完选题后，务必要对应自己的`创作人设`，如果与`创作人设`不符，你要有自我调整的过程；
- 选题需要有关键的细节；
    - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
- 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
    - 选题的句式应该为简单句；避免使用复杂句式；
    - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
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


def xuanti_generate_by_note_20250110(base_topic, renshe_keypoint, renshe_keypoint_with_xuanti, renshe_unique_point,
                                     note_info, xuanti_mode, xuanti_category_style):
    prompt = f'''
你是一名内容灵感创作大师，拥有以下能力：
1. 丰富的内容创作经验，能够根据关键点创作出高质量的内容
2. 擅长基于自己的创作风格、参考内容创作出高质量的内容

首先深刻理解你的 创作方向：
{json.dumps(base_topic, ensure_ascii=False)}

并且保持自己的 创作灵魂：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

你创作选题通常的模式：
{json.dumps(xuanti_mode, ensure_ascii=False)}

再保持结合自己创作中的 重要关键点：
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

并且你常见的 创作特征：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

然后仔细思考自己创作中的 关键点：
{json.dumps(renshe_keypoint, ensure_ascii=False)}
{json.dumps(renshe_keypoint_with_xuanti, ensure_ascii=False)}

最后请保持你的 创作品类和风格：
{json.dumps(xuanti_category_style, ensure_ascii=False)}


以上就是你所有的`创作人设`，下面你将完成以下任务：
你需要根据以下参考内容的标题、正文、图片，基于自己的创作方向和关键点，创作出一个新的内容选题：
标题:
{note_info.get("title")}
正文：
{note_info.get("body_text")}

要求如下：
1. 产生选题：
- 新的内容选题需要符合你`创作人设`；
    - 首先最重要的事情就是：你要深刻白自己的创作人设；
    - 你新产生的选题必须符合自己的创作人设，如果偏离了自己的创作人设，那是一个非常糟糕的选题；
    - 一个好的选题必须有【明确的主题】和【一个或者多个的亮点】；
    - 选题要符合自己的创作方向、创作风格；
    - 内容选题可以包括但不限于`重要关键点`；
- 新的内容选题需要结合参考内容；
    - 请注意结合自己的`创作人设`，结合参考内容的标题、正文、图片，创作出一个新的内容选题；
    - 你需要从参考内容找到符合自己创作人设的关键带你，然后结合自己的创作人设，创作出一个新的内容选题；
    - 请注意你的参考点，亮点应该是具体的、明确的等等，而不是'状态','意境','氛围','趣味性'等指代不明的东西；
- 新的内容选题需要保持高质量的内容创作水准；
    - 创作完选题后，务必要对应自己的`创作人设`，如果与`创作人设`不符，你要有自我调整的过程；
- 选题需要有关键的细节；
    - 结合`选题方向`和`选题的详细描述信息`中的细节，在`最终的选题`中增加细节描述；
- 选题请避免出现概括性的总结，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
    - 选题的句式应该为简单句；避免使用复杂句式；
    - 选题中避免出现利用`:`的形式来做解释性的表达； 
2. 结果输出：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
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


def xuanti_estimate(renshe_topic, xuanti_creation, xuanti_creation_description):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。
    
我的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation}
选题描述：{xuanti_creation_description}
    
请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`内容选题`是否符合以下要求：
     - 内容选题符合自己的创作方向；
     - 内容选题用词精准拿捏，专业性强、无歧义；
     - 内容选题禁止出现`氛围`、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
     - 内容选题禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'、'反差'应该替换为具体的'反差意义'；
     - 请综合以上所有进行严格的评估；
     
要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `是否是一个好选题`(enum[是、否]) 
    - `explanation`(str)
'''

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_estimate_20250104(renshe_topic, xuanti_creation, xuanti_creation_description):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。

我的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation}
选题描述：{xuanti_creation_description}

请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`内容选题`是否符合以下要求：
     - 内容选题符合自己的创作方向；
     - 内容选题用词精准拿捏，专业性强、无歧义；
     - 符合创作方向的选题，有实际意义，而不是强行将创作方向和选题拼凑在一起；
     - 请综合以上所有进行严格的评估；

要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `是否是一个好选题`(enum[是、否]) 
    - `explanation`(str)
'''

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_estimate_20250106(renshe_topic, xuanti_creation, xuanti_creation_description, renshe_unique_point):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。

我的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

我的【创作灵魂】：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

我的【重要关键点】
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

我的【创作特征】：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation}
选题描述：{xuanti_creation_description}

请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`内容选题`是否符合以下要求：
     - 内容选题符合自己的创作方向；
     - 内容选题能够反映出自己的创作灵魂；
     - 内容选题结合了自己的重要关键点；
     - 内容选题包含了自己的创作特征；
     - 内容选题用词精准拿捏，专业性强、无歧义；
     - 符合创作方向的选题，有实际意义，而不是强行将创作方向和选题拼凑在一起；
     - 请综合以上所有进行严格的评估；

要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `是否是一个好选题`(enum[是、否]) 
    - `explanation`(str)
'''

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_estimate_20250107(renshe_topic, xuanti_creation, xuanti_creation_description, renshe_unique_point):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。

我的【创作灵魂】：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

我的【重要关键点】
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

我的【创作特征】：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

我的【历史优质选题】：
{json.dumps(renshe_unique_point.get("优质选题", ""), ensure_ascii=False)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation}
选题描述：{xuanti_creation_description}

请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`内容选题`是否符合以下要求：
     - 内容选题能够反映出自己的创作灵魂；
     - 内容选题结合了自己的重要关键点；
     - 内容选题包含了自己的创作特征；
     - 内容选题类似于自己的历史优质选题；
     - 内容选题用词精准拿捏，专业性强、无歧义；
     - 符合创作方向的选题，有实际意义，而不是强行将创作方向和选题拼凑在一起；
     - 请综合以上所有进行严格的评估；

要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `是否是一个好选题`(enum[是、否]) 
    - `explanation`(str)
'''

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_estimate_20250108(renshe_topic, xuanti_creation, xuanti_creation_description, renshe_unique_point, xuanti_category_style):
    prompt = f'''
你是一名资深的内容创作者，你拥有以下能力：
1. 对内容的选题具有极高的判断力。

下面我会给出我的创作方向和我将要创作的一个选题，你需要根据你的专业判断力，帮我判断这个选题是否是一个好选题。

我的【创作方向】：
{json.dumps(renshe_topic, ensure_ascii=False)}

我的【创作灵魂】：
{json.dumps(renshe_unique_point.get("创作灵魂", ""), ensure_ascii=False)}

我的【创作品类】和【风格】：
{json.dumps(xuanti_category_style, ensure_ascii=False)}

我的【重要关键点】
{json.dumps(renshe_unique_point.get("重要亮点", ""), ensure_ascii=False)}

我的【创作特征】：
{json.dumps(renshe_unique_point.get("主要特征", ""), ensure_ascii=False)}

我的【历史优质选题】：
{json.dumps(renshe_unique_point.get("优质选题", ""), ensure_ascii=False)}

我创作出一个新的内容选题【创作内容选题】：
选题：{xuanti_creation}
选题描述：{xuanti_creation_description}

请你从内容创作的角度，根据我给出的内容，完成以下任务：
1. 判断`内容选题`是否符合以下要求：
     - 内容选题符合自己的创作方向；
     - 内容选题能够反映出自己的创作灵魂；
     - 内容选题符合自己的创作品类和风格；
     - 内容选题结合了自己的重要关键点；
     - 内容选题包含了自己的创作特征；
     - 内容选题类似于自己的历史优质选题；
     - 内容选题用词精准拿捏，专业性强、无歧义；
     - 符合创作方向的选题，有实际意义，而不是强行将创作方向和选题拼凑在一起；
     - 请综合以上所有进行严格的评估；

要求如下：
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `是否是一个好选题`(enum[是、否]) 
    - `explanation`(str)
'''

    print(prompt)
    ans = claude(prompt)

    return ans


def xuanti_estimate_query_keyword(renshe_topic, xuanti_creation):
    prompt = f'''
我会给你一个选题：
{xuanti_creation}

还有我的创作方向：
{json.dumps(renshe_topic, ensure_ascii=False)}

请你根据我的创作方向和选题，提取选题结合人设的一个关键词；
这个关键词我将用于去小红书上面搜索，搜索的目的是为了验证这个选题是否是一个可做的好选题；

要求：
- 关键词一定要能够反应选题的核心；
- 请直接输出用于搜索的关键词；
- 不要有除了关键词之外的任何解释和输出；
'''.strip()

    print(prompt)
    ans = claude(prompt)

    return ans
