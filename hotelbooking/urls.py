from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/',include('contact.urls')),
    path('hotel/',include('hotel.urls')),
    path('dashboard/',include('dashboard.urls'))
]
