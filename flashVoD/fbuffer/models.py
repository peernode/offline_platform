from django.db import models

from vodBackend.models import version_info, ISP_info, Location_info, video_type, clarity_type

# Create your models here.
class web_fbuffer(models.Model):
    isp = models.ForeignKey(ISP_info)
    loc = models.ForeignKey(Location_info)
    ver = models.ForeignKey(version_info)
    vtype = models.ForeignKey(video_type)
    ctype = models.ForeignKey(clarity_type)
    hour = models.IntegerField()
    date = models.DateField()
    PNtype = models.IntegerField()
    PNvalue = models.IntegerField()
    
    class Meta:
        db_table="web_fbuffer"
    
    def _get_full_info(self):
        "Return full info of this record"
        return u'%s %s %s %s %s %s %s %s %s %s' \
                    % (self.isp, self.loc, self.ver, self.vtype, self.ctype, self.hour, self.date, self.PNtype, self.PNvalue)
    full_info = property(_get_full_info)
    
    
class web_fbuffer_records2(models.Model):
    isp = models.ForeignKey(ISP_info)
    loc = models.ForeignKey(Location_info)
    ver = models.ForeignKey(version_info)
    vtype = models.ForeignKey(video_type)
    ctype = models.ForeignKey(clarity_type)
    hour = models.IntegerField()
    date = models.DateField()
    count = models.IntegerField()
    
    class Meta:
        db_table="web_fbuffer_records2"

class web_fbuffer_suc_rate(models.Model):
    isp = models.ForeignKey(ISP_info)
    loc = models.ForeignKey(Location_info)
    ver = models.ForeignKey(version_info)
    vtype = models.ForeignKey(video_type)
    ctype = models.ForeignKey(clarity_type)
    hour = models.IntegerField()
    date = models.DateField()
    sucrate = models.FloatField()

    class Meta:
        db_table="web_fbuffer_suc_rate"


