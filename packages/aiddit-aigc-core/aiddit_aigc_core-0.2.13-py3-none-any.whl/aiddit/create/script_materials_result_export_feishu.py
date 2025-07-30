import sys

sys.path.append("/Users/nieqi/Documents/workspace/python")
from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import aiddit.utils as utils
from aiddit.model.google_genai import  gemini_upload_file

# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/materials'
data = []

script_data_list = [i for i in os.listdir(data_dir) if i.startswith("materials_") and i.endswith(".json")]

all_result = []
for i in script_data_list:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

script_inserted = False
for r_index, result in enumerate(all_result):

    script = result.get("script").get("script").get("创作的脚本").get("图集描述")

    script_materials = result.get("script_materials")

    for index, r in enumerate(script_materials):

        for source_index, source in enumerate(r.get("材料来源")):
            material_image = utils.x_oss_process_format_jpeg(source.get("image"))

            if material_image is not None:
                print(material_image)
                material_image = gemini_upload_file.handle_file_path(material_image)
                print(utils.get_file_uri(material_image))

            source_note_type = "历史帖子"
            if r.get("search_keyword") is not None:
                source_note_type = "搜索关键词："+ r.get("search_keyword")
            else:
                source_note_type = "历史帖子/搜索同题帖子"

            row = {
                "脚本": json.dumps(script, ensure_ascii=False, indent=4) if not script_inserted else None,
                "材料名": r.get("材料名") if source_index == 0 else None,
                "材料类型": r.get("材料类型") if source_index == 0 else None,
                "材料描述": r.get("材料描述") if source_index == 0 else None,
                "材料图片来源帖子类型": source_note_type if source_index == 0 else None,
                "材料图片": utils.get_file_uri(material_image)
            }
            data.append(row)
            script_inserted = True

    script_inserted = False

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'N4MOVY'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
