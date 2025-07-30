import json
import os.path

import aiddit.comprehension.script0221.script_prompt as script_prompt
import concurrent.futures
import aiddit.utils as utils
from tqdm import tqdm


def note_script(note):
    script_ans = script_prompt.note_script(note)
    return utils.try_remove_markdown_tag_and_to_json(script_ans)

def note_create_style(note):
    return utils.try_remove_markdown_tag_and_to_json(script_prompt.note_create_style(note))

def process_note(input_note_info, target_output_dir=None, use_cache=True):
    output_dir = target_output_dir if target_output_dir is not None else "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/script0221/result"
    output_file_name = f"{input_note_info.get('channel_content_id')}.json"

    images = utils.remove_duplicates(input_note_info.get("images", []))
    if os.path.exists(os.path.join(output_dir, output_file_name)):
        result = json.load(open(os.path.join(output_dir, output_file_name), "r"))
    else:
        result = {"note_info": input_note_info}

    image_description_results = [{"index": index + 1, "image": image} for index, image in
                                 enumerate(images)] if result.get(
        "image_description_results") is None else result.get("image_description_results")

    def process_image(image_description_result):
        if image_description_result.get("description") is None:
            description = script_prompt.image_description(image_description_result.get("image"))
            image_description_result["description"] = description

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(process_image, image_description_results)

    result["image_description_results"] = image_description_results
    utils.save(result, os.path.join(output_dir, output_file_name))

    if result.get("script") is not None and use_cache:
        return result.get("script")

    script_ans = script_prompt.note_script_from_image_description(input_note_info, image_description_results)
    script = utils.try_remove_markdown_tag_and_to_json(script_ans)

    # # script["标题"]["标题"] = input_note_info.get("title")
    # # script["正文"]["正文"] = input_note_info.get("body_text")
    # # script.get("图片", {}).get('封面', {})['image_url'] = image_description_results[0].get("image")
    # script.get("图片", {}).get('封面', {})['图片描述'] = image_description_results[0].get("description")
    #
    # for i in script.get("图片").get('图集', {}).get("图集图片列表", []):
    #     # i["image_url"] = image_description_results[i.get("index") - 1].get("image")
    #     i["图片描述"] = image_description_results[i.get("index") - 1].get("description")
    #
    result["script"] = script
    utils.save(result, os.path.join(output_dir, output_file_name))

    return script


def note_dir_process():
    dir_path = "/image_article_comprehension/aigc_data/note_data/account_山越记_5a492e234eacab66bd2a3f8d"
    list_dir = os.listdir(dir_path)

    output_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/script0221/result/" + \
                 os.path.basename(dir_path).split("_")[-3] + "_" + os.path.basename(dir_path).split("_")[-2]

    target_note_dir = [json.load(open(os.path.join(dir_path, i), "r")) for i in list_dir if i.endswith(".json")][:30]

    for note in tqdm(target_note_dir):
        process_note(note, output_dir)


if __name__ == "__main__":
    # note_dir_process()

    input_note_info = {
        "channel_content_id": "67be9f2d000000000603e42f",
        "link": "https://www.xiaohongshu.com/explore/67be9f2d000000000603e42f?xsec_token=",
        "xsec_token": "",
        "comment_count": None,
        "images": [
            "http://res.cybertogether.net/crawler/image/76aa38898b4910a941e54f23b0721001.webp",
            "http://res.cybertogether.net/crawler/image/76aa38898b4910a941e54f23b0721001.webp",
            "http://res.cybertogether.net/crawler/image/86d7761c83f2ed9d5d73634e1b913fb1.webp",
            "http://res.cybertogether.net/crawler/image/e55c3cfc4ed0e92edb36a2388dbe82a3.webp",
            "http://res.cybertogether.net/crawler/image/95ba4dba087d0314a23e935ab9ed1156.webp",
            "http://res.cybertogether.net/crawler/image/ec14da7ecdd7050a60230b5c93c34061.webp",
            "http://res.cybertogether.net/crawler/image/04feb37c8cb9bbebd012356d19936d18.webp",
            "http://res.cybertogether.net/crawler/image/27d92ac754343afda6eb131e2227e91f.webp"
        ],
        "like_count": 807,
        "body_text": "#简笔画[话题]# #零基础学画画[话题]# #日常碎片PLOG[话题]# #画画的日常[话题]# #简笔画教程[话题]# #治愈[话题]# #儿童画[话题]# #长城[话题]# #手绘教程[话题]# #每日一画画[话题]#",
        "title": "日更简笔教程",
        "collect_count": 697,
        "content_type": "note"
    }

    script = note_create_style(input_note_info)
    print(json.dumps(script, ensure_ascii=False, indent=4))
    pass
