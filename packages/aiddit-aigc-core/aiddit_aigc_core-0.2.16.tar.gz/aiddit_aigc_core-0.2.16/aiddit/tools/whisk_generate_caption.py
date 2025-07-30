import requests
import json
import time
import base64
import os
import hashlib
import logging
from image_article_comprehension.aiddit.model import translate_to_chinese

CACHE_DIR = 'image_cache'
COMPREHENSION_CACHE_DIR = 'comprehension_cache'

logging.basicConfig(level=logging.INFO)

MAX_RETRY_COUNT = 10


def get_image_base64(image_url):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    url_hash = hashlib.md5(image_url.encode('utf-8')).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{url_hash}.txt")

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            logging.info(f"url base64  {image_url} is cached")
            return file.read()

    response = requests.get(image_url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        image_data = f"data:{content_type};base64,{image_base64}"

        with open(cache_file, 'w') as file:
            file.write(image_data)

        return image_data
    else:
        raise Exception(f"Failed to fetch image. Status code: {response.status_code}")


def caption(caption_image_url, use_cache=True, translate_to_zh=False, try_cnt=0):
    url = "https://labs.google/fx/api/trpc/backbone.generateCaption"

    if not os.path.exists(COMPREHENSION_CACHE_DIR):
        os.makedirs(COMPREHENSION_CACHE_DIR)

    url_hash = hashlib.md5(caption_image_url.encode('utf-8')).hexdigest()
    cache_file = os.path.join(COMPREHENSION_CACHE_DIR, f"{url_hash}.json")

    if use_cache and os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            logging.info(f"caption_with_cache {caption_image_url} is cached")
            cache_result = json.load(file)
            if translate_to_zh and cache_result.get("zh") is not None:
                return cache_result.get("zh")
            elif translate_to_zh is False and cache_result.get("en") is not None:
                return cache_result.get("en")

    payload = json.dumps({
        "json": {
            "imageBase64": get_image_base64(caption_image_url),
            "category": "LOCATION",
            "sessionId": f";{int(time.time() * 1000)}"
        }
    })
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://labs.google',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://labs.google/fx/zh/tools/whisk',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': '__Host-next-auth.csrf-token=e703e9f27cb2b20ac2685528e3fd6611d5753d1b23789a06dd01ea5e5d601d7c%7C25d3f02f67707c2161b7ad316f9ff63d9cf7135118f1c187883ad0649302b5d5; _ga=GA1.1.82801817.1734441383; EMAIL=%22burningpush%40gmail.com%22; _ga_X5V89YHGSH=GS1.1.1735306514.1.1.1735306570.0.0.0; __Secure-next-auth.callback-url=https%3A%2F%2Flabs.google%2Ffx%2Ftools%2Fwhisk; email=burningpush%40gmail.com; _ga_X2GNH8R5NS=GS1.1.1735306503.14.1.1735306938.0.0.0; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..7HIUW98b3RqqfE8q.ALsmXnMi0060VIoIHmY9IGOXvHrQuYfkCuUIf2rXHxKfGEl_rfNxZD5Zo76_gamcs36D1I6K9ht_aYTDWLHACKWrVENC54ZGMvNz7bw_N2oTRhR7p1Bu7WGxswFkwmzrKoPMGoGGmweRpB2WqDMD7xfKnAP2_tLCtEoR58dDvT93AFqICg3fKsen1DwjR0xEc0pNLe1zMnEr6gWhukEIn0ztVRXFiyVqAqjwR7jrHg_pNtVdBmZA7Z-GdcSdMaIgGhgy-qplMwLAlPR1jID8Q-IK06RDMy7FYRRxZtGDI7TxmDlW91vih_b14Ic50MZxeE7esl2v4EupiHWbQHlA3I5GzC2ruMlmVRqBsTuIbndJrLWL_wnC-6V7rSesvJ1OM5eh-ORjb8NAPEmrMdG_CWFgNQThiMl1pnAndk-1S_5mCfE5OTWpo-LhgkANTL_XiDvTkRc3jUcA3dFACzGf8U3izyqA4qtzgL3s3sMx68zKG0Qh09FfjpI2NoTAOuCt9p17lzpS5EwtJNl2WS-ByOQFV_yjdAxvnESeJKiusBW5FCJkra1ibW801iZdGszjx3CdpWKaZxzxSM0WGCksotHBxYnCpGW0knLzqKGjC91dmw8OqAwor7FipxczQ5PHYtFDHMaL_ZRHCy3jLwMoyaggauHBHgAHPng6GtJ9ZW63TkfwQiBwK_UkwU1H9Qkzu_v5NsoieTzqpu8V1sSU48TIbf8cI2lmxgz-ZBeLfeXBAXQ_kETZgPARBgxnxqsLsDGXPpifpzEFQE86iX_XepGwZtz3KGaX8Ej2V1yV4e_ylg1wroSecPlGfh0UrHMOO6DsY8GLYCDsegPGz8Ni0LCTUA_50Mbv8m9XkdMpuW16hUh-qJO-T9hg0CP2pNkZSwU0n9TJ2ySMU43b5ZlcPQn07oaIB4kpZviZQ4b-4U8QkBQbXo-0TNw8ZD6HhUpgUotqLoPpYh3Bu70sI2YS7Zshmej1omMdB-mvbOC-8WWxD0iRMnEkKT3RWvegZKIJwM014g.qRc2AcvrJp-CwtJgHVzxEw'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        result_english = json.loads(response.text).get("result", {}).get("data", {}).get("json", None)
        result_cache = {
            "en": result_english
        }
        print("result=", result_english)

        r = result_english
        if translate_to_zh:
            print("translate to chinese")
            r = translate_to_chinese(result_english)
            result_cache["zh"] = r

        with open(cache_file, 'w') as file:
            json.dump(result_cache, file, ensure_ascii=False, indent=4)

        return r
    else:
        if response.status_code == 429:
            if try_cnt > MAX_RETRY_COUNT:
                raise Exception(f"Failed to caption image. reach max try count: {try_cnt}")
            else:
                logging.info(
                    f"Failed to caption image {caption_image_url}. \n {response.text} \nRetry after 1 second. try count: {try_cnt} , max_try_count: {MAX_RETRY_COUNT}")
                time.sleep(1)
                return caption(caption_image_url, use_cache=use_cache, translate_to_zh=translate_to_zh,
                               try_cnt=try_cnt + 1)
        else:
            raise Exception(f"Failed to caption image. Status code: {response.status_code} , {response.text}")


if __name__ == '__main__':
    caption_image_url = "https://sns-webpic-qc.xhscdn.com/202502281120/d0cd13261782cff0f1c849d839cc8df2/01026h01krjhudj5nr0010ii48w285bd2t!nd_dft_wlteh_webp_3"

    caption_result = caption(caption_image_url, translate_to_zh=True, use_cache=False)
    print(caption_result)
