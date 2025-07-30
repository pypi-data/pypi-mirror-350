import json
import os
import requests
from urllib.parse import urlparse, parse_qs
import mimetypes
import traceback
import hashlib
import aiddit.utils as utils
from google.generativeai.types.file_types import File
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv

load_dotenv()


def generate_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


cached_download_file_dir = os.getenv("google_genai_download_files_save_dir")
cached_google_upload_file_dir = os.getenv("google_generativeai_upload_file_cache_dir")

if not os.path.exists(cached_download_file_dir):
    os.makedirs(cached_download_file_dir)

if not os.path.exists(cached_google_upload_file_dir):
    os.makedirs(cached_google_upload_file_dir)


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except Exception as e:
        return False


def download_file(url, local_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type')
    extension = mimetypes.guess_extension(content_type)
    if extension:
        if "." not in local_path:
            local_path += extension
        if os.path.exists(local_path):
            # print(f"url  {url} exists in {local_path}")
            return local_path
    with open(local_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return local_path


def get_file_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    base_filename = os.path.basename(path)
    return base_filename

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def handle_file_path(url, file_name=None):
    if is_url(url):
        if file_name is None:
            parsed_url = urlparse(url)
            path = parsed_url.path
            query = parse_qs(parsed_url.query)

            base_filename = os.path.basename(path)

            local_filename = None

            if "x-oss-process" in url and "format," in url:
                oss_params = query.get('x-oss-process', [''])[0].split('/')
                first_format_string = next((s for s in oss_params if 'format' in s), None)
                if first_format_string is not None:
                    file_format = first_format_string.split(",")[1]
                    local_filename = f"{base_filename.split('.')[0]}.{file_format}"

            if local_filename is None:
                local_filename = base_filename

            if local_filename == "" or local_filename is None:
                local_filename = generate_md5_hash(url)
        else:
            local_filename = file_name

        local_path = os.path.join(cached_download_file_dir, local_filename)
        # print(f"Downloading {path} to {local_path}")
        local_path = download_file(url, local_path)
        return local_path
    else:
        if os.path.exists(url):
            # print(f"File {path} is already a local file.")
            return url
        else:
            raise FileNotFoundError(f"The file {url} does not exist.")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def do_genai_upload_file(genai, local_file_path, mime_type):
    print(f"preparing uploading to google ,  {local_file_path} ， mime_type = {mime_type}")
    try:
        return genai.upload_file(local_file_path, mime_type=mime_type)
    except Exception as e:
        print(f"upload file {local_file_path} failed , {str(e)}")
        raise e


def upload_file(path, genai):
    try:
        local_file_path = handle_file_path(path)
        mime_type, _ = mimetypes.guess_type(local_file_path)
        if mime_type is None:
            mime_type = "video/mp4"

        cached_google_upload_file_path = os.path.join(cached_google_upload_file_dir,
                                                      f"{generate_md5_hash(local_file_path)}.json")
        # print("cache_upload_file", cached_google_upload_file_path)
        if os.path.exists(cached_google_upload_file_path):
            file_dict = json.load(open(cached_google_upload_file_path, 'r'))
            # print(
            #     f"upload file {local_file_path} exists in {cached_google_upload_file_path} \n {json.dumps(file_dict, ensure_ascii=False, indent=4)}")
            cached_google_upload_file = File(file_dict)
            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            if current_time < cached_google_upload_file.expiration_time:
                # print(f"upload file {local_file_path} exists in {cached_google_upload_file_path} Available")
                return cached_google_upload_file
            else:
                print(f"upload file {local_file_path} exists in {cached_google_upload_file_path} Expired")

        file = do_genai_upload_file(genai, local_file_path, mime_type)
        utils.save(file.to_dict(), cached_google_upload_file_path)
        return file
    except Exception as e:
        error = traceback.format_exc()
        print(str(e))
        print(error)

    return None


if __name__ == "__main__":
    images =   [
            "http://res.cybertogether.net/crawler/image/6206c586987cf3321b14755f4778e3d9.webp",
            "http://res.cybertogether.net/crawler/image/6206c586987cf3321b14755f4778e3d9.webp",
            "http://res.cybertogether.net/crawler/image/68291a9f85f66ffec9d490271dd5f32f.webp",
            "http://res.cybertogether.net/crawler/image/0e2de9dd5da3e0321e3923b4142a0ea4.webp",
            "http://res.cybertogether.net/crawler/image/e1c8e7c1b1da2c2798eb79b066e2445a.webp",
            "http://res.cybertogether.net/crawler/image/3dbe7231256fdfd397b8bbcfb954aca1.webp",
            "http://res.cybertogether.net/crawler/image/d821158cd7f6b1ef2a9b7b6eed3ef862.webp"
        ]

    save_dir = "/Users/nieqi/Downloads/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs(save_dir)
    images = utils.remove_duplicates(images)

    for img in images:
        download_file(img, os.path.join(save_dir, get_file_name(img)))
