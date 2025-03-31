from rest_framework import serializers
from .models import Hotel, Room, Reservation
from .enums import ReservationStatus
from .services import ReservationService
from rest_framework.exceptions import ValidationError


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "address",
            "city",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class RoomSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",  
            "hotel_name",  
            "name",
            "room_type",
            "price",
            "capacity",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

class ReservationSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)
    hotel_name = serializers.CharField(source="room.hotel.name", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "name",
            "surname",
            "email",
            "phone",
            "room",
            "room_name",
            "hotel_name",
            "check_in",
            "check_out",
            "total_price",
            "status",
            "created_at",
            "updated_at",
            "cancel_code",
        ]
        read_only_fields = ("id", "created_at", "updated_at", "total_price", "status", "cancel_code")

    def validate(self, data):
        check_in= data["check_in"]
        check_out= data["check_out"]
        room= data.get("room")

        if check_in >= check_out:
            raise serializers.ValidationError("Your check-out date must be after your check-in date.")
        
        overlapping= Reservation.objects.filter(
            room= room,
            status__in= [ReservationStatus.PENDING, ReservationStatus.CONFIRMED],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        
        if overlapping:
            raise serializers.ValidationError("This room is already booked for the selected dates.")
        return data

    def create(self, validated_data):
        nights = (validated_data["check_out"] - validated_data["check_in"]).days
        room = validated_data["room"]
        total_price = room.price * nights
        validated_data["total_price"] = total_price
        validated_data["status"] = ReservationStatus.PENDING
        return super().create(validated_data)
    
class ReservationStatusSerializer(serializers.ModelSerializer):
    cancellation_reason= serializers.CharField(required= False, allow_blank=True)

    class Meta:
        model = Reservation
        fields = ["id", "status", "cancellation_reason"]
        read_only_fields = ["id", "status"]

class CancelReservationInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    cancel_code = serializers.CharField(max_length=10)
    cancellation_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        email = data["email"]
        cancel_code = data["cancel_code"]

        try:
            reservation = Reservation.objects.get(email=email, cancel_code=cancel_code)
        except Reservation.DoesNotExist:
            raise ValidationError("E-mail or cancellation code is incorrect.")

        if reservation.status == ReservationStatus.CANCELLED:
            raise ValidationError("This reservation is already cancelled.")

        self.context["reservation"] = reservation
        return data

    def save(self, **kwargs):
        reservation = self.context["reservation"]
        reason = self.validated_data.get("cancellation_reason")

        return ReservationService.cancel_reservation(reservation, reason)