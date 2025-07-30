import aiddit.model.dsr3 as dsr3
import json
import aiddit.model.chat as chat
import aiddit.model.google_genai as google_genai


def dispatch(xuanti_result, renshe_xuanti_unique, script_mode, renshe_material_data):
    prompt = f"""
 你是一个小红书内容创作专家，拥有以下能力：
- 根据人设信息、内容选题、创作方式，能够利用丰富的创作经验创作出符合人设的内容脚本； 

现在有以下信息：
人设信息：
{json.dumps(renshe_xuanti_unique, ensure_ascii=False, indent=4)}

创作方式:
{json.dumps(script_mode, ensure_ascii=False, indent=4)}

创作内容选题：
{xuanti_result.get("最终的选题")}

创作内容选题的详细描述信息:
{xuanti_result.get("选题的详细描述信息")}   
选题依赖的关键信息：
{xuanti_result.get("选题依赖的关键信息")}

在你的历史创作中，你有如下高频使用的材料：
{json.dumps(renshe_material_data, ensure_ascii=False, indent=4)}

根据人设信息和脚本创作方式，在当前创作内容选题的的基础上，要生成一个完整的小红书内容创作脚本，
下面你要根据以上信息完成以下任务：
- 你需要判断对于生成脚本中的 标题、正文、图片、图集的生成顺序；
  - 你需要从【小红书】内容创作的角度出发，结合人设信息和脚本创作方式，判断生成脚本中的 标题、正文、封面、图集的生成顺序；
  - 请注意每个模块的创作模式之间的逻辑关系
  - 请根据实际的生成过程，确定每个模块的创作过程；

要求：
- 请直接输出 标题、正文、封面、图集的生成顺序，用"-"分隔，不要有其他任何多余的输出；
""".strip()

    return prompt


def conversation_deepseek(history_messages, prompt):
    print(prompt)
    history_messages.append({"role": "user", "content": prompt})
    # print(f"----------------------")
    # print(f"{json.dumps(history_messages, ensure_ascii=False, indent=4)}")
    # print(f"----------------------")
    reason, ans = dsr3.deepseek_r3_conversation_stream(history_messages)
    history_messages.append({"role": "assistant", "content": ans})
    return {
        "prompt": prompt,
        "reason": reason,
        "ans": ans
    }


def conversation_claude(history_messages, prompt):
    print(prompt)
    history_messages.append({"role": "user", "content": prompt})

    ans = chat.claude35_conversation(history_messages)
    print(ans)
    history_messages.append({"role": "assistant", "content": ans})
    return {
        "prompt": prompt,
        "reason": "ok",
        "ans": ans
    }


def conversation_gemini(history_messages, prompt, format_json=False):
    print(prompt)
    ans = google_genai.google_genai_conversation(history_messages, prompt, "application/json" if format_json else None)
    history_messages.append({"role": "user", "content": prompt})
    print(ans)
    history_messages.append({"role": "assistant", "content": ans})
    return {
        "prompt": prompt,
        "reason": "ok",
        "ans": ans
    }


def title():
    return f"""请根据人设信息和脚本创作方式，生成一个符合人设的小红书内容创作脚本的标题。
- 请结合脚本创作方式中各个模块的生成关系及关联，结合整体上下文生成；    
- 请直接输出标题的生成结果(str)。不要有任何其他的解释和多余的信息。"""


def content():
    return f"""请根据人设信息和脚本创作方式，生成一个符合人设的小红书内容创作脚本的正文。
- 请结合脚本创作方式中各个模块的生成关系及关联，结合整体上下文生成；    
- 请直接输出正文的生成结果(str)。不要有任何其他的解释和多余的信息。"""


