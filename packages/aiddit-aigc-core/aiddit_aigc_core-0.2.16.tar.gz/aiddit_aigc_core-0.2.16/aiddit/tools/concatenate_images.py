from PIL import Image
import os
import json
import requests
from io import BytesIO
from tqdm import tqdm
from image_article_comprehension.aiddit import utils
from image_article_comprehension.aiddit.model import claude
import base64
import mimetypes


def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def concatenate_images(image_urls, output_path, images_per_row=5, margin=30):
    images = [download_image(url) for url in tqdm(image_urls, desc="Downloading images")]

    # Calculate the size of the new image
    max_width = max(image.width for image in images)
    max_height = max(image.height for image in images)
    rows = (len(images) + images_per_row - 1) // images_per_row
    total_width = images_per_row * max_width + (images_per_row - 1) * margin
    total_height = rows * max_height + (rows - 1) * margin

    new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    for index, image in enumerate(images):
        row = index // images_per_row
        col = index % images_per_row
        x = col * (max_width + margin)
        y = row * (max_height + margin)
        new_image.paste(image, (x, y))

    new_image.save(output_path)


def prepare_image():
    dir = "/image_article_comprehension/aiddit/comprehension/note_data/account_20250104_手訫_5fdeea180000000001009b87"
    listdir = os.listdir(dir)

    images = []
    for i in listdir:
        note = json.load(open(os.path.join(dir, i), 'r'))
        image_url = note.get("images")[0]
        images.append(utils.x_oss_process(image_url))

    # Example usage
    output_path = f'/image_article_comprehension/aiddit/tools/{os.path.basename(dir)}.jpg'
    concatenate_images(images, output_path)


##本地图片转换成base64
def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()

    media_type, _ = mimetypes.guess_type(image_path)
    image_base64 = f"data:{media_type};base64,{img_base64}"
    return image_base64


def caption_account_homepage_image():
    image_path = "/image_article_comprehension/aiddit/tools/account_20250104_手訫_5fdeea180000000001009b87.jpg"
    image_base64 = image_to_base64(image_path)

    renshe_path = "/image_article_comprehension/comprehension/renshe/result/result_20250110_before/手訫.json"
    renshe = json.load(open(renshe_path, 'r'))

    prompt = f'''
我会给你一张小红书的账号主页截图，你可以看到这个账号的主页上有哪些内容，然后我会再给你提供该账号的以下信息：
账号创作灵魂：
{json.dumps(renshe.get("renshe_unique_point").get("创作灵魂"), ensure_ascii=False)}

重要亮点：
{json.dumps(renshe.get("renshe_unique_point").get("重要亮点"), ensure_ascii=False)}

主要特征：
{json.dumps(renshe.get("renshe_unique_point").get("主要特征"), ensure_ascii=False)}

你要根据我提供的以上信息帮我完成以下任务：
1. 基于账号创作灵魂、重要亮点、主要特征，结合主页截图，进一步提取该账号的必须的关键信息；

要求如下：
- 输出为中文；
- 请只描述客观事实，不要添加主观评价；
- 请直接输出JSON格式，不要有除了JSON格式之外的其他输出；
- output in JSON format , with keys:
    - `result`(dict)
'''.strip()
    print(prompt)
    ans = claude(prompt=prompt, image_list=[image_base64])
    print(ans)
    pass


if __name__ == "__main__":
    # prepare_image()

    caption_account_homepage_image()

    pass
