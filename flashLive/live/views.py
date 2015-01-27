# Create your views here.
# -*- coding: utf-8 -*- 

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import *
import time
import liveBackend.models

def home(request):
    return render_to_response("index.html",{})

def nav(request):
    return render_to_response("nav.html",{})

def panel(request):
    return render_to_response("panel.html",{})

def display(request):
    return render_to_response("display.html",{})

def flow_one_day(date,ver,infohash,isp):
    qispid = liveBackend.models.isp_info.get_isp_id(isp)
    qinfohashid = liveBackend.models.infohash_info.objects.get(Name=infohash,Rate='800')
    qftype = liveBackend.models.flow_infohash_type.get_flowtype_id(ver,qinfohashid)
    data = liveBackend.models.flow_by_hour.objects.filter(Infohash_type=qftype,ISP_type=qispid,Date=date).order_by("Timestamp")

    starttime = time.mktime(datetime.strptime(date+' 00:00', '%Y-%m-%d %H:%M').timetuple())
    count=0
    sdata = {}
    sdata['time'] = []
    sdata['p2p'] = []
    sdata['cdn'] = []
    sdata['fdb'] = []
    
    for i in data:
        if i.Timestamp != 24 :
            t = i.Timestamp
            allp2p = i.P2P.split(',')
            allcdn = i.CDN.split(',')
            for j in range(12):
                stime = starttime + count*5
                sdata['time'].append(datetime.fromtimestamp(stime).strftime('%M:%S'))
                p2p = float(allp2p[j])/float(40265318400)
                sdata['p2p'].append(float('%.4f'%p2p))
                cdn = float(int(allcdn[j])+1)/float(40265318400)       
                sdata['cdn'].append(float('%.4f'%cdn))
                fdb = float(allp2p[j])/float(int(allcdn[j])+1)
                if fdb > 6.0:
		            fdb = 6.0
                sdata['fdb'].append(float('%.4f'%fdb))
                count = count + 1
    return sdata

def flow_multi_day(fdate,tdate,ver,infohash,isp):
    qispid = liveBackend.models.isp_info.get_isp_id(isp)
    qinfohashid = liveBackend.models.infohash_info.objects.get(Name=infohash,Rate='800')
    qftype = liveBackend.models.flow_infohash_type.get_flowtype_id(ver,qinfohashid)
    data = liveBackend.models.flow_by_hour.objects.filter(Infohash_type=qftype,ISP_type=qispid,Timestamp=24,Date__gte=fdate, Date__lte=tdate).order_by("Date")
    
    sdata = {}
    sdata['time'] = []
    sdata['p2p'] = []
    sdata['cdn'] = []
    sdata['fdb'] = []
    for i in data:
        sdata['time'].append(str(i.Date))
        p2p = float(i.P2P)/float(40265318400)
        sdata['p2p'].append(float('%.4f'%p2p))
        cdn = float(int(i.CDN)+1)/float(40265318400)       
        sdata['cdn'].append(float('%.4f'%cdn))
        fdb = float(i.P2P)/float(int(i.CDN)+1)
        if fdb > 6.0:
            fdb = 6.0
        sdata['fdb'].append(float('%.4f'%fdb))
    return sdata

def flow(request):
    qver = request.GET.get("version")
    qinfohash = request.GET.get("infohash")
    qisp = request.GET.get("isp")
    qfdate = request.GET.get("from")
    qtdate = request.GET.get("to")
    if not qfdate and not qtdate and not qver and not qinfohash and not qisp:
        return render_to_response("live_flow.html", {"error":"Please select the query conditions"})
    elif cmp(qver,'All')==0 and cmp(qinfohash,u"所有")!=0:
        return render_to_response("live_flow.html", {"error":"Wrong condition! Please select again"})

    if cmp(qfdate,qtdate) == 0:
        sdata = flow_one_day(qfdate,qver,qinfohash,qisp)
        step=12
    else:
        sdata = flow_multi_day(qfdate,qtdate,qver,qinfohash,qisp)
        step=0

    if sdata['cdn'] and sdata['p2p'] and sdata['time'] and sdata['fdb']:
        return render_to_response("live_flow.html", {"content":sdata,"step":step,"fdate":qfdate,"tdate":qtdate})
    else:
        return render_to_response("live_flow.html", {"error":"No data","fdate":qfdate,"tdate":qtdate})

