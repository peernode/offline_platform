"""
Definition of urls for flashLive.
"""

from django.conf.urls import patterns, include, url
#import liveBackend.views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'live.views.home'),
    url(r'^nav$','live.views.nav',name='nav'),
    url(r'^panel$','live.views.panel',name='panel'),
    url(r'^display$','live.views.display',name='display'),
    url(r'^live_flow', 'live.views.flow', name='live_flow'),
    url(r'^live_loc_flow', 'live.views.flow_loc', name='live_flow_loc'),
    url(r'^live_selector', 'live.views.selector', name='live_selector'),
    url(r'^live_loc_selector', 'live.views.selector_loc', name='live_selector_loc'),
    url(r'^live_connect_selector', 'rate.views.cselector', name='live_connect_selector'),
    url(r'^live_connect_ratio', 'rate.views.cratio', name='live_connect_ratio'),
    url(r'^live_rate_selector', 'rate.views.rselector', name='live_rate_selector'),
    url(r'^live_rates', 'rate.views.rates', name='live_rates'),
    # url(r'^flashLive/', include('flashLive.flashLive.urls')),
    url(r'update/live_version_info', 'liveBackend.views.update_ver_info'),
    url(r'update/live_infohash_info', 'liveBackend.views.update_infohash_info'),
    url(r'update/live_flow_type', 'liveBackend.views.update_flow_type'),
    url(r'update/live_isp_info', 'liveBackend.views.update_isp_info'),
    url(r'update/live_loc_info', 'liveBackend.views.update_loc_info'),
    url(r'update/live_flow_by_hour', 'liveBackend.views.update_flow_by_hour'),
    url(r'update/live_flow_loc_by_hour', 'liveBackend.views.update_flow_loc_by_hour'),
    url(r'update/live_connect_type', 'liveBackend.views.update_connect_type'),
    url(r'update/live_connect_ratio', 'rate.views.update_connect_ratio'),
    url(r'update/live_rate_type', 'liveBackend.views.update_rate_type'),
    url(r'update/live_rate', 'rate.views.update_rate'),
    url(r'update/live_delay_play', 'delay.views.update_delay'),
    url(r'update/live_delay_record', 'delay.views.update_delay_record'),

    #url(r'test', 'liveBackend.tests.test'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
