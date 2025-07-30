from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data = []
name = "星有野"
data_dir = f'/Users/nieqi/Documents/workspace/python/image_article_comprehension/video/data/xuanti/{name}'
renshe = json.load(
    open(f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/video/data/renshe/{name}.json", "r"))

all_result = []
for i in os.listdir(data_dir):
    all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))

fail_list = []
for index, result in enumerate(all_result):
    try:
        print(result.get("reference_note").get("channel_content_id"))
        dr = result.get("帖子亮点选题结果_deepseek_r3", {})
        xuan_result_list = result.get("帖子亮点选题结果_deepseek_r3", {}).get("选题结果", [])
        for i, xuanti_result in enumerate(xuan_result_list):
            row = {
                "创作灵魂": json.dumps(renshe.get("创作灵魂"), ensure_ascii=False, indent=4),
                "内容分类": json.dumps(renshe.get("内容品类"), ensure_ascii=False, indent=4),
                "重要亮点": json.dumps(renshe.get("重要亮点"), ensure_ascii=False, indent=4),
                "创作特点": json.dumps(renshe.get("创作特点"), ensure_ascii=False, indent=4),
                "选题特点": json.dumps(renshe.get("选题特点"), ensure_ascii=False, indent=4),
                "选题禁忌": json.dumps(renshe.get("选题禁忌"), ensure_ascii=False, indent=4),
                "选题必要点": json.dumps(renshe.get("选题必要点"), ensure_ascii=False, indent=4),
                "选题模式JSON": json.dumps(renshe.get("选题模式"), ensure_ascii=False, indent=4),

                "刺激源": result.get("reference_note").get("content_link") if i == 0 else None,
                "刺激源亮点": json.dumps(dr.get("亮点"), ensure_ascii=False,
                                         indent=4) if i == 0 else None,
                "推理过程": dr.get("推理过程") if i == 0 else None,
                "选题模式": xuanti_result.get("参考的选题模式"),
                "能否产生选题": xuanti_result.get("能否产生选题"),
                "不能产生选题的原因": xuanti_result.get("不能产生选题的原因") if xuanti_result.get(
                    "不能产生选题的原因") is not None else None,
                "最终的选题": xuanti_result.get("最终的选题"),
                "选题的详细描述信息": xuanti_result.get("选题的详细描述信息"),
                "选题的参考来源": xuanti_result.get("选题的参考来源"),
                "选题依赖的关键信息": json.dumps(xuanti_result.get("选题依赖的关键信息"), ensure_ascii=False,
                                                 indent=4) if xuanti_result.get(
                    "选题依赖的关键信息") is not None else None,

            }
            data.append(row)
    except Exception as e:
        print(f"Error in {index} , {str(e)}")
        fail_list.append(result.get("reference_note").get("channel_content_id"))
        continue

    # Convert DataFrame to list with header
    df = pd.DataFrame(data)
    header = df.columns.tolist()
    data_rows = df.values.tolist()
    data_with_header = [header] + data_rows

    sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
    sheet_id = 'zyaCfV'

    write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                        sheetid=sheet_id, )

    print(fail_list)
