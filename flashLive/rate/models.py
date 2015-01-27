from django.db import models
from liveBackend.models import *

# Create your models here.
class connect_ratio(models.Model):
    Date=models.DateField()
    Version=models.ForeignKey(version_info)
    ISPType=models.ForeignKey(isp_info)
    ConnectType=models.ForeignKey(connect_type)
    Hour=models.IntegerField()
    PostTotal=models.IntegerField()
    SucTotal=models.IntegerField()
    FailTotal=models.IntegerField()

    class Meta:
        db_table="Connect_ratio"
        unique_together=("Date", "Version", "ISPType", "ConnectType", "Hour")

class rate(models.Model):
    Version=models.ForeignKey(version_info)
    ISPType=models.ForeignKey(isp_info)
    RateType=models.ForeignKey(rate_type)
    Date=models.DateField()
    Hour=models.IntegerField()
    PType=models.IntegerField()
    Speed=models.IntegerField()

    class Meta:
        db_table="Rate"
        unique_together=("Date", "Version", "ISPType", "Hour", "RateType", "PType")

class rate_records(models.Model):
    Version=models.ForeignKey(version_info)
    ISPType=models.ForeignKey(isp_info)
    RateType=models.ForeignKey(rate_type)
    Date=models.DateField()
    Hour=models.IntegerField()
    Record=models.IntegerField()

    class Meta:
        db_table="Rate_records"
        unique_together=("Date", "Version", "ISPType", "Hour", "RateType")