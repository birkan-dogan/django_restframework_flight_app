from rest_framework import serializers
from .models import Flight, Reservation, Passenger

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many = True, required = True)
    flight = serializers.StringRelatedField(read_only = True)
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = (
            "id",
            "flight",
            "flight_id",
            "user",
            "passenger",
        )

    # Reservation ve Passenger tabloları arasındaki ilişki many-to-many olduğundan passenger data'sı ayrı bir tabloya kaydediliyor, ve burada Reservation tablomuz için passenger data'sını çıkarmalıyız
    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")
        validated_data["user_id"] = self.context["request"].user.id
        reservation = Reservation.objects.create(**validated_data)

        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)

        reservation.save()
        return reservation


class StaffSerializer(serializers.ModelSerializer):

    reservation = ReservationSerializer(many = True, read_only = True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservation",
        )