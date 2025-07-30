import logging
import os
import requests
import json
import traceback
from tqdm import tqdm
import time
import aiddit.utils as utils
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import uuid
from aiddit.model.gemini_upload_file import handle_file_path
from aiddit.tools.oss_upload import upload_oss


def get_note_detail(content_link):
    print(f"get note detail {content_link}")

    url = "http://crawler.aiddit.com/crawler/xiao_hong_shu/detail"

    payload = json.dumps({
        "content_link": content_link,
        "is_upload": True
    })
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.uU_4v9ukxon47prl6EEV2U5YqSIoJr8r6wS1SBnOJiA',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        note_detail_response = json.loads(response.text)
        if note_detail_response.get("code") != 0:
            raise Exception(
                f"Failed to get note detail {content_link} , code = {note_detail_response.get('code')} , {response.text}")

        return note_detail_response.get("data").get("data")
    else:
        raise Exception(f"Failed to get note detail {content_link} , http status code = {response.status_code}")

from tenacity import retry, stop_after_attempt, wait_fixed
@retry(stop=stop_after_attempt(10), wait=wait_fixed(10))
def batch_get_note_detail_with_retries(note_dir):
    cached_cnt, total_cnt, success_cnt = batch_get_note_detail(note_dir)

    if cached_cnt + success_cnt < total_cnt:
        raise Exception(
            f"批量获取小红书详情失败, cached_cnt={cached_cnt}, total_cnt={total_cnt}, success_cnt={success_cnt}")
    pass

def batch_get_note_detail(note_dir):
    note_list = os.listdir(note_dir)

    success_cnt = 0
    cached_cnt = 0
    for note_filename in tqdm(note_list,desc=f"batch_get_note_detail , {os.path.basename(note_dir)}"):
        with open(os.path.join(note_dir, note_filename), 'r') as f:
            note = json.load(f)
            if not note.get("images"):
                while True:
                    try:
                        note_detail = get_note_detail(note.get("link"))
                        print(f"get note detail success {note.get('link')}")

                        note["comment_count"] = note_detail.get("comment_count")

                        note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                                          note_detail.get("image_url_list", [])]
                        note["like_count"] = note_detail.get("like_count")
                        note["body_text"] = note_detail.get("body_text")
                        note["title"] = note_detail.get("title")
                        note["collect_count"] = note_detail.get("collect_count")
                        note["content_type"] = note_detail.get("content_type")
                        note["link"] = note_detail.get("content_link")

                        with open(os.path.join(note_dir, note_filename), 'w') as wf:
                            json.dump(note, wf, ensure_ascii=False, indent=4)
                            success_cnt += 1
                        break
                    except Exception as e:
                        error = traceback.format_exc()
                        print(error)
                        print(f"Failed to get note detail , {e}")
                        if "访问频次异常" in error:
                            print(f"访问频次异常 sleep 3s")
                            time.sleep(3)
                        else:
                            break
            else:
                cached_cnt += 1
                print(f"note {note.get('link')} already has detail data")

    print(f"cached count = {cached_cnt} , total count = {len(note_list)} success count = {success_cnt}")
    return cached_cnt, len(note_list), success_cnt


def single_detail(link, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    note_id = link.split("?")[0].split("/")[-1]
    if os.path.exists(os.path.join(output_dir, f"{note_id}.json")):
        print(f"{note_id}.json already exists , skip , {link}")
        return

    note_detail = get_note_detail(link)
    print(note_detail)
    note = {}

    note["comment_count"] = note_detail.get("comment_count")
    note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                      note_detail.get("image_url_list", [])]
    note["like_count"] = note_detail.get("like_count")
    note["body_text"] = note_detail.get("body_text")
    note["title"] = note_detail.get("title")
    note["collect_count"] = note_detail.get("collect_count")
    note["link"] = note_detail.get("content_link")
    note["channel_content_id"] = note_detail.get("channel_content_id")

    content_type = note_detail.get("content_type")
    note["content_type"] = content_type
    if content_type == "video":
        video = note_detail.get("video_url_list", [])[0]
        xhs_cnd_video_url  = video.get("video_url")
        try:
            video = note_detail.get("video_url_list", [])[0]
            video_url = upload_video_2_oss(xhs_cnd_video_url)
            video_info = {
                "origin_video_url": video.get("video_url"),
                "duration": video.get("video_duration"),
                "video_url": video_url
            }
            note["video"] = video_info
        except Exception as e:
            note["video"] = {}
            print(f"upload xhs video {xhs_cnd_video_url} error , {str(e)}")
    else:
        note["video"] = {}

    with open(os.path.join(output_dir, f"{note_detail.get('channel_content_id')}.json"), 'w') as wf:
        json.dump(note, wf, ensure_ascii=False, indent=4)


def upload_video_2_oss(video_url):
    video_name = f"{uuid.uuid4().int}.mp4"
    local_path = handle_file_path(video_url, video_name)
    key = f"aigc_creation/xhs/video/{video_name}"
    oss_url = upload_oss(key, local_path)
    print(f"upload_video_2_oss {video_url} to {oss_url}")
    return oss_url


