from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import traceback

directory = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result/renshe_script_0213'
json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

data = []

for json_file in json_files:
    r = json.load(open(os.path.join(directory, json_file), 'r'))
    try:
        row = {
            "账号名": json_file.replace('.json', '').split("_")[1],
            "账号链接": r.get("帖子"),
            "标题创作模式": json.dumps(r.get("脚本模式").get("标题创作模式"), ensure_ascii=False, indent=4),
            "正文创作模式": json.dumps(r.get("脚本模式").get("正文创作模式"), ensure_ascii=False, indent=4),
            "封面创作模式": json.dumps(r.get("脚本模式").get("封面创作模式"), ensure_ascii=False, indent=4),
            "图集创作模式": json.dumps(r.get("脚本模式").get("图集创作模式"), ensure_ascii=False, indent=4),
        }
        data.append(row)
    except Exception as e:
        traceback.print_exc()

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'CNWXIo'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, skip_images=False, start_row=1)
