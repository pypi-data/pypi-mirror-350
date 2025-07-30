import json
import os
import aiddit.utils as utils

if __name__ == "__main__":

    path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/script_result_0428"

    path_simple = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/script_result_0428_simple"

    dirs = os.listdir(path)
    print(dirs)

    for d in dirs:

        for script_name in os.listdir(os.path.join(path, d)):

            try:
                script = json.load(open(os.path.join(path, d, script_name), "r"))

                key = next((key for key in script.keys() if "script_generate_result" in key), None)

                utils.save(script.get(key).get("script_with_materials").get("带材料的脚本"), os.path.join(path_simple, d, script_name))
            except Exception as e:
               print(d,script_name)

    pass
