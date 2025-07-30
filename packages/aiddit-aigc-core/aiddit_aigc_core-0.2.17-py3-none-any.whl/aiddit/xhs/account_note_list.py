import logging

import requests
import json
import os
from aiddit.xhs.xiao_hong_shu_helper import XiaoHongShuHelper
import aiddit.xhs.note_detail as note_detail
from tenacity import retry, stop_after_attempt, wait_fixed


def user_note_list(user_id):
    xhs = XiaoHongShuHelper
    url = f"https://edith.xiaohongshu.com/api/sns/web/v1/user_posted?num=30&user_id={user_id}&image_formats=jpg,webp,avif&xsec_token=&xsec_source=pc_feed"

    query_param = {}

    cookie = "abRequestId=c8018b40-a9ac-5f48-961f-685e76a39456; a1=19270552c6fucbpdlpupf4kp8dvzynlcodoxjf10y50000269580; webId=53c58069ad609fbc4b7e2b7c9346e9b2; gid=yjJW822q0JlfyjJW822JSfiyKi7SDUf1U7Uil8v4TUYfhC28uvI1SV888JKj2Y88qf4DSDjD; web_session=04006975fcbffb0509486d3332354b37e09e23; x-user-id-creator.xiaohongshu.com=589bb3576a6a693a0c3d591e; customerClientId=270896288267942; customer-sso-sid=68c5174551971675043898644c73558f3fa313e1; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517455197167502919748oyjo3vz0evuoniey; galaxy_creator_session_id=w6DyrVjyd8zXkoRZgxPD4vXh7mxwommKWbr6; galaxy.creator.beaker.session.id=1735798355322078058102; xsecappid=xhs-pc-web; webBuild=4.53.0; acw_tc=0ad6fb1717362372234238427ec80bce8fb066c5ad3ad9226fdf7c26550772; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=c31dbf3f-4d9b-47f3-aa45-5419d0718ca3; unread={%22ub%22:%226774af5c0000000014025f28%22%2C%22ue%22:%22676fda990000000013018e24%22%2C%22uc%22:25}"

    sign_result = xhs.get_sign(url=url,
                               data=query_param,
                               cookie=cookie)
    sign = sign_result[0]

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.xiaohongshu.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        "cookie": cookie,
        "x-t": sign["X-t"],
        "x-s-common": sign["X-s-common"],
        "x-s": sign["X-s"],
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"response status code = {response.status_code}, {response.text}")

    print(response.status_code)
    if response.status_code != 200:
        raise Exception(f"response status code = {response.status_code}, {response.text}")

    for i in json.loads(response.content)["data"]["notes"]:
        print(f"https://www.xiaohongshu.com/explore/{i['note_id']}?xsec_token={i['xsec_token']}")

    return json.loads(response.content)["data"]["notes"]

@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def save_account_note(account_id, account_name, save_dir):
    # dir_name = f"account_{account_name}_{account_id}"
    # dir = f"{save_dir}/{dir_name}"
    os.makedirs(save_dir, exist_ok=True)

    url = "http://crawler.aiddit.com/crawler/xiao_hong_shu/blogger"
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

    # data = user_note_list(account_id)

    logging.error(f"{account_id} {account_name} note count: {len(data)}")

    for d in data:
        # print(json.dumps(d))
        note_id = d["note_id"]
        xsec_token = d.get("xsec_token", "")
        note_url = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}"

        file_name = f"{note_id}.json"

        note_info = {
            "channel_content_id": note_id,
            "link": note_url,
            "xsec_token": xsec_token
        }

        if os.path.exists(f"{save_dir}/{file_name}") is True:
            print(f"file exists {file_name}")
            continue

        with open(os.path.join(save_dir, file_name), 'a') as f:
            f.write(json.dumps(note_info, ensure_ascii=False, indent=4))

    return save_dir


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_account_info(account_id):
    url = "http://crawler.aiddit.com/crawler/xiao_hong_shu/account_info"

    payload = json.dumps({
        "account_id": account_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    response.raise_for_status()

    data = json.loads(response.text).get("data", {}).get("data")

    if data is None:
        raise Exception(f"no data for account_id {account_id} , {response.text}")

    if data.get("account_name") is None:
        raise Exception(f"account_name is None, please check the account_id {account_id}")

    return {
        "account_name": data.get("account_name"),
        "description": data.get("description"),
        "avatar_url": data.get("avatar_url"),
        "account_id": account_id,
        "account_link": data.get("account_link"),
    }


if __name__ == '__main__':
    # 修改变量account_id start
    # account_阿橘的小窝_5bb61a0a59b9bf0001e9a986.txt
    account_id = "5bb61a0a59b9bf0001e9a986"
    account_name = "阿橘的小窝"
    dir = f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/comprehension/note_data"
    dir_name = f"account_{account_name}_{account_id}"
    save_dir = f"{dir}/{dir_name}"
    # save_account_note(account_id, account_name, save_dir)

    note_detail.batch_get_note_detail(save_dir)

    # print(json.dumps(get_account_info(account_id), ensure_ascii=False, indent=4))
