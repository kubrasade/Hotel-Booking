from django.db import models
from django.utils.translation import gettext_lazy as _

class ReservationStatus(models.IntegerChoices):
    PENDING = 1, _("Pending")
    CONFIRMED = 2, _("Confirmed")
    CANCELLED = 3, _("Cancelled")

class RoomType(models.IntegerChoices):
    SINGLE= 1, _("Single")
    DOUBLE= 2, _("Double")
    SUIT= 3, _("Suit")
    