"""Gongkookmin_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.routers import DefaultRouter
from api_server.views import *
from rest_framework.schemas import get_schema_view

router = DefaultRouter()
router.register('offer', OfferViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('my-offer', MyOffer.as_view()),
    path('search', SearchOffer.as_view()),

    path('openapi', get_schema_view(
        title="Gongkookmin",
        description="API for all things of this project",
        version="1.0.0"
    ), name="openapi-schema")
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
