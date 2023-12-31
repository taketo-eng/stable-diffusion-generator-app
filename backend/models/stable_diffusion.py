import base64
import io
import os

from fastapi.encoders import jsonable_encoder
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
import torch
from torch import autocast


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

model_id = "Ojimi/anime-kawai-diffusion"

def generate_image(prompt='best quality, background illustration, Uyuni salt lake', num_of_images=1):
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        use_auth_token=ACCESS_TOKEN,
    )
    pipe = pipe.to("cuda")

    base64_images = []
    for _ in range(num_of_images):
        with autocast('cuda'):
            image = pipe(prompt,
                        width=512,
                        height=512,
                        num_inference_steps=50,
                        ).images[0]
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='png')
        base64_image = jsonable_encoder(img_bytes.getvalue(), custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')})
        base64_images.append(base64_image)
    return base64_images