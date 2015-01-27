# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

import json
import datetime

from fbuffer import models
from fbuffer.models import web_fbuffer, web_fbuffer_records2, web_fbuffer_suc_rate
from vodBackend.models import version_info, ISP_info, Location_info, video_type, clarity_type

# Create your views here.

def scan_web_fbuffer_time_by_hour(request, date, ver, isp, vtype, ctype):
    subinfo = []
    for pt in ['25', '50', '75', '90', '95']:
        datas = web_fbuffer.objects.filter(date=date,hour__gte=0,hour__lte=23,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ctype.ClarityType,PNtype=pt).order_by("hour")

        data = []
        for item in datas:
            data.append(item.PNvalue*1.0)

        name = "%s_%s_P%s"%(request.GET.get("vtype", 'all'), ctype.Description, pt)

        subinfo.append('''{
            name: 'fbuffer_%s',
            data: %s
        }'''%(name, data))

    yaxis = []
    yaxis.append('''{
        labels: {
            format: '{value}ms',
        },
        title: {
            text: 'fbuffer time(ms)',
        }
    }''')

    re = {}
    re['idx'] = "fbuffer"
    re['charttype'] = '''{type: 'spline'}'''
    re['title'] = 'web fbuffer %s'%(date)
    re['suffix'] = 'ms'
    re['xaxis'] = range(0,24)
    re['tickinterval'] = 1
    re['yaxis'] = ','.join(yaxis)
    re['data'] = ','.join(subinfo)

    return re


def scan_web_fbuffer_records_by_hour(request, date, ver, isp, vtype, ctype):
    subinfo = []

    ctlist = [ctype]
    if ctype.ClarityType == 0:
        ctlist = clarity_type.objects.all()
    for ct in ctlist:
        datas = web_fbuffer_records2.objects.filter(date=date,hour__gte=0,hour__lte=23,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ct).order_by("hour")
	data = []
        for item in datas:
            data.append(item.count*1.0)
	
        name = "%s_%s"%(request.GET.get("vtype", 'all'), ct.Description)

        subinfo.append('''{
            name: 'fbuffer_%s',
	    type: 'column',
            data: %s
        }'''%(name, data))

	datas2 = web_fbuffer_suc_rate.objects.filter(date=date,hour__gte=0,hour__lte=23,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ct).order_by("hour")
	data = []
        for item in datas2:
            data.append(item.sucrate*1.0)

	subinfo.append('''{
            name: 'fbuffer_%s',
            type: 'spline',
	    yAxis: 1,
            data: %s
        }'''%(name, data))

    yaxis = []
    yaxis.append('''{
        labels: {
            format: '{value}',
        },
        title: {
            text: 'fbuffer records',
        }
    }''')
    yaxis.append('''{
        labels: {
            format: '{value}',
        },
        title: {
            text: 'fbuffer sucrate',
        },
	opposite: true
    }''')

    re = {}
    re['idx'] = "record"
    re['charttype'] = '''{zoomType: 'xy'}'''
    re['title'] = 'web fbuffer records by hour %s'%(date)
    re['suffix'] = ''
    re['xaxis'] = range(0,24)
    re['tickinterval'] = 1
    re['yaxis'] = ','.join(yaxis)
    re['data'] = ','.join(subinfo)

    return re


def query_web_fbuffer_by_hour(request):
    response = {'result':"error"}
    yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1), '%Y-%m-%d')

    try:
        date = request.GET.get("date", yesterday)
        ver = version_info.objects.filter(Description=request.GET.get("ver", "master"))[0]
        isp = ISP_info.objects.filter(Description=request.GET.get("isp", "所有"))[0]
	vtype = video_type.objects.filter(Description=request.GET.get("vtype", "all"))[0]
	ctype = clarity_type.objects.filter(Description=request.GET.get("ctype", "所有"))[0]

	print isp, ver, vtype, ctype
	
	fbuffer = {}	
	fbuffer['time'] = scan_web_fbuffer_time_by_hour(request, date, ver, isp, vtype, ctype)
	fbuffer['record'] = scan_web_fbuffer_records_by_hour(request, date, ver, isp, vtype, ctype)

	resp = []
	for key in ['time', 'record']:
	    resp.append(fbuffer[key])

        verlist = version_info.objects.all()
        isplist = ISP_info.objects.all()
	vtlist = video_type.objects.all()
	ctlist = clarity_type.objects.all()

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    now = datetime.datetime.now()
    return render_to_response('fbuffer_hour.html',
                              {'current_date':now, 'datalist':resp, 
				'verlist':verlist, 'isplist':isplist, 'vtlist':vtlist, 'ctlist':ctlist, 'date':date, 
				'selectedver':ver.Version, 'selectedisp':isp.ISP, 'selectedvt':vtype.VideoType, 'selectedct':ctype.ClarityType})


