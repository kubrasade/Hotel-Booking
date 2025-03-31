from django.urls import path
from .views import (ApproveReservationAPIView)

urlpatterns = [
    path("reservation/status/<int:pk>/", ApproveReservationAPIView.as_view(), name="reservation-status"),
    ]
