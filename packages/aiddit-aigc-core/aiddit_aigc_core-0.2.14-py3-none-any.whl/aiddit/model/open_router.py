import logging

from openai import OpenAI
import os
import aiddit.utils as utils

from dotenv import load_dotenv

load_dotenv()

class OpenRouter:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY'),
        )

    def get_image_description(self, model, prompt, image_url_list, retry_cnt=0):
        messages = [
            {
                "type": "text",
                "text": prompt
            }
        ]

        if image_url_list is not None and len(image_url_list) > 0:
            seen = set()
            unique_image_urls = [url for url in image_url_list if not (url in seen or seen.add(url))]
            for image_url in unique_image_urls:
                resize_image_url = utils.oss_resize_image(image_url)
                print("resize_image_url ", resize_image_url)
                messages.append({
                    "type": "image_url",
                    "image_url": {
                        "url": resize_image_url
                    }
                })

        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": messages
                }
            ],
            max_completion_tokens=8096,
            temperature=0
        )

        if hasattr(completion, "error") and "message" in completion.error:
            error = completion.error
            if "Unknown MIME type" in error.get("message", ""):
                if retry_cnt < 3:
                    logging.error("OpenRouter error: %s ,retrying %d times", error, retry_cnt)
                    return self.get_image_description(model, prompt, image_url_list, retry_cnt + 1)
                else:
                    raise Exception(f"OpenRouter error: {error} ,after {retry_cnt} retries")
            raise Exception(f"OpenRouter error: {error}")

        if completion.choices is None or len(completion.choices) == 0:
            raise Exception(f"OpenRouter error: {completion}")

        if completion.choices[0].finish_reason == "length":
            raise Exception(f"OpenRouter error: reached  maximum number of tokens")

        return completion.choices[0].message.content

    def claude_3_5_sonnet(self, prompt: str | None = None, image_url_list: list | None = None):
        return self.get_image_description("anthropic/claude-3.5-sonnet", prompt, image_url_list)

    def claude_3_5_sonnet_conversation(self, model, history_messages):
        completion = self.client.chat.completions.create(
            model=model,
            messages=history_messages
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    open_router = OpenRouter()
    print(open_router.claude_3_5_sonnet())
