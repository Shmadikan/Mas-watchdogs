from django.db import models
from dns.rdatatype import NULL


# Create your models here.
class IpTable(models.Model):
    ip = models.GenericIPAddressField()
    subnet = models.GenericIPAddressField()

class ScanResult(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField()
    date = models.DateTimeField()
    ip_fk = models.ForeignKey(IpTable, on_delete=models.SET_NULL, related_name="scanResult", null=True)

