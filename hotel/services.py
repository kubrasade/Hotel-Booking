from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from .models import Reservation
from .enums import ReservationStatus
from .serializers import ReservationStatusSerializer
from rest_framework import status
from rest_framework.response import Response


class ReservationService:
    @staticmethod
    def cancel_reservation(reservation: Reservation, reason: str = None) -> Reservation:
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValidationError("Reservation already cancelled.")

        if reservation.status not in [ReservationStatus.PENDING, ReservationStatus.CONFIRMED]:
            raise ValidationError("This reservation cannot be canceled.")

        if reservation.check_in <= now().date():
            raise ValidationError("A reservation that has started or passed cannot be cancelled.")

        reservation.status = ReservationStatus.CANCELLED
        if reason:
            reservation.cancellation_reason = reason
        reservation.save()
        return reservation
    
    @staticmethod
    def cancel_reservation_and_respond(request, reservation: Reservation) -> Response:
        updated = ReservationService.cancel_reservation(reservation)
        serializer = ReservationStatusSerializer(updated, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)