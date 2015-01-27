from django.contrib import admin
from liveBackend.models import *

class version_info_admin(admin.ModelAdmin):
    ordering=('VType',)

class isp_info_admin(admin.ModelAdmin):
    ordering=('IType',)

class infohash_info_admin(admin.ModelAdmin):
    ordering=('Infohash',)

class flow_infohash_admin(admin.ModelAdmin):
    ordering=('FType',)

class rate_type_admin(admin.ModelAdmin):
    ordering=('RateType',)

class connect_type_admin(admin.ModelAdmin):
    ordering=('ConnectType',)

class loc_info_admin(admin.ModelAdmin):
    ordering=('LType',)

admin.site.register(version_info, version_info_admin)
admin.site.register(infohash_info, infohash_info_admin)
admin.site.register(flow_infohash_type, flow_infohash_admin)
admin.site.register(rate_type, rate_type_admin)
admin.site.register(isp_info, isp_info_admin)
admin.site.register(connect_type, connect_type_admin)
admin.site.register(loc_info, loc_info_admin)
