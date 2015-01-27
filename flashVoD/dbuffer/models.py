from django.db import models
from vodBackend.models import *

# Create your models here.

class vod_dbuffer(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    VideoType=models.ForeignKey(video_type, to_field="VideoType")
    Clarity_type=models.ForeignKey(clarity_type, to_field="ClarityType")
    ISP=models.ForeignKey(ISP_info, to_field="ISP")
    Location=models.ForeignKey(Location_info, to_field="Location")
    Hour=models.IntegerField()
    PNType=models.IntegerField()
    PNValue=models.IntegerField()

    class Meta:
        db_table="vod_dbuffer"
        unique_together=('Date', 'Version', 'VideoType', 'Clarity_type', 'ISP', 'Location', 'Hour', 'PNType')

class vod_dbuffer_records(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    VideoType=models.ForeignKey(video_type, to_field="VideoType")
    Clarity_type=models.ForeignKey(clarity_type, to_field="ClarityType")
    ISP=models.ForeignKey(ISP_info, to_field="ISP")
    Location=models.ForeignKey(Location_info, to_field="Location")
    Hour=models.IntegerField()
    Count=models.IntegerField()

    class Meta:
        db_table="vod_dbuffer_records"
        unique_together=('Date', 'Version', 'VideoType', 'Clarity_type', 'ISP', 'Location', 'Hour')

