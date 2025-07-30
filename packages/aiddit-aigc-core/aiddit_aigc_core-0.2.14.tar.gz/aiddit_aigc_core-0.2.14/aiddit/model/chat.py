from openai import OpenAI
from aiddit.model.open_router import OpenRouter
import logging
import sseclient
import requests
import json
import aiddit.utils as utils
import aiddit.model.google_genai as google_genai
from dotenv import load_dotenv
import os

load_dotenv()

open_api_key = os.getenv("OPENAI_API_KEY")

deepseek_api_key = os.getenv("deepseek_api_key")
deepseek_aliyun_api_key = os.getenv("deepseek_aliyun_api_key")
deepseek_tencent_api_key = os.getenv("deepseek_tencent_api_key")
tencent_cloud_bot_app_key = os.getenv("tencent_cloud_bot_app_key")

open_router = OpenRouter()
from tenacity import retry, stop_after_attempt, wait_fixed

openai_client = OpenAI(api_key=open_api_key)


def pack_image_content(image_list, img_num=100):
    image_content = []
    image_url_set = set([])
    for image_url in image_list[:img_num]:
        if image_url not in image_url_set:
            image_content.append({"type": "image_url", "image_url": {"detail": "low", "url": image_url}})
            image_url_set.add(image_url)
    return image_content


def claude35(prompt, image_list=None):
    return open_router.claude_3_5_sonnet(prompt, image_list)


def claude35_conversation(history_messages):
    return open_router.claude_3_5_sonnet_conversation("anthropic/claude-3.5-sonnet", history_messages)


def claude(prompt, image_list=None, model="claude-3-5-sonnet-20241022", temperature=0.0):
    ans = claude35(prompt, image_list)
    return ans


def gpt4o(prompt, image_list=None, model="gpt-4o-2024-11-20	"):
    note_data = [{"text": prompt, "type": "text"}]

    if image_list is not None and len(image_list) > 0:
        image_content = pack_image_content(image_list)
        note_data = image_content + [{"text": prompt, "type": "text"}]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": note_data
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def gemini(prompt, model="gemini-2.0-flash", response_mime_type="application/json", images=None, temperature=0):
    # return gemini_chat.start_chat(prompt, model_name=model, response_mime_type=response_mime_type, images=images,
    #                               temperature=temperature)
    return google_genai.google_genai(prompt, model_name=model, response_mime_type=response_mime_type, images=images,
                                     temperature=temperature)


def gemini_google_genai(prompt, model="gemini-2.0-flash", response_mime_type="application/json", images=None,
                        temperature=0):
    return google_genai.google_genai(prompt, model_name=model, response_mime_type=response_mime_type, images=images,
                                     temperature=temperature)


def deepseek_chat(prompt, temperature=1, response_format_json=False):
    return deepseek(prompt, model="deepseek-chat", temperature=temperature, response_format_json=response_format_json)


def deepseek_r1(prompt, temperature=1):
    return deepseek(prompt, model="deepseek-reasoner", temperature=temperature,
                    response_format_json=False)


def deepseek(prompt, model="deepseek-chat", temperature=1, response_format_json=True, try_cnt=0):
    client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{prompt}"},
            ],
            response_format={
                "type": "json_object" if response_format_json else "text"
            },
            temperature=temperature,
            stream=False
        )
    except Exception as e:
        logging.error(e)
        print(str(e))
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            if try_cnt >= 3:
                logging.error(f"Deepseek {model} failed after {try_cnt} tries: {e}")
                raise e
            else:
                return deepseek(prompt, model=model, temperature=temperature, response_format_json=response_format_json,
                                try_cnt=try_cnt + 1)
        else:
            raise e

    if hasattr(response.choices[0].message, 'reasoning_content') \
            and response.choices[0].message.reasoning_content is not None:
        return response.choices[0].message.content, response.choices[0].message.reasoning_content

    return response.choices[0].message.content


def aliyun_deepseek_r1(prompt):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=deepseek_aliyun_api_key,
        # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        stream=True
    )

    reasoning_content = ""
    content = ""
    for chunk in completion:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            print(chunk.choices[0].delta.reasoning_content, end="")
        else:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
    return reasoning_content, content


