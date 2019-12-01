from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    body = serializers.CharField(min_length=5)

    class Meta:
        model = Offer
        fields = '__all__'

