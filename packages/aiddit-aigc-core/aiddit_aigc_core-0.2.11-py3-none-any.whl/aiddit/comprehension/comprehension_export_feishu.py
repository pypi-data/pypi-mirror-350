from image_analyzer.utils.feshu import write_data_to_sheet, write_images
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/comprehension/result/xuanti_result_v5_选题理解测试数据'
data = []

all_result = []
for i in os.listdir(data_dir):
    all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))

for result in all_result:
    note = result.get('note_info')
    if note.get('images') is None or len(note.get('images')) == 0:
        continue

    if result.get('xuanti_result') is None:
        continue

    images = [f"\"{i}\"" for i in note.get('images')[:1]]

    row = {
        '帖子id': note.get('channel_content_id'),
        # '帖子封面': f"[{','.join(images)}]",
        '帖子封面': note.get('images')[0] if note.get('images') else None,
        '标题': note.get('title'),
        '正文': note.get('body_text'),
        '来源抓取计划': note.get('source_plan_name'),
        'analysis_xuanti_v5': result.get('xuanti_result').get('analysis_xuanti_v5', {}).get('关键点'),
        'analysis_xuanti_v6': result.get('xuanti_result').get('analysis_xuanti_v6', {}).get('关键点'),
        'analysis_xuanti_v7_class': result.get('xuanti_result').get('analysis_xuanti_v7', {}).get('内容所属领域'),
        'analysis_xuanti_v7': result.get('xuanti_result').get('analysis_xuanti_v7', {}).get('内容选题'),
    }
    data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Rbsysi6FChzCp7tfv19crkWNnEb'
sheet_id = '9UOd7X'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