def vision_prepare():
    return """在进行封面和图集生成之前，需要准备好以下信息：
- 视觉生成规划：根据人设信息和脚本创作方式，确定视觉的整体生成规划，比如确定生成图片的数量、内容、加工方式等等一切围绕选题的生成规划；
- 视觉通用信息：在图片的创作过程中，所有需要统一、不变的信息，比如女性的容貌、物品的样式、图片的风格等等所有一切细节；

要求如下：
- 确保正文、图片、标题之间的逻辑关系且能够相对应；
    - 比如：标题或者正文中提到了5张图片，请确保封面+图集的数量也应该是5张图片；图片数量 = 封面 + 图集数量！
- 视觉整体包含了封面和图集；图集是不包括封面的；
- 确保生成的视觉是符合人设信息的，视觉图片应该在侧重如何表达、突出 创作内容的选题 & 人设的创作风格；这一点非常重要！   
    - 生成的视觉必须在`脚本创作方式`中有有迹可循；而不是随意生成；
    - 视觉需要与`脚本创作方式`保持一致性；
- 创作必须符合自己人设：比如创作的内容要符合自己人设的创意、风格、主题等；而不是随意创作忽略了人设；
    - 你的重点不是为了完成任务，而是为了创作出符合人设的内容；
    - 比如重点突出人设中的反差行为、搞怪行为、幽默行为等等；
- 请根据人设信息和脚本创作方式，先做好整体的规划，你的规划是有明确的指导意义的，所以这一个步骤至关重要；
- 请直接输出以上JSON格式，不要有除了JSON格式之外的其他输出；
    - 视觉生成规划(dict)
    - 视觉通用信息(list[str])：
        - 从整体出发，确保封面、图集的图片中的统一信息；
        - 直接给出对应的词条即可，并且确保词条能够被后续引用，并且对词条进行一定程度的抽象和总结；
        - 词条应该简洁概括，不要有详细的描述；
        - 不应该出现 `词条:描述` 这样的结构；
    - 视觉关键信息(dict)：从整体来上规划视觉的关键信息，从而使得创作的视觉更加符合人设信息、脚本创作方式；
"""


def cover():
    return f"""请根据人设信息和脚本创作方式，生成一个符合人设的小红书内容创作脚本的封面图。
- 在生成封面图之前，请仔细理解人设信息、脚本创作方式、视觉生成规划、视觉通用信息；
- 封面需要优先参考历史创作中，你有如下高频使用的材料中关于封面的描述；
- 如果图集已经生成了，请结合封面和图集的关系作出决策；
- 生成的封面图包含如下信息：
    - 生成过程(dict)
    - 图片描述(str)
    - 图片生成方式(Enum[独立生成,图集选取])：根据整体规划，确定封面是独立生成，还是从图集中选取；请从小红书封面的表现力出发去决策
    - 独立生成(dict|None):
        - 图片描述(str)
        - 加工流程(dict|None): 如果图片需要二次加工：比如加文字等等；
    - 图集选取(dict|None):
        - 依赖的图片序号(List[int])：依赖的图集中的图片序号，从图集中选取后作为封面图；
        - 加工方式(Enum[原图,加工])：封面图是否需要加工；
        - 加工流程(dict|None): 如果封面图需要二次加工：比如多图拼接、加文字等等；

要求如下：
- 要求用词精准，不要使用模糊、不确定的词语；   
- 请根据上下文完成封面图的生成；
- 加工流程请从脚本创作方式出发，确定加工流程，而不需要随意加工、联想；
- 请确保封面图符合人设、选题等信息，图片描述应该详实具体，而不是简单的概括；
- 图片描述(str)
    - 图片的描述应该详细具体，且符合人设、选题等信息，每张图片之间需要保持连续或者整体一致性等要求，因为这是一个完整的创作；
    - 结合视觉规划中的视觉通用信息、视觉关键信息，确定图片的描述；
    - 如果关联到`视觉生成规划`中的`视觉通用信息`，请在描述中体现，并用`[]`标注；
    - 对图片描述中的关键信息用`<>`标注，确保`<>`标注的都是最关键、最核心的信息；
    - `<>` 、`[]`的内容应该都为图片中的关键信息或者关联到视觉规划的信息，不要有包含其他无关、冗余的信息
    - 不要对`<>`、`[]`的信息进行解释；
- 结果请直接输出JSON信息，不要有其他任何多余的输出；
"""


def images():
    return """请根据人设信息和脚本创作方式，生成一个符合人设的小红书内容创作脚本的图集内容
- 在生成封面图之前，请仔细理解人设信息、脚本创作方式、视觉生成规划、视觉通用信息；
- 请确保生成的图集数量是符合视觉整体规划的；
- 图片序号从1开始；
- 生成的图集包含如下信息：
    - 生成过程(dict)
    - 图片(List[dict]) , each dict with keys:
        - 图片序号(int)
        - 图片描述(str)
        - 其他重要信息(dict | None)
        
要求如下：
- 要求用词精准，不要使用模糊、不确定的词语；   
- 请根据上下文和图集创作模式完成图集的生成；
- 确保图集的描述准确符合图集`视觉呈现方式`；
- 请不要随意加工、联想，基于客观事实，保持图集的结果和创作模式的一致性；
- 请确保图集的创作符合人设、选题等信息，图片描述应该详实具体，而不是简单的概括；
- 加工流程请从脚本创作方式出发，确定加工流程，而不需要随意加工、联想；
- 图片关键点(list[str])
    - 结合人设信息、特点、脚本创作方式、视觉规划，确定图片的关键点；
- 图片描述(str)
    - 图片的描述应该详细具体，且符合人设、选题等信息；
        - 结合视觉规划中的视觉通用信息、视觉关键信息，确定图片的描述；
        - 图片描述的目的是为清晰的表达这张图片的内容，而不是简单的概括；所以图片描述应该具体，对画面整体进行描述；
        - 请不要给出总结式的结果；
        - 确保内容具体，不要有模糊、不确定的词语；
    - 如果关联到`视觉生成规划`中的`视觉通用信息`，请在描述中体现，并用`[]`标注；
    - 对图片描述中的关键信息用`<>`标注
        - 关键信息指的是图片中最重要、最核心的信息；
        - 最重要、最核心指的是能够反映人设的特点、选题的特点、当前图片的要点；
        - 请严格控制标注的标准，不要进行整句的标注，而是核心关键信息；
    - `<>` 、`[]`的内容应该都为图片中的关键信息或者关联到视觉规划的信息，不要有包含其他无关、冗余的信息
    - 不要对`<>`、`[]`的信息进行解释，直接标注即可；
- 结果请直接输出JSON信息，不要有其他任何多余的输出；
"""


