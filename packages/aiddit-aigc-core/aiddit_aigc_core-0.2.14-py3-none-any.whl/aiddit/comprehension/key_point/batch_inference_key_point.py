from comprehension_key_point import analysis_key_point_v1, distinct_image_content
import json
import os
from tqdm import tqdm
import traceback
import concurrent.futures
import logging

# 修改变量 start

# 理解版本
comprehension_function = analysis_key_point_v1
comprehension_version = "analysis_key_point_v1"
# 理解输出目录
output_dir = f"result/{comprehension_version}"

# 理解来源帖子目录
note_dir = [
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/要点_脚本_材料测试数据"
]


# 修改变量 end

def load_notes(dir_path):
    files = os.listdir(dir_path)

    note_data = []
    for f in files:
        if f.endswith('.json'):
            n = json.load(open(os.path.join(dir_path, f), 'r'))
            note_data.append(n)

    return note_data


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


def note_comprehension(note):
    ans = None
    try:
        print(f"note comprehension start {note['channel_content_id']}")
        result_file = f"{output_dir}/{note['channel_content_id']}.json"

        if os.path.exists(result_file) is True:
            save_result = json.load(open(result_file, 'r'))
            if save_result.get('result').get(comprehension_function.__name__) is not None:
                print(f"note comprehension end {note['channel_content_id']}  {comprehension_function.__name__} cached")
                return
        else:
            save_result = {
                "result": {},
                "note_info": note
            }

        if note.get("images") is None or len(note.get("images")) == 0:
            print(f"note comprehension end {note['channel_content_id']} no images")
            return

        if any("https://p3-pc-sign.douyinpic.com" in s for s in note.get("images")):
            return

        ans = comprehension_function(note)
        r = json.loads(ans)

        images = distinct_image_content(note)

        for item in r:
            key_point_details = item.get('亮点组成', {})
            if key_point_details.get('image_index') is not None:
                key_point_details['image_index'] = [i for i in key_point_details.get('image_index', []) if
                                                    i < len(images)]
                vision_images = [images[i] for i in key_point_details.get('image_index')]
                key_point_details['vision_images'] = vision_images
                item["亮点组成"] = key_point_details

        save_result.get("result")[comprehension_function.__name__] = r

        print(f"note comprehension start finished {note['channel_content_id']}")
        save(save_result, result_file)
    except json.decoder.JSONDecodeError:
        print("json.decoder.JSONDecodeError")
        logging.error(f"json.decoder.JSONDecodeError \n {ans}")
        print()
    except Exception as e:
        err = traceback.format_exc()
        logging.error(err)


# 创建文件夹output_dir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

notes = []

for dir_item in note_dir:
    notes.extend(load_notes(dir_item))

notes = notes[:100]
print(f"notes = {len(notes)}")


def process_batch(batch):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(note_comprehension, note) for note in batch]
        for future in concurrent.futures.as_completed(futures):
            future.result()


batch_size = 3
batches = [notes[i:i + batch_size] for i in range(0, len(notes), batch_size)]

for batch in tqdm(batches, total=len(batches)):
    process_batch(batch)

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     for batch in tqdm(batches, total=len(batches)):
#         future = executor.submit(process_batch, batch)
#         future.result()
