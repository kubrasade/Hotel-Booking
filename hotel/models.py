from django.db import models
from core.models import BaseModel
from .enums import ReservationStatus, RoomType
from django.utils.translation import gettext_lazy as _
import uuid

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
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    cancellation_reason = models.TextField(null=True, blank=True)
    cancel_code= models.CharField(max_length=10, unique=True, blank=True, null=True)

    class Meta: 
        verbose_name= "Reservation"
        verbose_name_plural= "Reservations"
    

    def save(self, *args, **kwargs):
        if not self.cancel_code:
            self.cancel_code = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.room.name} ({self.check_in} to {self.check_out})"