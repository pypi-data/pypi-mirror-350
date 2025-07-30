from tenacity import retry, stop_after_attempt, wait_fixed
import os
from dotenv import load_dotenv

load_dotenv()
import aiddit.xhs.account_note_list as account_note_list
import aiddit.xhs.note_detail as note_detail
import aiddit.utils as utils
import json

xhs_cache_dir = os.getenv("xhs_cache_dir")


def _get_xhs_account_info(xhs_user_id) -> dict:
    if xhs_cache_dir is None:
        raise Exception("小红书缓存文件夹不存在，请配置环境变量xhs_cache_dir")

    xhs_cache_account_info = os.path.join(xhs_cache_dir, "account_info")

    account_user_info_path = os.path.join(xhs_cache_account_info, f"{xhs_user_id}.json")
    if not os.path.exists(account_user_info_path):
        try:
            account_info = account_note_list.get_account_info(xhs_user_id)
            utils.save(account_info, account_user_info_path)
        except Exception as e:
            raise Exception(f"获取{xhs_user_id}的账号信息失败, {str(e)}")

    account_info = json.load(open(account_user_info_path, "r"))

    return account_info


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def _get_xhs_account_note_list(xhs_user_id) -> str:
    account_info = _get_xhs_account_info(xhs_user_id)

    account_name = account_info.get("account_name")

    if account_name is None:
        raise Exception(
            f"获取小红书用户ID： {xhs_user_id} 的账号名称失败 \n{json.dumps(account_info, ensure_ascii=False, indent=4)}")

    account_note_save_path = os.path.join(xhs_cache_dir, "account_note", account_name)

    if not os.path.exists(account_note_save_path) or len(os.listdir(account_note_save_path)) < 5:
        try:
            # 获取小红书主页帖子列表
            account_note_list.save_account_note(xhs_user_id, account_name, account_note_save_path)
            # 依次请求主页帖子详情（转存图片至oss，方便后续通过oss图片resize）
            note_detail.batch_get_note_detail_with_retries(account_note_save_path)
        except Exception as e:
            raise e

    # 删除没有图片（没有获取到详情的）的帖子
    if os.path.exists(account_note_save_path):
        note_file_name_list = [i for i in os.listdir(account_note_save_path) if i.endswith(".json")]
        for note_file_name in note_file_name_list:
            note = json.load(open(os.path.join(account_note_save_path, note_file_name), "r"))
            if len(note.get("images", [])) == 0:
                print(f"{os.path.join(account_note_save_path, note_file_name)} 没有图片，删除")
                utils.delete_file(os.path.join(account_note_save_path, note_file_name))

    if len(os.listdir(account_note_save_path)) < 5:
        raise Exception(f"获取小红书用户ID： {xhs_user_id} 的帖子列表失败，帖子数量不足")

    return account_note_save_path


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def _get_note_detail_by_id(note_id):
    note_save_dir = os.path.join(xhs_cache_dir, "note_detail")
    note_save_path = os.path.join(note_save_dir, f"{note_id}.json")

    if os.path.exists(note_save_path):
        note_info = json.load(open(note_save_path, "r"))
        if note_info.get("images", None) is not None:
            print(f"{note_id} has cache")
            return note_info

    note_detail.single_detail("https://www.xiaohongshu.com/explore/" + note_id, note_save_dir)

    return json.load(open(note_save_path, "r"))


if __name__ == "__main__":
    note_info = _get_note_detail_by_id("6822c53c000000002301778e")
    print(note_info)
