from django.db import models
from user.models import CustomUser


class GeneratedImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='./')
    created_at = models.DateTimeField(auto_now_add=True)

