from django.db import models

# Create your models here.

class video_type(models.Model):
    VideoType=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="video_type"

    @classmethod
    def get_video_type(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.VideoType, self.Description)

class clarity_type(models.Model):
    ClarityType=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="clarity_type"

    @classmethod
    def get_clarity_type(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.ClarityType, self.Description)

class version_info(models.Model):
    Version=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="version_info"

    @classmethod
    def get_version(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.Version, self.Description)

class ISP_info(models.Model):
    ISP=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="ISP_info"

    @classmethod
    def get_ISP(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.ISP, self.Description)

class Location_info(models.Model):
    Location=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="Location_info"

    @classmethod
    def get_location(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.Location, self.Description)

class connect_type(models.Model):
    ConnectType=models.IntegerField(primary_key=True)
    Description=models.CharField(max_length=30)

    class Meta:
        db_table="connect_type"

    @classmethod
    def get_connect_type(cls, description):
        q=cls.objects.get(Description=description)
        return q

    def __unicode__(self):
        return u'%d - %s' % (self.ConnectType, self.Description)
