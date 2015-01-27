from django.db import models
from vodBackend.models import *

# Create your models here.
class seed_ratio(models.Model):
    Date=models.DateField()
    VideoType=models.ForeignKey(video_type, to_field="VideoType")
    Version=models.ForeignKey(version_info, to_field="Version")
    Hour=models.IntegerField()
    Totals=models.IntegerField()
    Seeds=models.IntegerField()

    class Meta:
        db_table="seed_ratio"
        unique_together=("Date","VideoType", "Version", "Hour")

class connect_ratio(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    ConnectType=models.IntegerField()
    Hour=models.IntegerField()
    PostTotal=models.IntegerField()
    Fenzi=models.IntegerField()

    class Meta:
        db_table="connect_ratio"
        unique_together=("Date", "Version", "ConnectType", "Hour")
