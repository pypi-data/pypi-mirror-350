from dashvector.pins.pins_api import search as pins_search
import os
import json
import traceback
from urllib.parse import quote
from tqdm import tqdm

dir = "/image_article_comprehension/comprehension/result/xuanti_result_v5_烟熏妆容"

for i in tqdm(os.listdir(dir)):
    try:
        # print(f"{i}")
        path = os.path.join(dir, i)
        n = json.load(open(path, 'r'))
        if n.get("xuanti_result") is None:
            continue

        if n.get("xuanti_pins_search") is not None:
            continue

        xt_description = n["xuanti_result"]["关键点"]
        n["xuanti_pins_search"] = pins_search(xt_description)

        n["xuanti_pins_search_link"] = f"https://www.pinterest.com/search/pins/?q={quote(xt_description)}&rs=typed"

        with open(path, 'w') as f:
            json.dump(n, f, ensure_ascii=False, indent=4)

    except Exception as e:
        error = traceback.format_exc()
        print(error)
