from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/aiddit/create/result/script/20250109_脆肚火锅噗噜噗噜'

all_result = []
for i in [f for f in os.listdir(data_dir) if f.endswith('.json')]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

data = []

for result in all_result:
    script = result.get("generated_script")

    images = [script.get("图片").get("封面图")] + script.get("图片").get("图集")

    depend_renshe = result.get("xuanti").get("renshe")

    index = 0

    xuanti_mode_name = result.get("xuanti").get("xuanti").get("xuanti_mode")
    xuanti_mode = next((
        item for item in depend_renshe.get("renshe_xuanti_mode", {}).get("modes", []) \
        if item.get("选题模式") == xuanti_mode_name), None)

    for image in images:
        print(image)
        mj_images = [f"\"{i}\"" for i in image.get('mid_journey', [])]
        row = {
            '创作灵魂': f'{json.dumps(depend_renshe.get("renshe_xuanti_unique").get("创作灵魂"), ensure_ascii=False, indent=4)} \n\n\n {depend_renshe.get("account_link", "")}',
            '内容品类': f'{json.dumps(depend_renshe.get("renshe_xuanti_unique").get("内容品类"), ensure_ascii=False, indent=4)}',
            '选题必要点': f'{json.dumps(depend_renshe.get("renshe_xuanti_unique").get("选题必要点"), ensure_ascii=False, indent=4)}',

            '选题模式': xuanti_mode_name if index == 0 else None,
            '产生的选题': result.get("xuanti").get("xuanti").get("xuanti_creation").get(
                "最终的选题") if index == 0 else None,
            '产生的选题描述': result.get("xuanti").get("xuanti").get("xuanti_creation").get(
                "选题的详细描述信息") if index == 0 else None,
            '选题依赖的关键信息': json.dumps(
                result.get("xuanti").get("xuanti").get("xuanti_creation").get("选题依赖的关键信息"),
                ensure_ascii=False, indent=4) if index == 0 else None,

            '脚本模式': json.dumps(next(iter(xuanti_mode.get("script", {}).get("modes", [])), None), ensure_ascii=False,
                                   indent=4) if index == 0 else None,

            '标题': f"{script.get('标题').get('标题结果')}" if index == 0 else None,
            '标题内容': f"{json.dumps(script.get('标题'), ensure_ascii=False, indent=4)}" if index == 0 else None,

            '正文': f"{script.get('正文内容').get('正文内容结果')}" if index == 0 else None,
            '正文内容': f"{json.dumps(script.get('正文内容'), ensure_ascii=False, indent=4)}" if index == 0 else None,

            '图片通用信息': json.dumps(script.get("图片").get("图片通用信息"), ensure_ascii=False, indent=4) if index == 0 else None,
            '图片描述': image.get("图片描述"),
            "图片内容": json.dumps(image, ensure_ascii=False, indent=4),

            'midjourney': f"[{','.join(mj_images)}]",
            "whisk": image.get("whisk_images"),
        }
        data.append(row)
        index += 1

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = '5R9w7u'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, start_row=3)
