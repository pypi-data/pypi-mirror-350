import requests
import json

url = "http://aigc-api.cybertogether.net/aigc/produce/plan/listFilterReferContent"

payload = json.dumps({
    "params": {
        "filterItems": [],
        "pageNum": 1,
        "pageSize": 200,
        "contentFilters": [],
        "filterMatchMode": 2,
        "inputSources": [
            {
                "contentType": 1,
                "inputSourceModal": 4,
                "inputSourceChannel": 2,
                "inputSourceType": 2,
                "inputSourceValue": "20250208120905478491333",
                "inputSourceSubType": None,
                "fieldName": None
            }
        ],
        "contentOrders": [],
        "listType": 2,
        "addModal": None
    },
    "baseInfo": {
        "token": "adc66c43c41b4fd3b7936f5b9894efb5",
        "appType": 9,
        "platform": "pc",
        "appVersionCode": 1000,
        "clientTimestamp": 1,
        "fid": 1,
        "loginUid": 1,
        "pageSource": 1,
        "requestId": 1,
        "rid": 1,
        "uid": 1
    }
})
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://aigc-admin.cybertogether.net',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

import json
import aiddit.utils as utils

d = json.loads(response.text)

for video in d.get("data").get("data"):
    r = {
        "channel_content_id": video.get("channelContentId"),
        "video_url": video.get("videoUrl"),
        "title": video.get("title"),
        "content_link": video.get("contentLink")
    }
    utils.save(r,
               f"/image_article_comprehension/aiddit/video/data/reference_note/抖音热榜0212/{video.get('channelContentId')}.json")
