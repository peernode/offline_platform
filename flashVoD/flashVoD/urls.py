"""
Definition of urls for flashVoD.
"""

from datetime import datetime
from django.conf.urls import patterns, url

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'vod.views.home', name='home'),
    url(r'^nav$', 'vod.views.nav'),
    url(r'^panel$', 'vod.views.panel'),
    
    # base tables
    url(r'^update/video_type$', 'vodBackend.base_tables_views.update_video_type'),
    url(r'^update/clarity_type$', 'vodBackend.base_tables_views.update_clarity_type'),
    url(r'^update/version$', 'vodBackend.base_tables_views.update_version_info'),
    url(r'^update/ISP_info$', 'vodBackend.base_tables_views.update_ISP_info'),
    url(r'^update/Location_info$', 'vodBackend.base_tables_views.update_location_info'),
    url(r'^update/connect_type$', 'vodBackend.base_tables_views.update_connect_type'),

    # by xujy, seed ratio, connect ratio, mp4meta
    url(r'^update/seed_ratio$', 'rate.seed_ratio_views.update_seed_ratio'),
    url(r'^update/connect_ratio$', 'rate.connect_ratio_views.update_connect_ratio'),
    url(r'^update/fbuffers_private$', 'mp4meta.views.update_fbuffer_private'),
    url(r'^update/fbuffer_mp4meta$', 'mp4meta.views.update_fbuffer_mp4meta'),
    url(r'^mp4meta/fbuffer_records', 'mp4meta.views.get_fbuffer_records'),
    url(r'^mp4meta/download_fbuffer_record', 'mp4meta.views.download_fbuffer_records'),
    url(r'^mp4meta/fbuffer_success', 'mp4meta.views.get_fbuffer_success'),
    url(r'^mp4meta/mp4info', 'mp4meta.views.get_mp4info'),
    url(r'^rate/conect_ratio', 'rate.views.get_connect_ratio'),
    url(r'^rate/connect_hour_ratio', 'rate.views.get_connect_hour_ratio'),
    url(r'^rate/seed_ratio', 'rate.seed_ratio_views.get_seed_ratio'),
    url(r'^rate/seed_hour_ratio', 'rate.seed_ratio_views.get_seed_hour_ratio'),

    url(r'^update/vod/mp4info_ct', 'mp4meta.mp4info_ct_views.update_mp4info_ct'),
    url(r'^update/vod/mp4info_access_ratio', 'mp4meta.mp4info_access_raito_views.update_ratio'),
    url(r'^update/vod/uncompress', 'mp4meta.uncompress_views.update_uncompress'),

    # for dbuffer
    url(r'^update/vod/dbuffer', 'dbuffer.views.update_dbuffer'), 
    url(r'^dbuffer/all_dbuffer', 'dbuffer.dbuffer_daily_views.all_dbuffer'), 
    url(r'^dbuffer/movie_dbuffer', 'dbuffer.dbuffer_daily_views.movie_dbuffer'),
    url(r'^dbuffer/tv_dbuffer', 'dbuffer.dbuffer_daily_views.tv_dbuffer'),
    url(r'^dbuffer/cartoon_dbuffer', 'dbuffer.dbuffer_daily_views.cartoon_dbuffer'),
    url(r'^dbuffer/all_hour_dbuffer', 'dbuffer.dbuffer_hour_views.all_hour_dbuffer'), 
    url(r'^dbuffer/movie_hour_dbuffer', 'dbuffer.dbuffer_hour_views.movie_hour_dbuffer'),
    url(r'^dbuffer/tv_hour_dbuffer', 'dbuffer.dbuffer_hour_views.tv_hour_dbuffer'),
    url(r'^dbuffer/cartoon_hour_dbuffer', 'dbuffer.dbuffer_hour_views.cartoon_hour_dbuffer'),

    # for update
    url(r'^update/vod/playtm', 'playtm.views.update_web_playtm'),
    url(r'^update/vod/fbuffer$', 'fbuffer.updates.update_web_fbuffer'),
    url(r'^update/vod/fbuffer_records', 'fbuffer.updates.update_web_fbuffer_records'),
    url(r'^update/vod/fbuffer_sucrate', 'fbuffer.updates.update_web_fbuffer_suc'),
 
    # for query
    url(r'^query/vod/playtm/hour', 'playtm.views.query_web_playtm_by_hour'),
    url(r'^query/vod/playtm/date', 'playtm.views.query_web_playtm_by_date'),
    url(r'^query/vod/fbuffer/hour', 'fbuffer.views.query_web_fbuffer_by_hour'),
    url(r'^query/vod/fbuffer/date', 'fbuffer.views.query_web_fbuffer_by_date'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
)
