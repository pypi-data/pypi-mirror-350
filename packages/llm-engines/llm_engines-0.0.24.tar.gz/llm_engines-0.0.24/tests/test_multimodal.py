from llm_engines import LLMEngine
from PIL import Image
import requests
from io import BytesIO
response = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")
image = Image.open(BytesIO(response.content)).resize((256, 256))
image.save("./test.jpg")
messages_with_image = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in the image?"
            },
            {
                "type": "image",
                "image": image
            }
        ]
    }
] # the 'image' type is not offical format of openai API, LLM-Engines will convert it into image_url type internally
messages_with_image_url = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in the image?"
            },
            {
                "type": "image_url",
                "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}
            }
        ]
    }
] # the 'image_url' type is the offical format of openai API
additional_args=[]
# engine="openai"; model_name="gpt-4o-mini"
# engine="claude"; model_name="claude-3-5-sonnet-20241022"
# engine="gemini"; model_name="gemini-2.0-flash"
# engine="grok"; model_name="grok-2-vision-latest"
# engine="sglang"; model_name="meta-llama/Llama-3.2-11B-Vision-Instruct"; additional_args=["--chat-template=llama_3_vision"] # refer to 
engine="vllm"; model_name="microsoft/Phi-3.5-vision-instruct"; additional_args=["--limit-mm-per-prompt", "image=2", "--max-model-len", "4096"] # refer to vllm serve api
llm = LLMEngine()
llm.load_model(
    model_name=model_name, 
    engine=engine, # or "vllm", "together", "mist
    use_cache=False,
    additional_args=additional_args,
)
response = llm.call_model(model_name, messages_with_image, temperature=0.0, max_tokens=None)
print(response)
response = llm.call_model(model_name, messages_with_image_url, temperature=0.0, max_tokens=None)
print(response)