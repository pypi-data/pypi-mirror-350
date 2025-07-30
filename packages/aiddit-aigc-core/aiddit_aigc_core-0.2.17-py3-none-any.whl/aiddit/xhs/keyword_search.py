import os
import requests
import json
import traceback
import time
import aiddit.utils as utils
import aiddit.xhs.note_detail as xhs_detail
from tenacity import retry, stop_after_attempt, wait_fixed
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

search_max_count = 5

xhs_search_result_dir = os.getenv("xhs_search_result_dir")

def _search(keyword, retry_cnt=0):
    print(f"search keyword {keyword}")

    url = "http://crawler.aiddit.com/crawler/xiao_hong_shu/keyword"

    payload = json.dumps({
        "keyword": keyword,
        "content_type": "图文",
        "sort_type": "最热",
        "cursor": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        search_response = json.loads(response.text)
        if search_response.get("code") != 0:
            if retry_cnt < search_max_count:
                time.sleep(2)
                print(f"retry search {keyword} sleep 2s ... ， {search_response}")
                return _search(keyword, retry_cnt + 1)
            else:
                raise Exception(
                    f"Failed to search keyword {keyword} , code = {search_response.get('code')} , {response.text} , reach max retry count {search_max_count}")

        return search_response.get("data").get("data")
    else:
        raise Exception(f"Failed to get note detail {keyword} , http status code = {response.status_code}")


def convert_to_note_data(search_note_data):
    # print(json.dumps(search_note_data, ensure_ascii=False, indent=4))
    if search_note_data.get("model_type") != "note":
        return None
    images = []
    for img in search_note_data.get('note_card', {}).get('image_list', []):
        images.append(img.get("image_url"))

    return {
        "channel_content_id": search_note_data.get("id", ""),
        "link": f"https://www.xiaohongshu.com/explore/{search_note_data.get('id')}?xsec_token={search_note_data.get('xsec_token', '')}",
        "xsec_token": search_note_data.get('xsec_token', ''),
        "comment_count": None,
        "images": images,
        "like_count": search_note_data.get('note_card', {}).get('interact_info', {}).get('liked_count', 0),
        "body_text": "",
        "title": search_note_data.get('note_card', {}).get('display_title', ""),
        "collect_count": None,
        "user": search_note_data.get("note_card", {}).get("user", {})
    }

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def key_word_search_without_oss_save(keyword):
    if keyword is None or keyword == "":
        raise Exception("keyword is None or empty")

    if xhs_search_result_dir is None:
        raise Exception("xhs_search_result_dir is None , please config env xhs_search_result_dir")

    if not os.path.exists(xhs_search_result_dir):
        os.makedirs(xhs_search_result_dir)

    keyword_search_dir = os.path.join(xhs_search_result_dir, keyword)
    if not os.path.exists(keyword_search_dir) or len(os.listdir(keyword_search_dir)) == 0:
        search_result = _search(keyword)
        print(f"search {keyword} success ,  result count {len(search_result)} , save_path = {keyword_search_dir}")
        os.makedirs(keyword_search_dir, exist_ok=True)
        try:
            for sn in search_result:
                r = convert_to_note_data(sn)
                if r is not None:
                    utils.save(r, os.path.join(keyword_search_dir, f"{r.get('channel_content_id')}.json"))
        except Exception as e:
            os.remove(keyword_search_dir)
            traceback.print_exc()
            print(str(e))
            raise e

    search_notes = [json.load(open(os.path.join(keyword_search_dir, i))) for i in os.listdir(keyword_search_dir) if
                    i.endswith(".json")]

    return keyword_search_dir


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def key_word_search(keyword, min_required_search_count=15):
    if keyword is None or keyword == "":
        raise Exception("keyword is None or empty")

    if xhs_search_result_dir is None:
        raise Exception("xhs_search_result_dir is None , please config env xhs_search_result_dir")

    if not os.path.exists(xhs_search_result_dir):
        os.makedirs(xhs_search_result_dir)

    keyword_search_dir = os.path.join(xhs_search_result_dir, keyword)
    if not os.path.exists(keyword_search_dir) or len(os.listdir(keyword_search_dir)) == 0:
        search_result = _search(keyword)
        print(f"search success ,  result count {len(search_result)}")
        os.makedirs(keyword_search_dir, exist_ok=True)
        try:
            for sn in search_result:
                r = convert_to_note_data(sn)
                if r is not None:
                    utils.save(r, os.path.join(keyword_search_dir, f"{r.get('channel_content_id')}.json"))
        except Exception as e:
            os.remove(keyword_search_dir)
            traceback.print_exc()
            print(str(e))
            raise e

    search_notes = [json.load(open(os.path.join(keyword_search_dir, i))) for i in os.listdir(keyword_search_dir) if
                    i.endswith(".json")]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_detail, i, keyword_search_dir) for i in search_notes]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                traceback.print_exc()
                print(f"get detail failed, {str(e)}")

    detail_failure_cnt = 0
    search_total_count = len(search_notes)
    for i in search_notes:
        if any("res.cybertogether.net" in images_url for images_url in i.get("images")) is False:
            detail_failure_cnt += 1

    min_required_search_count = min(search_total_count, min_required_search_count)
    print(f"search {keyword} success , detail_failure_cnt {detail_failure_cnt} , search_total_count {search_total_count}")
    if search_total_count - detail_failure_cnt >= min_required_search_count:
        # 删除keyword_search_dir 目录下的文件
        for i in search_notes:
            if any("res.cybertogether.net" in images_url for images_url in i.get("images")) is False:
                print(f"获取详情失败，删除 {i.get('channel_content_id')}")
                os.remove(os.path.join(keyword_search_dir, f"{i.get('channel_content_id')}.json"))
        return keyword_search_dir
    else:
        raise Exception(f"search {keyword} result count {search_total_count} , detail failure count {detail_failure_cnt} , success less than {min_required_search_count}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_detail(search_note, dir):
    if any("res.cybertogether.net" in images_url for images_url in search_note.get("images")):
        print(f"{search_note.get('channel_content_id')}, {search_note.get('title')} has detail , skip")
        return

    note_detail = xhs_detail.get_note_detail(search_note.get("link").split("?")[0])

    search_note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                             note_detail.get("image_url_list", [])]
    search_note["like_count"] = note_detail.get("like_count")
    search_note["body_text"] = note_detail.get("body_text")
    search_note["collect_count"] = note_detail.get("collect_count")
    search_note["link"] = note_detail.get("content_link")

    note_save_path = os.path.join(dir, f"{search_note.get('channel_content_id')}.json")

    utils.save(search_note, note_save_path)
    print(f"save {search_note.get('channel_content_id')} , {search_note.get('title')} detail to success")


if __name__ == "__main__":
    # search("猫咪特写摄影")
    # save_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note/image_search_中医食疗方案"
    # search_notes = search("中医食疗方案")
    # for search_note in search_notes:
    #     n = convert_to_note_data(search_note)
    #     utils.save(n, os.path.join(save_dir, f"{n.get('channel_content_id')}.json"))

    key_word_search_without_oss_save("hhhhh")
    pass
