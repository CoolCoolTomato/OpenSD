import requests
import json
from PIL import Image
from io import BytesIO
import base64
from django.conf import settings


class Text2Img:
    def __init__(self,
        prompt,
        api_url=settings.SD_API_URL + "sdapi/v1/txt2img",
        negative_prompt="",
        seed=-1,
        sampler_name="",
        scheduler="",
        batch_size=1,
        n_iter=1,
        steps=20,
        cfg_scale=7.0,
        width=512,
        height=512,
        sampler_index="Euler",
        send_images=True,
        save_images=False,
    ):
        self.prompt = prompt
        self.api_url = api_url
        self.negative_prompt = negative_prompt
        self.seed = seed
        self.sampler_name = sampler_name
        self.scheduler = scheduler
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.sampler_index = sampler_index
        self.send_images = send_images
        self.save_images = save_images

    def generate_image_from_text(self):
        data = {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "sampler_name": self.sampler_name,
            "scheduler": self.scheduler,
            "batch_size": self.batch_size,
            "n_iter": self.n_iter,
            "steps": self.steps,
            "cfg_scale": self.cfg_scale,
            "width": self.width,
            "height": self.height,
            "sampler_index": self.sampler_index,
            "send_images": self.send_images,
            "save_images": self.save_images,
        }
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return response_data["images"]
            else:
                print(f"Failed to generate image. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

