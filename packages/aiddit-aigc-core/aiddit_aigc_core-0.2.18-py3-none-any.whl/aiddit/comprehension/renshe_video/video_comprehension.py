from image_article_comprehension.aiddit.model import gemini, claude


def video_keypoint(reference_video_note):
    video_caption = gemini(f"""
视频标题是：

{reference_video_note.get("title")}

任务：
请你从内容创作的角度，根据我给出的内容，找到这个内容最吸引人的地方？
禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'；'反差'应该替换为具体的'什么什么反差'""",
                           images=[reference_video_note.get("video_url")])

    print("内容吸引人的点", video_caption)

    claude_prompt = f"""
{video_caption}    
以上是我视频关键点的总结。
任务：
1.总结找到这个内容最吸引人的地方（即亮点）（1个）
2.请结构化的描述以上亮点的详细组成部分，比如：亮点的主体、亮点的背景、亮点的细节等等；

要求；
1.的分析必须基于我的内容，不能凭空想象；
2.禁止出现'氛围'、'和谐'、'视觉呈现','美学','视觉','构图'等指代无不明确的用词；
3.禁止出现总结性的描述，比如'有趣'应该替换为具体的'什么什么有趣'；'反差'应该替换为具体的'什么什么反差'
4.亮点的组成是为了二次创作时，通过AIGC还原以上亮点
5.亮点和亮点的是一个短句子，亮点组成的描述，应该是短句子或者4-6个字的短语
- 请直接输出JSON格式，确保输出能够被JSON语法正确解析，不要有除了JSON格式之外的其他输出；
- output in JSONArray format , each JSONObject with keys:
    - `亮点 `(str)
    - `亮点组成`(Dict)'''
"""
    claude_ans = claude(claude_prompt)
    print("亮点", claude_ans)
    return claude_ans


def video_xuanti(reference_video_note):
    prompt = f'''
请请用一句话输出视频的选题是什么，选题类似论文的标题，描述内容选题的关键信息；并从创作者的角度，对选题进行补充说明
视频的标题为： {reference_video_note.get("title")}
要求：
- 选题要能体现视频中，最独特，最独一无二的特点，可以通过选题来快速检索视频。
- 输出为中文，不要解释，直接输出结论；
- 请只描述客观事实，不要加入任何主观评价性语言；
- 选题语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；
- 请不要泛泛而谈；根据视频进行详细的描述。描述要具体，比如，不要说行为变化，要具体说行为变化了什么;不要说有趣，要说具体怎么样的有趣。
- 使用对应领域的转悠名次
- 直接输出结论，不要解释分析这个视频的主要内容
- output in JSON with keys:
- 选题(str) 
- 选题描述(str)'''

    result = gemini(prompt, images=[reference_video_note.get("video_url")])
    print("选题：" + result)
    return result


def video_renshe(renshe_video_dir):
    pass
