from image_analyzer.lib.xuanti_v1_0_0 import pack_image_content, analysis_xuanti, analysis_xuanti_v2, \
    analysis_xuanti_v4, analysis_xuanti_v5, analysis_xuanti_cot, analysis_xuanti_v6, analysis_xuanti_v7
import json
import os
from tqdm import tqdm
import traceback
import concurrent.futures
import time


def note_comprehension(note):
    try:
        ans = analysis_xuanti(note)
        print("ans:", ans)
    except Exception as e:
        err = traceback.format_exc()
        print(err)


# note_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/account_5f93ca250000000001007ac0/6659d553000000000500660b.json"

note_path = "/image_article_comprehension/aiddit/comprehension/note_data/选题理解测试数据/62ae86fd000000000e00cac4.json"

note = json.load(open(note_path, 'r'))

# v1_result = analysis_xuanti_v2(note)
# print(f"{v1_result}")

v2_result = analysis_xuanti_v7(note)
print(f"{json.dumps(json.loads(v2_result), ensure_ascii=False, indent=4)}")

# test_ljg(note)

# def load_notes(dir_path):
#     files = os.listdir(dir_path)
#
#     note_data = []
#     for f in files:
#         if f.endswith('.json'):
#             n = json.load(open(os.path.join(dir_path, f), 'r'))
#             note_data.append(n)
#
#     return note_data
#
#
# note_dir = [
#     "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/result/xuanti_result_v5_选题理解测试数据"]
#
# for dir_item in note_dir:
#     notes = load_notes(dir_item)
#     for n in notes:
#         try:
#             path = f"{dir_item}/{n.get('note_info').get('channel_content_id')}.json"
#             xuanti_result = n.get('xuanti_result').get('12_13')
#             r = {
#                 "analysis_xuanti_v5": xuanti_result
#             }
#             n['xuanti_result'] = r
#             with open(path, 'w') as f:
#                 json.dump(n, f, ensure_ascii=False, indent=4)
#         except Exception as e:
#             err = traceback.format_exc()
#             print(err)
