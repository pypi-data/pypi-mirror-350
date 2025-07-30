import os
import json
from image_article_comprehension.tools.midjourney_generate_image import generate_midjourney_image
from image_article_comprehension.aiddit.model import gemini
import traceback
from tqdm import tqdm


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


def image_generate(xuanti_result_dir):
    for i in tqdm(os.listdir(xuanti_result_dir)):
        print(f"process image generate {i}")
        r = json.load(open(os.path.join(xuanti_result_dir, i), 'r'))

        # xuanti_creation_new = r.get("xuanti_creation_by_note", {})
        # if xuanti_creation_new.get("xuanti_creation", []) is not None:

        xuanti_creation_by_note = r.get("xuanti_creation_by_note")
        xuanti_estimate_pass = xuanti_creation_by_note.get("xuanti_estimate", {}).get("是否是一个好选题", "")
        if xuanti_estimate_pass != "是":
            print(f'{xuanti_creation_by_note.get("xuanti_creation", {}).get("最终的选题")} 不是一个好的选题')
            continue

        if xuanti_creation_by_note.get("midjourney_image") is None:
            try:
                mj_prompt = generate_midjourney_prompt(
                    xuanti_creation_by_note.get("xuanti_creation", {}).get("选题的详细描述信息"),
                    json.dumps(xuanti_creation_by_note.get("xuanti_creation", {}).get("选题依赖的关键信息"),
                               ensure_ascii=False, indent=4))
                images = generate_midjourney_image(mj_prompt)
                xuanti_creation_by_note["midjourney_image"] = images
                xuanti_creation_by_note["midjourney_prompt"] = mj_prompt
                save(r, os.path.join(xuanti_result_dir, i))
            except Exception as e:
                if "banned_prompt_detected" in str(e):
                    xuanti_creation_by_note["midjourney_image"] = ['banned_prompt_detected']
                    save(r, os.path.join(xuanti_result_dir, i))
                traceback.print_exc()
                print(f"midjourney_image {i}, {str(e)}")
        else:
            print("midjourney_image already exists")

        # for xuanti_creation in r.get("xuanti_creation", []):
        #     xuanti_creation_result = xuanti_creation.get("xuanti_creation", {})
        #     xuanti_estimate_pass = xuanti_creation.get("xuanti_estimate", {}).get("是否是一个好选题", "")
        #     if xuanti_estimate_pass != "是":
        #         print(f'{xuanti_creation.get("xuanti_creation", {}).get("最终的选题")} 不是一个好的选题')
        #         continue
        #     try:
        #         if xuanti_creation_result.get("whisk_image") is None:
        #             description = xuanti_creation.get("xuanti_creation", {}).get("选题的详细描述信息")
        #             eng_prompt = translate_to_english(description)
        #             print(f"whisk_image {description}\n{eng_prompt}")
        #             response = json.loads(text_to_image(eng_prompt))
        #             print("response: ", response)
        #             if response.get("code") != 0:
        #                 raise Exception(response.get("msg"))
        #             image = response.get("data")
        #             print(f"{image}\n")
        #             xuanti_creation_result["whisk_image"] = image
        #             save(r, os.path.join(xuanti_result_dir, i))
        #         else:
        #             print("whisk_image already exists")
        #     except Exception as e:
        #         traceback.print_exc()
        #         print(f"whisk_image {i}, {str(e)}")
        #
        #     try:
        #         if xuanti_creation_result.get("midjourney_image") is None:
        #             description = xuanti_creation.get("xuanti_creation", {}).get("选题的详细描述信息")
        #             mj_prompt = translate_to_mj_prompt(description)
        #             print(f"midjourney_image {description}\n{mj_prompt}")
        #             images = generate_midjourney_image(mj_prompt)
        #             xuanti_creation_result["midjourney_image"] = images
        #             save(r, os.path.join(xuanti_result_dir, i))
        #         else:
        #             print("midjourney_image already exists")
        #     except Exception as e:
        #         if "banned_prompt_detected" in str(e):
        #             xuanti_creation_result["midjourney_image"] = ['banned_prompt_detected']
        #             save(r, os.path.join(xuanti_result_dir, i))
        #         traceback.print_exc()
        #         print(f"midjourney_image {i}, {str(e)}")


def generate_midjourney_prompt(description, keypoint_with_xuanti):
    prompt = f"""
1. 你非常熟悉Midjourney，以及其提示词的使用规则

你需要帮我完成以下任务：
将一段`描述`结合`关键点`转换为一个完整的Midjourney的提示词，以便生成图片。

要求如下：
-注意不要有Midjourney的banned word：
    ALLOWED
    Safe For Work (SFW) content.
    Respectful or light-hearted parodies, satire, andcaricatures using real images.
    Fictional or exaggerated scenarios, includingabsurd or humorous situations.
    NOT ALLOWED
    Content that disrespects, harms, or misleadsabout public figures or events.
    Hate speech, explicit or real-world violence.Nudity or overtly sexualized images.Imagery that might be considered culturallyinsensitive.
-在避免banned word的基础上，应该详细、准确的还原中文意思;
-结尾不要有任何Midjourney的变量；
-请直接输出指令的英文结果，不要有任何解释以及命令;
-输出结果应该去掉json标记;

描述如下：
{description}

关键点：
{keypoint_with_xuanti}
""".strip()

    print("prompt: ", prompt)
    ans = gemini(prompt, response_mime_type="text/plain")
    print("ans: ", ans)
    return ans


if __name__ == "__main__":
    xuanti_result_dir = "/image_article_comprehension/create/result/image/20250110_EllenEveryday"
    image_generate(xuanti_result_dir)

    # r = translate_to_english("以秋季枫叶的自然色调为灵感，从浅杏色到酒红色的渐变眼影晕染，搭配蝴蝶水晶点缀眼尾，展示一步步如何打造层次丰富的眼妆。使用珊瑚色打底，逐层叠加深浅不同的枫叶色系眼影，最后用闪粉在眼尾处点缀，呈现出落叶层叠般的立体效果。")
    # print(r)

    # r = translate_to_mj_prompt(
    #     "设计一款多层透明展示柜，专门用于中药材的分类收纳与展示。每层按照功效分区（如补气、养血、祛湿等），配以白色雕花装饰框展示各类养生方案说明。展示柜采用多层设计，每层标注药材克数与功效，并配备独立小包装。展示柜内设计特殊隔层，可分别存放颗粒、饮片等不同剂型，便于日常养生使用。")
    # print(r)

    pass