def tencent_cloud_deepseek_r1(prompt):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=deepseek_tencent_api_key,
        # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://api.lkeap.cloud.tencent.com/v1",
    )

    completion = client.chat.completions.create(
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'user', 'content': prompt}
        ]
        , stream=True
    )

    reasoning_content = ""
    content = ""
    for chunk in completion:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            print(chunk.choices[0].delta.reasoning_content, end="")
        else:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
    return reasoning_content, content


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def tencent_cloud_sse_deepseek_r1_xxx(prompt):
    req_data = {
        "content": "",
        "bot_app_key": "nDOFFbpN",
        "visitor_biz_id": "nieqi111",
        "session_id": utils.uuid_str(),
        "streaming_throttle": 1
    }

    reasoning_content = ""
    content = ""
    references = []

    try:
        while True:
            req_data["content"] = prompt
            resp = requests.post("https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse", data=json.dumps(req_data),
                                 stream=True, headers={"Accept": "text/event-stream"})
            # print(f"resp:{resp.text}")
            client = sseclient.SSEClient(resp)
            for ev in client.events():
                # print(f'event:{ev.event}, "data:"{ev.data}')
                data = json.loads(ev.data)
                if ev.event == "reply":
                    if not data["payload"]["is_final"]:  # 服务端event传输完毕；服务端的回复是流式的，最后一条回复的content，包含完整内容
                        # print(f'is_final, event:{ev.event}, "content:"{data["payload"]["content"]}')
                        ans_content = data["payload"]["content"]
                        print(ans_content.replace(content, ''), end="")
                        content = ans_content
                        if content == "抱歉，当前咨询量大，请重新再问我一次":
                            print("")
                            raise Exception(content)
                    else:
                        break
                elif ev.event == "thought":
                    if data.get("type") == "thought":
                        rc = data.get("payload").get("procedures")[0]["debugging"]["content"]
                        print(rc.replace(reasoning_content, ''), end="")
                        reasoning_content = rc
                elif ev.event == "reference":
                    references = data["references"]
                elif ev.event == "error":
                    raise Exception(data['error'])
                else:
                    print(f'event:{ev.event}, "data:"{ev.data}')
    except Exception as e:
        print(f"tencent_cloud_sse_deepseek_r1 error : {str(e)}")
        raise


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def tencent_cloud_sse_deepseek_r1(prompt):
    req_data = {
        "content": "",
        "bot_app_key": tencent_cloud_bot_app_key,
        "visitor_biz_id": "nieqi111",
        "session_id": utils.uuid_str(),
        "streaming_throttle": 1
    }

    reasoning_content = ""
    content = ""
    references = []

    try:
        req_data["content"] = prompt
        # print(f'req_data:{req_data}')
        resp = requests.post("https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse", data=json.dumps(req_data),
                             stream=True, headers={"Accept": "text/event-stream"})
        # print(f"resp:{resp.text}")
        client = sseclient.SSEClient(resp)
        for ev in client.events():
            # print(f'event:{ev.event}, "data:"{ev.data}')
            data = json.loads(ev.data)
            if ev.event == "reply":
                if data["payload"]["is_from_self"]:  # 自己发出的包
                    print(f'is_from_self, event:{ev.event}, "content:"{data["payload"]["content"]}')
                elif data["payload"]["is_final"]:  # 服务端event传输完毕；服务端的回复是流式的，最后一条回复的content，包含完整内容
                    print(f'is_final, event:{ev.event}, "content:"{data["payload"]["content"]}')
                    content = {data["payload"]["content"]}
            elif ev.event == "thought":
                if data.get("type") == "thought":
                    rc = data.get("payload").get("procedures")[0]["debugging"]["content"]
                    print(rc.replace(reasoning_content, ''), end="")
                    reasoning_content = rc
            elif ev.event == "reference":
                references = data["references"]
            elif ev.event == "error":
                raise Exception(data['error'])
            else:
                print(f'event:{ev.event}, "data:"{ev.data}')
    except Exception as e:
        print(e)

    print(reasoning_content)
    print(references)
    print(content)


if __name__ == "__main__":
    # ans = gemini(prompt="", images=["https://sns-webpic.xhscdn.com/spectrum/1040g34o31aeofg4s6o0g5pbq9hhn36aunlpudvo?imageView2/2/w/0/format/jpg/v3"])
    # print(ans)

    # ans = caption(
    #     "https://sns-webpic.xhscdn.com/spectrum/1040g34o31aeofg4s6o0g5pbq9hhn36aunlpudvo?imageView2/2/w/0/format/jpg/v3")

    # ans = gpt4o(prompt="请用中文详细这张图片，包括图片中的所有细节，只描述客观事实，不要加入任何'主观'评价性语言，不要其他有任何多余的解释和无关的信息输出。请直接输出结果"
    #             , image_list=["https://sns-webpic.xhscdn.com/spectrum/1040g34o31aeofg4s6o0g5pbq9hhn36aunlpudvo?imageView2/2/w/0/format/jpg/v3"])
    # print(ans)

    import image_article_comprehension.aiddit.model.dsr3 as dsr3

    ans_reason, ans = dsr3.deepseek_r3_stream("""
""")

    # tencent_cloud_sse_deepseek_r1("简单解释外汇对普通人的影响")

    # ans = claude("描述这张图片", ["http://res.cybertogether.net/aimodel/openai/image/20240924124133454622656.png"])

    pass
