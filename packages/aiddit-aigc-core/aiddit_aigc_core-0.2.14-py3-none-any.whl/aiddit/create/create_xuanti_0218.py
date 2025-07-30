import json
import logging
import aiddit.create.xuanti_prompt_0218 as xuanti_prompt_0218
import os
from tqdm import tqdm
import traceback
import aiddit.utils as utils

# 刺激源
reference_note_keypoint_dir = "/image_article_comprehension/xhs/search_result/萌宠日常 萌宠装扮"
# 人设
renshe_path = "/image_article_comprehension/aigc_data/renshe_0305/account_李尾鱼_615657520000000002026e7c.json"
renshe = json.load(open(renshe_path, 'r'))

output_dir = "/image_article_comprehension/aiddit/create/result/xuanti_result_0218"
output_renshe_name = os.path.basename(renshe_path).split(".")[0]
output_renshe_dir = os.path.join(output_dir, output_renshe_name)

if os.path.exists(output_renshe_dir) is not True:
    os.mkdir(output_renshe_dir)


def creation(reference_note, use_cache=True):
    note_info = reference_note.get("note_info", reference_note)
    output_path = os.path.join(output_renshe_dir, note_info.get("channel_content_id") + ".json")
    if os.path.exists(output_path) and use_cache:
        output = json.load(open(output_path, 'r'))
    else:
        output = {
            "reference_note": note_info,
            "renshe": renshe,
            "xuanti_creation": []
        }

    xuanti_creation = output.get("xuanti_creation")

    xuanti_modes = renshe.get("renshe_xuanti_mode", {}).get("modes", [])
    for xuanti_mode in xuanti_modes:
        mode_created = False
        for c in xuanti_creation:
            if json.dumps(c.get("xuanti_mode", {})) == json.dumps(xuanti_mode):
                mode_created = True
                break

        if mode_created and use_cache:
            logging.info(f"keypoint {xuanti_mode.get('选题模式')} created")
            continue

        ans = xuanti_prompt_0218.xuanti_creation_20250113(renshe_xuanti_unique=renshe.get("renshe_xuanti_unique", {}),
                                                          xuanti_mode=xuanti_mode, note_info=note_info,
                                                          script_mode=renshe.get("script_mode"))
        print(ans)
        generated_xuanti_creation = json.loads(ans)

        xuanti_estimate = {}
        if generated_xuanti_creation.get("能否产生选题") == "是":
            # 选题评估
            xuanti_estimate_ans = xuanti_prompt_0218.xuanti_estimate_20250113(renshe.get("renshe_xuanti_unique", {}),
                                                                              xuanti_mode,
                                                                              generated_xuanti_creation)
            print(xuanti_estimate_ans)
            xuanti_estimate = json.loads(xuanti_estimate_ans)

        xuanti_result = {
            "xuanti_mode": xuanti_mode.get("选题模式"),
            "xuanti_creation": generated_xuanti_creation,
            "xuanti_estimate": xuanti_estimate
        }
        xuanti_creation.append(xuanti_result)
        utils.save(output, output_path)


def filter_available_xuanti_creation():
    xuanti_result_path = output_renshe_dir

    result = [json.load(open(os.path.join(xuanti_result_path, i), "r")) for i in
              os.listdir(xuanti_result_path) if i.endswith(".json") and i.startswith("6")]

    filter_xuanti = []

    for i in result:
        for c in i.get("xuanti_creation"):
            creation = c.get("xuanti_creation")
            if c.get("xuanti_creation").get("能否产生选题") == "否":
                continue
            xuanti_estimate = c.get("xuanti_estimate")
            if xuanti_estimate.get("选题符合是否要求") == "是" and xuanti_estimate.get("选题描述符合是否要求") == "是":
                filter_xuanti.append({
                    "xuanti_creation": creation,
                    "reference_note": i.get("reference_note"),
                })

    save_filter_file_path = os.path.join(xuanti_result_path, "filter_xuanti.json")
    utils.save(filter_xuanti, save_filter_file_path)


def batch_create_executor():
    ## 刺激源
    import concurrent.futures

    def process_reference_note(i):
        try:
            logging.info(f"start process {i}")
            reference_note = json.load(open(os.path.join(reference_note_keypoint_dir, i), 'r'))
            creation(reference_note)
        except Exception as e:
            logging.error(f"process {i} error: {str(e)}")
            logging.error(traceback.format_exc())

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in tqdm(os.listdir(reference_note_keypoint_dir)):
            futures.append(executor.submit(process_reference_note, i))

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    batch_create_executor()

    filter_available_xuanti_creation()

    # reference_note = json.load(
    #     open(
    #         "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note/image_0109/67753f3f00000000090167b6.json",
    #         "r"))
    # creation(reference_note, use_cache=False)

    # xuanti_output_result = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/image_since_0113/20250110_摸鱼阿希_copy/67753f3f00000000090167b6.json"
    # xuanti = json.load(open(xuanti_output_result, 'r'))
    # renshe = xuanti.get("renshe")
    # for creation in xuanti.get("xuanti_creation"):
    #     ans = xuanti_estimate_20250113(renshe.get("renshe_xuanti_unique",{}),creation.get("xuanti_mode"), creation.get("xuanti_creation"))
    #     print(ans)
