import requests
from urllib.parse import quote, urlencode
import json


def search(keyword):
    url = "https://www.pinterest.com/resource/BaseSearchResource/get/"

    encoded_keyword = quote(keyword)

    source_url = f"/search/pins/?q={encoded_keyword}"
    data = {
        "options": {
            "applied_unified_filters": None,
            "appliedProductFilters": "---",
            "article": None,
            "auto_correction_disabled": False,
            "corpus": None,
            "customized_rerank_type": None,
            "domains": None,
            "dynamicPageSizeExpGroup": None,
            "filters": None,
            "journey_depth": None,
            "page_size": None,
            "price_max": None,
            "price_min": None,
            "query_pin_sigs": None,
            "query": keyword,
            "redux_normalize_feed": True,
            "request_params": None,
            "rs": "typed",
            "scope": "pins",
            "selected_one_bar_modules": None,
            "source_id": None,
            "source_module_id": None,
            "source_url": f"/search/pins/?q={encoded_keyword}&rs=typed",
            "top_pin_id": None,
            "top_pin_ids": None
        },
        "context": {

        }
    }

    payload = {}
    headers = {
        'accept': 'application/json, text/javascript, */*, q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cache-control': 'no-cache',
        'cookie': 'ar_debug=1; csrftoken=697825390599d206327f16f3a3aba80e; _auth=1; cm_sub=allowed; ar_debug=1; _pinterest_cm="TWc9PSZ4VHBpYXhUdjRtN0xKQ3FaVFlUZzJYRFFMbG51akxWL0hhWjRaTXNQcnVZdVpza0J0SmM0OHozMmFvenNqbTJSd0xBL1R6c1RnS1dOZFFFL1Fzd0RNblhGN0pLSTNidi9iUlV3aUxjcEJWODdFZHRPYWhHK0s3RTdqekRSSExxZmMya0FzTE9XNVp3SlUrSE5FMUwwZ083cDZDR0ZuelRETlZ3T2g2Zm1PSE9nOTMzMUlhaHpvSnA1S0VLRXJHNkYmYlVVeUNtSm9YWHdkaVdtVEJVRDhzaWozajJrPQ=="; _b="AYEy2/hffsRK35IYbbXZKQ8/4/IkihAwATQSjGyoPime9PBEDirFgv9GfFRwZcR6zyM="; _pinterest_sess=TWc9PSZmWVJ5c2hVdmg3cjBDVWZ2Y2pUYllzR2p2ZzZTWjBrbFZjRmlSK1dEeHVRb1JoM2ppWENlTmRHVGExRzBFY0FtRTR0UW84VGJqZDltSG5qQ1pZUlMwd2lNNVkxMkxVcVhia1B2RGxyKzdocUdocDVTOGt6VHNUdWRoQis3NFhGcTBqR0NuK3hISEl6RXhrU2llYWhFMWl1WEM0ekUveDBHcE4zZmU4OWRVKzc5Nmc4cFJZMCs5MGczamFaU1VVTm1WbG5IaHhtZDVQZmRZY1NwY2pNdW5la1hHbHJOV3VLZHBuQnlVRGIySVBZMUZWYmlEQy9OTC9xR1pHODZJUXhLTFdZYU9pOGg2cUFzVUhFZVVVV1JLZ3FFYnZjY3h2UFYyc0dBVGx2YVFTMnFKUW5WNnZIV3N4cjc3YWhkQzNoSGcwL1ZySjFvcnovSE10SXNJcEtXcldDVVVNZGRLS0dXbFc2Y0RTZkNkK29XSjZhYWZ0VjhrSVJ1SXZOSlcwVHp5ZlIvaTJMWnJiSTFQa2tRbWkvWHJSNUEvS2Z5a3VLZ1JaTnJQd0VsMk9NcThiVWZZS0hkSEErYWFDcTJNS3g3Z1ZjeE9ucGVQdEd6djJPOXJycDVROG5yTndZWC9Dc0lGQ01jWmlyS1RMMzJXbnJtZE5oNTBoT0NHa0xCUVBkSEZCd1NLajdUSFZwSVNmYTAxSWdkYUpjbmZXQkFJMHdqUVFISkZrMHVtSXIvY0J5ZGV4R3FoQjZZWlVRdTJqeGpRZTJNdGxvTjJOY0tMeUtVTlVCVlB0WDk0OVVYVUJJWmI1U2ppTVJIU3VuV3pCNkdYVUNLQURVYndDMGUrK01yT1dOVVJoNTNzT0RiaThSb2RLSmFWU09NSktlUTBDZnQzaTlXbWlrbnpyZkwxSTFKVHh4aWY5S0hZRlUyUWVQcVJPOXV5bEFpbm9aOWFYcGFjcC9vSkFQdldnWHhpbHNOTzV0dThLMEpqb1BQZXpqdXl2QkQ2R25BaGROSXI0R3ZZSVR1UEJiaVdpWDIzd1hJU2RZL3cwWCtzdk1PZnlaZy9VVWVESVJiTHNNQkZxNmNVS2tsWGpDOE5xYXRGcFUyYnltVVBXWmdHV0lhSFQxT0VxYXgwNjMwc0J0OFZBRnZNbXFPY0VndjJVVWozdElnYStSaDZMdzBLYzB2anRLM2RVZi9jL1AwRUpNMFBuTDlibjgxWGFxYVpwZGhuaVdxdVRmdjFVWVFpVUhTZFhHZ2xIVkM2VlJRYTdGeXloTHZSY1JSZkpkZXVJdDE5K0M1Tk9UUHloV3B1WUxtUWEyb01FTk5kQ1Jvc0hJa3V1YmtUTUVySUpwRXd0Tm01eXJVL1ZFVExOb0Y1RzQ0TUVNQ2ZIcFM3U2xHc0NwVzZZLzBvSjR1U3NYTXMyZlQwSXFuU1lySlNzSENSQk1yN3oyYSsrWjhXeDk1VnVoL3F1SkFPTE5YNFlqdHYvUEpEaUVxYlMreThQOEp5VTJPaWg4R0VwZDRKVGNsYUJxRnVYdVljTjlXYTllS0trNGxPUHk5Vy83dE5FZGZ1Wmlrd1FiMjVQWU11YUdUVWpmNDI1c0ZtWldEUENDaEh4VW1OY05lWmIzSWplaUFGZDV2MktVSjZUd2JxVzI3QVkrUWMwOUQ1b2VWQ0dTR2E5LzYwV01OTEI3Y2VCeElSeTIveUpObFFCSTVRb2dsN0JvaWxrR3lCZDMvY0dFcWxiTkUxclhjdUYwcU9vMHltYlQ1dWFTMFhkOEo4dTN6a1BSNjBGd3omNmhjS1FQczVyb2NMZkhWcVJyQTZYZ0J6enI4PQ==; __Secure-s_a=a0R0T0pWV2V3Vmh5eXArVnI0UUhzd3lLcGlHYTZmWTZtN0VCTDA5cjVTV1Q0MjZuYWJvM3ZkQTdoNC9hQldkRXFCTEtNZHlJdFptNytpd3BVdTlud0V5dWtiMENLeFlNUnlTYTZrNkZnMGdvY2xjWkN6T0d0U1ZFMUFtV1l4cks0VHc1Y0V2eFhJL0hiT3h4d1pDMEpweDN4b2FBWTZTY1lYakJ5dDBjQ2lWTHJoT01WdDBMWU9EdkRObTBlRmhUSmthMmxhcHlNd2lkMnVWNVBSQzB5UW8xWEJxL3llV2tMbzVTNmhmdUUzTVltY0NkS1A4WVl1UkU3MjJObUZYSngvOVpOdTRSL3dhU3lSU0cyUGNEV0pDRDNsVVpSZ3E4Qkx6MkhFNUxmSmFqQ2s1a2hkaTR1RTFrZXU5dnBXUWNxNTI0eXNkaisvMk91YnRscHJnQ3NrQlBydDN3UmxiQUpOeWZTcXlvdkZWdkpVUlRpamhJVnRJbGk2d1pLMkRUcVJFU0cxU3JTSW5Fc0ZENFNENE5JSStZd2lzdUJkQWpYd1NjamY3NXAya2JVVlJ6bjdzWXhGOHNybUxxWnloUHJXUGtxQU1DYW1HUk9ocjlZWlNueXhqQjQ4TjgzWHNaQVhOWENFa1R4M2hCQTl4WXU0VjkxK0dWcTYybkFvZ1lrZGdkeithU2xEdTVHbytqa2xNTXJ3THNyZTZlUGtKZkE2NG1SdWRmclVUSTlqMWdFVTIvdmNzSVRrTnNLNWovWnBLdXNVVDlXY3phWHc0a3l2U0xXNHNPYjQ0Q0FRbXZVc2hzaUFMQTljcDVqbmd2cjNLVzB6RjI0WE1YYXZ4bkQ5eTIweTRITnhpWjVNak9Jd09jQzlZU3dhMUMxakRvWGNRa2ZRK0sxUUVlb2JoQVlpR1BFR0ZZTnoxeDlPbzVVTWRoMzBORGxma3QrbHJMWHV6ZW9GUW5IS0YvK0dwQms5dEVidUxUZFoyOXR5YzEwR2p3Mk8vOFhrT0Q4UGFPSU9jcGFKYlAwT2IrZk1iSUlxQ256MnlEOTNTVlRUYTNyRXJTM3YrQ2dTVHNSRmRXTEMzUVlGRXhhU2dNdnBLUXBGNzE5dTJoYjlXY2xvSUU2bE5WVGxwcm43cVE0L2lKMDlvcFpUWXB0R0VtTG54SjVaVGJUNDRBSkc5MXlOUlFrVHhwb1pjZWNwVDZ0aTR1eTMvdWY5aVI0M0krbnpMOC9OWVRDY2FyNTd5WU02TElPOU00b3FLd2MwdWpXTjBhRDN3RCtjMGs1OURWT2g2T1NYQUdtcGU4aCswTEkrVklCVWV2OG1ha0s0ND0mcXpUYWk5QU5ndHN0UmJDTHA4d2swVk1leUNFPQ==; _routing_id="f6a0237a-0afe-4bd6-94b3-52613c2a3184"; sessionFunnelEventLogged=1',
        'is-preload-enabled': '1',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.pinterest.com/',
        'screen-dpr': '2',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.87", "Chromium";v="131.0.6778.87", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.3.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    # Encode the data dictionary to a query string
    query_string = urlencode({'source_url': source_url, 'data': json.dumps(data)})
    # Append the query string to the URL
    full_url = f"{url}?{query_string}"

    response = requests.request("GET", full_url, headers=headers, data=payload)

    r = json.loads(response.text)

    data = []
    for result in r.get("resource_response").get("data").get("results"):
        image = result.get("images")["orig"]["url"]

        data.append({
            "title": result.get("grid_title"),
            "description": result.get("description"),
            "image": image,
            "link": f"https://www.pinterest.com/pin/{result.get('id')}/",
        })

    return data


if __name__ == '__main__':
    r = search("新疆")
    for i in r:
        print(json.dumps(r, ensure_ascii=False, indent=4))
