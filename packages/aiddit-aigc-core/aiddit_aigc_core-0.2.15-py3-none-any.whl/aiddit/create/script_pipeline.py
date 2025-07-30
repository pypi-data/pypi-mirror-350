import json
import aiddit.utils as utils

import aiddit.create.script_pipeline_prompt as prompt
from aiddit.tools.midjourney_generate_image import generate_midjourney_image
import aiddit.model.google_genai as google_genai
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType


def pipeline(xuanti_result, renshe_xuanti_unique, script_mode, renshe_material_data, save_result_path=None,
             reference_note=None, renshe_path=None):
    save_result_path = save_result_path if save_result_path is not None else f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/script_pipeline/waste/{xuanti_result.get('最终的选题')}.json"
    messages = []

    step_result = {}

    def do_message(module_name, module_prompt, format_json=False):
        r = prompt.conversation_gemini(messages, module_prompt, format_json)
        step_result[module_name] = {
            "reason": r.get("reason"),
            "ans": utils.try_remove_markdown_tag_and_to_json(r["ans"]) if format_json else r["ans"]
        }

        save_result = {
            "script_mode": script_mode,
            "xuanti_result": xuanti_result,
            "reference_note": reference_note,
            "renshe_path": renshe_path,
            "step_result": step_result,
            "messages": messages
        }
        utils.save(save_result, save_result_path)
        return r

    dispatch_result = do_message("dispatch", prompt.dispatch(xuanti_result, renshe_xuanti_unique, script_mode,
                                                             renshe_material_data),
                                 format_json=False)

    dispatch_ans = dispatch_result.get("ans").strip()

    # 标题、正文、封面、图集
    for module in dispatch_ans.split("-"):
        if step_result.get(module) is not None:
            continue

        if module == "正文":
            do_message(module, prompt.content())
        if module == "标题":
            do_message(module, prompt.title())
        if module in ["图集", "封面"]:
            if step_result.get("vision_prepare") is None:
                do_message("vision_prepare", prompt.vision_prepare(), format_json=True)

            if module == "封面":
                do_message(module, prompt.cover(), format_json=True)

            if module == "图集":
                do_message(module, prompt.images(), format_json=True)

    return save_result_path


def detail_provider(script_data, renshe_material_data):
    vision_common = script_data.get("step_result").get("vision_prepare").get("ans").get("视觉通用信息", [])

    image_list = []

    cover_from_images_select_index = None
    try:
        if script_data.get("step_result").get("封面").get("ans").get("图片生成方式") == "图集选取":
            cover_from_images_select_index = \
                script_data.get("step_result").get("封面").get("ans").get("图集选取").get("依赖的图片序号")[0]
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(str(e))

    if cover_from_images_select_index is None:
        image_list.append(script_data.get("step_result").get("封面").get("ans").get("图片描述"))

    for img in script_data.get("step_result").get("图集").get("ans").get("图片"):
        if img.get("图片序号") == cover_from_images_select_index:
            image_list.insert(0, img.get("图片描述"))
        else:
            image_list.append(img.get("图片描述"))

    ans = prompt.vision_common_build(vision_common, image_list, renshe_material_data)
    print(ans)
    return ans


def generate_image(path):
    data = json.load(open(path, "r"))
    images = data.get("image_detail").get("图片描述")
    for d in images:
        if d.get("results") is None:
            try:
                results = generate_midjourney_image(d.get("Midjourney Prompt"))
            except Exception as e:
                print(f"generate image fail, {e}")
                results = [str(e)]

            d["results"] = results
            utils.save(data, path)


class VisionMaterial:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    @staticmethod
    def build(name, image: str):
        return VisionMaterial(name, image)


def generate_image_by_gemini(image_description_list, vision_materials: list[VisionMaterial] = None):
    generate_image_description_list = [i for i in image_description_list]
    history_messages = []

    for vm in vision_materials:
        if type(vm.name) is list:
            name_declaration = "、".join([f"<<{i}>>" for i in vm.name])
        else:
            name_declaration = str(vm.name)
        ml: list[GenaiMessagePart] = [
            GenaiMessagePart(MessageType.TEXT, f"下面包含{name_declaration}的图片，请在后续的创作过程中从图片中进行参考")]
        if vm.image.startswith("http") is True:
            ml.append(GenaiMessagePart(MessageType.URL_IMAGE, vm.image))
        else:
            ml.append(GenaiMessagePart(MessageType.LOCAL_IMAGE, vm.image))

        mess = GenaiConversationMessage("user", ml)
        history_messages.append(mess)


    start_prompt = "下面是我会直接依次给出图片生成的描述，每一个描述请生成对应的一张图片，请按照我的要求给我生成图片吧。请保持图片与图片之间的连续性和一致性。我相信你一定可以出色我的任务，thank you bro ：），你准备好了，请回复OK"
    generate_image_description_list.insert(0, start_prompt)

    for index, prompt in enumerate(generate_image_description_list):
        ml: list[GenaiMessagePart] = [GenaiMessagePart(MessageType.TEXT, prompt)]

        mess = GenaiConversationMessage("user", ml)

        res = google_genai.google_genai_output_images_and_text(mess, history_messages=history_messages)
        history_messages.append(mess)
        history_messages.append(res)
        print("---------------------prompt--------------------")
        print(prompt)
        print("---------------------response--------------------")
        print(res)
        print("\n\n")

    generated_images = google_genai.get_generated_images(history_messages)
    return generated_images


if __name__ == "__main__":
    xuanti_path = "/image_article_comprehension/aiddit/create/result/script_pipeline/陸清禾/xuanti/黄昏时分城市建筑光影与飞鸟.json"
    renshe_path = "/image_article_comprehension/aigc_data/renshe_0305/account_陸清禾_5657ba2703eb846a34fcc55b.json"
    output_path = xuanti_path.replace("xuanti", "result")
    save_file_path = output_path.replace(".json", "_detail.json")

    renshe = json.load(open(renshe_path, 'r'))
    xuanti = json.load(open(xuanti_path, 'r'))
    renshe_material_data = renshe.get("renshe_constants")
    xuanti_result = xuanti.get("xuanti_creation")

    # 脚本生成
    pipeline(xuanti_result, renshe.get("renshe_xuanti_unique"), renshe.get("script_mode"), renshe_material_data,
             output_path, reference_note=xuanti.get("reference_note"), renshe_path=renshe_path)
    script_data = json.load(open(output_path, "r"))
    image_detail_ans = detail_provider(script_data, renshe_material_data)
    image_detail = utils.try_remove_markdown_tag_and_to_json(image_detail_ans)

    # 生成图片
    generate_image_by_gemini(image_detail)

    utils.save({
        "script_data": script_data,
        "renshe_material_data": renshe_material_data,
        "image_detail": image_detail
    }, save_file_path)
    pass
