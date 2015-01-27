from django.db import models

# Create your models here.
class version_info(models.Model):
    VType = models.IntegerField(primary_key=True)
    Version = models.CharField(max_length=255)
    class Meta:
        db_table="Version_info"

    @classmethod
    def get_version_type(cls,ver):
        q = cls.objects.get(Version=ver)
        return q

    def __unicode__(self):
        return u'%d - %s'%(self.VType,self.Version)

class infohash_info(models.Model):
    Infohash = models.CharField(max_length=40, primary_key=True)
    Name = models.CharField(max_length=255)
    Rate = models.IntegerField()
    
    class Meta:
        db_table="Infohash_info"

    @classmethod
    def get_infohash_name(cls,infohash):
        q = cls.objects.get(Infohash=infohash)
        return q

    def __unicode__(self):
        return u'%s - %d Kbps'%(self.Name,self.Rate)

class flow_infohash_type(models.Model):
    FType = models.IntegerField(primary_key=True)
    Ver =  models.ForeignKey(version_info)
    Infohash = models.ForeignKey(infohash_info)

    class Meta:
        db_table="Flow_infohash_type"

    @classmethod
    def get_flowtype_id(cls,ver,info):
        vtype = version_info.get_version_type(ver)
        q = cls.objects.get(Ver=vtype,Infohash=info)
        return q

    def __unicode__(self):
        return u'%d - %s - %s'%(self.FType,self.Ver,self.Infohash)

class isp_info(models.Model):
    IType = models.IntegerField(primary_key=True)
    ISP = models.CharField(max_length=255)

    class Meta:
        db_table="ISP_info"

    @classmethod
    def get_isp_id(cls,name):
        q = cls.objects.get(ISP=name)
        return q
    
    def __unicode__(self):
        return u'%d - %s'%(self.IType,self.ISP)

class loc_info(models.Model):
    LType = models.IntegerField(primary_key=True)
    Location = models.CharField(max_length=255)

    class Meta:
        db_table="Loc_info"

    @classmethod
    def get_loc_id(cls,name):
        q = cls.objects.get(Location=name)
        return q
    
    def __unicode__(self):
        return u'%d - %s'%(self.LType,self.Location)

class flow_by_hour(models.Model):
    Infohash_type = models.ForeignKey(flow_infohash_type)
    ISP_type = models.ForeignKey(isp_info)
    Date = models.DateField()
    Timestamp = models.IntegerField()
    #Timestamp = models.CharField(max_length=5)
    P2P = models.CharField(max_length=255)
    CDN = models.CharField(max_length=255)

    class Meta:
        db_table="Flow_by_hour"
        unique_together=(('Infohash_type', 'ISP_type', 'Date', 'Timestamp'),)

    @classmethod
    def get_flow_records(cls,infohash,isp,date,timestamp):
        q = cls.objects.filter(Infohash_type=infohash, ISP_type=isp, Date=date, Timestamp=timestamp)
        return q

class flow_loc_by_hour(models.Model):
    Infohash_type = models.ForeignKey(flow_infohash_type)
    Loc_type = models.ForeignKey(loc_info)
    Date = models.DateField()
    Timestamp = models.IntegerField()
    P2P = models.CharField(max_length=255)
    CDN = models.CharField(max_length=255)

    class Meta:
        db_table="Flow_loc_by_hour"
        unique_together=(('Infohash_type', 'Loc_type', 'Date', 'Timestamp'),)

    @classmethod
    def get_flow_records(cls,infohash,loc,date,timestamp):
        q = cls.objects.filter(Infohash_type=infohash, Loc_type=loc, Date=date, Timestamp=timestamp)
        return q

class connect_type(models.Model):
    ConnectType=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="Connect_type"

    @classmethod
    def get_connect_type(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s'%(self.ConnectType,self.Description)

class rate_type(models.Model):
    RateType=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="Rate_type"

    @classmethod
    def get_rate_type(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s'%(self.RateType,self.Description)

