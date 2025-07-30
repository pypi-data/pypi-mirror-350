import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)  # 设置日志级别为INFO
logger = logging.getLogger(__name__)

cookie = "AMP_MKTG_437c42b22c=JTdCJTdE; _ga=GA1.1.467376067.1728631563; __stripe_mid=f51ed747-d4a9-4644-acfa-9e8ffb996ac092882e; _gcl_au=1.1.1205502907.1736408466; _ga_Q0DQ5L7K0D=GS1.1.1737725521.53.0.1737725521.0.0.0; cf_clearance=PAUJQqleCpTtwjMpuvUJVOtsJeTfDjHpuLXiGs5SJrM-1740643958-1.2.1.1-Gh6rQzTJtapgomz.ELeNgnNFucZk5mdnn17rOoDkNzphZkZCgsxgt4p8.Z5sdVsnOgfKgPUf9bee2FRfqpfnTs3uHpKwhYQzeQEDKSfQD505hwlothGiDe3ZROtvdSUJqL9VC_pDsAFLwRq4oVQw73SHeqTtTjGYjbUkqjvnjuIkrnX2KgnoKqOHkyx3AQabLNx84h9xG3mXMGPruYW3B2LBhM_6RYVlzIQpx.jsbCp4qHtvhzilhT2kr_muopxkpu17zTXLRWCqxsf5n9EntovmlY4IMCDDJt1I80WgF10; __Host-Midjourney.AuthUserTokenV3_i=eyJhbGciOiJSUzI1NiIsImtpZCI6ImRjNjI2MmYzZTk3NzIzOWMwMDUzY2ViODY0Yjc3NDBmZjMxZmNkY2MiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiZGVib3JhaF91YTg4MzY4NjFfMTE5MTAiLCJtaWRqb3VybmV5X2lkIjoiNjA4MGI4YzUtMjNmMy00ZDUzLThjMmUtODMxNzAzM2Y3NzAzIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2F1dGhqb3VybmV5IiwiYXVkIjoiYXV0aGpvdXJuZXkiLCJhdXRoX3RpbWUiOjE3NDA2NDM5NzgsInVzZXJfaWQiOiJXaWU4R3U5amZwWXNYSXp0ZW9rVUUzVFdBQlEyIiwic3ViIjoiV2llOEd1OWpmcFlzWEl6dGVva1VFM1RXQUJRMiIsImlhdCI6MTc0MDY0Mzk3OCwiZXhwIjoxNzQwNjQ3NTc4LCJlbWFpbCI6ImNocmlzdG9waGVyc2FyYWhjYXJ0ZXJ5b3VuZ3hlcW9nQG91dGxvb2suY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZGlzY29yZC5jb20iOlsiMTMxODAyNDA0NTMxMjM0NDE0OCJdLCJlbWFpbCI6WyJjaHJpc3RvcGhlcnNhcmFoY2FydGVyeW91bmd4ZXFvZ0BvdXRsb29rLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImRpc2NvcmQuY29tIn19.h6KoOcEBFgQsEHRt2dIHgAPO4elayzGxto86Iob--Q-HHt1qwX9k1q0jHvCUgav2lFhDFSMPaPRSsCgzx0ZzPcg4lSX5v0xjo0-65jtifFiA7fQ1EbtOo99JxbYett3UA2fAYla15om2ELUC-bHzzrpN6ywjc089fi-zsqaa3lpw23Rukfxer9deIk-d-41Ly2kqa9ypEvrwsjPATLsRlLbuIxn_i4EfuAyoPxH1qjurrC79FprSKz0h0iwPH0FNJ0JhXzld2UT2He3uKaBd-5ZXrcD6vFUqKzq8rISMu0f9I51nRadMvcu8yzI3JHu7FTTt_e0biX5zxODpLWNbYA; __Host-Midjourney.AuthUserTokenV3_r=AMf-vBwQrA8lRFqOSW45Oi_OAtyWrCWC4sykjETTBj7inIjwkEhLbUuqn_tPqHwZXltQgivCGi5ItbPyIJzPUwPAGZU4JPsg63RV-iDHSPNOllyroPREYofvff_tnn3vYz6WvdCqa9yGWx_CFHElhP_r5Kqsq3hmSOCTN5U9bjQfHr2_ct6lvmYnJjAbbN4ht7J1JnUS09r2o0qj6P4Z5Mw51yfa4OkBiZePqd0MDo-Nnm-phcgXXhvxNXi8lSPD-zrQd7XnymEUA8xkIlaKyRBk4jLtIM5K8QR5IOijcGWjTOLe1HeBB9SV2BSr5kp0kIMXmVB6Iowy; __cf_bm=cDA3fDJ9t3Ggf1u60B9TF1pSv15ulxRZs3Jy3iceWvI-1740644327-1.0.1.1-YM.pLtAlhxGihNVWEWZhzFfLFLks1A14nN87n4WbBBcQx0apm5wRjjbCxdtFZf5u6PIsFOCnTV6ZEnW6wxTJJw; AMP_437c42b22c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1ZDc1ODczYi1jNGE1LTQzODgtOWM1My1mYmIwMjgzNTljYjIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI2MDgwYjhjNS0yM2YzLTRkNTMtOGMyZS04MzE3MDMzZjc3MDMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQwNjQzOTU4MTY1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0MDY0NDM4MjgzNCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTM5OCU3RA=="
user_id = "6080b8c5-23f3-4d53-8c2e-8317033f7703"


