# views.py
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, GeneratedImage
from .serializers import GeneratedImageSerializer
from sdapi.text2img import Text2Img
import os
from django.conf import settings
from PIL import Image
from io import BytesIO


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_image_view(request):
    user = request.user
    if user.points <= 0:
        return JsonResponse({'error': 'Insufficient points'}, status=400)

    # 获取请求中的参数
    prompt = request.data.get("prompt")
    negative_prompt = request.data.get("negative_prompt", "")
    steps = request.data.get("steps", 50)
    sampler_index = request.data.get("sampler_index", "Euler")
    cfg_scale = request.data.get("cfg_scale", 7.0)
    width = request.data.get("width", 512)
    height = request.data.get("height", 512)
    batch_size = request.data.get("batch_size", 1)
    n_iter = request.data.get("n_iter", 1)
    seed = request.data.get("seed", None)
    noise_settings = request.data.get("noise_settings", None)
    init_image = request.data.get("init_image", None)
    init_image_strength = request.data.get("init_image_strength", 0.75)
    mask = request.data.get("mask", None)
    mask_blur = request.data.get("mask_blur", 4)

    # 创建 Text2Img 实例
    text2img = Text2Img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        steps=steps,
        sampler_index=sampler_index,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        batch_size=batch_size,
        n_iter=n_iter,
        seed=seed,
        noise_settings=noise_settings,
        init_image=init_image,
        init_image_strength=init_image_strength,
        mask=mask,
        mask_blur=mask_blur
    )

    # 调用生成图像的函数
    img = text2img.generate_image_from_text()

    if img is None:
        return JsonResponse({'error': 'Failed to generate image'}, status=500)

    # 保存图像到指定文件夹
    now = datetime.now()
    time_str = now.strftime("%Y%m%d_%H%M%S")
    image_filename = f"{user.username}_{user.id}_{time_str}.png"
    image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', image_filename)
    img.save(image_path)

    # 将图像记录保存到数据库
    generated_image = GeneratedImage.objects.create(user=user, image=f'generated_images/{image_filename}')

    # 扣除点数
    user.points -= 1
    user.save()

    serializer = GeneratedImageSerializer(generated_image)
    return JsonResponse(serializer.data)
