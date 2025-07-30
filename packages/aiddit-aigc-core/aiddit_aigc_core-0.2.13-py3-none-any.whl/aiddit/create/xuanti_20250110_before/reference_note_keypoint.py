import json
import os
import logging
from tqdm import tqdm

reference_note_dir = "/image_article_comprehension/create/reference_note/image_search_中医食疗方案"
reference_note_keypoint_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/" + os.path.basename(
    reference_note_dir)

if os.path.exists(reference_note_keypoint_dir) is not True:
    os.mkdir(reference_note_keypoint_dir)

from image_article_comprehension.aiddit.comprehension.key_point.comprehension_key_point import analysis_key_point_v1


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


for reference_note_file_name in tqdm(os.listdir(reference_note_dir)):
    try:
        if os.path.exists(os.path.join(reference_note_keypoint_dir, reference_note_file_name)):
            print(f"{reference_note_file_name} already exists")
            continue

        logging.info("start process %s", reference_note_file_name)

        note_info = json.load(open(os.path.join(reference_note_dir, reference_note_file_name), 'r'))

        if len(note_info.get("images", [])) == 0:
            logging.info("%s images is empty", reference_note_file_name)
            continue

        keypoint_ans = analysis_key_point_v1(note_info)
        logging.info(keypoint_ans)
        keypoint = json.loads(keypoint_ans)

        result = {
            "note_info": note_info,
            "keypoint": keypoint
        }

        save(result, os.path.join(reference_note_keypoint_dir, reference_note_file_name))
    except Exception as e:
        logging.error(e)