def vision_common_build(vision_common, image_list, renshe_material_data):
    prompt = f"""    
我会给你以下图片描述：
{json.dumps(image_list, ensure_ascii=False, indent=4)}

还有以下创作素材信息：
{json.dumps(renshe_material_data, ensure_ascii=False, indent=4)}

请基于这些图片场景的描述，完成以下工作：  
1. 对于图片描述中关联`创作素材信息`的存在的素材，请用`<<>>`标注，并保留完整的素材名称；
2. 另外去除图片描述中的[]和<>符号；
    
要求：
1. 请结合通用信息和图片描述，完成上述工作；
2. 输出的JSON格式如下：
{{
    "图片描述":[
        {{
            "图片序号":1,
            "原始图片描述":"原始图片描述",
            "图片描述":"图片描述"
        }},
        ...
    ],
    "引用的创作素材" list[str]: ["创作素材名称1", "创作素材名称2", ...]
}}
"""

    print(prompt)
    ans = google_genai.google_genai(prompt, "gemini-2.0-flash", "application/json")
    # ans = chat.claude(prompt, model="anthropic/claude-3.7-sonnet")
    return ans


def vision_common_build_before(vision_common, image_list, renshe_material_data):
    prompt = f"""    
我会给你以下图片描述：
{json.dumps(image_list, ensure_ascii=False, indent=4)}

关于图片描述中的通用素材:
{json.dumps(vision_common, ensure_ascii=False, indent=4)}

还有以下素材信息：
{json.dumps(renshe_material_data, ensure_ascii=False, indent=4)}

请基于这些图片场景的描述，完成以下工作：    
1. 结合所有的图片描述，对通用素材中的每个词进行详细描述，要求如下：
    - 如果素材信息中有对应的词，可以引用素材信息进行描述；
    - 你不是对通用素材进行解释，而是结合图片描述对通用素材进行细节完善；
    - 描述是完善通用素材在图片中的细节，而不是对通用素材进行解释、总结；
    - 直接输出对应通用素材的描述即可，不需要结合其他通用素材进行说明；
    - 如果词不能或者不需要进行细节描述，请在描述中直接输出原来的通用素材；
    - 目的是为了每张图片图片通过AI能力独立生成的时候，能够让每张图片中的通用素材都能够保持一致性；
    - 避免使用'氛围'、'感觉'等模糊、指代不明的词语；
        - 比如物品类应该是物品的细节、形状、大小、颜色等等
        - 比如颜色类应该是颜色的具体描述，而不是颜色等；
    - 请结合所有图片的整体协调性，确保每个通用素材的描述是符合整体的；
2. 根据上一步关于通用素材中的详细描述，图片描述有引用到通用素材，现在需要完善每一张的图片描述，要求如下：
    - 去除图片描述中的[]和<>符号
    - 对[]中的词，替换为通用素材的详细描述：
        - 完善整个图片描述
        - 确保通用素材中的细节依然存在；
    - 根据完善后图片描述生成其对应的Midjourney Prompt，英文格式

要求：
1. 请结合通用信息和图片描述，完成上述工作；
2. 输出的JSON格式如下：
{{
    "通用信息":{{
        "词1":"词1的详细描述",
        "词2":"词2的详细描述",
        ...
    }}
    "图片描述":[
        {{
            "图片序号":1,
            "原始图片描述":"原始图片描述",
            "图片描述":"图片描述",
            "Midjourney Prompt":"Midjourney Prompt"
        }},
        ...
    ]
}}
"""

    print(prompt)
    ans = google_genai.google_genai(prompt, "gemini-2.0-flash", "application/json")
    # ans = chat.claude(prompt, model="anthropic/claude-3.7-sonnet")
    return ans