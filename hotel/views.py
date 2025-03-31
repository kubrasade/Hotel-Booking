from rest_framework import generics, permissions, status
from .models import Hotel, Room, Reservation
from .serializers import (
    HotelSerializer,
    RoomSerializer, 
    ReservationSerializer, 
    ReservationStatusSerializer,
    CancelReservationInputSerializer)
from rest_framework.response import Response

class HotelDetailAPIView(generics.RetrieveAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def get_object(self):
        return Hotel.objects.first()
    
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.filter(is_deleted=False).order_by("id")
    serializer_class = RoomSerializer

class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.filter(is_deleted=False)
    serializer_class = RoomSerializer

class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes= [permissions.IsAdminUser]
    queryset = Room.objects.all()

    def perform_create(self, serializer):
        hotel = Hotel.objects.first()
        serializer.save(hotel=hotel)

class ReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes= [permissions.IsAdminUser]
    queryset = Reservation.objects.all().order_by("-created_at")

class ReservationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes= [permissions.IsAdminUser]
    queryset = Reservation.objects.all()

class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    
class CancelReservationAPIView(generics.GenericAPIView):
    serializer_class = CancelReservationInputSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save() 

        output_serializer = ReservationStatusSerializer(reservation, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)