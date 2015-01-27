from django.http import HttpResponse, Http404

import json

from fbuffer import models
from fbuffer.models import web_fbuffer, web_fbuffer_records2, web_fbuffer_suc_rate
from vodBackend.models import version_info, ISP_info, Location_info, video_type, clarity_type

# Create your views here.
# update fbuffer time
def update_web_fbuffer(request):
    response = {'result':"error"}

    if request.method != "POST":
        return HttpResponse(json.dumps(response))

    try:
        req = json.loads(request.read())
        print(req)
        obj = web_fbuffer(isp=ISP_info(ISP=req['isp']), loc=Location_info(Location=req['loc']), ver=version_info(Version=req['ver']),
                                vtype=video_type(VideoType=req['vtype']), ctype=clarity_type(ClarityType=req['ctype']),
                                hour=req['hour'], date=req['date'], PNtype=req['PNtype'], PNvalue=req['PNvalue'])

        obj.save(force_insert=True)

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    response['result'] = "ok"
    return HttpResponse(json.dumps(response))

# updete records of fbuffer
def update_web_fbuffer_records(request):
    response = {'result':"error"}

    if request.method != "POST":
        return HttpResponse(json.dumps(response))

    try:
        req = json.loads(request.read())
        print(req)
        obj = web_fbuffer_records2(isp=ISP_info(ISP=req['isp']), loc=Location_info(Location=req['loc']), ver=version_info(Version=req['ver']),
                                vtype=video_type(VideoType=req['vtype']), ctype=clarity_type(ClarityType=req['ctype']),
                                hour=req['hour'], date=req['date'], count=req['count'])

        obj.save(force_insert=True)

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    response['result'] = "ok"
    return HttpResponse(json.dumps(response))

# updete records of fbuffer
def update_web_fbuffer_suc(request):
    response = {'result':"error"}

    if request.method != "POST":
        return HttpResponse(json.dumps(response))

    try:
        req = json.loads(request.read())
        print(req)
        obj = web_fbuffer_suc_rate(isp=ISP_info(ISP=req['isp']), loc=Location_info(Location=req['loc']), ver=version_info(Version=req['ver']),
                                vtype=video_type(VideoType=req['vtype']), ctype=clarity_type(ClarityType=req['ctype']),
                                hour=req['hour'], date=req['date'], sucrate=req['sucrate'])

        obj.save(force_insert=True)

    except Exception, e:
        response = {'result':"error - %s"%e}
        return HttpResponse(json.dumps(response))

    response['result'] = "ok"
    return HttpResponse(json.dumps(response))
