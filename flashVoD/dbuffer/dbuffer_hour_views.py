# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dbuffer.models import *
from vod.date_time_tool import *

def get_dbuffer_hour_content(objs, select_ver, ct, isps):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)
    items={}
    for i in isps:
        isp_temp=ISP_info.get_ISP(i)
        filter_objs=objs.filter(Version=ver_temp, Clarity_type=ct_temp, ISP=isp_temp, Hour=24).order_by("PNType")
        item=[]
        if len(filter_objs)==0:
            item=['1', '1', '1', '1', '1']
        else:
            for k in filter_objs:
                item.append(("%s")%(k.PNValue*1.0/1000))

        items[i]=item
    return items

def get_dbuffer_hour_record(objs, select_ver, ct, isps):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)
    items={}
    for i in isps:
        isp_temp=ISP_info.get_ISP(i)
        try:
            filter_obj=objs.get(Version=ver_temp, Clarity_type=ct_temp, ISP=isp_temp, Hour=24)
            items[i]="%s"%(filter_obj.Count)
        except Exception, e:
            items[i]="%s"%(1)

    return items


def get_dbuffer_24hour_content(objs, select_ver, ct, isp):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)
    isp_temp=ISP_info.get_ISP(isp)
    filter_objs=objs.filter(Version=ver_temp, Clarity_type=ct_temp, ISP=isp_temp, Hour__lt=24).order_by("Hour")
    keys=['hour', 25, 50, 75, 90, 95]
    items={}
    for i in keys:
        items[i]=[]

    for i in range(24):
        items['hour'].append('%s'%i)

    for i in filter_objs:
        items[i.PNType].append("%s"%(i.PNValue*1.0/1000))
   
    return items        

def get_dbuffer_24hour_record(objs, select_ver, ct, isp):
    ver_temp = version_info.get_version(select_ver)
    ct_temp=clarity_type.get_clarity_type(ct)
    isp_temp=ISP_info.get_ISP(isp)
    filter_objs=objs.filter(Version=ver_temp, Clarity_type=ct_temp, ISP=isp_temp, Hour__lt=24).order_by("Hour")
    items=[]
    for i in filter_objs:
        items.append("%s"%(i.Count))
    return items 

def make_dbuffer_hour_item(content, record, select_ver, vt, ct, item_idx, isps):
    x_list=['25', '50', '75', '90', '95']   
    item={}
    item["title"]=u'dbuffer - 版本: %s'%(select_ver)
    item["subtitle"]=u'视频类型:%s  -  清晰度:%s'%(vt, ct)
    item["xAxis"]=",".join(x_list)

    series=[]       
    yAxis=0       
    show_format='spline'
    keys=isps
    for key in keys:
        ylist=content[key]
        count=record[key]        
        serie_item='''{
            name: '%s - %s',
            yAxis: %s,
            type: '%s',
            data: [%s]
        }'''%(key, count, yAxis, show_format, ",".join(ylist))
        series.append(serie_item)

    item["series"]=",".join(series)
    item["index"]=item_idx
    return item

def make_all_dbuffer_hour_item(content, record, vers, vt, ct, item_idx, isp):
    x_list=['25', '50', '75', '90', '95']
   
    item={}
    item["title"]='dbuffer'
    item["subtitle"]=u'视频类型:%s  -  清晰度:%s  -  运营商:%s'%(vt, ct, isp)
    item["xAxis"]=",".join(x_list)

    series=[]       
    yAxis=0       
    show_format='spline'
    for i in vers:
        ylist=content[i][isp]
        count=record[i][isp]        
        serie_item='''{
            name: '%s - %s',
            yAxis: %s,
            type: '%s',
            data: [%s]
        }'''%(i, count, yAxis, show_format, ",".join(ylist))
        series.append(serie_item)
            

    item["series"]=",".join(series)
    item["index"]=item_idx
    return item

