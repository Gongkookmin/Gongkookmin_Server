from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

from .models import Offer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name')


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        jwt_payload_handler = settings.JWT_AUTH['JWT_PAYLOAD_HANDLER']
        jwt_encode_handler = settings.JWT_AUTH['JWT_ENCODE_HANDLER']

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name', 'last_name')



class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'