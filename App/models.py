from django.db import models
from django.utils import timezone

# Create your models here.
class Machine(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    hostName = models.CharField(max_length=250, blank=True, null=True)
    hostOs = models.CharField(max_length=250, blank=True, null=True)
    ip = models.CharField(max_length=250, blank=True, null=True, unique=True)
    disk = models.FloatField(blank=True, null=True)
    ram = models.FloatField(blank=True, null=True)
    cpu = models.FloatField(blank=True, null=True)
    interface = models.CharField(max_length=250, blank=True, null=True)
    graphic = models.TextField(blank=True, null=True)
    fileName = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.ip