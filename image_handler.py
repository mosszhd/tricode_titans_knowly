import ollama
from prompt_templates import LLAVA_SYSTEM_PROMPT
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def multimodal_response(prompt:str, image_path):
    stream = ollama.generate(model=config["image_model"]["model_name"],
                             prompt=prompt,
                             system=LLAVA_SYSTEM_PROMPT,
                             stream=True,
                             images=[image_path])
    for chunk in stream:
        yield chunk["response"]