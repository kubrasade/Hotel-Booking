from rest_framework import serializers
from hotel.models import Reservation
from hotel.enums import ReservationStatus
from rest_framework.exceptions import ValidationError

class ReservationApprovalSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[
        ReservationStatus.CONFIRMED,
        ReservationStatus.CANCELLED
    ])

    class Meta:
        model = Reservation
        fields = ["id", "status",]

    def update(self, instance, validated_data):
        new_status = validated_data.get("status")

        if instance.status != ReservationStatus.PENDING:
            raise ValidationError("Only pending reservations can be approved or rejected.")

        if new_status not in [ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED]:
            raise ValidationError("Invalid status for approval.")

        instance.status = new_status
        instance.save()
        return instance