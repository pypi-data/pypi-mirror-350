import json
import image_article_comprehension.aiddit.model.dsr3 as dsr3
import image_article_comprehension.aiddit.model.google_genai as google_genai


def renshe_unique(note_summary_list):
    prompt = f'''
我会给你一个小红书账号的历史创作数据，包括选题和选题描述，你需要依次帮我完成以下任务：
- 提取该账号下的内容创作的创作灵魂：
    - 创作灵魂指的是该账号基于内容创作层面上来说，最具有代表性的、最核心的、最重要的、最具有特色的部分；
    - 创作灵魂指的是能够区别与其他同品类创作账号的核心特征；
    - 创作灵魂之间不能有重复的部分；
    - 创作灵魂是指所有内容创作中的共性点，是所有内容创作的核心；
    - 创作灵魂的结果请输出1～3个，但是一定要精准，能够代表该账号的创作内核；
- 总结出内容创作涉及到的的主要内容品类/分类：
    - 品类/分类指的是该账号下的内容创作涉及到的主要品类/分类；
    - 用言简意赅的词语输出品类；
    - 品类不是枚举所有涉及到的品类，而是所有的内容都可以归类到的几个主要品类；
    - 品类需要结合`创作灵魂`，是创作灵魂的具体体现；
- 提取该账号下的内容创作的选题必要点；
    - 每一条内容都对应着一个选题，请从历史选题数据中提取出选题的必要点；
    - 选题必要点是指所有选题中的共性点，是所有选题的共同亮点；
    - 选题必要点是为了后续的创作，保持账号的人设一致性，用以产生新的选题也需要包含的必要点；
    - 选题必要点可以是风格、创作形式等，但是一定是账号下必备的；
- 提取该账号下的人设必要信息：
    - 人设必要信息是指该账号下所有内容创作中的人设信息；
- 提取的结果的要求：
    - 请只描述客观事实，不要加入任何'主观'评价性语言；
    - 要求用词精准，不要使用模糊、不确定的词语；
    - 语言表达上注意不要使用倒装句、长句、复杂句，尽量使用陈述句、简单句；

- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- direct output in JSONObject with keys:
    - 创作灵魂 (list[str])
    - 内容品类 (list[str])
    - 选题必要点 (list[str])
    - 人设必要信息 (dict)

下面是历史创作数据，请忽略历史创作数据中涉及到商品推广、广告植入的内容：

{json.dumps(note_summary_list, ensure_ascii=False, indent=4)}

'''.strip()

    print(prompt)
    # reason, ans = dsr3.deepseek_r3_stream(prompt)
    ans = google_genai.google_genai(prompt)
    return ans
