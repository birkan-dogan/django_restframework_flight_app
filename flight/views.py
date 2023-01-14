from rest_framework import viewsets
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer, StaffSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsStafforReadOnly

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly, )

    # personel, uçuş bilgilerinin yanında rezervasyonları da görsün istiyoruz ve bunu gerçekleştirmek için get_serializer_class() methodunu override ediyoruz.
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if(self.request.user.is_staff):
            return StaffSerializer
        return serializer


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    # kullanıcı sadece kendi rezervasyonlarını listelesin istiyoruz (filtreleme). Bunun için get_queryset methodunu override ediyoruz

    def get_queryset(self):
        queryset = super().get_queryset()

        if(self.request.user.is_staff):
            return queryset

        return queryset.filter(user = self.request.user)
