from dotenv import load_dotenv
import os
import oss2
import time

load_dotenv()

access_key_id = os.getenv('aliyun_oss_access_key_id')
access_key_secret = os.getenv("aliyun_oss_access_key_secret")

if access_key_id is None or access_key_secret is None:
    raise Exception("aliyun_oss_access_key_id or aliyun_oss_access_key_secret is None")

auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, 'https://oss-ap-southeast-1.aliyuncs.com', 'aigc-admin')

def upload_oss(key, local_file_path):
    start_time = time.time()

    with open(local_file_path, "rb") as file:
        bucket.put_object(key, file)

    cdn_url = f"http://res.cybertogether.net/" + key

    print(f"{key} upload success , {cdn_url} , 耗时 = {time.time() - start_time} 秒")

    return cdn_url

