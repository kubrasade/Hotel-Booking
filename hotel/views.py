from rest_framework import generics
from .models import Hotel, Room
from .serializers import HotelSerializer,RoomSerializer

class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_object(self):
        return Hotel.objects.first()
    
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.filter(is_deleted=False).order_by("id")
    serializer_class = RoomSerializer


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.filter(is_deleted=False)
    serializer_class = RoomSerializer


class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        hotel = Hotel.objects.first()
        serializer.save(hotel=hotel)