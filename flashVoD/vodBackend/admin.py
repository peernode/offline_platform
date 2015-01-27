from django.contrib import admin
from vodBackend.models import *

class video_type_admin(admin.ModelAdmin):
    ordering=('VideoType',)

class clarity_type_admin(admin.ModelAdmin):
    ordering=('ClarityType',)

class version_info_admin(admin.ModelAdmin):
    ordering=('Version',)

class ISP_info_admin(admin.ModelAdmin):
    ordering=('ISP',)

class Location_info_admin(admin.ModelAdmin):
    ordering=('Location',)

class connect_type_admin(admin.ModelAdmin):
    ordering=('ConnectType',)

admin.site.register(video_type, video_type_admin)
admin.site.register(clarity_type, clarity_type_admin)
admin.site.register(version_info, version_info_admin)
admin.site.register(ISP_info, ISP_info_admin)
admin.site.register(Location_info, Location_info_admin)
admin.site.register(connect_type, connect_type_admin)
