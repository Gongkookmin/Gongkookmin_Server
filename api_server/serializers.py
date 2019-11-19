from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Offer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Offer
        fields = '__all__'