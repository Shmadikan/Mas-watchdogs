from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserSetting(models.Model):
    language = models.CharField(max_length=3)
    site_theme = models.CharField(max_length=30)
    pooling_interval = models.IntegerField(default=2, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='setting', unique=False)
