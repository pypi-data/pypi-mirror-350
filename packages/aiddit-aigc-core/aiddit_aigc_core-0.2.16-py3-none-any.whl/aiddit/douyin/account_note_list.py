import logging

import requests
import json
import os
from tenacity import retry, stop_after_attempt, wait_fixed
from aiddit.tools.oss_upload import upload_oss
from aiddit.model.gemini_upload_file import handle_file_path
import uuid
import aiddit.utils as utils
import concurrent.futures
from typing import List, Dict


def save_account_note(account_id, save_dir):
    # dir_name = f"account_{account_name}_{account_id}"
    # dir = f"{save_dir}/{dir_name}"
    os.makedirs(save_dir, exist_ok=True)

    url = "http://crawler.aiddit.com/crawler/dou_yin/blogger"
    payload = json.dumps({
        "account_id": account_id,
        "cursor": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    data = json.loads(response.text)["data"]['data']

    if data is None or len(data) == 0:
        raise Exception(f"no data for account_id {account_id} , {response.text}")

    for d in data:
        channel_content_id = d.get("aweme_id")

        file_name = f"{channel_content_id}.json"

        note_info = {
            "channel_content_id": channel_content_id,
            "desc": d.get("desc"),
            "create_time": d.get("create_time"),
            "origin_video_url": d.get("video", {}).get("play_addr", {}).get("url_list", [])[0],
            "link": f"https://www.douyin.com/video/{channel_content_id}"
        }

        if os.path.exists(f"{save_dir}/{file_name}") is True:
            print(f"file exists {file_name}")
            continue

        with open(os.path.join(save_dir, file_name), 'a') as f:
            f.write(json.dumps(note_info, ensure_ascii=False, indent=4))

    do_upload_note_video_2_oss(save_dir)
    return dir


def do_upload_note_video_2_oss(note_dir_path):
    note_list = [json.load(open(os.path.join(note_dir_path, i), "r")) for i in os.listdir(note_dir_path) if
                 i.endswith(".json")]

    total_count = len(note_list)
    def process_note(note: Dict, index: int = None) -> None:
        origin_video_url = note.get("origin_video_url")
        if origin_video_url and note.get("video_url") is None:
            note["video_url"] = upload_video_2_oss(origin_video_url)
            utils.save(note, os.path.join(note_dir_path, f"{note['channel_content_id']}.json"))
        else:
            print("--")

        print(f"upload_video_2_oss {note.get('channel_content_id')}.json, success {index + 1} of {total_count} , {note.get('video_url')}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # executor.map(lambda  x: process_note(x), note_list)
        futures = [executor.submit(process_note, note, idx) for idx, note in enumerate(note_list)]
        concurrent.futures.wait(futures)

def upload_video_2_oss(video_url):
    video_name = f"{uuid.uuid4().int}.mp4"
    local_path = handle_file_path(video_url, video_name)
    key = f"aigc_creation/douyin/video/{video_name}"
    oss_url = upload_oss(key, local_path)
    print(f"upload_video_2_oss {video_url} to {oss_url}")
    return oss_url


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_account_info(account_id):
    url = "http://crawler.aiddit.com/crawler/dou_yin/account_info"

    payload = json.dumps({
        "account_id": account_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    data = json.loads(response.text).get("data", {}).get("data")

    if data is None:
        raise Exception(f"no data for account_id {account_id} , {response.text}")

    return {
        "account_name": data.get("account_name"),
        "description": data.get("description"),
        "avatar_url": data.get("avatar_url"),
        "account_id": account_id,
        "account_link": data.get("account_link"),
    }


if __name__ == '__main__':
    account_id = "MS4wLjABAAAAS3pOM-LyGmbfLKmpgKsiobmZUw9uHP5irTeVePR-y96YEwJyCuto3jBW5navVv4o"

    # r= upload_video_2_oss(
    #     "https://v5-dy-o-abtest.zjcdn.com/22d2baeb8caeba77d6d10579b061e8bf/67ebc2bf/video/tos/cn/tos-cn-ve-15/oc0wCE15PtRTAQiHi5tIZY1gIPAZBQcs9nS4N/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1271&bt=1271&cs=0&ds=4&ft=l1GzaFA-VVyw3pRf5Xg5wNO5fnAZ60iXSm3dmUMyeF~4&mime_type=video_mp4&qs=0&rc=aWQ7NDY8NjY8ZDc7aWY0ZUBpMzV5d3M5cms0dzMzNGkzM0AvXzYyXzVgNTUxYzFiM18uYSNwZmBgMmQ0bGBgLS1kLTBzcw%3D%3D&btag=80000e00028000&cc=46&cquery=100B_100x_100z_100o_101r&dy_q=1743493140&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=202504011538594753482B8CD8C402561D&req_cdn_type=")
    # print(r)
    save_account_note(account_id,"/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/douyin/result/丁公子")
    # print(json.dumps(get_account_info(account_id), ensure_ascii=False, indent=4))
