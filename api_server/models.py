from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Offer(models.Model):
    image = models.ImageField(upload_to="offer_images", null=True, blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors = [Thumbnail(100, 100)],
        format='JPEG',
        options={'quality':60}
    )
    owner = models.ForeignKey(User, related_name="offers", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    open_kakao_link = models.URLField()

    class Meta:
        unique_together = ["id", "owner"]
        ordering = ["-id"]

    def __str__(self):
        return self.title