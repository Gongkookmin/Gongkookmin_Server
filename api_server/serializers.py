from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
