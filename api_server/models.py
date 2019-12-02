from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.conf import settings
from django.contrib.auth import get_user_model

import uuid
import os

User = get_user_model()


# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('offer_images', filename)


class Offer(models.Model):
    owner = models.ForeignKey(User, blank=True, related_name="offers", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=400)
    open_kakao_link = models.URLField()
    expires = models.CharField(max_length=10, default="none")
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 60}
    )
    image2 = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=get_file_path, blank=True, null=True)

    class Meta:
        unique_together = ["id", "owner"]
        ordering = ["-id"]

    def __str__(self):
        return self.title


class Image(models.Model):
    offer = models.ForeignKey(Offer, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="offer_images", null=True, blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors = [Thumbnail(100, 100)],
        format='JPEG',
        options={'quality':60}
    )

    def __str__(self):
        return self.image.path
