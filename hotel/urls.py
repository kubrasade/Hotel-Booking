from django.urls import path
from .views import HotelDetailAPIView

urlpatterns = [
    path("", HotelDetailAPIView.as_view(), name="hotel-detail"),
]