from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import traceback

directory = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result'
json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

json_files = ["20250110_摸鱼阿希_0125.json",
              "20250109_每天一点心理学_claude35.json"]
data = []

for json_file in json_files:
    r = json.load(open(os.path.join(directory, json_file), 'r'))
    try:
        renshe_xuanti_unique = r.get("renshe_xuanti_unique", {})
        for i, mode in enumerate(r.get("renshe_xuanti_mode", {}).get("modes", [])):
            script = mode.get("script").get("modes",[])[0]
            row = {
                '个人主页链接': f"{json_file.split('_')[1].split('.')[0]} \n\n{r.get('account_link', '')}" if i == 0 else "",
                "创作灵魂": json.dumps(renshe_xuanti_unique.get("创作灵魂", []), ensure_ascii=False,
                                       indent=4) if i == 0 else "",
                "内容品类": json.dumps(renshe_xuanti_unique.get("内容品类", []), ensure_ascii=False,
                                       indent=4) if i == 0 else "",
                "选题必要点": json.dumps(renshe_xuanti_unique.get("选题必要点", []), ensure_ascii=False,
                                         indent=4) if i == 0 else "",
                "脚本模式必要点":"",

                "选题模式": mode.get("选题模式", ""),
                "选题创作方式": mode.get("选题创作方式", ""),
                "选题模式要点": json.dumps(mode.get("选题模式要点", {}), ensure_ascii=False, indent=4),
                "选题模式灵感": json.dumps(mode.get("选题模式灵感", {}), ensure_ascii=False, indent=4),
                "历史优质选题": json.dumps(mode.get("历史优质选题", []), ensure_ascii=False, indent=4),
                "历史优质选题的亮点": json.dumps(mode.get("历史优质选题的亮点", {}), ensure_ascii=False, indent=4),

                "脚本模式名": script.get("创作脚本模式名"),
                "创作脚本模式的特点": json.dumps(script.get("创作脚本模式的特点"), ensure_ascii=False, indent=4),
                "整体规划": json.dumps(script.get("创作脚本模式详情").get("整体规划"), ensure_ascii=False, indent=4),
                "标题": json.dumps(script.get("创作脚本模式详情").get("标题"), ensure_ascii=False, indent=4),
                "正文": json.dumps(script.get("创作脚本模式详情").get("正文"), ensure_ascii=False, indent=4),
                "图片": json.dumps(script.get("创作脚本模式详情").get("图片"), ensure_ascii=False, indent=4)
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
sheet_id = 'tFGZjv'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, skip_images=False, start_row=1)
