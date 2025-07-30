import json
import os.path

import image_article_comprehension.aiddit.utils as utils


renshe_json_path = "/image_article_comprehension/aigc_data/renshe/account_陸清禾_5657ba2703eb846a34fcc55b.json"
renshe = json.load(open(
    renshe_json_path,
    "r"))

renshe_xuanti_mode = renshe.get("renshe_xuanti_mode", {})

modes = renshe_xuanti_mode.get("modes", [])

format_modes = []
for m in modes:
    format_mode = {
        "选题模式名称": m.get("选题模式"),
        "选题模式": {
            "选题模式": m.get("选题模式"),
            "选题创作方式": m.get("选题创作方式"),
            "选题模式要点": m.get("选题模式要点"),
            "选题模式灵感": m.get("选题模式灵感")
        },
        "创作脚本": m.get("script").get("modes"),
        "历史优质选题": m.get("历史优质选题"),
    }

    format_modes.append(format_mode)

renshe_xuanti_mode = format_modes

renshe['renshe_xuanti_mode'] = renshe_xuanti_mode
print(json.dumps(renshe, ensure_ascii=False, indent=4))

utils.save(renshe, f"./{os.path.basename(renshe_json_path)}")
