from openai import OpenAI
import base64

openai_client = OpenAI(
    api_key="sk-ZdUMj9U0NAXCmiw_wglkmFv8jpaOQ_psosLuN6RSLtl2lj6RbUgkocdRaZY",
    base_url="https://openai.linktre.cc/v1"
)

if __name__ == "__main__":
    prompt = """
    Generate a photorealistic image of a gift basket on a white background 
    labeled 'Relax & Unwind' with a ribbon and handwriting-like font, 
    containing all the items in the reference pictures.
    """

    result = openai_client.images.edit(
        model="gpt-image-1-official",
        image=[
            open("/Users/nieqi/Downloads/body-lotion.png", "rb"),
            open("/Users/nieqi/Downloads/bath-bomb.png", "rb"),
            open("/Users/nieqi/Downloads/incense-kit.png", "rb"),
            open("/Users/nieqi/Downloads/soap.png", "rb"),
        ],
        prompt=prompt,
        timeout=60*10,
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open("gift-basket.png", "wb") as f:
        f.write(image_bytes)