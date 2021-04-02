from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from rest_framework.authtoken.models import Token



class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=200)
    date = models.DateTimeField()


class Guest(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)


class Reservation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_Reservations")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="guest_Reservations")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_create_token(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)