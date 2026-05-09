from django.db import models
from django.shortcuts import render


class IpPool(models.Model):
    ip = models.GenericIPAddressField()
    description = models.TextField(
        max_length=255
    )
    ports = models.JSONField(default=list)


class Settings(models.Model):

    class Speed(models.TextChoices):
        Panic = "T0","panic"
        Slow = "T1","slow"
        Default = "T2","normal"
        High = "T3","high speed"
        Aggressive = "T4", "aggressive"
        Hyper = "T5", "hyper aggressive"

    class Intensity(models.TextChoices):
        Normal = "N","normal"
        Medium = "M","medium"
        High = "H","high"



    ip = models.ForeignKey(IpPool, on_delete=models.SET_NULL, null=True)
    speed = models.CharField(
        max_length=100,
        choices=Speed,
    )

    intensity = models.CharField(
        max_length=100,
        choices=Intensity,
    )

    short_note = models.CharField(
        max_length=75,
    )




