from django import forms
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.compat import force_str, ugettext_lazy as _


class OnlyForKookminAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        email_domain = email.split("@")[1]
        allowed_list = list(settings.EMAIL_DOMAIN_RESTRICTION_LIST)
        if email_domain not in allowed_list:
            raise forms.ValidationError("국민대학교 메일로만 가입할 수 있습니다.")
        return email

    def clean_username(self, username, shallow=False):
        if len(username) < 2:
            raise forms.ValidationError("닉네임은 두 글자 이상이어야 합니다.")
        super().clean_username(username, shallow)
        return username