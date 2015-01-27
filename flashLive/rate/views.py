# -*- coding: utf-8 -*- 

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import *
import time
import json
from rate.models import *

# Create your views here.
def update_connect_ratio(request):
    result = "ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            fdate = decodes['date']
            fver = version_info.get_version_type(decodes['ver'])
            ftime = decodes['hour']

            count = 0
            vlen = len(decodes['isp'])
            while count < vlen:
                ispid = isp_info.get_isp_id(decodes['isp'][count]['name'])
                post = decodes['isp'][count]['post_total']
                succ = decodes['isp'][count]['suc_total']
                fail = decodes['isp'][count]['fail_total']
                fpost = decodes['isp'][count]['first_post_total']
                fsucc = decodes['isp'][count]['first_suc_total']
                ffail = decodes['isp'][count]['first_fail_total']
                count = count + 1
                ctype = connect_type.get_connect_type("Total")
                vft = connect_ratio(Date=fdate,Version=fver,ISPType=ispid,ConnectType=ctype,Hour=ftime,PostTotal=post,SucTotal=succ,FailTotal=fail)
                vft.save()
                ctype = connect_type.get_connect_type("First")
                vft = connect_ratio(Date=fdate,Version=fver,ISPType=ispid,ConnectType=ctype,Hour=ftime,PostTotal=fpost,SucTotal=fsucc,FailTotal=ffail)
                vft.save()
        except BaseException, e:
           result = "save error:" + e.message
    else:
        result = "error"

    respStr = json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_rate(request):
    result = "ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            fdate = decodes['date']
            fver = version_info.get_version_type(decodes['ver'])
            ftime = decodes['hour']
            fisp = isp_info.get_isp_id(decodes['isp'])
            count = 0
            vlen = len(decodes['rtype'])
            while count < vlen:
                ratetype = rate_type.objects.get(RateType=decodes['rtype'][count]['name'])
                records = decodes['rtype'][count]['records']
                vft = rate_records(Date=fdate,Version=fver,ISPType=fisp,RateType=ratetype,Hour=ftime,Record=records)
                vft.save()
                for key in decodes['rtype'][count].keys():
                    if cmp(key,'name') != 0 and cmp(key,'records'):
                        ptype = int(key)
                        speed = decodes['rtype'][count][key]
                        vft = rate(Date=fdate,Version=fver,ISPType=fisp,RateType=ratetype,Hour=ftime,PType=ptype,Speed=speed)
                        vft.save()
                count = count + 1
        except BaseException, e:
           result = "save error:" + e.message
    else:
        result = "error"

    respStr = json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def cselector(request):
    #Version
    versions = version_info.objects.all()
    para1 = []
    for i in versions:
        para1.append(i.Version)
    #ISP
    isps = isp_info.objects.all()
    para3 = []
    for i in isps:
        para3.append(i.ISP)

    qfdate = str((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
    qtdate = qfdate
    return render_to_response("live_connect_selector.html", {"ver":para1,"isp":para3,"qver":"All","qisp":u"所有","fdate":qfdate,"tdate":qtdate})

def rselector(request):
    #Version
    versions = version_info.objects.all()
    para1 = []
    for i in versions:
        para1.append(i.Version)
    #Rate Type
    rtypes = rate_type.objects.all()
    para2 = []
    para2.append("All")
    for i in rtypes:
        para2.append(i.Description)
    #ISP
    isps = isp_info.objects.all()
    para3 = []
    for i in isps:
        para3.append(i.ISP)

    qfdate = str((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
    qtdate = qfdate
    return render_to_response("live_rate_selector.html", {"ver":para1,"rtype":para2,"isp":para3,"qver":"All","qrtype":"All","qisp":u"所有","fdate":qfdate,"tdate":qtdate})

def cratio(request):
    qver = request.GET.get("version")
    qisp = request.GET.get("isp")
    qfdate = request.GET.get("from")
    qtdate = request.GET.get("to")
    if not qfdate and not qtdate and not qver and not qisp:
        return render_to_response("live_connect_ratio.html", {"error":"Please select the query conditions"})
    
    if cmp(qfdate,qtdate) == 0:
        sdata = connect_one_day(qfdate,qver,qisp)
    else:
        sdata = connect_multi_day(qfdate,qtdate,qver,qisp)

    if sdata['postrecords'] and sdata['fpostrecords'] and sdata['postratio'] and sdata['fpostratio']:
        return render_to_response("live_connect_ratio.html", {"content":sdata,"fdate":qfdate,"tdate":qtdate})
    else:
        return render_to_response("live_connect_ratio.html", {"error":"No data","fdate":qfdate,"tdate":qtdate})

def connect_one_day(date,ver,isp):
    qispid = isp_info.get_isp_id(isp)
    qverid = version_info.get_version_type(ver)

    qctype = connect_type.get_connect_type("Total")
    data = connect_ratio.objects.filter(Version=qverid,ISPType=qispid,Date=date,ConnectType=qctype).order_by("Hour")
    sdata = {}
    sdata['time'] = []
    sdata['postrecords'] = []
    sdata['postratio'] = []
    sdata['failratio'] = []
    
    for i in data:
        if i.Hour != 24:
            sdata['time'].append(str(i.Hour))
            sdata['postrecords'].append(int(i.PostTotal))
            postratio = float(i.SucTotal) / float(int(i.PostTotal) + 1)
            sdata['postratio'].append(float('%.4f' % postratio))
            failratio = float(i.FailTotal) / float(int(i.PostTotal) + 1)
            sdata['failratio'].append(float('%.4f' % failratio))

    qctype = connect_type.get_connect_type("First")
    data = connect_ratio.objects.filter(Version=qverid,ISPType=qispid,Date=date,ConnectType=qctype).order_by("Hour")
    sdata['fpostrecords'] = []
    sdata['fpostratio'] = []
    for i in data:
        if i.Hour != 24:
            sdata['fpostrecords'].append(int(i.PostTotal))
            postratio = float(i.SucTotal) / float(int(i.PostTotal) + 1)
            sdata['fpostratio'].append(float('%.4f' % postratio))

    return sdata

def connect_multi_day(fdate,tdate,ver,isp):
    qispid = isp_info.get_isp_id(isp)
    qverid = version_info.get_version_type(ver)

    qctype = connect_type.get_connect_type("Total")
    data = connect_ratio.objects.filter(Version=qverid,ISPType=qispid,Hour=24,ConnectType=qctype,Date__gte=fdate,Date__lte=tdate).order_by("Date")
    sdata = {}
    sdata['time'] = []
    sdata['postrecords'] = []
    sdata['postratio'] = []
    sdata['failratio'] = []
    
    for i in data:
        sdata['time'].append(str(i.Date))
        sdata['postrecords'].append(int(i.PostTotal))
        postratio = float(i.SucTotal) / float(i.PostTotal)
        sdata['postratio'].append(float('%.4f' % postratio))
        failratio = float(i.FailTotal) / float(i.PostTotal)
        sdata['failratio'].append(float('%.4f' % failratio))

    qctype = connect_type.get_connect_type("First")
    data = connect_ratio.objects.filter(Version=qverid,ISPType=qispid,Hour=24,ConnectType=qctype,Date__gte=fdate,Date__lte=tdate).order_by("Date")
    sdata['fpostrecords'] = []
    sdata['fpostratio'] = []
    for i in data:
        sdata['fpostrecords'].append(int(i.PostTotal))
        postratio = float(i.SucTotal) / float(i.PostTotal)
        sdata['fpostratio'].append(float('%.4f' % postratio))
    return sdata

def rates(request):
    qver = request.GET.get("version")
    qisp = request.GET.get("isp")
    qfdate = request.GET.get("from")
    qtdate = request.GET.get("to")
    qrtype = request.GET.get("rtype")

    if not qfdate and not qtdate and not qver and not qisp and not qrtype:
        return render_to_response("live_connect_ratio.html", {"error":"Please select the query conditions"})
    
    if cmp(qfdate,qtdate) == 0:
        sdata = rate_one_day(qfdate,qver,qisp,qrtype)
    else:
        sdata = rate_multi_day(qfdate,qtdate,qver,qisp,qrtype)

    if sdata:
        return render_to_response("live_rates.html", {"content":sdata,"fdate":qfdate,"tdate":qtdate})
    else:
        return render_to_response("live_rates.html", {"error":"No data","fdate":qfdate,"tdate":qtdate})

def get_rate_data(fdate,tdate,ver,isp,rtype,order):
    try:
        if cmp(order, "Hour") == 0:
            data = rate.objects.filter(Version=ver,ISPType=isp,Date=fdate,RateType=rtype).order_by("Hour")
        elif cmp(order, "Date") == 0:
            data = rate.objects.filter(Version=ver,ISPType=isp,RateType=rtype,Hour=24,Date__gte=fdate,Date__lte=tdate).order_by("Date")
        else:
            data = ""
    except BaseException, e:
        data = ""
    return data

def package_data(index,data,ver,isp,date,rtype,order):
    sdata = {}
    sdata["index"] = index
    sdata["title"] = str(rtype.Description)
    sdata['time'] = []
    sdata['records'] = []
    sdata['p25'] = []
    sdata['p50'] = []
    sdata['p75'] = []
    sdata['p90'] = []
    sdata['p95'] = []
    lasthour = -1
    for j in data:
        if j.Hour != 24:
            if lasthour != int(j.Hour):
                sdata['time'].append(str(j.Hour))
                records = rate_records.objects.get(Version=ver,ISPType=isp,Date=date,RateType=rtype,Hour=int(j.Hour))
                sdata['records'].append(int(records.Record))
                lasthour = int(j.Hour)
            ptype = int(j.PType)
            speed = int(j.Speed)
            sdata['p%d' % ptype].append(speed)
    return sdata

def package_data_by_date(index,data,ver,isp,rtype,order):
    sdata = {}
    sdata["index"] = index
    sdata["title"] = str(rtype.Description)
    sdata['time'] = []
    sdata['records'] = []
    sdata['p25'] = []
    sdata['p50'] = []
    sdata['p75'] = []
    sdata['p90'] = []
    sdata['p95'] = []
    lasthour = ""
    for j in data:
        if cmp(lasthour, str(j.Date)) != 0:
            sdata['time'].append(str(j.Date))
            records = rate_records.objects.get(Version=ver,ISPType=isp,Date=str(j.Date),RateType=rtype,Hour=24)
            sdata['records'].append(int(records.Record))
            lasthour = str(j.Date)
        ptype = int(j.PType)
        speed = int(j.Speed)
        sdata['p%d' % ptype].append(speed)
    return sdata

def rate_one_day(date,ver,isp,rtype):
    content = []
    qispid = isp_info.get_isp_id(isp)
    qverid = version_info.get_version_type(ver)

    if cmp(rtype, "All") == 0:
        qrtype = rate_type.objects.all()
        count = 1
        for i in qrtype:
            data = get_rate_data(date,date,qverid,qispid,i,"Hour")
            if not data:
                continue
            sdata = package_data(count,data,qverid,qispid,date,i,"Hour")
            count = count + 1
            content.append(sdata)
    else:
        qrtype = rate_type.get_rate_type(rtype)
        data = get_rate_data(date,date,qverid,qispid,qrtype,"Hour")
        if data:
            sdata = package_data(1,data,qverid,qispid,date,qrtype,"Hour")
            content.append(sdata)
    return content

def rate_multi_day(fdate,tdate,ver,isp,rtype):
    content = []
    qispid = isp_info.get_isp_id(isp)
    qverid = version_info.get_version_type(ver)

    if cmp(rtype, "All") == 0:
        qrtype = rate_type.objects.all()
        count = 1
        for i in qrtype:
            data = get_rate_data(fdate,tdate,qverid,qispid,i,"Date")
            if not data:
                continue
            sdata = package_data_by_date(count,data,qverid,qispid,i,"Date")
            count = count + 1
            content.append(sdata)
    else:
        qrtype = rate_type.get_rate_type(rtype)
        data = get_rate_data(fdate,tdate,qverid,qispid,qrtype,"Date")
        if data:
            sdata = package_data_by_date(1,data,qverid,qispid,qrtype,"Hour")
            content.append(sdata)
    return content
