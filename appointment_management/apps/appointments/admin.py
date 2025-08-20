from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_id", "appointment_date", "appointment_time")
    list_filter = ("appointment_date",)
    search_fields = ("id", "patient__name", "patient__contact_info")
