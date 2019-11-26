from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import Offer
from .serializers import *
from .paginations import OfferPagination


# Create your views here.
class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer
    pagination_class = OfferPagination


@api_view(['GET'])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data.get('user')
        if not user:
            return Response({'response': 'error', 'message': 'No data found'})
        serializer = UserSerializerWithToken(data=user)

        if serializer.is_valid():
            saved_user = serializer.save()
        else:
            return Response({'response': 'error', 'message':serializer.errors})

        return Response({"response": 'success', 'message': 'user created successfully'})
