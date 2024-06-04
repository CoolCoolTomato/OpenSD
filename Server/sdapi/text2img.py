import requests
import json
from PIL import Image
from io import BytesIO
import base64
from Server import settings


class Text2Img:
    def __init__(self,
        prompt,
        api_url=settings.SD_API_URL + "sdapi/v1/txt2img",
        negative_prompt="",
        steps=50,
        sampler_index="Euler",
        cfg_scale=7.0,
        width=512,
        height=512,
        batch_size=1,
        n_iter=1,
        seed=None,
        noise_settings=None,
        init_image=None,
        init_image_strength=0.75,
        mask=None,
        mask_blur=4
    ):
        self.prompt = prompt
        self.api_url = api_url
        self.negative_prompt = negative_prompt
        self.steps = steps
        self.sampler_index = sampler_index
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.seed = seed
        self.noise_settings = noise_settings
        self.init_image = init_image
        self.init_image_strength = init_image_strength
        self.mask = mask
        self.mask_blur = mask_blur

    def generate_image_from_text(self):
        data = {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "steps": self.steps,
            "sampler_index": self.sampler_index,
            "cfg_scale": self.cfg_scale,
            "width": self.width,
            "height": self.height,
            "batch_size": self.batch_size,
            "n_iter": self.n_iter,
            "seed": self.seed,
            "noise_settings": self.noise_settings,
            "init_image": self.init_image,
            "init_image_strength": self.init_image_strength,
            "mask": self.mask,
            "mask_blur": self.mask_blur
        }
        try:
            response = requests.post(self.api_url, json=data)

            if response.status_code == 200:
                response_data = response.json()
                img_data = base64.b64decode(response_data["images"][0])
                img = Image.open(BytesIO(img_data))
                return img
            else:
                print(f"Failed to generate image. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

# api = Text2Img(prompt="cat")
# image = api.generate_image_from_text()
# if image:
#     image.show()
#     # Optionally, save the image
#     image.save("generated_image.png")