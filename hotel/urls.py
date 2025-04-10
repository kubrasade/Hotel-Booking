from django.urls import path
from .views import (
    HotelDetailAPIView,
    RoomListAPIView,
    RoomDetailAPIView,
    RoomCreateAPIView,
    ReservationListAPIView,
    ReservationDetailAPIView,
    ReservationCreateAPIView,
    CancelReservationAPIView,
    monthly_availability
)

urlpatterns = [
    path("", HotelDetailAPIView.as_view(), name="hotel-detail"),
    path("rooms/", RoomListAPIView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailAPIView.as_view(), name="room-detail"),
    path("rooms/create/", RoomCreateAPIView.as_view(), name="room-create"),
    path("reservations/", ReservationListAPIView.as_view(), name="reservation-list"),
    path("reservations/<int:pk>/", ReservationDetailAPIView.as_view(), name="reservation-detail"),
    path("reservations/create/", ReservationCreateAPIView.as_view(), name="reservation-create"),
    path("reservations/cancel/", CancelReservationAPIView.as_view(), name="cancel-reservation"), 
    path('availability/monthly/', monthly_availability, name='monthly-availability'),

    ]
