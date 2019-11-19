from rest_framework import serializers

from .models import Offer


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'