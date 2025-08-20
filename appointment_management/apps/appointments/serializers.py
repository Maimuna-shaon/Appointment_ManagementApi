from rest_framework import serializers
from apps.patients.models import Patient
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    # INPUT (write-only)
    PatientId = serializers.UUIDField(write_only=True, required=True)
    AppointmentDate = serializers.DateField(source="appointment_date", required=False)
    AppointmentTime = serializers.TimeField(source="appointment_time", required=False)
    Reason = serializers.CharField(source="reason", required=False)

    # OUTPUT (read-only)
    AppointmentId = serializers.IntegerField(source="id", read_only=True)
    # Echo patient UUID on output
    PatientIdOut = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "AppointmentId",
            "PatientIdOut",      # read-only mirror for output
            "AppointmentDate",
            "AppointmentTime",
            "Reason",
            "PatientId",         # write-only for input
        ]

    def get_PatientIdOut(self, obj):
        return str(obj.patient_id)

    def validate(self, attrs):
        """
        Ensure PatientId refers to a registered patient.
        """
        patient_uuid = attrs.get("PatientId")
        if patient_uuid:
            try:
                attrs["patient_obj"] = Patient.objects.get(pk=patient_uuid)
            except Patient.DoesNotExist:
                raise serializers.ValidationError({"PatientId": "Patient not registered"})
        return attrs

    def create(self, validated_data):
        patient = validated_data.pop("patient_obj")
        # remove write-only field
        validated_data.pop("PatientId", None)
        return Appointment.objects.create(patient=patient, **validated_data)

    def update(self, instance, validated_data):
        # Disallow changing patient on update (only date/time/reason)
        validated_data.pop("PatientId", None)
        validated_data.pop("patient_obj", None)
        return super().update(instance, validated_data)

    # Make output keys exactly as spec (replace PatientIdOut -> PatientId)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["PatientId"] = rep.pop("PatientIdOut")
        return rep
