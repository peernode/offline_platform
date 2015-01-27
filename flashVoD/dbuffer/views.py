# -*- coding: utf-8 -*- 
import json
import csv
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dbuffer.models import *
from vod.date_time_tool import *

def update_dbuffer(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)

        try:      
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            ver = version_info.get_version(decodes['ver'])
            vt=video_type.get_video_type(decodes['video_type'])
            ctype=clarity_type.objects.get(ClarityType=decodes['clarity_type'])
            isp=ISP_info.get_ISP(decodes['ISP'])
            location=Location_info.get_location(decodes['Location'])
            hour=decodes['hour']

            countObj=vod_dbuffer_records(Date=create_date,
                            Version=ver,
                            VideoType=vt,
                            Clarity_type=ctype,
                            ISP=isp,
                            Location=location,
                            Hour=hour,
                            Count=decodes['recordCount'])
            countObj.save()

            PNValues=decodes['PNValues']
            for key in sorted(PNValues.keys()):
                obj=vod_dbuffer(Date=create_date,
                            Version=ver,
                            VideoType=vt,
                            Clarity_type=ctype,
                            ISP=isp,
                            Location=location,
                            Hour=hour,
                            PNType=key,
                            PNValue=PNValues[key])
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
