from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Offer, Image


class OfferAdmin(admin.ModelAdmin):
    # list_display = ('admin_thumbnail', 'title',  'owner', 'open_kakao_link', 'created_at', 'updated_at', 'body')
    # admin_thumbnail = AdminThumbnail(image_field='images.0.thumbnail')
    list_display = ('title',  'owner', 'open_kakao_link', 'created_at', 'updated_at', 'body', 'get_images')

    def get_images(self, obj):
        try:
            return obj.images.image
        except:
            return None


admin.site.register(Offer, OfferAdmin)
admin.site.register(Image)