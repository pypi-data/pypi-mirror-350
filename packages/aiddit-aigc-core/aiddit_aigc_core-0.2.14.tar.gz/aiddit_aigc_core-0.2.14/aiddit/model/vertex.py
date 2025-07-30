import vertexai
from vertexai.generative_models import GenerativeModel
import os

os.environ['http_proxy'] = 'http://127.0.0.1:8118'
os.environ['https_proxy'] = 'http://127.0.0.1:8118'
os.environ['all_proxy'] = 'socks5://127.0.0.1:8119'

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"
# vertexai.init(project="starlit-road-423411-v7", location="us-central1")
#
# model = GenerativeModel("gemini-1.5-flash-002")
#
# response = model.generate_content(
#     "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
# )
#
# print(response.text)

from anthropic import AnthropicVertex

LOCATION="us-east5" # or "europe-west1"

client = AnthropicVertex(region=LOCATION, project_id="xiaohui-local")

message = client.messages.create(
  max_tokens=1024,
  messages=[
    {
      "role": "user",
      "content": "Send me a recipe for banana bread.",
    }
  ],
  model="claude-3-5-sonnet-v2@20241022",
)
print(message.model_dump_json(indent=2))