from tenacity import retry, stop_after_attempt, wait_fixed

from aiddit.api.xhs_api import _get_xhs_account_info, _get_xhs_account_note_list, _get_note_detail_by_id
import aiddit.api.topic.prompt as prompt
import aiddit.model.google_genai as google_genai
import aiddit.utils as utils
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
import aiddit.api.topic.topic_generator as topic_generator
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("google_genai_api_key")

prompt_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/agent/agent_prompt_backup/topic_generate_agent_v4.md"
generate_instruction_prompt = utils.read_file_as_string(prompt_path)

stimulus_source_determination = {
    "name": "stimulus_source_determination",
    "description": "基于人设的选题创作，判断特定刺激源是否能与人设进行结合，判断人设基刺激源能否产生合适的选题",
    "parameters": {
        "type": "object",
        "properties": {
            "xhs_user_id": {
                "type": "string",
                "description": "小红书博主的ID.",
            },
            "reference_note_id": {
                "type": "string",
                "description": "刺激源内容的ID.",
            }
        },
        "required": ["xhs_user_id", "reference_note_id"],
    },
}


def model_request(ask_contents):
    client = genai.Client(api_key=api_key)
    tools = types.Tool(function_declarations=[stimulus_source_determination])
    config = types.GenerateContentConfig(tools=[tools], system_instruction=generate_instruction_prompt)

    # Send request with function declarations
    response = client.models.generate_content(
        model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
        contents=ask_contents,
        config=config,
    )

    response_parts = []
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
            response_parts.append(types.Part(text=part.text))
        elif part.function_call is not None:
            function_call = part.function_call
            response_parts.append(types.Part(function_call=function_call))
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
        else:
            print("Unknown part:", part)

    return types.Content(role="model", parts=response_parts)


def generate_topic(xhs_user_id: str, xhs_reference_note_id: str):
    conversation_contents = []

    user_input = f"小红书user_id: {xhs_user_id} , 刺激源{xhs_reference_note_id}"

    ask_content = types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    )
    conversation_contents.append(ask_content)

    response_content = model_request(ask_content)
    conversation_contents.append(response_content)
    print("response_content", response_content)

    if response_content.parts:
        for part in response_content.parts:
            if part.function_call is not None:
                function_call = part.function_call
                args = function_call.args
                print(f"Function call: {function_call.name}")
                print(f"Arguments: {args}")

                conversation_contents.append(
                    types.Content(role="model", parts=[types.Part(function_call=function_call)]))

                if function_call.name == "stimulus_source_determination":
                    user_id = args["xhs_user_id"]
                    reference_note_id = args["reference_note_id"]
                    ans = topic_generator.reference_note_available(user_id, reference_note_id)

                    if "无法产生选题" in ans:
                        raise Exception("无法产生选题")

                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": ans},
                    )

                    conversation_contents.append(
                        types.Content(role="user", parts=[function_response_part]))  # Append the function response

                    response_content = model_request(conversation_contents)
                    print("response_content", response_content)


if __name__ == "__main__":
    ans = generate_topic("615657520000000002026e7c", "6807744b000000001b03d943")
    pass
