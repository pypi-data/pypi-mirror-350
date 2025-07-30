import json
import logging
from aiddit.create.xuanti_20250110_before.llm_generation import xuanti_generate_20240108, xuanti_estimate_20250108, \
    xuanti_generate_by_note_20250110
import os
from tqdm import tqdm
import traceback


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


### 人设base数据
renshe_path = "/image_article_comprehension/create/renshe/image/20250110_EllenEveryday.json"
renshe = json.load(open(renshe_path, 'r'))
base_topic = renshe.get("renshe_xuanti_v2", {}).get("base_topic", [])
if len(base_topic) == 0:
    raise Exception("base_topic is empty")
print(base_topic)
renshe_keypoint_with_xuanti = renshe.get("renshe_keypoint_v4", {}).get("keypoint_summary", [])
if len(renshe_keypoint_with_xuanti) == 0:
    raise Exception("renshe_keypoint is empty")

renshe_keypoint = renshe.get("renshe_keypoint_v2", {}).get("keypoint_summary", [])
if len(renshe_keypoint) == 0:
    raise Exception("renshe_keypoint is empty")

print(renshe_keypoint)
xuanti_reference = [f"选题: {i.get('选题')}\n选题描述: {i.get('选题描述')}" for i in
                    renshe.get("history_nice_xuanti", [])]
# xuanti_reference +=  [f"选题: {i.get('选题')}\n选题描述: {i.get('选题描述')}" for i in renshe.get("similar_nice_xuanti", {}).get("serach_nice_xuanti", [])]

renshe_unique_point = renshe.get("renshe_unique_point", {})
xuanti_mode = renshe.get("选题模式", {})
xuanti_category_style = renshe.get("选题品类", {})

output_dir = "/image_article_comprehension/create/result/image"
output_renshe_name = os.path.basename(renshe_path).split(".")[0]
output_renshe_dir = os.path.join(output_dir, output_renshe_name)

if os.path.exists(output_renshe_dir) is not True:
    os.mkdir(output_renshe_dir)


def creation(reference_note, use_cache=True):
    output_path = os.path.join(output_renshe_dir, reference_note.get("note_info").get("channel_content_id") + ".json")
    if os.path.exists(output_path) and use_cache:
        output = json.load(open(output_path, 'r'))
    else:
        output = {
            "reference_note": reference_note.get("note_info"),
            "renshe": renshe,
            "xuanti_creation": []
        }
    xuanti_creation = output.get("xuanti_creation")
    for kp in reference_note.get("keypoint"):
        kp_created = False
        for c in xuanti_creation:
            if json.dumps(c.get("reference_note_keypoint", [])) == json.dumps(kp):
                kp_created = True
                break

        if kp_created and use_cache:
            logging.info(f"keypoint {kp.get('亮点')} created")
            continue
        # 生成选题
        ans = xuanti_generate_20240108(base_topic, renshe_keypoint, renshe_keypoint_with_xuanti, kp,
                                       renshe_unique_point)
        print(ans)
        generated_xuanti_creation = json.loads(ans)
        # 选题评估
        xuanti_estimate = creation_estimate(base_topic, generated_xuanti_creation.get("最终的选题"),
                                            generated_xuanti_creation.get("选题的详细描述信息"))
        print(xuanti_estimate)

        xuanti_result = {
            "reference_note_keypoint": kp,
            "xuanti_creation": generated_xuanti_creation,
            "xuanti_estimate": json.loads(xuanti_estimate)
        }
        xuanti_creation.append(xuanti_result)
        save(output, output_path)


def creation_estimate(base_topic, xuanti_creation, xuanti_creation_description):
    return xuanti_estimate_20250108(renshe_topic=base_topic, xuanti_creation=xuanti_creation,
                                    xuanti_creation_description=xuanti_creation_description,
                                    renshe_unique_point=renshe_unique_point,
                                    xuanti_category_style=xuanti_category_style)


def create_xuanti_by_note(reference_note, use_cache=True):
    note_info = reference_note.get("note_info", reference_note)
    output_path = os.path.join(output_renshe_dir, note_info.get("channel_content_id") + ".json")
    if os.path.exists(output_path) and use_cache:
        output = json.load(open(output_path, 'r'))
    else:
        output = {
            "reference_note": note_info,
            "renshe": renshe,
        }

    if output.get("xuanti_creation_by_note") is not None and use_cache:
        logging.info(f"reference {os.path.basename(output_path)} created")
        return

    ans = xuanti_generate_by_note_20250110(base_topic, renshe_keypoint, renshe_keypoint_with_xuanti,
                                           renshe_unique_point,
                                           note_info, xuanti_mode, xuanti_category_style)
    print(ans)
    generated_xuanti_creation = json.loads(ans)

    # 选题评估
    xuanti_estimate = creation_estimate(base_topic, generated_xuanti_creation.get("最终的选题"),
                                        generated_xuanti_creation.get("选题的详细描述信息"))
    print(xuanti_estimate)

    xuanti_result = {
        "reference_note_keypoint": {
            "选题的参考来源": generated_xuanti_creation.get("选题的参考来源")
        },
        "xuanti_creation": generated_xuanti_creation,
        "xuanti_estimate": json.loads(xuanti_estimate)
    }
    output["xuanti_creation_by_note"] = xuanti_result
    save(output, output_path)


def batch_create_executor():
    ## 刺激源
    import concurrent.futures

    reference_note_keypoint_dir = "/image_article_comprehension/create/reference_note/image_0109"

    def process_reference_note(i):
        try:
            logging.info(f"start process {i}")
            reference_note = json.load(open(os.path.join(reference_note_keypoint_dir, i), 'r'))
            # creation(reference_note)
            create_xuanti_by_note(reference_note)
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

    # 刺激源
    # reference_note = json.load(
    #     open(
    #         "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/image_merge_0102_1230/675ce18b00000000020162b0.json",
    #         "r"))
    # creation(reference_note, use_cache=False)

    # reference_note = json.load(
    #     open(
    #         "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note/image_0109/674053ee0000000006015c22.json",
    #         "r"))
    # create_xuanti_by_note(reference_note, use_cache=False)

    # xuanti_output_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/image/0104Lily的美食日记_1644_copy/673ab0350000000007030cef.json"
    # xuanti_output = json.load(open(xuanti_output_path, 'r'))
    # for i in xuanti_output.get('xuanti_creation', []):
    #     ans = xuanti_estimate_query_keyword(base_topic, i.get("xuanti_creation").get("最终的选题"))
    #     print(ans)

    pass