def scan_web_fbuffer_time_by_date(request, fromdate, todate, ver, isp, vtype, ctype):
    subinfo = []
    if_need_xaxis = True
    xaxis = []
    for pt in ['25', '50', '75', '90', '95']:
        datas = web_fbuffer.objects.filter(hour=24,date__gte=fromdate,date__lte=todate,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ctype.ClarityType, PNtype=pt).order_by("date")

        data = []
        for item in datas:
            data.append(item.PNvalue*1.0)

        if if_need_xaxis:
            for item in datas:
                xaxis.append("%s"%item.date)
            if_need_xaxis = False

        name = "%s_%s_P%s"%(request.GET.get("vtype", 'movie'), ctype.Description, pt)
        subinfo.append('''{
            name: 'fbuffer_%s',
            data: %s
        }'''%(name, data))

    yaxis = []
    yaxis.append('''{
        labels: {
            format: '{value}ms',
        },
        title: {
            text: 'fbuffer time(ms)',
        }
    }''')

    re = {}
    re['idx'] = "fbuffer"
    re['charttype'] = '''{type: 'spline'}'''
    re['title'] = 'web fbuffer %s - %s'%(fromdate, todate)
    re['suffix'] = 'ms'
    re['xaxis'] = xaxis
    re['tickinterval'] = 1 if len(xaxis)<=24 else round(len(xaxis)/24)
    re['yaxis'] = ','.join(yaxis)
    re['data'] = ','.join(subinfo)

    return re

def scan_web_fbuffer_record_by_date(request, fromdate, todate, ver, isp, vtype, ctype):
    subinfo = []
    if_need_xaxis = True
    xaxis = []
    ctlist = [ctype]
    if ctype.ClarityType == 0:
        ctlist = clarity_type.objects.all()
    for ct in ctlist:
        datas = web_fbuffer_records2.objects.filter(hour=24,date__gte=fromdate,date__lte=todate,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ct).order_by("date")

        data = []
        for item in datas:
            data.append(item.count*1.0)

        if if_need_xaxis:
            for item in datas:
                xaxis.append("%s"%item.date)
            if_need_xaxis = False

        name = "%s_%s"%(request.GET.get("vtype", 'all'), ct.Description)
        subinfo.append('''{
            name: 'fbuffer_%s',
	    type: 'column',
            data: %s
        }'''%(name, data))

	datas2 = web_fbuffer_suc_rate.objects.filter(hour=24,date__gte=fromdate,date__lte=todate,isp=isp.ISP,ver=ver.Version,vtype=vtype.VideoType,ctype=ct).order_by("date")
        data = []
        for item in datas2:
            data.append(item.sucrate*1.0)

        subinfo.append('''{
            name: 'fbuffer_%s',
            type: 'spline',
            yAxis: 1,
            data: %s
        }'''%(name, data))

    yaxis = []
    yaxis.append('''{
        labels: {
            format: '{value}',
        },
        title: {
            text: 'fbuffer records',
        }
    }''')
    yaxis.append('''{
        labels: {
            format: '{value}',
        },
        title: {
            text: 'fbuffer sucrate',
        },
        opposite: true
    }''')

    re = {}
    re['idx'] = "record"
    re['charttype'] = '''{zoomType: 'xy'}'''
    re['title'] = 'web fbuffer record %s - %s'%(fromdate, todate)
    re['suffix'] = ''
    re['xaxis'] = xaxis
    re['tickinterval'] = 1 if len(xaxis)<=24 else round(len(xaxis)/24)
    re['yaxis'] = ','.join(yaxis)
    re['data'] = ','.join(subinfo)

    return re

def query_web_fbuffer_by_date(request):
    response = {'result':"error"}

    try:
	default_from = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=14), '%Y-%m-%d')
	default_to = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1), '%Y-%m-%d')
    	
	fromdate = request.GET.get("from", default_from)
        todate = request.GET.get("to", default_to)
        if fromdate == '' or todate == '':
            response = {'result':"Both FROM and TO can not be empty"}
            return HttpResponse(json.dumps(response))    
	
	print fromdate, todate

	ver = version_info.objects.filter(Description=request.GET.get("ver", "master"))[0]
        isp = ISP_info.objects.filter(Description=request.GET.get("isp", "所有"))[0]
	vtype = video_type.objects.filter(Description=request.GET.get("vtype", "all"))[0]
	ctype = clarity_type.objects.filter(Description=request.GET.get("ctype", "所有"))[0]

	print ver, isp, vtype, ctype

        fbuffer = {}	
	fbuffer['time'] = scan_web_fbuffer_time_by_date(request, fromdate, todate, ver, isp, vtype, ctype)
	fbuffer['record'] = scan_web_fbuffer_record_by_date(request, fromdate, todate, ver, isp, vtype, ctype)

	resp = []
        for key in ['time', 'record']:
	    resp.append(fbuffer[key])

        verlist = version_info.objects.all()
        isplist = ISP_info.objects.all()
        vtlist = video_type.objects.all()
	ctlist = clarity_type.objects.all()

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    now = datetime.datetime.now()
    return render_to_response('fbuffer_date.html',
                              {'current_date':now, 'datalist':resp,
                                'verlist':verlist, 'isplist':isplist, 'vtlist':vtlist, 'ctlist':ctlist, 'fromdate':fromdate, 'todate':todate, 
				'selectedver':ver.Version,'selectedisp':isp.ISP, 'selectedvt':vtype.VideoType, 'selectedct':ctype.ClarityType})	

