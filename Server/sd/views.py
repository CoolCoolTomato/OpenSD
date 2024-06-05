# views.py
from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import GeneratedImage
from PIL import Image
from io import BytesIO
import base64
from .serializers import GeneratedImageSerializer
from sdapi.text2img import Text2Img
from django.conf import settings
import os
from sdapi.options import Options
from sdapi.get_models import GetModels
from sdapi.schedulers import Schedulers
from sdapi.samplers import Samplers

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def text_to_img(request):
    user = request.user
    if user.points <= 0:
        return JsonResponse({'error': 'Insufficient points'}, status=400)

    # 获取请求中的参数并设置默认值
    params = {
        "prompt": request.data.get("prompt"),
        "negative_prompt": request.data.get("negative_prompt", ""),
        "seed": request.data.get("seed", -1),
        "sampler_name": request.data.get("sampler_name", ""),
        "scheduler": request.data.get("scheduler", ""),
        "batch_size": request.data.get("batch_size", 1),
        "n_iter": request.data.get("n_iter", 1),
        "steps": request.data.get("steps", 20),
        "cfg_scale": request.data.get("cfg_scale", 7.0),
        "width": request.data.get("width", 512),
        "height": request.data.get("height", 512),
        "sampler_index": request.data.get("sampler_index", "Euler a"),
        "send_images": request.data.get("send_images", True),
        "save_images": request.data.get("save_images", False),
    }

    # 创建 Text2Img 实例
    text2img = Text2Img(**params)

    # 调用生成图像的函数
    response_data = text2img.generate_image_from_text()

    if response_data is None:
        return JsonResponse({'error': 'Failed to generate image'}, status=500)

    img_path_list = []
    for i, j in enumerate(response_data):
        # 保存图像到指定文件夹
        img_data = base64.b64decode(j)
        img = Image.open(BytesIO(img_data))
        now = datetime.now()
        time_str = now.strftime("%Y%m%d%H%M%S")
        image_filename = f"{user.id}{time_str}{str(i)}.png"
        image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', image_filename)
        img.save(image_path)

        # 将图像记录保存到数据库
        generated_image = GeneratedImage.objects.create(user=user, image=f'generated_images/{image_filename}')
        img_path_list.append(settings.MEDIA_URL + 'generated_images/' + image_filename)

    # 扣除点数
    user.points -= 1
    user.save()

    return JsonResponse(img_path_list, safe=False)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_models(request):
    getModels = GetModels()
    models = getModels.get_models()
    return JsonResponse(models, safe=False)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_config(request):
    options = Options()
    config = options.get_config()
    return JsonResponse(config, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_config(request):
    options = Options()
    params = request.data
    res = options.set_config(params)
    return JsonResponse(res, safe=False)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_schedulers(request):
    schedulers = Schedulers()
    config = schedulers.get_schedulers()
    return JsonResponse(config, safe=False)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_samplers(request):
    samplers = Samplers()
    config = samplers.get_samplers()
    return JsonResponse(config, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    images = GeneratedImage.objects.filter(user=user)
    serializer = GeneratedImageSerializer(images, many=True)
    image_urls = [str(img['image']) for img in serializer.data]
    return JsonResponse(image_urls, safe=False)
