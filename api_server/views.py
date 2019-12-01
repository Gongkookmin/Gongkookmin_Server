from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework_jwt import authentication

from .serializers import *
from .paginations import OfferPagination


# Create your views here.
class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication, )


class MyOffer(ListModelMixin, GenericAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        offer = self.request.user.offers
        return offer.all()


class SearchOffer(ListModelMixin, GenericAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        keyword = self.request.GET['keyword']
        search_offer = Offer.objects.filter(title__contains=keyword)
        return search_offer.all()
