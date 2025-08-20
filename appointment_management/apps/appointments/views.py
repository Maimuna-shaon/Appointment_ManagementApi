from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Endpoints:
      POST   /api/appointments/          -> Create
      GET    /api/appointments/          -> List
      GET    /api/appointments/{id}/     -> Retrieve
      PUT    /api/appointments/{id}/     -> Update
      PATCH  /api/appointments/{id}/     -> Partial Update
      DELETE /api/appointments/{id}/     -> Delete
    """
    queryset = Appointment.objects.select_related("patient").all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create to return the exact success message per requirement.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        data = self.get_serializer(appointment).data
        data["Message"] = "Appointment created successfully"
        return Response(data, status=status.HTTP_201_CREATED)
