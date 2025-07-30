import sys
sys.path.append("/Users/nieqi/Documents/workspace/python")
from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import aiddit.utils as utils

# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/script_result_0418/陸清禾'
data = []

script_data_list = os.listdir(data_dir)

# script_data_list = [
#     "同事把巨型向日葵穿在身上，结果忘记浇水把自己‘晒蔫儿’了_use_script_mode.json",
#     "同事为了图省事不洗杯子，用外卖塑料袋当内胆喝水_use_script_mode.json"
# ]

all_result = []
for i in script_data_list:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

renshe_info_inserted  = False

for r_index, result in enumerate(all_result):

    generated_results = []

    renshe_info = json.load(open(result.get("renshe_path"), 'r'))
    account_link = renshe_info.get("account_info").get("account_link")

    for i in result.keys():
        if i.startswith("script_generate_result"):
            generated_results.append(result[i])
    xuanti_inserted = False

    for index, r in enumerate(generated_results):
        script = r.get("script").get("创作的脚本")

        image_description = script.get('图集描述')

        optimize_script = r.get("optimize_script").get("优化的脚本")
        optimize_image_description = optimize_script.get('优化后的图集描述')

        loop_count = max(len(image_description), len(optimize_image_description))
        for generated_index in range(loop_count):
            row = {
                "人设特点": account_link if  renshe_info_inserted is False else None,
                "选题": result.get("xuanti_creation").get("选题") if  xuanti_inserted is False else None,
                "镜头描述（优化前）": image_description[generated_index] if generated_index in range(
                    len(image_description)) else None,
                "镜头描述(优化后)":  optimize_image_description[generated_index] if generated_index in range(
                    len(optimize_image_description)) else None,
                "优化逻辑/理由": optimize_script.get("优化逻辑/理由") if generated_index == 0 else None,
                "镜头统一规划": json.dumps(optimize_script.get("镜头统一规划"), indent=4, ensure_ascii=False) if generated_index == 0 else None,
            }

            xuanti_inserted = True
            renshe_info_inserted = True

            data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'VAQeWH'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
