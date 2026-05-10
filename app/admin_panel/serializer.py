from rest_framework.serializers import ModelSerializer
from auditor_panel import models


class IpSerializer(ModelSerializer):
    class Meta:
        model = models.IpPool
        fields = '__all__'