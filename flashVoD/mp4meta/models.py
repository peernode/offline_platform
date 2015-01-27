from django.db import models
from vodBackend.models import *

# Create your models here.

class fbuffer_records_private(models.Model):
    Date=models.DateField()
    VideoType=models.ForeignKey(video_type, to_field="VideoType")
    count=models.IntegerField()

    class Meta:
        db_table="fbuffer_records_private"
        unique_together=("Date","VideoType")

class fbuffer_success(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    Hour=models.IntegerField()
    Mp4meta=models.IntegerField()
    Uncompress=models.IntegerField()
    Fbuffer=models.IntegerField()

    class Meta:
        db_table="fbuffer_success"
        unique_together=("Date", "Version", "Hour")

class mp4info_ct(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    Hour=models.IntegerField()
    PNType=models.IntegerField()
    PNValue=models.IntegerField()

    class Meta:
        db_table="mp4info_ct"
        unique_together=("Date", "Version", "Hour", "PNType")

class mp4info_access_ratio(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    Hour=models.IntegerField()
    Total=models.IntegerField()
    Fail=models.IntegerField()

    class Meta:
        db_table="mp4info_access_ratio"
        unique_together=("Date", "Version", "Hour")

class uncompress(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info, to_field="Version")
    Total=models.IntegerField()
    Fail=models.IntegerField()

    class Meta:
        db_table="uncompress"
        unique_together=("Date", "Version")
    


