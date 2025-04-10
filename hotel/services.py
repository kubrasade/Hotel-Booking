from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from .models import Reservation, Room
from .enums import ReservationStatus
import calendar
from datetime import date, timedelta
from rest_framework.exceptions import NotFound, ValidationError

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
    def get_monthly_availability(room_id: int, year: int, month: int) -> dict:
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise NotFound("Room not found.")

        try:
            num_days = calendar.monthrange(year, month)[1]
        except Exception:
            raise ValidationError("Invalid year or month.")

        availability = {str(day): "available" for day in range(1, num_days + 1)}

        reservations = Reservation.objects.filter(
            room=room,
            check_in__lte=date(year, month, num_days),
            check_out__gte=date(year, month, 1),
        )

        for reservation in reservations:
            current_day = reservation.check_in
            while current_day < reservation.check_out:
                if current_day.year == year and current_day.month == month:
                    availability[str(current_day.day)] = "unavailable"
                current_day += timedelta(days=1)

        return {
            "room_id": room.id,
            "year": year,
            "month": month,
            "availability": availability,
        }