import sys

sys.path.append("/Users/nieqi/Documents/workspace/python")
from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby
import pandas
import aiddit.utils as utils


def filter_links_and_output(search_string):
    csv_path = "/Users/nieqi/Downloads/未命名表格 - Sheet1.csv"
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Filter rows where 内容链接 contains the search string
    filtered_df = df[df['内容链接'].str.contains(search_string, na=False)]

    # Select only the required columns
    result = filtered_df[['搜索词来源', '搜索词', '刺激源内容模态']]

    return result


# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/topic_result_0415/猫小司'
data = []

all_result = []
for i in [f for f in os.listdir(data_dir) if f.endswith('.json')]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for result in all_result:
    reference_note = result.get("reference_note", {})
    images = [f"\"{i}\"" for i in utils.remove_duplicates(reference_note.get("images", []))]

    r = result.get("topic", {})

    if type(r) is list:
        r = r[0]

    topic = r.get("选题结果", {})

    row = {
        "帖子id": reference_note.get("channel_content_id", ""),
        "链接": reference_note.get("link", ""),
        '刺激源': f"[{','.join(images)}]",
        "刺激源内容模态": "视频" if reference_note.get("content_type", "") == "video" else "图文",
        '刺激源标题正文': reference_note.get("title", "") + "\n\n" + reference_note.get("body_text", ""),
        "选题": topic.get("选题", None) if topic.get("选题", None) is not None else topic.get(
            "不能产生选题的原因", ""),
        "选题描述": topic.get("选题描述", None),
        "选题创作的关键点": json.dumps(topic.get("选题创作的关键点", []), ensure_ascii=False, indent=4),
        "知识库引用说明": topic.get("知识库引用说明", None),
        "选题产生的逻辑": topic.get("选题产生的逻辑", None),
    }
    data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'qM0SD6'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
