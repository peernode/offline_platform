# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dbuffer.models import *
from vod.date_time_tool import *

def get_dbuffer_content(objs, select_ver, ct):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)

    filter_objs=objs.filter(Version=ver_temp, Clarity_type=ct_temp)
    keys=['date', 25, 50, 75, 90, 95]
    items={}
    for i in keys:
        items[i]=[]

    for i in filter_objs:
        dt='%s'%i.Date
        format_dt=dt.split("-")
        fdt="".join(format_dt)
        if fdt not in items['date']:
            items['date'].append(fdt)
        items[i.PNType].append("%s"%(i.PNValue*1.0/1000))
   
    return items    

def get_dbuffer_record(objs, select_ver, ct):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)

    filter_objs=objs.filter(Version=ver_temp, Clarity_type=ct_temp)
    items=[]
    for i in filter_objs:
        items.append("%s"%(i.Count))
    return items 

def make_dbuffer_item(content, record, select_ver, vt, ct, isp, item_idx):
    item={}
    item["title"]=u'dbuffer - 版本: %s'%(select_ver)
    item["subtitle"]=u'视频类型:%s  -  清晰度:%s  -  运营商:%s '%(vt, ct, isp)
    item["xAxis"]=",".join(content['date'])
    item["t_interval"]=1
    if len(content['date'])>30:
        item["t_interval"]=len(content['date'])/30

    series=[]       
    yAxis=0
    show_format='column'
    serie_item='''{
            name: 'records',
            yAxis: %s,
            type: '%s',
            data: [%s]
        }'''%(yAxis, show_format, ",".join(record))
    series.append(serie_item)
    
    key_idxs=[25, 50, 75, 90, 95]
    for idx in key_idxs:
        ylist=content[idx]
        yAxis=1
        show_format='spline'
        serie_item='''{
            name: '%s',
            yAxis: %s,
            type: '%s',
            data: [%s]
        }'''%(idx, yAxis, show_format, ",".join(ylist))
        series.append(serie_item)

    item["series"]=",".join(series)
    item["index"]=item_idx
    return item

def all_dbuffer(request):
    #prepare display data
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")
        
    vt='all'
    ct=u'所有'
    isp=u'所有'
    vers=['beta', 'master', 'VIP']
    item_contents=[]
    item_idx=1
    vt_temp=video_type.get_video_type(vt)
    isp_temp=ISP_info.get_ISP(isp)
    objs=vod_dbuffer.objects.filter(VideoType=vt_temp, ISP=isp_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
    record_objs=vod_dbuffer_records.objects.filter(VideoType=vt_temp, Hour=24, ISP=isp_temp, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
    for i in vers:
        content=get_dbuffer_content(objs, i, ct)
        record=get_dbuffer_record(record_objs, i, ct)
        item=make_dbuffer_item(content, record, i, vt, ct, isp, item_idx)
        item_idx+=1
        item_contents.append(item)

    return render_to_response("all_dbuffer.html", {'begin_date':str(begin_date),'end_date':str(end_date), "contents":item_contents})

def return_vt_dbuffer_by_ver_isp(request, vt):
    #prepare select data
    ver_objs=version_info.objects.all()
    vers=[]
    for i in ver_objs:
        if i.Description!='all':
            vers.append(i.Description);

    ct_objs=clarity_type.objects.all()
    clarity_types=[]
    for i in ct_objs:
        clarity_types.append(i.Description)

    isp_objs=ISP_info.objects.all()
    isps=[]
    for i in isp_objs:
        isps.append(i.Description)

    #prepare display data
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    ver="beta"
    isp=u"所有"
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")
        isp=request.GET.get("isp")
        ver=request.GET.get("ver")
        
    vt_temp=video_type.get_video_type(vt)
    item_contents=[]
    item_idx=1
    vt_temp=video_type.get_video_type(vt)
    isp_temp=ISP_info.get_ISP(isp)
    objs=vod_dbuffer.objects.filter(VideoType=vt_temp, ISP=isp_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
    record_objs=vod_dbuffer_records.objects.filter(VideoType=vt_temp, ISP=isp_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
    for i in clarity_types:
        content=get_dbuffer_content(objs, ver, i)
        record=get_dbuffer_record(record_objs, ver, i)
        item=make_dbuffer_item(content, record, ver, vt, i, isp, item_idx)
        item_idx+=1
        item_contents.append(item)
    
    select_item={}
    select_item['vt']=vt
    select_item['sver']=ver
    select_item['isp']=isp
    return render_to_response("daily_dbuffer.html", {'begin_date':str(begin_date),'end_date':str(end_date), "vers":vers, "isps":isps, "select_item":select_item, "contents":item_contents})

def movie_dbuffer(request):
    return return_vt_dbuffer_by_ver_isp(request, 'movie')

def tv_dbuffer(request):
    return return_vt_dbuffer_by_ver_isp(request, 'tv')

def cartoon_dbuffer(request):
    return return_vt_dbuffer_by_ver_isp(request, 'cartoon')