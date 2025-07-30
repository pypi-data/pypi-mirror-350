import os.path
import aiddit.utils as utils
import json
import aiddit.comprehension.renshe.renshe_summary_prompt_0218 as renshe_summary_prompt_0218
import aiddit.xhs.account_note_list as account_note_list


def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


def renshe_info_summary(comprehension_note_dir_path, save_result_dir_path, account_id=None):
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

    if account_id is not None and save_output.get("account_info") is None:
        account_info = account_note_list.get_account_info(account_id)
        save_output["account_info"] = account_info
        save(save_output, save_output_path)

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

    for note in note_list:
        xuanti = note.get("xuanti_result", {}).get("内容选题")
        xuanti_description = note.get("xuanti_result", {}).get("内容选题描述")

        note_summary = {
            "帖子id": note.get("note_info").get("channel_content_id"),
            "帖子选题": xuanti,
            "帖子选题描述": xuanti_description,
            "内容亮点": note.get("key_point", [])
        }

        note_summary_list.append(note_summary)

    if save_output.get("renshe_xuanti_unique") is None:
        ans = renshe_summary_prompt_0218.renshe_unique(note_summary_list)
        print(ans)
        save_output["renshe_xuanti_unique"] = json.loads(ans)
        save(save_output, save_output_path)

    renshe_xuanti_unique = save_output.get("renshe_xuanti_unique")
    if renshe_xuanti_unique is not None and save_output.get("renshe_xuanti_mode") is None:
        ans = renshe_summary_prompt_0218.renshe_xuanti_mode(renshe_xuanti_unique, note_summary_list)
        save_output["renshe_xuanti_mode"] = utils.try_remove_markdown_tag_and_to_json(ans)
        save(save_output, save_output_path)
        print(ans)

    if save_output.get("script_mode") is None:
        ans = renshe_summary_prompt_0218.script_summary(note_list)
        save_output["script_mode"] = utils.try_remove_markdown_tag_and_to_json(ans)
        save(save_output, save_output_path)
    #
    # if save_output.get("renshe_constants") is None:
    #     sampling_note_list = [i.get("note_info") for i in note_list][:15]
    #     ans = renshe_materials_summary.extract_renshe_constant(save_output.get("account_info"), sampling_note_list,
    #                                                            None)
    #     save_output["renshe_constants"] = utils.try_remove_markdown_tag_and_to_json(ans)
    #     save(save_output, save_output_path)

    return save_output_path


if __name__ == "__main__":
    dir_path = "/image_article_comprehension/aigc_data/note_data_comprehension/account_陸清禾_5657ba2703eb846a34fcc55b"
    # dir_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/20250110_摸鱼阿希"
    save_result_path = "/image_article_comprehension/aigc_data/renshe_0228"
    save_file_path = renshe_info_summary(dir_path, save_result_path)

    # result = json.load(open(save_file_path, 'r'))
    # note_data = []
    #
    # for comprehension_note in [json.load(open(os.path.join(dir_path, d), "r")) for d in os.listdir(dir_path) if d.endswith('.json')]:
    #     note_info = comprehension_note.get("note_info")
    #     note_info["选题"] = comprehension_note.get("xuanti_result", {}).get("内容选题")
    #     note_data.append(note_info)
    #
    # result["note_data"] = note_data
    # save(result, save_file_path)
