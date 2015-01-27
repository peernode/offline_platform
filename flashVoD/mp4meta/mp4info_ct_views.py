# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mp4meta.models import *
from vod.date_time_tool import *

def update_mp4info_ct(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)

        try:
            ver = version_info.get_version(decodes['ver'])
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            hour=decodes['hour']

            PNValues=decodes['PNValues']
            for key in sorted(PNValues.keys()):
                obj=mp4info_ct(Date=create_date,
                            Version=ver,
                            Hour=hour,
                            PNType=key,
                            PNValue=PNValues[key])
                obj.save()               

        except ValueError, e:
            result="error: %s"%e
            print e
        except Exception, e:
            result="error: %s"%e
            print e
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="application/json")

def get_mp4info_ct_contents(begin_date, end_date, ver):
    #prepare ver,ctype list
    ver_list=[]
    if ver==u"全选":
        ver_list.append("beta")
        ver_list.append("master")
    else:
        ver_list.append(ver)

    values_map={}
    for i in ver_list:        
        values_map[i]=[]

    for i in ver_list:
        ver_temp = version_info.get_version(i)
        objs = mp4info_ct.objects.filter(Version=ver_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
        items={}
        keys=['date', 25, 50, 75, 90, 95]
        for key in keys:
            items[key]=[]

        for obj in objs:
            dt='%s'%obj.Date
            format_dt=dt.split("-")
            fdt="".join(format_dt)
            if fdt not in items['date']:
                items['date'].append(fdt)
            items[obj.PNType].append("%s"%(obj.PNValue))

        values_map[i]=items

    return values_map

def make_mp4info_ct_contents(input):
    contents=[]
    item_idx=1

    for i in input.keys(): # beta, master     
        ver_item=input[i]    
 
        item={}
        item["title"]=u'获取压缩头信息耗时'
        item["subtitle"]=u'%s版本'%(i)
        item["xAxis"]=",".join(ver_item['date'])
        item["t_interval"]=1
        if len(ver_item['date'])>30:
            item["t_interval"]=len(ver_item['date'])/30

        series=[]  
        key_idxs=[25, 50, 75, 90, 95]          
        for idx in key_idxs:
            ylist=ver_item[idx]
            yAxis=0
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
        item_idx+=1
        contents.append(item)

    return contents

