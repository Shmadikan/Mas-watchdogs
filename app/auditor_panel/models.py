from django.db import models
from django.shortcuts import render


class IpPool(models.Model):
    ip = models.GenericIPAddressField()
    description = models.TextField(
        max_length=255
    )
    ports = models.JSONField(default=list)




