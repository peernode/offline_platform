# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rate.models import *
from mp4meta.models import *
from vod.date_time_tool import *

def update_seed_ratio(request):
    result="ok"
    if request.method == 'POST':
        decodes=json.loads(request.body)

        try:
            ver = version_info.get_version(decodes['ver'])
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            # mv info
            vtype = video_type.get_video_type("movie")       
            mv_obj = seed_ratio(Date=create_date,
                            VideoType=vtype,
                            Version=ver,
                            Hour=decodes['hour'],
                            Totals=decodes['mv_totals'],
                            Seeds=decodes['mv_seeds'])
            mv_obj.save()

            # tv info
            vtype = video_type.get_video_type("tv")        
            tv_obj = seed_ratio(Date=create_date,
                            VideoType=vtype,
                            Version=ver,
                            Hour=decodes['hour'],
                            Totals=decodes['tv_totals'],
                            Seeds=decodes['tv_seeds'])
            tv_obj.save()

            # cartoon info
            vtype = video_type.get_video_type("cartoon")        
            ct_obj = seed_ratio(Date=create_date,
                            VideoType=vtype,
                            Version=ver,
                            Hour=decodes['hour'],
                            Totals=decodes['cartoon_totals'],
                            Seeds=decodes['cartoon_seeds'])
            ct_obj.save()
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

