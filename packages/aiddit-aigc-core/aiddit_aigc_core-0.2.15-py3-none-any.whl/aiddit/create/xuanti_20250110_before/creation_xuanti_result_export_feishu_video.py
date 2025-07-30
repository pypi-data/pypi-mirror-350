from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/create/result/video/光'
data = []

all_result = []
for i in os.listdir(data_dir):
    all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))

for result in all_result:
    images = [f"\"{i}\"" for i in result.get('reference_note', {}).get('cover_image_url', [])]

    for xuanti_creation in result.get("xuanti_creation", []):
        mj_images = [f"\"{i}\"" for i in xuanti_creation.get('xuanti_creation', {}).get('midjourney_image', [])]
        row = {
            '人设方向': json.dumps(result.get("renshe", {}).get("base_topic", {}), ensure_ascii=False, indent=4),
            '人设要点': json.dumps(result.get("renshe", {}).get("renshe_keypoint", {}), ensure_ascii=False, indent=4),
            '刺激源链接': result.get("reference_note", {}).get("link", ''),
            '刺激源封面': result.get('reference_note', {}).get('cover_image_url', ''),
            '刺激源要点': json.dumps(xuanti_creation.get("reference_note_keypoint"), ensure_ascii=False, indent=4),
            '选题': xuanti_creation.get("xuanti_creation", {}).get("最终的选题"),
            '选题的详细描述信息': xuanti_creation.get("xuanti_creation", {}).get("选题的详细描述信息"),
            '选题的参考来源': xuanti_creation.get("xuanti_creation", {}).get("选题的参考来源"),
            '选题依赖的关键信息': json.dumps(xuanti_creation.get("xuanti_creation", {}).get("选题依赖的关键信息"),
                                             ensure_ascii=False, indent=4),
            "选题判断-是否可行": xuanti_creation.get("xuanti_estimate", {}).get("是否是一个好选题", ""),
            "选题判断-explanation": xuanti_creation.get("xuanti_estimate", {}).get("explanation", ""),
            "选题判断-是否可行(claude)": xuanti_creation.get("xuanti_estimate_claude", {}).get("是否是一个好选题", ""),
            "选题判断-explanation(claude)": xuanti_creation.get("xuanti_estimate_claude", {}).get("explanation", ""),
        }
        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'N8NlsG4sUhS3aktj5mTcqW7AnOe'
sheet_id = 'aiphTM'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
