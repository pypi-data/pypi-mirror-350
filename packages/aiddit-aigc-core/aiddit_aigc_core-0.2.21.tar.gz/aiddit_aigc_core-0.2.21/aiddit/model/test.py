# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from aiddit.model.google_genai import upload_file

load_dotenv()
api_key = os.getenv("google_genai_api_key")

# Define the function declaration for the model
create_chart_function = {
    "name": "create_image_by_description",
    "description": "根据用户输入的描述进行图片生成",
    "parameters": {
        "type": "object",
        "properties": {
            "image_description": {
                "type": "string",
                "description": "图片生成的描述.",
            },
        },
        "required": ["image_description"],
    },
}


def model_generate(ask_contents):
    client = genai.Client(api_key=api_key)
    tools = types.Tool(function_declarations=[create_chart_function])
    config = types.GenerateContentConfig(tools=[tools])

    # Send request with function declarations
    response = client.models.generate_content(
        model="gemini-2.0-flash",
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


if __name__ == "__main__":
    contents = []

    ask_content = types.Content(
        role="user",
        parts=[types.Part(text="利用工具`create_image_by_description` 根据以下描述 直接生成图片，不用确认 \n\n猫狗在一起玩耍")]
    )

    contents.append(ask_content)

    response_content = model_generate(contents)

    print("response_content", response_content)


    if response_content.parts:
        for part in response_content.parts:
            if part.function_call is not None:
                function_call = part.function_call
                args = function_call.args
                image_description = args["image_description"]
                print(f"Function call: {function_call.name}")
                print(f"Arguments: {args}")

                contents.append(types.Content(role="model", parts=[types.Part(function_call=function_call)]))

                if function_call.name == "create_image_by_description":
                    # print(f"Generating image with description: {image_description}")
                    # image_url = "http://res.cybertogether.net/gpt4oGenerateImageTools/20250515073847363188946.png?x-oss-process=image/resize,w_400"
                    # f=  upload_file(image_url)
                    # tools_content = types.Content(
                    #     role="user",
                    #     parts=[types.Part.from_uri(file_uri=f.uri, mime_type=f.mime_type)]
                    # )
                    # contents.append(tools_content)

                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": "http://res.cybertogether.net/gpt4oGenerateImageTools/20250515073847363188946.png?x-oss-process=image/resize,w_400"},
                    )

                    contents.append(
                        types.Content(role="user", parts=[function_response_part]))  # Append the function response

                    response_content = model_generate(contents)
                    print("response_content", response_content)
    pass