def submit_job(prompt):
    url = "https://mid-api-proxy.aiddit.com/submit_job"

    payload = json.dumps({
        "prompt": prompt,
        "cookie": cookie,
        "user_id": user_id,
        "mode": "fast"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(f"submit job fail, status code is {response.status_code} , {response.text}")

    response_data = json.loads(response.text)

    failure = response_data.get("failure", [])
    success = response_data.get("success", [])

    if len(failure) > 0:
        raise Exception(f"submit job fail, failure is {failure}")

    return success[0].get("job_id")


def error_keywords(failure):
    return failure.get("error_keywords")


def query_job_status(job_id):
    url = "https://mid-api-proxy.aiddit.com/query_job_status"

    payload = json.dumps({
        "job_id": job_id,
        "cookie": cookie,
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(f"query_job_status fail, status code is {response.status_code},  {response.text}")

    response_data = json.loads(response.text)

    if len(response_data) == 0:
        return "running"

    # completed、running
    return response_data[0].get("current_status")


def get_generate_images(job_id):
    url = "https://mid-api-proxy.aiddit.com/get_image_urls"

    payload = json.dumps({
        "job_id": job_id,
        "image_num": 4
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def generate_midjourney_image(prompt):
    job_id = submit_job(prompt)
    logging.info(f"generate_midjourney_image job_id: {job_id} , prompt = {prompt}")
    time.sleep(2)

    job_status = query_job_status(job_id)
    logging.info(f"query job_status: {job_status} , job_id: {job_id} , prompt = {prompt}")

    max_retry_cnt = 60
    retry_cnt = 0
    while job_status != "completed":
        time.sleep(2)
        job_status = query_job_status(job_id)
        if retry_cnt > max_retry_cnt:
            raise Exception("generate image timeout")
        retry_cnt += 1
        logging.info(f"query job_status: 当前耗时 {2 * (retry_cnt + 1)} 秒, {job_status} , job_id: {job_id}")

    images = get_generate_images(job_id)
    logging.info(f"get_generate_images images: {images} , job_id: {job_id} , prompt = {prompt}")
    return images


if __name__ == "__main__":
    # job_id = submit_job("water")
    # print(f"job_id: {job_id}")

    # job_status = query_job_status("30f7fc1b-9169-439e-8d80-7072d090d3d8")
    # print(f"job_status: {job_status}")

    # images = get_generate_images("30f7fc1b-9169-439e-8d80-7072d090d3d8")
    # print(images)

    generate_midjourney_image("water")
    pass
