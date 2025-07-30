from image_analyzer.lib.xuanti_v1_0_0 import pack_image_content, analysis_xuanti, analysis_xuanti_v5, \
    analysis_xuanti_v6, analysis_xuanti_v7
import json
import os
from tqdm import tqdm
import traceback
import concurrent.futures
import logging

# 修改变量 start

# 理解版本
comprehension_function = analysis_xuanti_v7
comprehension_version = "v5_选题理解测试数据"
# 理解输出目录
output_dir = f"result/xuanti_result_{comprehension_version}"
# 理解来源帖子目录
# note_dir = [
#     "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/新红-低粉爆款排行",
#     "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/新红-暴增笔记排行"]
note_dir = [
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/选题理解测试数据"
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
            if save_result.get('xuanti_result').get(comprehension_function.__name__) is not None:
                print(f"note comprehension end {note['channel_content_id']}  {comprehension_function.__name__} cached")
                return
        else:
            save_result = {
                "xuanti_result": {},
                "note_info": note
            }

        if note.get("images") is None or len(note.get("images")) == 0:
            print(f"note comprehension end {note['channel_content_id']} no images")
            return

        if any("https://p3-pc-sign.douyinpic.com" in s for s in note.get("images")):
            return

        ans = comprehension_function(note)
        xuanti_result = json.loads(ans)

        save_result.get("xuanti_result")[comprehension_function.__name__] = xuanti_result

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

# notes = notes[:20]
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
