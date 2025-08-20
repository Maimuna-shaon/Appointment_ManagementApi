import uuid
from django.db import models

class Patient(models.Model):
    # UUID is the primary key exposed as PatientId
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.id})"


# Create your models here.
