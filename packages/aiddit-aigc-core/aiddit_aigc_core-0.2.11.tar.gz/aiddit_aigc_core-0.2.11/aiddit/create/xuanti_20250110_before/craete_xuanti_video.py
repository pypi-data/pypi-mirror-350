import json
import logging
from image_article_comprehension.aiddit.create.xuanti_20250110_before.llm_generation import xuanti_estimate, xuanti_generate_20240103
import os
from tqdm import tqdm


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


### 人设base数据
renshe_path = "/image_article_comprehension/create/renshe/video/光.json"
renshe = json.load(open(renshe_path, 'r'))
base_topic = renshe.get("renshe_xuanti_v2", {}).get("base_topic", [])
if len(base_topic) == 0:
    raise Exception("base_topic is empty")
print(base_topic)
renshe_keypoint = renshe.get("renshe_keypoint_v2", {}).get("keypoint_summary", [])
if len(renshe_keypoint) == 0:
    raise Exception("renshe_keypoint is empty")
print(renshe_keypoint)
xuanti_reference = []
# xuanti_reference +=  [f"选题: {i.get('选题')}\n选题描述: {i.get('选题描述')}" for i in renshe.get("similar_nice_xuanti", {}).get("serach_nice_xuanti", [])]

output_dir = "/image_article_comprehension/create/result/video"
output_renshe_name = os.path.basename(renshe_path).split(".")[0]
output_renshe_dir = os.path.join(output_dir, output_renshe_name)

if os.path.exists(output_renshe_dir) is not True:
    os.mkdir(output_renshe_dir)


def creation_estimate(base_topic, xuanti_creation, xuanti_creation_description):
    return xuanti_estimate(renshe_topic=base_topic, xuanti_creation=xuanti_creation,
                           xuanti_creation_description=xuanti_creation_description)


def creation(reference_note):
    if reference_note.get('keypoint') is None:
        return

    output_path = os.path.join(output_renshe_dir, reference_note.get("note_info").get("channel_content_id") + ".json")
    if os.path.exists(output_path):
        output = json.load(open(output_path, 'r'))
    else:
        output = {
            "reference_note": reference_note.get("note_info"),
            "renshe": {
                "base_topic": base_topic,
                "renshe_keypoint": renshe_keypoint
            },
            "xuanti_creation": []
        }
    xuanti_creation = output.get("xuanti_creation")

    # 数据结构适配
    video_keypoints = [reference_note.get('keypoint')]

    for kp in video_keypoints:
        kp_created = False
        for c in xuanti_creation:
            if json.dumps(c.get("reference_note_keypoint", [])) == json.dumps(kp):
                kp_created = True
                break

        if kp_created:
            logging.info(f"keypoint {kp.get('亮点')} created")
            continue

        # 生成选题
        ans = xuanti_generate_20240103(base_topic, renshe_keypoint, kp)
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


def update_creation_estimate():
    for i in tqdm(os.listdir(output_renshe_dir)):
        r = json.load(open(os.path.join(output_renshe_dir, i), 'r'))

        for xuanti_creation in r.get("xuanti_creation", []):
            xuanti_estimate_pass = xuanti_creation.get("xuanti_estimate", {}).get("是否是一个好选题", "")
            xuanti_creation_result = xuanti_creation.get("xuanti_creation", {})
            print(f'{i} , {xuanti_creation_result.get("最终的选题")} : 是否是一个好选题 {xuanti_estimate_pass}')

            xuanti_estimate = creation_estimate(base_topic, xuanti_creation_result.get("最终的选题"),
                                                xuanti_creation_result.get("选题的详细描述信息"))
            print(xuanti_estimate)

            xuanti_creation["xuanti_estimate_claude"] = json.loads(xuanti_estimate)
            save(r, os.path.join(output_renshe_dir, i))


if __name__ == "__main__":
    # ## 刺激源
    # reference_note_keypoint_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/video_0120"
    # for i in tqdm(os.listdir(reference_note_keypoint_dir)):
    #     try:
    #         logging.info(f"start process {i}")
    #         reference_note = json.load(open(os.path.join(reference_note_keypoint_dir, i), 'r'))
    #         creation(reference_note)
    #     except Exception as e:
    #         logging.error(f"process {i} error: {str(e)}")
    #         logging.error(traceback.format_exc())

    ## 刺激源
    # reference_note = json.load(
    #     open(
    #         "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/video_0120/7452993457116745012.json",
    #         "r"))
    # creation(reference_note)

    update_creation_estimate()
