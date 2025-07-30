import os
import google.generativeai as genai


os.environ['http_proxy'] = 'http://127.0.0.1:8118'
os.environ['https_proxy'] = 'http://127.0.0.1:8118'
os.environ['all_proxy'] = 'socks5://127.0.0.1:8119'

genai.configure(api_key="AIzaSyDP8v6Q_vIYH9dZIPqSShB0GNVx21RAV4Q")

# print("List of models that support generateContent:\n")
# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)
#
# print("List of models that support embedContent:\n")
# for m in genai.list_models():
#     if "embedContent" in m.supported_generation_methods:
#         print(m.name)

imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

result = imagen.generate_images(
    prompt="Fuzzy bunnies in my kitchen",
    number_of_images=2,
    safety_filter_level="block_only_high",
    person_generation="allow_adult",
    aspect_ratio="3:4",
    negative_prompt="Outside",
)

for image in result.images:
    print(image)

# Open and display the image using your local operating system.
for image in result.images:
    image._pil_image.show()
