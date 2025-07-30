from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/comprehension/result/xuanti_result_v5_家居'
data = []

all_result = []
for i in os.listdir(data_dir):
    all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))

# all_result.sort(key=lambda x: x['note_info']['user_id'])
# grouped_data = {k: list(v) for k, v in groupby(all_result, key=lambda x: x['note_info']['user_id'])}
# for key, value in grouped_data.items():
#     print(f"{key} , len = {len(value)}")
# for result in grouped_data.get("5f93ca250000000001007ac0"):
for result in all_result:
    if result.get('xuanti_pins_search') is None:
        continue

    note = result.get('note_info')
    if note.get('images') is None:
        continue

    images = [f"\"{i}\"" for i in note.get('images')[:1]]

    pins_image = [f"\"{i.get('image')}\"" for i in result.get('xuanti_pins_search')[:5]]

    row = {
        '个人主页': f"https://www.xiaohongshu.com/user/profile/{note.get('user_id')}?xsec_token=&xsec_source=pc_feed",
        '帖子链接': note.get('link', ''),
        '帖子图片': f"[{','.join(images)}]",
        '选题描述': result.get('xuanti_result').get('关键点'),
        '选题思路': result.get('xuanti_result').get('关键点描述'),
        # '选题视觉呈现': json.dumps(result.get('xuanti_result').get('选题视觉呈现'), ensure_ascii=False, indent=4),
        'Pinterest搜索链接': result.get('xuanti_pins_search_link'),
        'Pinterest搜索结果': f"[{','.join(pins_image)}]",
    }
    data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Rbsysi6FChzCp7tfv19crkWNnEb'
sheet_id = 'kKDzVT'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