def refresh_detail_images():
    refresh_dir = "/image_article_comprehension/aiddit/create/reference_note_keypoint/image_merge_0102_1230"
    total_count = len(os.listdir(refresh_dir))

    files = os.listdir(refresh_dir)
    files = ["67752b32000000000900c5cc.json"]

    success_cnt = 0
    for i in tqdm(files):
        try:
            note = json.load(open(os.path.join(refresh_dir, i), 'r'))

            if any("res.cybertogether.net" in images_url for images_url in note.get("note_info").get("images")):
                print(f"{json.dumps(note.get('note_info').get('images'))} has res.cybertogether.net , skip")
                continue

            note_detail = get_note_detail(note.get("note_info").get("link"))

            note["note_info"]["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                                           note_detail.get("image_url_list", [])]

            utils.save(note, os.path.join(refresh_dir, i))
            success_cnt += 1
        except Exception as e:
            print("Failed to refresh detail images", i, str(e))

    print(f"success count = {success_cnt} / {total_count}")
    pass


def refresh_crawler_detail_images():
    refresh_dir = "/image_article_comprehension/aiddit/comprehension/note_data/account_猫小司_6430bea30000000012011f2d"
    total_count = len(os.listdir(refresh_dir))

    files = os.listdir(refresh_dir)

    success_cnt = 0
    for i in tqdm(files):
        try:
            note = json.load(open(os.path.join(refresh_dir, i), 'r'))

            if any("res.cybertogether.net" in images_url for images_url in note.get("images")):
                print(f"{json.dumps(note.get('images'))} has res.cybertogether.net , skip")
                continue

            note_detail = get_note_detail(note.get("link").split("?")[0])

            print(f"{json.dumps(note_detail, ensure_ascii=False, indent=4)}")

            note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                              note_detail.get("image_url_list", [])]

            utils.save(note, os.path.join(refresh_dir, i))
            success_cnt += 1
        except Exception as e:
            print("Failed to refresh detail images", i, str(e))

    print(f"success count = {success_cnt} / {total_count}")
    pass


def simplify_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # 保留需要的参数
    simplified_query_params = {
        'xsec_token': query_params.get('xsec_token', [''])[0]
    }

    # 构建新的URL
    simplified_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        urlencode(simplified_query_params),
        parsed_url.fragment
    ))

    return simplified_url


if __name__ == "__main__":
    # refresh_detail_images()

    # refresh_crawler_detail_images()

    # batch_get_note_detail(
    #     '/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/account_20250110_春哥边走边画_62ad8bd7000000001b0267af')

    note_list = [
        "https://www.xiaohongshu.com/explore/680de768000000001c02b013",
        "https://www.xiaohongshu.com/explore/680de7d8000000001c013c11",
        "https://www.xiaohongshu.com/explore/680b95b8000000000f03984e",
        "https://www.xiaohongshu.com/explore/65a8c447000000002a0108ff",
        "https://www.xiaohongshu.com/explore/680e1708000000000b0172c3",
        "https://www.xiaohongshu.com/explore/680e2ea0000000000e004d3d",
        "https://www.xiaohongshu.com/explore/6711f52f000000002401415a",
        "https://www.xiaohongshu.com/explore/620bc2ef000000000102f37e",
        "https://www.xiaohongshu.com/explore/680b20ba000000001d00902d",
        "https://www.xiaohongshu.com/explore/63da460e000000001b01cd58",
        "https://www.xiaohongshu.com/explore/640aaa78000000000703ae44",
        "https://www.xiaohongshu.com/explore/666025a000000000150113e3",
        "https://www.xiaohongshu.com/explore/646383940000000013009907",
        "https://www.xiaohongshu.com/explore/680b64e0000000001202da62",
        "https://www.xiaohongshu.com/explore/61cebd5d000000000102fbee",
        "https://www.xiaohongshu.com/explore/672d470c000000001a0372e9",
        "https://www.xiaohongshu.com/explore/63d2894e000000001f023b7b",
        "https://www.xiaohongshu.com/explore/643648bc0000000027011d9a",
        "https://www.xiaohongshu.com/explore/680b1603000000001d015be4",
        "https://www.xiaohongshu.com/explore/62445fc0000000002103bfee",
        "https://www.xiaohongshu.com/explore/6214b483000000000102c435",
        "https://www.xiaohongshu.com/explore/6436902c000000001300775a",
        "https://www.xiaohongshu.com/explore/6369e7ca000000000601e637",
        "https://www.xiaohongshu.com/explore/657e8d2e000000000901cfb6",
        "https://www.xiaohongshu.com/explore/62a16dc1000000001d0198c0",
        "https://www.xiaohongshu.com/explore/680a05e4000000000b01eea0",
        "https://www.xiaohongshu.com/explore/67eca27e000000001c00b89b",
        "https://www.xiaohongshu.com/explore/678b072a0000000018031a03",
        "https://www.xiaohongshu.com/explore/67355f7b000000001b02db51",
        "https://www.xiaohongshu.com/explore/648d8031000000000703b888",
        "https://www.xiaohongshu.com/explore/6620c524000000000401951f",
        "https://www.xiaohongshu.com/explore/6805d1ae000000000f03b7e3",
    ]

    for n in tqdm(note_list):
        single_detail(n,
                      "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/xhs/result/小红书热搜0427")

    pass
