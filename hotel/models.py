from django.db import models
from django.conf import settings
from core.models import BaseModel
from .enums import ReservationStatus, RoomType

class Hotel(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Room(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=100)
    room_type = models.PositiveSmallIntegerField(choices=RoomType.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural= "Rooms"

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

class Reservation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    cancellation_reason = models.TextField(null=True, blank=True)

    class Meta: 
        verbose_name= "Reservation"
        verbose_name_plural= "Reservations"

    def __str__(self):
        return f"{self.user.username} - {self.room.name} ({self.check_in} to {self.check_out})"