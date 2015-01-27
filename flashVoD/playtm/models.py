from django.db import models

from vodBackend.models import version_info, ISP_info, Location_info, video_type, clarity_type

# Create your models here.

class web_playtm(models.Model):
    isp = models.ForeignKey(ISP_info)
    loc = models.ForeignKey(Location_info)
    ver = models.ForeignKey(version_info)
    vtype = models.ForeignKey(video_type)
    ctype = models.ForeignKey(clarity_type)
    hour = models.IntegerField()
    date = models.DateField()
    pchoke_ratio = models.FloatField()
    ptime_ratio1 = models.FloatField()
    ptime_ratio2 = models.FloatField()
    
    class Meta:
        db_table="web_playtm"
    
    def _get_full_info(self):
        "Return full info of this record"
        return u'%s %s %s %s %s %s %s %s %s %s' \
                    % (self.isp, self.loc, self.ver, self.vtype, self.ctype, self.hour, self.date, self.pchoke_ratio, self.ptime_ratio1, self.ptime_ratio2)
    full_info = property(_get_full_info)
    
    
class web_playtm_duration(models.Model):
    isp = models.ForeignKey(ISP_info)
    
    class Meta:
        db_table="web_playtm_duration"
