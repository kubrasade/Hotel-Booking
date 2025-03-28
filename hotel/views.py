from rest_framework import generics, permissions, status
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer,RoomSerializer, ReservationSerializer, ReservationStatusSerializer
from .services import ReservationService  


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

class ReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-created_at")


class ReservationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
    
class CancelReservationAPIView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return ReservationService.cancel_reservation_and_respond(request, instance)