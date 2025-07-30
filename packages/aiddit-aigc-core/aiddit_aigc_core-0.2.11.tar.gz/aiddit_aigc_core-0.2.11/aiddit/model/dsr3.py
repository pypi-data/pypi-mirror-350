import httpx
from volcenginesdkarkruntime import Ark

# Authentication
# 1.If you authorize your endpoint using an API key, you can set your api key to environment variable "ARK_API_KEY"
# or specify api key by Ark(api_key="${YOUR_API_KEY}").
# Note: If you use an API key, this API key will not be refreshed.
# To prevent the API from expiring and failing after some time, choose an API key with no expiration date.
# 2.If you authorize your endpoint with Volcengine Identity and Access Management（IAM),
# set your api key to environment variable "VOLC_ACCESSKEY", "VOLC_SECRETKEY"
# or specify ak&sk by Ark(ak="${YOUR_AK}", sk="${YOUR_SK}").
# To get your ak&sk, please refer to this document(https://www.volcengine.com/docs/6291/65568)
# For more information，please check this document（https://www.volcengine.com/docs/82379/1263279）
client = Ark(
    # The output time of the reasoning model is relatively long. Please increase the timeout period.
    timeout=httpx.Timeout(timeout=1800),
)


def deepseek_r3(prompt):
    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20250210210124-w2msk",
        messages=[
            {"role": "user", "content": f"{prompt}"},
        ],
    )

    return completion.choices[0].message.reasoning_content, completion.choices[0].message.content


def deepseek_r3_stream(prompt):
    # streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20250210210124-w2msk",
        messages=[
            {"role": "user", "content": f"{prompt}"},
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
            content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    return reasoning_content, content


def deepseek_r3_conversation_stream(messages):
    # streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20250210210124-w2msk",
        messages=messages,
        stream=True
    )
    reasoning_content = ""
    content = ""
    for chunk in completion:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            print(chunk.choices[0].delta.reasoning_content, end="")
        else:
            content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    return reasoning_content, content


if __name__ == "__main__":
    reason, ans = deepseek_r3_stream("对于一个小红书的图文帖子,进行创作脚本的拆解，我的目的为了拆解出一个脚本，然后根据这个脚本去还原这个帖子的内容，同时针对多个脚本再去聚类总结其脚本的特点。请从这个角度出发去定义脚本的结构。")
    pass
