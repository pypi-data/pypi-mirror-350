import requests
import json
import uuid


def text_to_image(prompt):
    url = "http://aigc-api.cybertogether.net/aigc/infrastructure/whisk/generateImageByPrompt"

    if prompt is None or prompt == "":
        raise Exception("prompt is empty")

    payload = json.dumps({
        "prompt": prompt,
        "bizId": f"nieqi-local-{uuid.uuid4()}"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # {"code":0,"msg":"success","data":"http://res.cybertogether.net/image/whisk/361af40cc07341848fcfdd27ac3cd507.png"}
    # print(response.text)

    return response.text


# 主函数
if __name__ == '__main__':
    text_to_image("")
