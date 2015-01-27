from django.db import models
from liveBackend.models import *

# Create your models here.
class delay_records(models.Model):
    Infohash_type = models.ForeignKey(flow_infohash_type)
    ISP_type = models.ForeignKey(isp_info)
    Date=models.DateField()
    Records=models.IntegerField()
    ValidRecords=models.IntegerField()

    class Meta:
        db_table="Delay_records"
        unique_together=(('Infohash_type', 'ISP_type', 'Date'),)

class delay_by_play(models.Model):
    Infohash_type = models.ForeignKey(flow_infohash_type)
    ISP_type = models.ForeignKey(isp_info)
    Date = models.DateField()
    Guid = models.CharField(max_length=36)
    Delay_chunks = models.IntegerField()
    Play_counts = models.IntegerField()
    Play_start = models.IntegerField()
    Play_end = models.IntegerField()

    class Meta:
        db_table="Delay_by_play"