def return_vt_hour_dbuffer_by_ver(request, vt):
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
    cur_date=get_day_of_day(-1)
    ver="beta"
    temp=request.GET.get("date")
    if temp is not None:
        cur_date=temp
        ver=request.GET.get("ver")
        
    vt_temp=video_type.get_video_type(vt)

    item_contents=[]
    item_idx=1
    vt_temp=video_type.get_video_type(vt)
    print "begin 24hour", datetime()
    objs=vod_dbuffer.objects.filter(VideoType=vt_temp, Date=cur_date)
    record_objs=vod_dbuffer_records.objects.filter(VideoType=vt_temp, Date=cur_date)
    for i in clarity_types:
        content=get_dbuffer_hour_content(objs, ver, i, isps)
        record=get_dbuffer_hour_record(record_objs, ver, i, isps)
        item=make_dbuffer_hour_item(content, record, ver, vt, i, item_idx, isps)
        item_idx+=1
        item_contents.append(item)
    print "end 24hour", datetime()
    select_item={}
    select_item['vt']=vt
    select_item['sver']=ver

    return render_to_response("hour_dbuffer.html", {'day':str(cur_date), "vers":vers, "select_item":select_item, "contents":item_contents})

def make_dbuffer_24hour_item(content, record, ver, vt, ct, item_idx, isp):
    item={}
    item["title"]=u'dbuffer - 版本: %s'%(ver)
    item["subtitle"]=u'视频类型:%s  -  清晰度:%s  -  运营商:%s '%(vt, ct, isp)
    item["xAxis"]=",".join(content['hour'])

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

def all_hour_dbuffer(request):
    #prepare display data
    cur_date=get_day_of_day(-1)
    temp=request.GET.get("date")
    if temp is not None:
        cur_date=temp
        
    vt='all'
    ct=u'所有'
    isp=u'所有'
    vers=['beta', 'master', 'VIP']
    item_contents=[]
    item_idx=1
    vt_temp=video_type.get_video_type(vt)
    isp_temp=ISP_info.get_ISP(isp)
    isps=[]
    isps.append(isp)
    print "begin 24hour", datetime()
    objs=vod_dbuffer.objects.filter(VideoType=vt_temp, ISP=isp_temp, Date=cur_date).order_by("Hour")
    record_objs=vod_dbuffer_records.objects.filter(VideoType=vt_temp, ISP=isp_temp, Date=cur_date).order_by("Hour")
    pncontents={}
    pnrecords={}
    for i in vers:
        content=get_dbuffer_hour_content(objs, i, ct, isps)
        record=get_dbuffer_hour_record(record_objs, i, ct, isps)
        pncontents[i]=content
        pnrecords[i]=record
       
    item=make_all_dbuffer_hour_item(pncontents, pnrecords, vers, vt, ct, item_idx, isp)    
    item_contents.append(item)

    #24 hours dbuffer
    items_24hour=[]
    item_idx=1
    for i in vers:
        contents_24hour=get_dbuffer_24hour_content(objs, i, ct, isp)
        records_24hour=get_dbuffer_24hour_record(record_objs, i, ct, isp)
        item=make_dbuffer_24hour_item(contents_24hour, records_24hour, i, vt, ct, item_idx, isp)
        item_idx+=1
        items_24hour.append(item)

    print "end 24hour", datetime()
    select_item={}
    select_item['vt']=vt
    return render_to_response("all_hour_dbuffer.html", {'day':str(cur_date), "select_item":select_item, "contents_day":item_contents, "contents_24":items_24hour})

def movie_hour_dbuffer(request):
    return return_vt_hour_dbuffer_by_ver(request, 'movie')

def tv_hour_dbuffer(request):
    return return_vt_hour_dbuffer_by_ver(request, 'tv')

def cartoon_hour_dbuffer(request):
    return return_vt_hour_dbuffer_by_ver(request, 'cartoon')