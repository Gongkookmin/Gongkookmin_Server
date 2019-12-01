from .models import Offer, Image
from rest_auth.serializers import LoginSerializer
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions

UserModel = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    body = serializers.CharField(min_length=5)

    class Meta:
        model = Offer
        fields = ("title", "body", "created_at", "open_kakao_link")

    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            user = request.user
        token = request.META["Authorization"]
        # validated_data.owner()
        print(type(validated_data))
        return Offer(**validated_data)


# 메일 인증을 안했을 때, 비밀번호, 아이디가 틀렸을 때 에러메시지 변경을 위해 생성
class CustomLoginSerializer(LoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = "이메일(아이디) 혹은 비밀번호가 틀립니다."
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError("이메일을 확인하시고 이메일 인증을 완료해주세요.")

        attrs['user'] = user
        return attrs
