import json
import os
import aiddit.utils as utils
import aiddit.video.video_xuanti_prompt as video_xuanti_prompt
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def create_xuanti_by_keypoint(reference_note, renshe, result, save_file_path):
    if result.get("帖子亮点选题结果") is not None:
        print("人设亮点选题结果 is not None")
        return

    def comprehension_keypoint():
        ans = video_xuanti_prompt.reference_note_keypoint(reference_note)
        return json.loads(ans)

    # 获取视频亮点
    reference_note_keypoint_result_path = f"/image_article_comprehension/aiddit/video/data/reference_note_comprehension/{reference_note.get('channel_content_id')}.json"
    if os.path.exists(reference_note_keypoint_result_path):
        reference_note_keypoint_result = json.load(open(reference_note_keypoint_result_path, "r"))
        if reference_note_keypoint_result.get("亮点") is None:
            reference_note_keypoint_result["亮点"] = comprehension_keypoint()
        else:
            print("亮点 is not None")
    else:
        reference_note_keypoint_result = {
            "reference_note": reference_note,
            "亮点": comprehension_keypoint()
        }
    utils.save(reference_note_keypoint_result, reference_note_keypoint_result_path)

    # 结合人设 + 视频亮点生成选题
    prompt, ans = video_xuanti_prompt.reference_note_keypoint_20250210(renshe,
                                                                       reference_note_keypoint_result.get("亮点"))

    r = estimate_xuanti(renshe, ans)
    r["亮点"] = reference_note_keypoint_result.get("亮点")
    result["帖子亮点选题结果"] = r
    utils.save(result, save_file_path)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def create_xuanti_by_keypoint_deepseek_r3(reference_note, renshe, result, save_file_path):
    if result.get("帖子亮点选题结果_deepseek_r3") is not None:
        print("人设亮点选题结果 deepseek r1 is not None")
        return

    def comprehension_keypoint():
        ans = video_xuanti_prompt.reference_note_keypoint_20250211(reference_note)
        return json.loads(ans)

    # 获取视频亮点
    key_point_version = "亮点0211"
    reference_note_keypoint_result_path = f"/image_article_comprehension/aiddit/video/data/reference_note_comprehension/{reference_note.get('channel_content_id')}.json"
    if os.path.exists(reference_note_keypoint_result_path):
        reference_note_keypoint_result = json.load(open(reference_note_keypoint_result_path, "r"))
        if reference_note_keypoint_result.get(key_point_version) is None:
            reference_note_keypoint_result[key_point_version] = comprehension_keypoint()
        else:
            print(f"{reference_note.get('channel_content_id')} {key_point_version} is not None")
    else:
        reference_note_keypoint_result = {
            "reference_note": reference_note,
            key_point_version: comprehension_keypoint()
        }
    utils.save(reference_note_keypoint_result, reference_note_keypoint_result_path)

    if reference_note_keypoint_result.get(key_point_version) is None:
        print(f"{reference_note.get('channel_content_id')} 亮点 is None")
        return

    # 结合人设 + 视频亮点生成选题
    reason, ans = video_xuanti_prompt.reference_note_keypoint_20250210_deepseek_r3(renshe,
                                                                                   reference_note_keypoint_result.get(
                                                                                       key_point_version))
    r = {
        "选题结果": utils.try_remove_markdown_tag_and_to_json(ans),
        "推理过程": reason,
        "亮点": reference_note_keypoint_result.get(key_point_version)
    }
    result["帖子亮点选题结果_deepseek_r3"] = r
    utils.save(result, save_file_path)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def create_xuanti_by_reference_note(reference_note, renshe, result, save_file_path):
    if result.get("人设亮点选题结果") is not None:
        print("人设亮点选题结果 is not None")
        return

    prompt, ans = video_xuanti_prompt.create_xuanti_by_note(reference_note, renshe)

    r = estimate_xuanti(renshe, ans)

    result["人设亮点选题结果"] = r
    utils.save(result, save_file_path)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def estimate_xuanti(renshe, xuanti_ans):
    r = {
        "选题结果": json.loads(xuanti_ans)
    }

    for created_xuanti in r.get("选题结果"):
        if created_xuanti.get("能否产生选题") != "是":
            continue

        xtmd = None
        for xuanti_mode in renshe.get("选题模式"):
            if created_xuanti.get("参考的选题模式") == xuanti_mode.get("选题模式"):
                xtmd = xuanti_mode
                break

        prompt, ans = video_xuanti_prompt.estimate_xuanti(created_xuanti, renshe, xtmd)
        created_xuanti["选题评估"] = {
            "prompt": prompt,
            "评估结果": json.loads(ans)
        }

    return r


if __name__ == "__main__":
    renshe_path = "/image_article_comprehension/aiddit/video/data/renshe/星有野.json"
    renshe = json.load(open(renshe_path, "r"))

    reference_note_dir = "/image_article_comprehension/aiddit/video/data/reference_note/抖音热榜0212"
    rs = [json.load(open(os.path.join(reference_note_dir, i), "r")) for i in os.listdir(reference_note_dir) if
          i.endswith(".json") and json.load(open(os.path.join(reference_note_dir, i), "r")).get("duration_seconds",
                                                                                                1000) < 120]

    save_file_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/video/data/xuanti/" + \
                    os.path.basename(renshe_path).split(".")[0]
    if not os.path.exists(save_file_dir):
        os.makedirs(save_file_dir)

    import concurrent.futures


    def process_reference_note(reference_note):
        # if reference_note.get("channel_content_id") != "7468149819232619833":
        #     continue

        save_file_path = f"{save_file_dir}/{reference_note.get('channel_content_id')}.json"
        if os.path.exists(save_file_path):
            result = json.load(open(save_file_path, "r"))
        else:
            result = {
                "reference_note": reference_note,
            }
        # create_xuanti_by_keypoint(reference_note, renshe, result, save_file_path)
        # create_xuanti_by_reference_note(reference_note, renshe, result, save_file_path)
        create_xuanti_by_keypoint_deepseek_r3(reference_note, renshe, result, save_file_path)


    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_reference_note, rs[:20])
