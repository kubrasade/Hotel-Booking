from django.urls import path
from .views import (
    HotelDetailAPIView,
    RoomListAPIView,
    RoomDetailAPIView,
    RoomCreateAPIView,
)

urlpatterns = [
    path("", HotelDetailAPIView.as_view(), name="hotel-detail"),
    path("rooms/", RoomListAPIView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailAPIView.as_view(), name="room-detail"),
    path("rooms/create/", RoomCreateAPIView.as_view(), name="room-create"),
    ]
