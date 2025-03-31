from django.shortcuts import render
from hotel.models import Reservation
from .serializers import ReservationApprovalSerializer
from rest_framework import generics, permissions
from .services import DashboardReservationService

class ApproveReservationAPIView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationApprovalSerializer
    permission_classes = [permissions.IsAdminUser]
