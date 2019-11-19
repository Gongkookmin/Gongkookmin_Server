from rest_framework.viewsets import ModelViewSet

from .models import Offer
from .serializers import OfferSerializer
from .paginations import OfferPagination


# Create your views here.
class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
