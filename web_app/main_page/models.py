from django.utils.timezone import now
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User


# Create your models here.
class IpTable(models.Model):
    ip = models.GenericIPAddressField()
    subnet = models.GenericIPAddressField()
    user_id = models.ForeignKey(User, on_delete=CASCADE, unique=False, null=False)

    @classmethod
    def ipv4_transform(cls, ip: str, subnet: str) -> str:
        bit_octet = sum(bin(int(octet)).count('1') for octet in subnet.split('.'))
        return f"{ip}/{bit_octet}"

class ScanResult(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField()
    date = models.DateTimeField()
    ip_fk = models.ForeignKey(IpTable, on_delete=models.SET_NULL, related_name="scanResult", null=True)

    @classmethod
    def handle_ip(cls, ip_list: list[dict[str, str]]):

        for data in ip_list:
            scan = ScanResult(title="", description="", date=now(), ip_fk=IpTable.objects.get(id=data['id']))
            scan.save()

    @classmethod
    def all_formating(cls):
        data = ScanResult.objects.all()
        return list(map(lambda x: {
            'id': x.pk,
            'date': x.date.strftime('%Y.%m.%d %H:%M'),
            'title': x.title,
            'desc': x.description
        }, data))

    @classmethod
    def get_format(clm, **kwargs):
        id = kwargs['id']
        result = ScanResult.objects.get(id=id)
        return {
            'id': result.pk,
            'date': result.date.strftime('%Y.%m.%d %H:%M'),
            'title': result.title,
            'desc': result.description
        }

