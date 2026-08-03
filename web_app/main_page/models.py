from django.db import models
from django.db.models import CASCADE
from dns.rdatatype import NULL
from django.contrib.auth.models import User


# Create your models here.
class IpTable(models.Model):
    ip = models.GenericIPAddressField()
    subnet = models.GenericIPAddressField()
    user_id = models.ForeignKey(User, on_delete=CASCADE, unique=False, null=False)

class ScanResult(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField()
    date = models.DateTimeField()
    ip_fk = models.ForeignKey(IpTable, on_delete=models.SET_NULL, related_name="scanResult", null=True)

