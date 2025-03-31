from hotel.models import Reservation
from hotel.enums import ReservationStatus
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReservationApprovalSerializer

class DashboardReservationService:
    @staticmethod
    def approve_reservation(reservation: Reservation, new_status: int) -> Reservation:
        if reservation.status != ReservationStatus.PENDING:
            raise ValidationError("Only pending reservations can be approved or rejected.")

        if new_status not in [ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED]:
            raise ValidationError("Invalid status for approval.")

        reservation.status = new_status
        reservation.save()
        return reservation

    @staticmethod
    def approve_reservation_and_respond(request, reservation: Reservation, status_value: int) -> Response:
        updated = DashboardReservationService.approve_reservation(reservation, status_value)
        serializer = ReservationApprovalSerializer(updated, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)