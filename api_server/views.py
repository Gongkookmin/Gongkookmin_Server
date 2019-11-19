from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from .models import Offer
from .serializers import OfferSerializer

# Create your views here.
class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().order_by('-date_joined')
    serializer_class = OfferSerializer