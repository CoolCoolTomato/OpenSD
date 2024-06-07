# views.py
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
from sdapi.img2img import Img2Img

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
    image_list = [{'id': img['id'], 'url': str(img['image'])} for img in serializer.data]
    return JsonResponse(image_list, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user_image(request):
    user = request.user
    image_id = request.data.get('image_id')

    if not image_id:
        return JsonResponse({'error': 'Image ID is required'}, status=400)

    # 获取图片对象，确保它属于当前用户
    image = get_object_or_404(GeneratedImage, id=image_id, user=user)

    # 删除图片文件
    image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
    if os.path.exists(image_path):
        os.remove(image_path)

    # 删除数据库中的记录
    image.delete()

    return JsonResponse({'message': 'Image deleted successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def img_to_img(request):
    user = request.user
    if user.points <= 0:
        return JsonResponse({'error': 'Insufficient points'}, status=400)

    # 获取请求中的参数并设置默认值
    init_images_base64 = request.data.get("init_images")
    if not init_images_base64:
        return JsonResponse({'error': 'Initial images are required'}, status=400)

    params = {
        "init_images": init_images_base64,
        "prompt": request.data.get("prompt", ""),
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
        "denoising_strength": request.data.get("denoising_strength", 0.75),
        "sampler_index": request.data.get("sampler_index", "Euler"),
        "send_images": request.data.get("send_images", True),
        "save_images": request.data.get("save_images", False),
    }

    # 创建 Img2Img 实例
    img2img = Img2Img(**params)

    # 调用生成图像的函数
    response_data = img2img.generate_image_from_image()

    if response_data is None:
        return JsonResponse({'error': 'Failed to generate image'}, status=500)

    img_path_list = []
    for i, img_base64 in enumerate(response_data):
        # 保存图像到指定文件夹
        img_data = base64.b64decode(img_base64)
        img = Image.open(BytesIO(img_data))
        now = datetime.now()
        time_str = now.strftime("%Y%m%d%H%M%S")
        image_filename = f"{user.id}_{time_str}_{str(i)}.png"
        image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', image_filename)
        img.save(image_path)

        # 将图像记录保存到数据库
        generated_image = GeneratedImage.objects.create(user=user, image=f'generated_images/{image_filename}')
        img_path_list.append(settings.MEDIA_URL + 'generated_images/' + image_filename)

    # 扣除点数
    user.points -= 1
    user.save()

    return JsonResponse(img_path_list, safe=False)
