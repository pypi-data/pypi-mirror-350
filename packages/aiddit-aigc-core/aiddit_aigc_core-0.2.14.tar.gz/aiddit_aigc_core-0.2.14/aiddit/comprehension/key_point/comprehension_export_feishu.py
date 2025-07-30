from image_analyzer.utils.feshu import write_data_to_sheet, write_images
from comprehension_key_point import distinct_image_content
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/comprehension/key_point/result/analysis_key_point_v1'
data = []

all_result = []
for i in os.listdir(data_dir):
    all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))

for result in all_result:
    note = result.get('note_info')
    if note.get('images') is None or len(note.get('images')) == 0:
        continue

    if result.get('result') is None:
        continue

    images = [f"\"{i}\"" for i in distinct_image_content(note)]

    for index, r in enumerate(result.get("result").get("analysis_key_point_v1")):
        key_point_details = r.get('亮点组成', {})
        vision_images = key_point_details.get("vision_images", None)
        if vision_images is not None:
            vision_images = [f"\"{i}\"" for i in vision_images]

        if key_point_details.get('vision_images') is not None:
            del key_point_details['vision_images']
        if key_point_details.get('image_index') is not None:
            del key_point_details["image_index"]

        row = {
            '帖子id': note.get('channel_content_id') if index == 0 else '',
            "帖子链接": note.get('link') if index == 0 else '',
            '帖子图集': f"[{','.join(images)}]" if index == 0 else '',
            '标题': note.get('title') if index == 0 else '',
            '正文': note.get('body_text') if index == 0 else '',
            '亮点角度': r.get('内容亮点的角度', ''),
            '亮点': r.get('亮点', ''),
            '亮点组成': json.dumps(key_point_details, ensure_ascii=False, indent=4),
            '视觉图片材料': f"[{','.join(vision_images)}]" if vision_images is not None else ''
        }

        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Rbsysi6FChzCp7tfv19crkWNnEb'
sheet_id = 'bhSH6t'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id,skip_images=True )
