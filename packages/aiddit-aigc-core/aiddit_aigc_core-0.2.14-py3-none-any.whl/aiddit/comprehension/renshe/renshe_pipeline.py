import json
import logging
import traceback

from aiddit.xhs.account_note_list import save_account_note
import os
from aiddit.xhs.note_detail import batch_get_note_detail
from tenacity import retry, stop_after_attempt, wait_fixed
from aiddit.comprehension.renshe.renshe_history_note_data_extract import process_note_path, \
    check_note_process_finished
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import aiddit.utils as utils

import aiddit.comprehension.renshe.renshe_summary_0218 as renshe_info_summary

output_dir = "/image_article_comprehension/aigc_data"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def account_crawler(account_id, account_name):
    save_note_dir = f"{output_dir}/note_data/account_{account_name}_{account_id}"
    if os.path.exists(save_note_dir) and len(os.listdir(save_note_dir)) > 20:
        return save_note_dir

    try:
        save_account_note(account_id, account_name, save_note_dir)
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Error in save_account_note: {e}")
        raise
    return save_note_dir


@retry(stop=stop_after_attempt(10), wait=wait_fixed(10))
def account_note_crawler(note_dir):
    cached_cnt, total_cnt, success_cnt = batch_get_note_detail(note_dir)

    if cached_cnt + success_cnt < total_cnt:
        raise Exception(
            f"batch_get_note_detail failed, cached_cnt={cached_cnt}, total_cnt={total_cnt}, success_cnt={success_cnt}")
    pass


@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def process_note(note_dir, account_id, account_name):
    output_dir = f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/note_data_comprehension/account_{account_name}_{account_id}"

    note_list_dir = os.listdir(note_dir)
    target_note_dir = [os.path.join(note_dir, i) for i in note_list_dir][:30]

    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(lambda note_path: process_note_path(note_path, output_dir), target_note_dir),
                  total=len(target_note_dir), desc="帖子所有理解"))

    process_note_completed = True

    for note in target_note_dir:
        finished = check_note_process_finished(note, output_dir)
        if not finished:
            logging.error(f"{note} not finished")
            process_note_completed = False
            break

    if process_note_completed:
        logging.error(f"All notes have been processed , {output_dir}")
        return output_dir
    else:
        raise Exception(f"process_note not completed")


def prepare_account_note_data(account_id, account_name):
    note_dir = account_crawler(account_id, account_name)
    account_note_crawler(note_dir)

    # Delete video notes
    for note in [json.load(open(os.path.join(note_dir, i), "r")) for i in os.listdir(note_dir) if i.endswith(".json")]:
        if note.get("content_type") == "video":
            utils.delete_file(os.path.join(note_dir, f"{note.get('channel_content_id')}.json"))
    return note_dir


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def renshe_summary(comprehension_note_dir, renshe_info_output_dir, account_id):
    try:
        save_output_path = renshe_info_summary.renshe_info_summary(comprehension_note_dir, renshe_info_output_dir,
                                                                   account_id)
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Error in save_account_note: {e}")
        raise


if __name__ == "__main__":
    renshe_info_output_dir = "/image_article_comprehension/aigc_data/renshe_0319"
    account_id = "649da24b000000002b0081a1"
    account_name = "山木木简笔画"
    note_dir = prepare_account_note_data(account_id, account_name)

    comprehension_note_dir = process_note(note_dir, account_id, account_name)
    #
    renshe_summary(comprehension_note_dir, renshe_info_output_dir, account_id)
    #
    logging.error("process all finished!")
    pass
