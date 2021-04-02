from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers

from .models import Movie, Guest, Reservation



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("pk", "hall", "movie", "date", "movie_Reservations")


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ("pk", "name", "phone", "guest_Reservations")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("pk", "movie", "guest")