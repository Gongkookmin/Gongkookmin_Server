from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from rest_framework_jwt import authentication
from jose import jwt

from .serializers import *
from .paginations import OfferPagination


# Create your views here.
class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
            return self.serializers.get(self.action,
                        self.serializers['default'])


class OfferViewSet(MultiSerializerViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication, )

    serializers = {
        'list': OfferMetaSerializer,
        'default': OfferFullSerializer,
    }

    def destroy(self, request, *args, **kwargs):
        user = request.user
        token = request.META["HTTP_AUTHORIZATION"]
        token = token.split()[-1]
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = get_object_or_404(User, pk=data["user_id"])

        try:
            instance = self.get_object()
            print(user)
            print(instance.owner)
            if user == instance.owner:
                self.perform_destroy(instance)
        except status.HTTP_404_NOT_FOUND:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyOffer(ListModelMixin, GenericAPIView):
    serializer_class = OfferMetaSerializer
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        offer = self.request.user.offers
        return offer.all()


class SearchOffer(ListModelMixin, GenericAPIView):
    serializer_class = OfferMetaSerializer
    pagination_class = OfferPagination
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        keyword = self.request.GET['keyword']
        search_offer = Offer.objects.filter(title__contains=keyword)
        return search_offer.all()
