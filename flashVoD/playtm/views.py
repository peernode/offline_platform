# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import json
import datetime

from playtm import models
from playtm.models import web_playtm
from vodBackend.models import version_info, ISP_info, Location_info, video_type, clarity_type

# Create your views here.

def update_web_playtm(request):
    response = {'result':"error"}
    
    if request.method != "POST":       
        return HttpResponse(json.dumps(response))
    
    try:
        req = json.loads(request.read())
        print(req)
        obj = web_playtm(isp=ISP_info(ISP=req['isp']), loc=Location_info(Location=req['loc']), ver=version_info(Version=req['ver']),
                           	vtype=video_type(VideoType=req['vtype']), ctype=clarity_type(ClarityType=req['ctype']), 
				hour=req['hour'], date=req['date'], pchoke_ratio=req['pchoke_ratio'],
                               	ptime_ratio1=req['ptr1'], ptime_ratio2=req['ptr2'])
        
        obj.save(force_insert=True)
        
    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))
    
    response['result'] = "ok"
    return HttpResponse(json.dumps(response))

def query_web_playtm_by_hour(request):
    response = {'result':"error"}
    yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1), '%Y-%m-%d')

    try:
        date = request.GET.get("date", yesterday)
        vers = version_info.objects.filter(Description=request.GET.get("ver"))
        isps = ISP_info.objects.filter(Description=request.GET.get("isp"))
	vtypes = video_type.objects.filter(Description=request.GET.get("vtype"))

        isp = 0 if isps.count()==0 else isps[0].ISP 
        ver = 1 if vers.count()==0 else vers[0].Version
	vtype = 1 if vtypes.count()==0 else vtypes[0].VideoType
	print isp, ver, vtype
	
	keys = ['pchoke', 'ptime1', 'ptime2']

	subinfo = {}
	for key in keys:
	    subinfo[key] = []
	
	ctypelist = clarity_type.objects.all()
	for ct in ctypelist:
	    datas = web_playtm.objects.filter(date=date,hour__gte=0,hour__lte=23,isp=isp,ver=ver,vtype=vtype,ctype=ct).order_by("hour")

	    data = {}
	    for key in keys:
            	data[key] = []
	    
            for item in datas:
            	data['pchoke'].append(item.pchoke_ratio)
	        data['ptime1'].append(item.ptime_ratio1)
            	data['ptime2'].append(item.ptime_ratio2)
	
	    name = "%s_%s"%(request.GET.get("vtype", 'movie'), ct.Description)
	    #print data
	    for key in keys:
	    	subinfo[key].append('''{
                    name: '%s_%s',
                    data: %s
                }'''%(key, name, data[key]))
	
	resp = []
	for key in keys:    	
	   resp.append({'idx':key, 'title':'web playtm - %s, %s'%(key, date), 'xaxis':range(0,24), 'data':','.join(subinfo[key])})

        verlist = version_info.objects.all()
        isplist = ISP_info.objects.all()
	vtlist = video_type.objects.all()

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    now = datetime.datetime.now()
    return render_to_response('playtm_hour.html',
                              {'current_date':now, 'datalist':resp, 
				'verlist':verlist, 'isplist':isplist, 'vtlist':vtlist, 'date':date, 'selectedver':ver, 
				'selectedisp':isp, 'selectedvt':vtype})

def query_web_playtm_by_date(request):
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

	vers = version_info.objects.filter(Description=request.GET.get("ver"))
        isps = ISP_info.objects.filter(Description=request.GET.get("isp"))
	vtypes = video_type.objects.filter(Description=request.GET.get("vtype"))

        isp = 0 if isps.count()==0 else isps[0].ISP
        ver = 1 if vers.count()==0 else vers[0].Version
	vtype = 1 if vtypes.count()==0 else vtypes[0].VideoType

	keys = ['pchoke', 'ptime1', 'ptime2']

        subinfo = {}
        for key in keys:
            subinfo[key] = []

	if_need_xaxis = True
	xaxis = []
        ctypelist = clarity_type.objects.all()
        for ct in ctypelist:
            datas = web_playtm.objects.filter(hour=24,date__gte=fromdate,date__lte=todate,isp=isp,ver=ver,vtype=vtype,ctype=ct).order_by("date")

            data = {}
            for key in keys:
                data[key] = []

            for item in datas:
                data['pchoke'].append(item.pchoke_ratio)
                data['ptime1'].append(item.ptime_ratio1)
                data['ptime2'].append(item.ptime_ratio2)

	    if if_need_xaxis:
		for item in datas:
		    xaxis.append("%s"%item.date)
		if_need_xaxis = False

            name = "%s_%s"%(request.GET.get("vtype", 'movie'), ct.Description)
            #print data
            for key in keys:
                subinfo[key].append('''{
                    name: '%s_%s',
                    data: %s
                }'''%(key, name, data[key]))

	tickinterval = 1 if len(xaxis)<=24 else round(len(xaxis)/24)

        resp = []
        for key in keys:
           resp.append({'idx':key, 'title':'web playtm - %s, %s - %s'%(key, fromdate, todate), 'xaxis':xaxis, 'tickinterval':tickinterval, 'data':','.join(subinfo[key])})

        verlist = version_info.objects.all()
        isplist = ISP_info.objects.all()
        vtlist = video_type.objects.all()

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    now = datetime.datetime.now()
    return render_to_response('playtm_date.html',
                              {'current_date':now, 'datalist':resp,
                                'verlist':verlist, 'isplist':isplist, 'vtlist':vtlist, 'fromdate':fromdate, 'todate':todate, 'selectedver':ver,
                                'selectedisp':isp, 'selectedvt':vtype})	

