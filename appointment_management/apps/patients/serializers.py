from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    # Expose UUID as 'patient_id' field name in API
    patient_id = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = Patient
        fields = ["patient_id", "name", "contact_info"]
