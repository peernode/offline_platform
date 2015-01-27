import json
from django.http import HttpResponse
from vodBackend.models import *

def update_video_type(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        for key in sorted(decodes.keys()):
            try:
                obj=video_type(VideoType=key, Description=decodes[key])
                obj.save(force_insert=True)
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

def update_clarity_type(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        for key in sorted(decodes.keys()):
            try:
                obj=clarity_type(ClarityType=key, Description=decodes[key])
                obj.save(force_insert=True)
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

def update_version_info(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)
        for key in sorted(decodes.keys()):
            try:
                obj=version_info(Version=key, Description=decodes[key])
                obj.save(force_insert=True)
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

def update_ISP_info(request):
    result="ok"
    if request.method == 'POST':
        decodes=json.loads(request.body)
        for key in sorted(decodes.keys()):
            try:
                obj=ISP_info(ISP=key, Description=decodes[key])
                obj.save(force_insert=True)
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

def update_location_info(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)
        for key in sorted(decodes):
            try:
                print key
                obj=Location_info(Location=key, Description=decodes[key])
                obj.save(force_insert=True)
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

def update_connect_type(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)
        for key in sorted(decodes):
            try:
                obj=connect_type(ConnectType=key, Description=decodes[key])
                obj.save(force_insert=True)
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

