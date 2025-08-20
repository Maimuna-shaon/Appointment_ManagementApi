from django.db import models
from apps.patients.models import Patient

class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)  # AppointmentId
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]

    def __str__(self):
        return f"Appt {self.id} for {self.patient_id} on {self.appointment_date} {self.appointment_time}"
