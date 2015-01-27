# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rate.models import *
from mp4meta.models import *
from vod.date_time_tool import *

def get_connect_ratio_contents(begin_date, end_date, ver, ctype):
    #prepare ver,ctype list
    ver_list=[]
    if ver==u"全选":
        ver_list.append("beta")
        ver_list.append("master")
    else:
        ver_list.append(ver)

    ctype_list=[]
    if ctype==u"全选":
        ct_objs=connect_type.objects.all()
        for i in ct_objs:
            ctype_list.append(i.Description)
    else:
        ctype_list.append(ctype)

    output={}
    for i in ver_list:
        ver_temp = version_info.get_version(i)
        values_map={}
        for j in ctype_list:
            values_map[j]=[]
        for j in ctype_list:            
            ctype_temp = connect_type.get_connect_type(j).ConnectType
            objs = connect_ratio.objects.filter(Version=ver_temp, ConnectType=ctype_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")         
            for idx in objs:                
                item={}  
                item['date']=idx.Date            
                item['total']=idx.PostTotal
                item['fenzi']=idx.Fenzi                
                values_map[j].append(item)
        
        # check if records lost
        records_num=len(values_map[ctype_list[0]])
        lost=False
        for k in ctype_list:
            if len(values_map[k]) != records_num:
                lost=True
                break

        # 以第一个选项为依据，调整数据
        if lost==True:
            for li in range(len(ctype_list)-1):
                if len(values_map[ctype_list[0]]) == len(values_map[ctype_list[li+1]]):
                    continue

                value_temp=[]
                for lli in range(len(values_map[ctype_list[0]])):
                    if values_map[ctype_list[0]][lli]['date'] == values_map[ctype_list[li+1]][lli]['date']:
                        value_temp[lli]=values_map[ctype_list[li+1]][lli];
                    else:
                        value_temp[lli]['date']=values_map[ctype_list[0]][lli]['date']
                        value_temp[lli]['total']=1
                        value_temp[lli]['fenzi']=0

                values_map[ctype_list[li+1]]=value_temp

        output[i]=values_map

    return output

def make_connect_ratio_contents(input):
    contents=[]
    item_idx=1
    for i in input.keys(): # beta, master          
        x_list=[]
        data_dict={}
        data_dict['total']=[]
        for sub_key in input[i].keys():
            data_dict[sub_key]=[]
        
        index=0
        for sub_key in input[i].keys():
            for j in input[i][sub_key]:
                if index==0:
                    x_list.append(('%d%02d%02d')%(j['date'].year, j['date'].month, j['date'].day))
                    data_dict['total'].append(("%s")%(j['total']))

                ratio="%.3f"%(j['fenzi']*1.0/j['total'])
                data_dict[sub_key].append(ratio)    
            
            index=1
        
        item={}
        item["title"]=u'peer连接成功率'
        item["subtitle"]=u'%s版本'%(i)
        item["xAxis"]=",".join(x_list)
        item["t_interval"]=1
        if len(x_list)>30:
            item["t_interval"]=len(x_list)/30

        series=[]    
        item_keys=['total']
        for sub_key in input[i].keys():
            item_keys.append(sub_key)
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


def get_connect_ratio(request):
    #prepare select data
    ver_objs=version_info.objects.all()
    vers=[]
    vers.append(u"全选")
    for i in ver_objs:
        if i.Description!='VIP' and i.Description!='all':
            vers.append(i.Description);

    ct_objs=connect_type.objects.all()
    connect_types=[]
    connect_types.append(u"全选")
    for i in ct_objs:
        connect_types.append(i.Description)

    #prepare display data
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    ver=u"全选"
    ctype=u"全选"
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")
        ver=request.GET.get("ver")
        ctype=request.GET.get("ctype")

 
    output=get_connect_ratio_contents(str(begin_date), str(end_date), ver, ctype)
    contents=make_connect_ratio_contents(output)
    select_item={}
    select_item['sver']=ver
    select_item['ctype']=ctype
    return render_to_response('connect_ratio.html', {'begin_date':str(begin_date),'end_date':str(end_date), "vers":vers, "connect_types":connect_types, "select_item":select_item, "contents":contents})


# hour ratio data
def get_connect_hour_ratio_contents(day, ver, ctype):
    #prepare ver,ctype list
    ver_list=[]
    if ver==u"全选":
        ver_list.append("beta")
        ver_list.append("master")
    else:
        ver_list.append(ver)

    ctype_list=[]
    if ctype==u"全选":
        ct_objs=connect_type.objects.all()
        for i in ct_objs:
            ctype_list.append(i.Description)
    else:
        ctype_list.append(ctype)

    output={}
    for i in ver_list:
        ver_temp = version_info.get_version(i)
        values_map={}
        for j in ctype_list:
            values_map[j]=[]
        for j in ctype_list:
            ctype_temp = connect_type.get_connect_type(j).ConnectType
            objs = connect_ratio.objects.filter(Version=ver_temp, ConnectType=ctype_temp, Hour__lt=24, Date=day).order_by("Hour")         
            for idx in objs:
                item={}  
                item['Hour']=idx.Hour            
                item['total']=idx.PostTotal
                item['fenzi']=idx.Fenzi                
                values_map[j].append(item)
        
        # check if records lost
        records_num=len(values_map[ctype_list[0]])
        lost=False
        for k in ctype_list:
            if len(values_map[k]) != records_num:
                lost=True
                break

        # 以第一个选项为依据，调整数据
        if lost==True:
            for li in range(len(ctype_list)-1):
                if len(values_map[ctype_list[0]]) == len(values_map[ctype_list[li+1]]):
                    continue

                value_temp=[]
                for lli in range(len(values_map[ctype_list[0]])):
                    if values_map[ctype_list[0]][lli]['Hour'] == values_map[ctype_list[li+1]][lli]['Hour']:
                        value_temp[lli]=values_map[ctype_list[li+1]][lli];
                    else:
                        value_temp[lli]['Hour']=values_map[ctype_list[0]][lli]['Hour']
                        value_temp[lli]['total']=1
                        value_temp[lli]['fenzi']=0

                values_map[ctype_list[li+1]]=value_temp

        output[i]=values_map

    return output

def make_connect_hour_ratio_contents(input, day):
    contents=[]
    item_idx=1
    for i in input.keys(): # beta, master          
        x_list=[]
        data_dict={}
        data_dict['total']=[]
        for sub_key in input[i].keys():
            data_dict[sub_key]=[]
        
        index=0
        for sub_key in input[i].keys():
            for j in input[i][sub_key]:
                if index==0:
                    x_list.append(('%s')%(j['Hour']))
                    data_dict['total'].append(("%s")%(j['total']))

                ratio="%.3f"%(j['fenzi']*1.0/j['total'])
                data_dict[sub_key].append(ratio)    
            
            index=1
        
        item={}
        item["title"]=u'peer连接成功率 by Hour'
        item["subtitle"]=u'%s版本 - %s'%(i, day)
        item["xAxis"]=",".join(x_list)

        series=[]    
        item_keys=['total']
        for sub_key in input[i].keys():
            item_keys.append(sub_key)
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

def get_connect_hour_ratio(request):
    #prepare select data
    ver_objs=version_info.objects.all()
    vers=[]
    vers.append(u"全选")
    for i in ver_objs:
        if i.Description!='VIP' and i.Description!='all':
            vers.append(i.Description);

    ct_objs=connect_type.objects.all()
    connect_types=[]
    connect_types.append(u"全选")
    for i in ct_objs:
        connect_types.append(i.Description)

    #prepare display data
    day=get_day_of_day(-1)
    ver=u"全选"
    ctype=u"全选"
    temp=request.GET.get("date")
    if temp is not None:
        day=temp
        ver=request.GET.get("ver")
        ctype=request.GET.get("ctype")

    output=get_connect_hour_ratio_contents(str(day), ver, ctype)

    contents=make_connect_hour_ratio_contents(output, str(day))

    select_item={}
    select_item['sver']=ver
    select_item['ctype']=ctype

    return render_to_response('connect_hour_ratio.html', {'day':str(day), "vers":vers, "connect_types":connect_types, "select_item":select_item, "contents":contents})