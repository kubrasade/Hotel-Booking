from rest_framework import serializers
from .models import Hotel, Room

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