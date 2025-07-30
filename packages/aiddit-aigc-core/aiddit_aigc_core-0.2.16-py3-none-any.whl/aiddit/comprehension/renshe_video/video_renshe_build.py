import image_article_comprehension.aiddit.comprehension.renshe_video.video_comprehension as video_comprehension
import os
from tqdm import tqdm
import json
import image_article_comprehension.aiddit.utils as utils
import traceback

output_dir = "/image_article_comprehension/aiddit/comprehension/renshe_video/video_key_point"


def extract_account_all_video(account_video_dir):
    extract_target_dir = os.path.join(output_dir, os.path.basename(account_video_dir))

    if os.path.exists(extract_target_dir) is not True:
        os.mkdir(extract_target_dir)

    for i in tqdm(os.listdir(account_video_dir)):
        video_info = json.load(open(os.path.join(account_video_dir, i), "r"))

        extract_target_path = os.path.join(extract_target_dir, i)

        if os.path.exists(extract_target_path):
            result = json.load(open(extract_target_path, "r"))
        else:
            result = {
                "video_info": video_info,
            }

        if result.get("xuanti") is None:
            try:
                xuanti_result = video_comprehension.video_xuanti(video_info)
                result["xuanti"] = json.loads(xuanti_result)
                utils.save(result, extract_target_path)
            except Exception as e:
                traceback.print_exc()
                print(f"extract xuanti error {i} {str(e)}")

        if result.get("keypoint") is None:
            try:
                keypoint_result = video_comprehension.video_keypoint(video_info)
                result["keypoint"] = json.loads(keypoint_result)
                utils.save(result, extract_target_path)
            except Exception as e:
                traceback.print_exc()
                print(f"extract keypoint error {i} {str(e)}")


if __name__ == "__main__":
    video = json.load(open(
        "/image_article_comprehension/aiddit/comprehension/note_data_video/大旭的远方/7424110757375233289.json",
        "r"))

    print(video_comprehension.video_xuanti(video))
    pass
