import os.path

import requests
import json
import aiddit.utils as utils
import traceback
from tqdm import tqdm


def get_account_note_data(account_id):
    url = "http://crawler.aiddit.com/crawler/dou_yin/blogger"

    payload = json.dumps({
        "account_id": account_id,
        "cursor": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"response status code: {response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for account {account_id}, status code: {response.status_code}")

    response_data = json.loads(response.text)

    if response_data.get("code", -1) != 0:
        raise Exception(f"Failed to fetch data for account {account_id}, code: {response_data.get('code')}")

    data = response_data.get("data").get("data")

    author_name = data[0].get("author", {}).get("nickname")

    output_dir = f"/image_article_comprehension/aiddit/comprehension/note_data_video/{author_name}"
    if os.path.exists(output_dir) is not True:
        os.mkdir(output_dir)

    for video in data:
        aweme_id = video.get("aweme_id")
        r = {
            "channel_content_id": aweme_id,
            "link": f"https://www.douyin.com/video/{aweme_id}",
            "cover_image_url": None,
            "title": None,
            "bodyText": video.get("desc"),
            "video_url": None
        }

        utils.save(r, os.path.join(output_dir, f"{aweme_id}.json"))

    return response_data


def get_video_detail(video_id):
    url = "http://crawler.aiddit.com/crawler/dou_yin/detail"

    payload = json.dumps({
        "content_id": video_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"get video detail {video_id} response = {response.text}")

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data for video {video_id}, status code: {response.status_code}")

    data = json.loads(response.text)

    if data.get("code", -1) != 0:
        raise Exception(
            f"Failed to fetch data for video {video_id}, code: {data.get('code')} , message: {data.get('message')}")

    return data.get("data", {}).get("data")


def batch_get_detail(target_dir):
    for i in tqdm(os.listdir(target_dir)):
        video_data = json.load(open(f"{target_dir}/{i}", "r"))

        if video_data.get("video_url") is None:
            print("fetching video url for video", i)
            try:
                d = get_video_detail(video_data.get("channel_content_id"))
                video_data["video_url"] = d.get("video_url_list", [])[0].get("video_url")
                video_data["cover_image_url"] = d.get("image_url_list", [])[0].get("image_url")
                video_data["title"] = d.get("title")
                utils.save(video_data, f"{target_dir}/{i}")
            except Exception as e:
                traceback.print_exc()
                print(e)
        else:
            print(f"video {i} has video url")


if __name__ == "__main__":
    # response = get_account_note_data("MS4wLjABAAAA9Amztv8llaX36ZDn4l-j-tKlkXMYjEQp-b4YU11jxw-68qRISNPMuGqZ_zZOy4NF")
    batch_get_detail(
        "/image_article_comprehension/aiddit/comprehension/note_data_video/大旭的远方")
    pass
