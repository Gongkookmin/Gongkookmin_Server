from .models import Offer, Image
from rest_auth.serializers import LoginSerializer
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers, exceptions

import ast, json
from jose import jwt

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class OfferMetaSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", allow_blank=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d-%H:%M")

    class Meta:
        model = Offer
        fields = ("id", "owner", "owner_name", "title", "created_at")


class OfferFullSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    body = serializers.CharField(min_length=5)
    owner_name = serializers.CharField(required=False, source="owner.username", allow_blank=True)
    owner = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d-%H:%M")

    class Meta:
        model = Offer
        fields = ("id", "owner", "owner_name", "title", "body", "created_at", "open_kakao_link")

    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            user = request.user
        token = request.META["HTTP_AUTHORIZATION"]
        token = token.split()[-1]
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = get_object_or_404(User, pk=data["user_id"])
        return Offer.objects.create(owner=user, **validated_data)


# 메일 인증을 안했을 때, 비밀번호, 아이디가 틀렸을 때 에러메시지 변경을 위해 생성
class CustomLoginSerializer(LoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = "이메일(아이디) 혹은 비밀번호가 틀립니다."
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        email_address = user.emailaddress_set.get(email=user.email)
        if not email_address.verified:
            raise serializers.ValidationError("이메일을 확인하시고 이메일 인증을 완료해주세요.")

        attrs['user'] = user
        return attrs
