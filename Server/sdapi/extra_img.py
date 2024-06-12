import requests
from django.conf import settings


class ExtraImage:
    def __init__(self,
                 api_url=settings.SD_API_URL + "sdapi/v1/extra-single-image",
                 resize_mode=0,
                 show_extras_results=True,
                 gfpgan_visibility=0,

                 codeformer_visibility=0,
                 codeformer_weight=0,

                 upscaling_resize=2,

                 upscaling_resize_w=512,
                 upscaling_resize_h=512,
                 upscaling_crop=True,

                 upscaler_1="None",
                 upscaler_2="None",
                 extras_upscaler_2_visibility=0,
                 upscale_first=False):
        self.api_url = api_url
        self.resize_mode = resize_mode
        self.show_extras_results = show_extras_results
        self.gfpgan_visibility = gfpgan_visibility
        self.codeformer_visibility = codeformer_visibility
        self.codeformer_weight = codeformer_weight
        self.upscaling_resize = upscaling_resize
        self.upscaling_resize_w = upscaling_resize_w
        self.upscaling_resize_h = upscaling_resize_h
        self.upscaling_crop = upscaling_crop
        self.upscaler_1 = upscaler_1
        self.upscaler_2 = upscaler_2
        self.extras_upscaler_2_visibility = extras_upscaler_2_visibility
        self.upscale_first = upscale_first

    def enhance_image(self, image_base64):
        data = {
            "resize_mode": self.resize_mode,
            "show_extras_results": self.show_extras_results,
            "gfpgan_visibility": self.gfpgan_visibility,
            "codeformer_visibility": self.codeformer_visibility,
            "codeformer_weight": self.codeformer_weight,
            "upscaling_resize": self.upscaling_resize,
            "upscaling_resize_w": self.upscaling_resize_w,
            "upscaling_resize_h": self.upscaling_resize_h,
            "upscaling_crop": self.upscaling_crop,
            "upscaler_1": self.upscaler_1,
            "upscaler_2": self.upscaler_2,
            "extras_upscaler_2_visibility": self.extras_upscaler_2_visibility,
            "upscale_first": self.upscale_first,
            "image": image_base64
        }
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return response_data["image"]
            else:
                print(f"Failed to enhance image. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