def get_seed_ratio_contents(begin_date, end_date, ver, vtype):
    #prepare ver,ctype list
    ver_list=[]
    if ver==u"全选":
        ver_list.append("beta")
        ver_list.append("master")
    else:
        ver_list.append(ver)

    vtype_list=[]
    if vtype==u"全选":
        vtype_list.append("movie")
        vtype_list.append("tv")
        vtype_list.append("cartoon")
    else:
        vtype_list.append(vtype)

    output={}
    for i in ver_list:
        ver_temp = version_info.get_version(i)
        values_map={}
        for j in vtype_list:
            values_map[j]=[]
        for j in vtype_list:
            vtype_temp = video_type.get_video_type(j)
            objs = seed_ratio.objects.filter(VideoType=vtype_temp, Version=ver_temp, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")         
            for idx in objs:                
                item={}  
                item['date']=idx.Date            
                item['total']=idx.Totals
                item['seeds']=idx.Seeds                
                values_map[j].append(item)
        
        # check if records lost
        records_num=len(values_map[vtype_list[0]])
        lost=False
        for k in vtype_list:
            if len(values_map[k]) != records_num:
                lost=True
                break

        # 以第一个选项为依据，调整数据
        if lost==True:
            for li in range(len(vtype_list)-1):
                if len(values_map[vtype_list[0]]) == len(values_map[vtype_list[li+1]]):
                    continue

                value_temp=[]
                for lli in range(len(values_map[vtype_list[0]])):
                    if values_map[vtype_list[0]][lli]['date'] == values_map[vtype_list[li+1]][lli]['date']:
                        value_temp[lli]=values_map[vtype_list[li+1]][lli];
                    else:
                        value_temp[lli]['date']=values_map[vtype_list[0]][lli]['date']
                        value_temp[lli]['total']=1
                        value_temp[lli]['seeds']=0

                values_map[vtype_list[li+1]]=value_temp

        output[i]=values_map

    return output

def make_seed_ratio_contents(input):
    contents=[]
    item_idx=1
    for i in input.keys(): # beta, master          
        x_list=[]
        data_dict={}        
        for sub_key in input[i].keys():
            data_dict[('%s_total')%(sub_key)]=[]
            data_dict[sub_key]=[]
        
        index=0
        for sub_key in input[i].keys():
            for j in input[i][sub_key]:
                if index==0:
                    x_list.append(('%d%02d%02d')%(j['date'].year, j['date'].month, j['date'].day))
                    
                data_dict[('%s_total')%(sub_key)].append(("%s")%(j['total']))
                ratio="%.3f"%(j['seeds']*1.0/j['total'])
                data_dict[sub_key].append(ratio)    
            
            index=1
        
        item={}
        item["title"]=u'peer可做种率'
        item["subtitle"]=u'%s版本'%(i)
        item["xAxis"]=",".join(x_list)
        item["t_interval"]=1
        if len(x_list)>30:
            item["t_interval"]=len(x_list)/30

        series=[]    
        item_keys=[]
        for sub_key in input[i].keys():
            item_keys.append("%s_total"%(sub_key))
            item_keys.append(sub_key)
        for idx in item_keys:
            ylist=data_dict[idx]
            yAxis=0
            show_format='column'
            if idx.find('total')==-1:
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

def get_seed_ratio(request):
    ver_objs=version_info.objects.all()
    vers=[]
    vers.append(u"全选")
    for i in ver_objs:
        if i.Description!='VIP' and i.Description!='all':
            vers.append(i.Description);

    video_types=[]
    video_types.append(u"全选")
    video_types.append("movie")
    video_types.append("tv")
    video_types.append("cartoon")

    #prepare display data
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    ver=u"全选"
    vtype=u"全选"
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")
        ver=request.GET.get("ver")
        vtype=request.GET.get("vtype")

    output=get_seed_ratio_contents(str(begin_date), str(end_date), ver, vtype)
    contents=make_seed_ratio_contents(output)
    select_item={}
    select_item['sver']=ver
    select_item['vtype']=vtype
    return render_to_response("seed_ratio.html", {'begin_date':str(begin_date),'end_date':str(end_date), "vers":vers, "video_types":video_types, "select_item":select_item, "contents":contents})


# seed hour ratio data
def get_seed_hour_ratio_contents(day, ver, vtype):
    #prepare ver,ctype list
    ver_list=[]
    if ver==u"全选":
        ver_list.append("beta")
        ver_list.append("master")
    else:
        ver_list.append(ver)

    vtype_list=[]
    if vtype==u"全选":
        vtype_list.append("movie")
        vtype_list.append("tv")
        vtype_list.append("cartoon")
    else:
        vtype_list.append(vtype)

    output={}
    for i in ver_list:
        ver_temp = version_info.get_version(i)
        values_map={}
        for j in vtype_list:
            values_map[j]=[]
        for j in vtype_list:
            vtype_temp = video_type.get_video_type(j)
            objs = seed_ratio.objects.filter(VideoType=vtype_temp, Version=ver_temp, Hour__lt=24, Date=day).order_by("Hour")         
            for idx in objs:                
                item={}  
                item['Hour']=idx.Hour            
                item['total']=idx.Totals
                item['seeds']=idx.Seeds                
                values_map[j].append(item)
        
        # check if records lost
        records_num=len(values_map[vtype_list[0]])
        lost=False
        for k in vtype_list:
            if len(values_map[k]) != records_num:
                lost=True
                break

        # 以第一个选项为依据，调整数据
        if lost==True:
            for li in range(len(vtype_list)-1):
                if len(values_map[vtype_list[0]]) == len(values_map[vtype_list[li+1]]):
                    continue

                value_temp=[]
                for lli in range(len(values_map[vtype_list[0]])):
                    if values_map[vtype_list[0]][lli]['Hour'] == values_map[vtype_list[li+1]][lli]['Hour']:
                        value_temp[lli]=values_map[vtype_list[li+1]][lli];
                    else:
                        value_temp[lli]['Hour']=values_map[vtype_list[0]][lli]['Hour']
                        value_temp[lli]['total']=1
                        value_temp[lli]['seeds']=0

                values_map[vtype_list[li+1]]=value_temp

        output[i]=values_map

    return output

def make_seed_hour_ratio_contents(input, day):
    contents=[]
    item_idx=1
    for i in input.keys(): # beta, master          
        x_list=[]
        data_dict={}        
        for sub_key in input[i].keys():
            data_dict[('%s_total')%(sub_key)]=[]
            data_dict[sub_key]=[]
        
        index=0
        for sub_key in input[i].keys():
            for j in input[i][sub_key]:
                if index==0:
                    x_list.append(('%s')%(j['Hour']))
                    
                data_dict[('%s_total')%(sub_key)].append(("%s")%(j['total']))
                ratio="%.3f"%(j['seeds']*1.0/j['total'])
                data_dict[sub_key].append(ratio)    
            
            index=1
        
        item={}
        item["title"]=u'peer可做种率'
        item["subtitle"]=u'%s版本 - %s'%(i, day)
        item["xAxis"]=",".join(x_list)

        series=[]    
        item_keys=[]
        for sub_key in input[i].keys():
            item_keys.append("%s_total"%(sub_key))
            item_keys.append(sub_key)
        for idx in item_keys:
            ylist=data_dict[idx]
            yAxis=0
            show_format='column'
            if idx.find('total')==-1:
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

def get_seed_hour_ratio(request):
    ver_objs=version_info.objects.all()
    vers=[]
    vers.append(u"全选")
    for i in ver_objs:
        if i.Description!='VIP' and i.Description!='all':
            vers.append(i.Description);

    video_types=[]
    video_types.append(u"全选")
    video_types.append("movie")
    video_types.append("tv")
    video_types.append("cartoon")

    #prepare display data
    day=get_day_of_day(-1)
    ver=u"全选"
    vtype=u"全选"
    temp=request.GET.get("date")
    if temp is not None:
        day=temp
        ver=request.GET.get("ver")
        vtype=request.GET.get("vtype")

    output=get_seed_hour_ratio_contents(str(day), ver, vtype)
    contents=make_seed_hour_ratio_contents(output, str(day))
    select_item={}
    select_item['sver']=ver
    select_item['vtype']=vtype
    return render_to_response("seed_hour_ratio.html", {'day':str(day), "vers":vers, "video_types":video_types, "select_item":select_item, "contents":contents})

