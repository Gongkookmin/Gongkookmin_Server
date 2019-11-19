from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Offer


class OfferAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title',  'owner', 'open_kakao_link', 'created_at', 'updated_at', 'body')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')


admin.site.register(Offer, OfferAdmin)