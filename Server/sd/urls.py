# urls.py
from django.urls import path
from .views import text_to_img, get_models, get_config, set_config, get_schedulers, get_samplers, get_user_images

urlpatterns = [
    path('text2img/', text_to_img, name='text_to_img'),
    path('get_models/', get_models, name='get_models'),
    path('get_config/', get_config, name='get_config'),
    path('set_config/', set_config, name='set_config'),
    path('get_schedulers/', get_schedulers, name='get_schedulers'),
    path('get_samplers/', get_samplers, name='get_samplers'),
    path('images/', get_user_images, name='get_user_images'),
]
