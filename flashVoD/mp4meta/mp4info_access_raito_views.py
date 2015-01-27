# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mp4meta.models import *
from vod.date_time_tool import *

def update_ratio(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)

        try:
            ver = version_info.get_version(decodes['ver'])
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            obj=mp4info_access_ratio(Date=create_date,
                            Version=ver,
                            Hour=decodes['hour'],
                            Total=decodes['total'],
                            Fail=decodes['fail'])
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

def get_mp4info_access_ratio_contents(begin_date, end_date, ver):
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
        objs = mp4info_access_ratio.objects.filter(Version=ver_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
        for obj in objs:
            item={}
            item['date']=obj.Date
            item['total']=obj.Total
            item['fail']=obj.Fail
            values_map[i].append(item)

    return values_map

def make_mp4info_access_ratio_contents(input):
    contents=[]
    item_idx=1
    for i in input.keys(): # beta, master          
        x_list=[]
        data_dict={}
        data_dict['total']=[]
        data_dict['fail_ratio']=[]
        
        l=input[i]
        for idx in l:
            x_list.append(('%d%02d%02d')%(idx['date'].year, idx['date'].month, idx['date'].day))
            data_dict['total'].append(("%s")%(idx['total']))
            ratio="%.3f"%(idx['fail']*1.0/idx['total'])
            data_dict['fail_ratio'].append(ratio)  
        
        item={}
        item["title"]=u'压缩头信息获取失败率'
        item["subtitle"]=u'%s版本'%(i)
        item["xAxis"]=",".join(x_list)
        item["t_interval"]=1
        if len(x_list)>30:
            item["t_interval"]=len(x_list)/30

        series=[]    
        item_keys=['total', 'fail_ratio']
        for idx in item_keys:
            ylist=data_dict[idx]
            yAxis=0
            show_format='column'
            if idx!='total':
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
        item_idx+=1
        contents.append(item)

    return contents