import json
import requests
import imghdr
import os
import hashlib
import uuid
from aiddit.model import chat
import datetime
import urllib.parse
import urllib.request

def get_file_uri(file_path):
    return urllib.parse.urljoin('file:', urllib.request.pathname2url(file_path))

def remove_duplicates(input_list):
    """
    Remove duplicates from a list while preserving the order of elements.

    :param input_list: List of elements that may contain duplicates
    :return: List of elements with duplicates removed
    """
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def remove_key_from_dict(data, key_to_remove):
    if isinstance(data, dict):
        if key_to_remove in data:
            del data[key_to_remove]
        for key, value in data.items():
            remove_key_from_dict(value, key_to_remove)
    elif isinstance(data, list):
        for item in data:
            remove_key_from_dict(item, key_to_remove)
    return data

def save(r, path):
    create_directory_from_file_path(path)
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


def create_directory_from_file_path(file_path):
    # Extract the directory path from the file path
    directory = os.path.dirname(file_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")


def x_oss_process(url, process="image/resize,h_300"):
    if "res.cybertogether.net" in url and "x-oss-process" not in url:
        return url + "?x-oss-process=" + process
    else:
        return url

def x_oss_process_format_jpeg(url):
    if "res.cybertogether.net" in url and "x-oss-process" not in url and "png" not in url:
        return url + "?x-oss-process=image/format,png"
    else:
        return url

def pack_image_content(images, img_num=100):
    image_content = []
    image_url_set = set([])
    for image_url in images[:img_num]:
        if image_url not in image_url_set:
            image_content.append({"type": "image_url", "image_url": {"detail": "low", "url": image_url}})
            image_url_set.add(image_url)
    return image_content


def oss_resize_image(url):
    if "res.cybertogether.net" in url and "x-oss-process" not in url:
        return f"{url}?x-oss-process=image/resize,h_300"

    return url


def md5_str(s):
    return str(hashlib.md5(s.encode()).hexdigest())


def uuid_str():
    return str(uuid.uuid4())

def generate_uuid_datetime():
    return f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{str(uuid.uuid4())[:4]}'

def save_image_from_url(img_url, save_path):
    try:
        # Fetch the image content
        response = requests.get(img_url)
        response.raise_for_status()  # Check if the request was successful

        # Extract the image name from the URL and add the correct extension
        image_name = f"{md5_str(img_url)}.jpeg"

        # Create the full path to save the image
        full_path = os.path.join(save_path, image_name)

        # Save the image content to a file
        with open(full_path, 'wb') as file:
            file.write(response.content)

        print(f"Image saved to {full_path}")
    except Exception as e:
        print(f"Failed to save image from URL {img_url}: {e}")


def try_remove_markdown_tag_and_to_json(ans):
    print("try_remove_markdown_tag_and_to_json")
    import re
    try:
        cleaned_text = re.sub(r'```json|```', '', ans.strip())
        return json.loads(cleaned_text.strip())
    except Exception as e:
        print(f"正则表达式 to_json error {ans} , {str(e)}")
        return _fix_json(ans)


def _fix_json(ans):
    print("gemini fix_json")
    try:
        prompt = f"""你需要将下面数据修复为标准的JSON的数据，保证其能够被程序正确解析为JSON。
注意：你仅需求修复格式问题而导致的JSON解析错误，不需要对数据内容进行任何修改。
- 常见错误的有：键名没有双引号包裹、字符串没有双引号包裹、键值没有双引号包裹、键值没有逗号分隔、字符串中间有双引号等。

错误数据如下：        
{ans}""".strip()

        ans = chat.gemini(prompt)
        return json.loads(ans)
    except Exception as e:
        print("gemini fix_json error", e)
        return ans


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except PermissionError:
        print(f"Permission denied to delete {file_path}.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")

def load_from_json_dir(dir_path):
    # 判断dir_path是否是文件夹
    if not os.path.exists(dir_path):
        raise Exception(f"dir_path {dir_path} does not exist")

    if not os.path.isdir(dir_path):
        raise Exception(f"dir_path {dir_path} is not a directory")

    return [json.load(open(os.path.join(dir_path, i), "r")) for i in os.listdir(dir_path) if i.endswith(".json")]

def read_file_as_string(file_path):
    if not os.path.exists(file_path):
        raise Exception(f"file_path {file_path} does not exist")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    file_uri = get_file_uri("/Users/nieqi/Pictures/34358-20190724165111732-667425422.jpg")
    print(file_uri)
    pass
