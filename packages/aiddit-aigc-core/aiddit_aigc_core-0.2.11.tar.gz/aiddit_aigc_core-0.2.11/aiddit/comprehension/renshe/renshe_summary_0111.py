import os.path
import traceback
from image_article_comprehension.aiddit.xhs import get_note_detail
from image_article_comprehension.aiddit.comprehension.renshe.renshe_prompt_0111 import renshe_unique, renshe_mode
from image_article_comprehension.aiddit.comprehension.renshe.note_script_prompt import prompt_script_summary, \
    prompt_script_summary_0213
import image_article_comprehension.aiddit.utils as utils
import json


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


def renshe_info_summary(comprehension_note_dir_path, save_result_dir_path):
    list_dir = os.listdir(comprehension_note_dir_path)

    target_note_dir = [os.path.join(comprehension_note_dir_path, i) for i in list_dir][:30]

    if os.path.exists(save_result_dir_path) is not True:
        os.makedirs(save_result_dir_path)

    save_output_path = os.path.join(save_result_dir_path, os.path.basename(comprehension_note_dir_path) + ".json")
    if os.path.exists(save_output_path) is not True:
        save_output = {
            "comprehension_note_path": comprehension_note_dir_path
        }
        save(save_output, save_output_path)
    else:
        save_output = json.load(open(save_output_path, 'r'))

    # 单个帖子的理解的选题 & 要点
    note_summary_list = []

    for v in target_note_dir:
        try:
            json.load(open(v, 'r'))
        except Exception as e:
            print(f"file {v} error {str}")
            continue

    note_list = [json.load(open(v, 'r')) for v in target_note_dir]

    if len(note_list) == 0:
        raise Exception("note_list is empty")

    # 获取个人主页链接
    if save_output.get("account_link") is None:
        try:
            user_id = note_list[0].get("note_info", {}).get("user_id", "")
            if user_id == "":
                user_id = get_note_detail(note_list[0].get("note_info", {}).get("link", "")).get("channel_account_id")
            account_link = "https://www.xiaohongshu.com/user/profile/" + user_id
            save_output["account_link"] = account_link
            save(save_output, save_output_path)
        except:
            traceback.print_exc()

    note_id_map = {item.get("note_info", {}).get("channel_content_id", ""): item for item in note_list}

    for note in note_list:
        note_id = note.get("note_info", {}).get("channel_content_id", "")
        print(note_id)
        xuanti = note.get("xuanti_result", {}).get("内容选题")
        xuanti_description = note.get("xuanti_result", {}).get("内容选题描述")

        note_summary = {
            "帖子id": note_id,
            "帖子选题": xuanti,
            "帖子选题描述": xuanti_description,
        }

        for kp in note.get('key_point', []):
            units = kp.get('亮点组成')
            if units.get('image_index') is not None:
                del units['image_index']
            v = f"""亮点:{kp.get('亮点')}\n亮点组成:{json.dumps(units, ensure_ascii=False)}"""
            note_summary["帖子亮点"] = kp.get('亮点')
            note_summary["帖子亮点组成"] = units

        note_summary_list.append(note_summary)

    if save_output.get("renshe_xuanti_unique") is None:
        ans = renshe_unique(note_summary_list)
        print(ans)
        save_output["renshe_xuanti_unique"] = json.loads(ans)
        save(save_output, save_output_path)

    renshe_xuanti_unique = save_output.get("renshe_xuanti_unique")
    if renshe_xuanti_unique is not None and save_output.get("renshe_xuanti_mode") is None:
        ans = renshe_mode(renshe_xuanti_unique, note_summary_list)
        save_output["renshe_xuanti_mode"] = json.loads(ans)
        save(save_output, save_output_path)
        print(ans)

    renshe_xuanti_mode = save_output.get("renshe_xuanti_mode", {})
    if renshe_xuanti_unique is not None and renshe_xuanti_mode is not None:
        for mode in renshe_xuanti_mode.get("modes", []):
            if mode.get("script") is not None:
                continue

            mode_note_list = [note_id_map.get(note_id) for note_id in mode.get("符合选题模式的所有内容id", []) if
                              note_id_map.get(note_id) is not None]

            if len(mode_note_list) == 0:
                print(f"mode_note_list is empty: {mode}")
                continue
            ans = prompt_script_summary(renshe_xuanti_unique, mode_note_list, mode)
            print(ans)

            mode["script"] = json.loads(ans)
            save(save_output, save_output_path)

    return save_output_path


if __name__ == "__main__":
    # dir_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250110_摸鱼阿希_claude35"
    # save_result_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result"
    #
    # renshe_info_summary(dir_path, save_result_path)

    dir_path_list = [
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_陸清禾_5657ba2703eb846a34fcc55b",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250109_每天一点心理学_claude35",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250110_摸鱼阿希_claude35",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250109_脆肚火锅噗噜噗噜_claude35",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_Isisruirr-_5f48c8540000000001004329",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_mmmmmm_53c4222ab4c4d63304f8b3ed",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_山越记_5a492e234eacab66bd2a3f8d",
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_李尾鱼_615657520000000002026e7c"
    ]

    dir_path_list = [
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250109_每天一点心理学_0219"
    ]

    save_dir = "/image_article_comprehension/aiddit/comprehension/renshe/result/renshe_script_0213"

    for dir_path in dir_path_list:
        save_result_path = os.path.join(save_dir, os.path.basename(dir_path) + ".json")
        # if os.path.exists(save_result_path):
        #     continue

        note_data = [json.load(open(os.path.join(dir_path, i), "r")) for i in os.listdir(dir_path) if
                     i.endswith(".json")]

        note_link = note_data[0].get("note_info").get("link")
        ans = prompt_script_summary_0213(note_data)

        result = {
            "脚本模式": utils.try_remove_markdown_tag_and_to_json(ans),
            "帖子": note_link
        }

        utils.save(result, save_result_path)
