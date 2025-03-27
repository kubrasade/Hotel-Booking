from rest_framework import generics
from .models import Hotel
from .serializers import HotelSerializer

class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_object(self):
        return Hotel.objects.first()