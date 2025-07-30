from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/image_article_comprehension/create/result/image/20250110_春哥边走边画'
data = []

depend_renshe_path = os.path.join(
    "/image_article_comprehension/create/renshe/image",
    os.path.basename(data_dir) + ".json")

all_result = []
for i in [f for f in os.listdir(data_dir) if f.endswith('.json')]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for result in all_result:
    images = [f"\"{i}\"" for i in result.get('reference_note', {}).get('images', [])]

    xuanti_creation_by_note = result.get("xuanti_creation_by_note", {})
    depend_renshe = result.get("renshe", {})
    mj_images = [f"\"{i}\"" for i in xuanti_creation_by_note.get('midjourney_image', [])]

    index = 0
    row = {
        '创作灵魂': f'{json.dumps(depend_renshe.get("renshe_unique_point").get("创作灵魂"), ensure_ascii=False, indent=4)} \n\n\n {depend_renshe.get("account_link", "")}',
        '选题模式': f"{json.dumps(depend_renshe.get('选题模式'), ensure_ascii=False, indent=4)}",
        '选题品类&风格':f"{json.dumps(depend_renshe.get('选题品类'), ensure_ascii=False, indent=4)}",
        '人设方向': f'{json.dumps(result.get("renshe", {}).get("renshe_xuanti_v2",{}).get("base_topic", {}), ensure_ascii=False, indent=4)}',
        '人设要点': json.dumps(result.get("renshe", {}).get("renshe_keypoint_v2", {}), ensure_ascii=False, indent=4),
        '人设要点-结合选题方向': json.dumps(result.get("renshe", {}).get("renshe_keypoint_v4", {}), ensure_ascii=False, indent=4),
        '重要亮点': json.dumps(depend_renshe.get("renshe_unique_point").get("重要亮点"), ensure_ascii=False,
                               indent=4),
        '主要特征': json.dumps(depend_renshe.get("renshe_unique_point").get("主要特征"), ensure_ascii=False,
                               indent=4),
        '优质选题': json.dumps(depend_renshe.get("renshe_unique_point").get("优质选题详情"), ensure_ascii=False,
                               indent=4),
        '刺激源链接': result.get('reference_note', {}).get('link', ''),
        '刺激源': f"[{','.join(images)}]",
        # '刺激源要点': json.dumps(xuanti_creation.get("reference_note_keypoint"), ensure_ascii=False, indent=4),
        # '选题': xuanti_creation.get("xuanti_creation", {}).get("最终的选题"),
        # '选题的详细描述信息': xuanti_creation.get("xuanti_creation", {}).get("选题的详细描述信息"),
        # "选题判断-是否可行": xuanti_creation.get("xuanti_estimate", {}).get("是否是一个好选题", ""),
        # "选题判断-explanation": xuanti_creation.get("xuanti_estimate", {}).get("explanation", ""),
        "人设视角下的选题来源":xuanti_creation_by_note.get("xuanti_creation").get("选题的参考来源") if index == 0 else "",
        "人设视角下选题": xuanti_creation_by_note.get("xuanti_creation").get("最终的选题") if index == 0 else "",
        "人设视角下描述": xuanti_creation_by_note.get("xuanti_creation").get("选题的详细描述信息") if index == 0 else "",
        "人设视角选题判断": xuanti_creation_by_note.get("xuanti_estimate").get("是否是一个好选题") if index == 0 else "",
        "人设视角选题判断-explanation":xuanti_creation_by_note.get("xuanti_estimate").get("explanation") if index == 0 else "",
        '选题依赖的关键信息': json.dumps(xuanti_creation_by_note.get("xuanti_creation", {}).get("选题依赖的关键信息"),
                                         ensure_ascii=False, indent=4),
        "whisk图片生成": xuanti_creation_by_note.get("xuanti_creation", {}).get("whisk_image"),
        "Midjourney图片生成": f"[{','.join(mj_images)}]",
    }
    data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'UeZVqB'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
