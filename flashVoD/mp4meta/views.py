# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mp4meta.models import *
from mp4meta.mp4info_ct_views import *
from mp4meta.mp4info_access_raito_views import *
from mp4meta.uncompress_views import *
from vod.date_time_tool import *

def update_fbuffer_private(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)

        try:
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            vt=["all", "movie", "tv", "cartoon", "variety", "micro", "other"]
            api_vt=['total', 'movie', 'tv', 'cartoon', 'variety', 'micro', 'others']
            for i in range(len(vt)):
                vtype = video_type.get_video_type(vt[i])
                fobj=fbuffer_records_private(Date=create_date,
                                            VideoType=vtype,
                                            count=decodes[api_vt[i]])
                fobj.save()

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

def get_fbuffer_records_contents(begin_date, end_date):
    vt=['all', 'movie', 'tv', 'cartoon', 'variety', 'micro', 'other']
    values_map={}
    for i in vt:
        vtype = video_type.get_video_type(i)
        objs = fbuffer_records_private.objects.filter(VideoType=vtype, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
        values_map[i]=objs
    
    contents=[]
    # check if records lost
    records_num=len(values_map['all'])
    lost=False
    for i in vt:
        if len(values_map[i]) != records_num:
            lost=True
            break

    if lost == True:
        for i in range(records_num):
            item={}
            item["date"]=values_map['all'][i].Date
            for type in vt:
                obj=values_map[type].get(Date=item["date"])
                if obj is None:
                    item[i]=0
                else:
                    item[i]=obj.count

            contents.append(item)
    else:
        for i in range(records_num):
            item={}
            item["date"]=values_map['all'][i].Date
            for type in vt:
                item[type]=values_map[type][i].count
            contents.append(item)

    return contents

def make_fbuffer_record_plot_item(title, subtitle, fr_list, begin_date, end_date):
    x_list=[]
    total_list=[]
    mv_list=[]
    tv_list=[]
    ct_list=[]
    variety_list=[]
    micro_list=[]
    for fr in fr_list:
        x_list.append(('%d%02d%02d')%(fr['date'].year, fr['date'].month, fr['date'].day))
        total_list.append(fr['all'])
        mv_list.append(fr['movie'])
        tv_list.append(fr['tv'])
        ct_list.append(fr['cartoon'])
        variety_list.append(fr['variety'])
        micro_list.append(fr['micro'])

    serial_list=[('all', total_list), ('mv', mv_list),('tv', tv_list),('ct', ct_list),('variety', variety_list),('micro', micro_list)]

    item={}
    item["title"]=title
    item["subtitle"]=subtitle+" "+begin_date+"  -  "+end_date
    item["t_interval"]=1
    if len(x_list)>30:
        item["t_interval"]=len(x_list)/30
    item["xAxis"]=",".join(x_list)

    series=[]
    for name, y_list in serial_list:
        y_list=[str(x) for x in y_list]
        serie_item='''{
            name: '%s',
            data: [%s]
        }'''%(name, ",".join(y_list))
        series.append(serie_item)
    item["series"]=",".join(series)
    return item

def get_fbuffer_records(request):
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")

    contents=get_fbuffer_records_contents(begin_date, end_date)
    header=['date', 'all', 'movie', 'tv', 'cartoon', 'variety', 'micro', 'other']
    print str(begin_date), end_date

    item = make_fbuffer_record_plot_item('fbuffer_records', 'by type', contents, str(begin_date), str(end_date))
    return render_to_response("fbuffer_recordss.html", {'begin_date':str(begin_date),'end_date':str(end_date), 'headers':header, 'contents':contents, "item":item})

def download_fbuffer_records(request):
    response=HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = "attachment; filename=fbuffer_records.csv"
    writer=csv.writer(response)
    header=['date', 'all', 'movie', 'tv', 'cartoon', 'variety', 'micro', 'other']
    writer.writerow(header)

    contents=get_fbuffer_records_contents('2014-11-10')
    for i in contents:
        r=[]
        for k in header:
            r.append(i[k])
        writer.writerow(r)

    return response

def update_fbuffer_mp4meta(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)

        try:
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            
            # beta info
            ver = version_info.get_version('beta')
            beta_obj = fbuffer_success(Date=create_date,
                                  Version=ver,
                                  Hour=decodes['hour'],
                                  Mp4meta=decodes['beta_mp4meta'],
                                  Uncompress=decodes['beta_uncompress'],
                                  Fbuffer=decodes['beta_fbuffer'])
            beta_obj.save()

            # master info
            ver = version_info.get_version('master')
            master_obj = fbuffer_success(Date=create_date,
                                  Version=ver,
                                  Hour=decodes['hour'],
                                  Mp4meta=decodes['master_mp4meta'],
                                  Uncompress=decodes['master_uncompress'],
                                  Fbuffer=decodes['master_fbuffer'])
            master_obj.save()

            # open info
            ver = version_info.get_version('open')
            open_obj = fbuffer_success(Date=create_date,
                                  Version=ver,
                                  Hour=decodes['hour'],
                                  Mp4meta=decodes['open_mp4meta'],
                                  Uncompress=decodes['open_uncompress'],
                                  Fbuffer=decodes['open_fbuffer'])
            open_obj.save()

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

def get_fbuffer_success_contents(begin_date, end_date):
    version=['master', 'beta']
    values_map={}
    for i in version:
        ver = version_info.get_version(i)
        objs = fbuffer_success.objects.filter(Version=ver, Hour=24, Date__gte=begin_date, Date__lte=end_date).order_by("Date")
        values_map[i]=objs
    
    contents=[]
    # check if records lost
    records_num=len(values_map[version[0]])
    lost=False
    for i in version:
        if len(values_map[i]) != records_num:
            lost=True
            break

    ori_key_idx=['mp4meta', 'uncompress', 'fbuffer', 'ratio']
    if lost == True:
        for i in range(records_num):
            item={}
            item["date"]=values_map[version[0]][i].Date
            for ver in version:
                key_idx=[]
                for ki in ori_key_idx:
                    key_idx.append(("%s_%s")%(ver, ki))

                obj=values_map[ver].get(Date=item["date"])                             
                if obj is None:
                    item[key_idx[0]]=0
                    item[key_idx[1]]=0
                    item[key_idx[2]]=0
                    item[key_idx[3]]=0
                else:
                    item[key_idx[0]]=obj.Mp4meta
                    item[key_idx[1]]=obj.Uncompress
                    item[key_idx[2]]=obj.Fbuffer
                    ratio="%.4f"%(obj.Fbuffer*1.0/obj.Mp4meta)
                    item[key_idx[3]]=ratio

            contents.append(item)
    else:
        for i in range(records_num):
            item={}
            item["date"]=values_map[version[0]][i].Date
            for ver in version:
                key_idx=[]
                for ki in ori_key_idx:
                    key_idx.append(("%s_%s")%(ver, ki))

                item[key_idx[0]]=values_map[ver][i].Mp4meta
                item[key_idx[1]]=values_map[ver][i].Uncompress
                item[key_idx[2]]=values_map[ver][i].Fbuffer
                ratio="%.4f"%(values_map[ver][i].Fbuffer*1.0/values_map[ver][i].Mp4meta)
                item[key_idx[3]]=ratio
            contents.append(item)

    return contents

def make_fbuffer_success_item(title, subtitle, fs_list, begin_date, end_date):
    x_list=[]

    key_idxs=['master_mp4meta', 'master_uncompress', 'master_fbuffer', 'master_ratio', 'beta_mp4meta', 'beta_uncompress', 'beta_fbuffer', 'beta_ratio']
    data_dict={}
    for i in key_idxs:
        data_dict[i]=[]

    for fs in fs_list:       
        x_list.append(('%d%02d%02d')%(fs['date'].year, fs['date'].month, fs['date'].day))
        for idx in key_idxs:
            data_dict[idx].append(("%s")%(fs[idx]))
   
    item={}
    item["title"]=title
    item["subtitle"]=subtitle+" "+begin_date+"  -  "+end_date
    item["xAxis"]=",".join(x_list)
    item["t_interval"]=1
    if len(x_list)>30:
        item["t_interval"]=len(x_list)/30

    series=[]    
    for idx in key_idxs:
        ylist=data_dict[idx]
        yAxis=0
        show_format='column'
        if idx=='master_ratio' or idx=='beta_ratio':
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
    return item

def get_fbuffer_success(request):
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")

    contents=get_fbuffer_success_contents(begin_date, end_date)
    header=['date', '正式版mp4meta', 'uncompress', 'fbuffer', '正式版ratio', '公测版mp4meta', 'uncompress', 'fbuffer', '公测版ratio']

    item = make_fbuffer_success_item('fbuffer_success_ratio', 'by version', contents, str(begin_date), str(end_date))
    return render_to_response("fbuffer_success_ratio.html", {'begin_date':str(begin_date),'end_date':str(end_date), 'headers':header, 'contents':contents, "item":item})

def get_mp4info(request):
    #prepare select data
    ver_objs=version_info.objects.all()
    vers=[]
    vers.append(u"全选")
    for i in ver_objs:
        if i.Description!='VIP' and i.Description!='all':
            vers.append(i.Description);

    #prepare display data
    begin_date=get_day_of_day(-30)
    end_date=get_day_of_day(-1)
    ver=u"全选"
    temp=request.GET.get("from")
    if temp is not None:
        begin_date=temp
        end_date=request.GET.get("to")
        ver=request.GET.get("ver")

    mp4info_ct_contents=get_mp4info_ct_contents(str(begin_date), str(end_date), ver)
    info_ct_items=make_mp4info_ct_contents(mp4info_ct_contents)
    mp4info_access_ratio_contents=get_mp4info_access_ratio_contents(str(begin_date), str(end_date), ver)
    info_ratio_items=make_mp4info_access_ratio_contents(mp4info_access_ratio_contents)
    uncompress_fail_ratio_contents=get_uncompress_fail_ratio_contents(str(begin_date), str(end_date), ver)
    uncompress_ratio_items=make_uncompress_fail_ratio_contents(uncompress_fail_ratio_contents)
    select_item={}
    select_item['sver']=ver
    return render_to_response("mp4info.html", {'begin_date':str(begin_date),'end_date':str(end_date), "vers":vers, "select_item":select_item, "info_ct":info_ct_items, "info_ratio":info_ratio_items, "uncompress_ratio":uncompress_ratio_items})