def selector(request):
    #Version
    versions = liveBackend.models.version_info.objects.all()
    para1 = []
    for i in versions:
        para1.append(i.Version)
    #Infohash
    infohashs = liveBackend.models.infohash_info.objects.all()
    para2 = []
    for i in infohashs:
        para2.append(i.Name)
    #ISP
    isps = liveBackend.models.isp_info.objects.all()
    para3 = []
    for i in isps:
        para3.append(i.ISP)

    qfdate = str((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
    qtdate = qfdate
    return render_to_response("live_selector.html", {"ver":para1,"infohash":para2,"isp":para3,"qver":"All","qinfohash":u"所有","qisp":u"所有","fdate":qfdate,"tdate":qtdate})

def selector_loc(request):
    #Version
    versions = liveBackend.models.version_info.objects.all()
    para1 = []
    for i in versions:
        para1.append(i.Version)
    #Infohash
    infohashs = liveBackend.models.infohash_info.objects.all()
    para2 = []
    for i in infohashs:
        para2.append(i.Name)
    #Loc
    isps = liveBackend.models.loc_info.objects.all()
    para3 = []
    for i in isps:
        para3.append(i.Location)

    qfdate = str((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
    qtdate = qfdate
    return render_to_response("live_loc_selector.html", {"ver":para1,"infohash":para2,"loc":para3,"qver":"All","qinfohash":u"所有","qloc":u"所有","fdate":qfdate,"tdate":qtdate})

def flow_one_day_loc(date,ver,infohash,loc):
    qlocid = liveBackend.models.loc_info.get_loc_id(loc)
    qinfohashid = liveBackend.models.infohash_info.objects.get(Name=infohash,Rate='800')
    qftype = liveBackend.models.flow_infohash_type.get_flowtype_id(ver,qinfohashid)
    data = liveBackend.models.flow_loc_by_hour.objects.filter(Infohash_type=qftype,Loc_type=qlocid,Date=date).order_by("Timestamp")

    starttime = time.mktime(datetime.strptime(date+' 00:00', '%Y-%m-%d %H:%M').timetuple())
    count=0
    sdata = {}
    sdata['time'] = []
    sdata['p2p'] = []
    sdata['cdn'] = []
    sdata['fdb'] = []
    
    for i in data:
        if i.Timestamp != 24 :
            t = i.Timestamp
            allp2p = i.P2P.split(',')
            allcdn = i.CDN.split(',')
            for j in range(12):
                stime = starttime + count*5
                sdata['time'].append(datetime.fromtimestamp(stime).strftime('%M:%S'))
                p2p = float(allp2p[j])/float(40265318400)
                sdata['p2p'].append(float('%.4f'%p2p))
                cdn = float(int(allcdn[j])+1)/float(40265318400)       
                sdata['cdn'].append(float('%.4f'%cdn))
                fdb = float(allp2p[j])/float(int(allcdn[j])+1)
                if fdb > 6.0:
		            fdb = 6.0
                sdata['fdb'].append(float('%.4f'%fdb))
                count = count + 1
    return sdata

def flow_multi_day_loc(fdate,tdate,ver,infohash,loc):
    qlocid = liveBackend.models.loc_info.get_loc_id(loc)
    qinfohashid = liveBackend.models.infohash_info.objects.get(Name=infohash,Rate='800')
    qftype = liveBackend.models.flow_infohash_type.get_flowtype_id(ver,qinfohashid)
    data = liveBackend.models.flow_loc_by_hour.objects.filter(Infohash_type=qftype,Loc_type=qlocid,Timestamp=24,Date__gte=fdate, Date__lte=tdate).order_by("Date")
    
    sdata = {}
    sdata['time'] = []
    sdata['p2p'] = []
    sdata['cdn'] = []
    sdata['fdb'] = []
    for i in data:
        sdata['time'].append(str(i.Date))
        p2p = float(i.P2P)/float(40265318400)
        sdata['p2p'].append(float('%.4f'%p2p))
        cdn = float(int(i.CDN)+1)/float(40265318400)       
        sdata['cdn'].append(float('%.4f'%cdn))
        fdb = float(i.P2P)/float(int(i.CDN)+1)
        if fdb > 6.0:
            fdb = 6.0
        sdata['fdb'].append(float('%.4f'%fdb))
    return sdata

def flow_loc(request):
    qver = request.GET.get("version")
    qinfohash = request.GET.get("infohash")
    qloc = request.GET.get("loc")
    qfdate = request.GET.get("from")
    qtdate = request.GET.get("to")
    if not qfdate and not qtdate and not qver and not qinfohash and not qloc:
        return render_to_response("live_flow.html", {"error":"Please select the query conditions"})
    elif cmp(qver,'All')==0 and cmp(qinfohash,u"所有")!=0:
        return render_to_response("live_flow.html", {"error":"Wrong condition! Please select again"})

    if cmp(qfdate,qtdate) == 0:
        sdata = flow_one_day_loc(qfdate,qver,qinfohash,qloc)
        step=12
    else:
        sdata = flow_multi_day_loc(qfdate,qtdate,qver,qinfohash,qloc)
        step=0

    if sdata['cdn'] and sdata['p2p'] and sdata['time'] and sdata['fdb']:
        return render_to_response("live_flow.html", {"content":sdata,"step":step,"fdate":qfdate,"tdate":qtdate})
    else:
        return render_to_response("live_flow.html", {"error":"No data","fdate":qfdate,"tdate":qtdate})

