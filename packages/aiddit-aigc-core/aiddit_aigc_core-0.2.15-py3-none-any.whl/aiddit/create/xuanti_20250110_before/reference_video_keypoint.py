import json
import os
import logging
import traceback

from image_article_comprehension.aiddit.comprehension.renshe_video.video_comprehension import video_keypoint


def prepare_video_reference_note():
    video_list = json.load(open("/Users/nieqi/Downloads/video_list.json", "r"))
    for video in video_list.get("data").get("data"):
        save_video = {
            "channel_content_id": video.get("channelContentId"),
            "link": video.get("contentLink"),
            "cover_image_url": video.get("coverImageUrl"),
            "title": video.get("title"),
            "bodyText": video.get("bodyText", ""),
            "video_url": video.get("videoUrl"),
        }
        save_path = os.path.join(
            "/image_article_comprehension/create/reference_note/video_0120",
            save_video.get("channel_content_id") + ".json")

        with open(save_path, 'w') as f:
            json.dump(save_video, f, ensure_ascii=False, indent=4)


def process_reference_video_note_keypoint(reference_note_dir, reference_note_keypoint_dir):
    for reference_note_file_name in os.listdir(reference_note_dir):
        try:
            if os.path.exists(os.path.join(reference_note_keypoint_dir, reference_note_file_name)):
                print(f"{reference_note_file_name} already exists")
                continue

            logging.info("start process %s", reference_note_file_name)

            note_info = json.load(open(os.path.join(reference_note_dir, reference_note_file_name), 'r'))
            keypoint = json.loads(video_keypoint(note_info))

            result = {
                "note_info": note_info,
                "keypoint": keypoint
            }

            with open(os.path.join(reference_note_keypoint_dir, reference_note_file_name), 'w') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error("process %s error: %s", reference_note_file_name, str(e))
            traceback.print_exc()


if __name__ == "__main__":
    reference_note_dir = "/image_article_comprehension/create/reference_note/video_0120"
    reference_note_keypoint_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/" + os.path.basename(
        reference_note_dir)

    if os.path.exists(reference_note_keypoint_dir) is not True:
        os.mkdir(reference_note_keypoint_dir)

    process_reference_video_note_keypoint(reference_note_dir, reference_note_keypoint_dir)

    # reference_video_note = json.load(open(
    #     "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note/video_0120/7452993457116745012.json",
    #     "r"))
    # video_keypoint(reference_video_note)
    pass
