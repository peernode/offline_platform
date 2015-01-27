# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from rate.models import *

def update_connect_ratio(request):
    result="ok"
    if request.method=='POST':
        decodes=json.loads(request.body)
        try:
            ver=version_info.get_version(decodes['ver'])
            create_date='%s-%s-%s'%(decodes['create_date'][0:4], decodes['create_date'][4:6], decodes['create_date'][6:8])
            # total suc info
            total_obj=connect_ratio(Date=create_date,
                                    Version=ver,
                                    ConnectType=0,
                                    Hour=decodes['hour'],
                                    PostTotal=decodes['post_total'],
                                    Fenzi=decodes['suc_total'])
            total_obj.save()

            # total offline info
            offline_obj=connect_ratio(Date=create_date,
                                    Version=ver,
                                    ConnectType=2,
                                    Hour=decodes['hour'],
                                    PostTotal=decodes['post_total'],                                    
                                    Fenzi=decodes['fail_total'])
            offline_obj.save()

            # first suc info
            first_obj=connect_ratio(Date=create_date,
                                    Version=ver,
                                    ConnectType=1,
                                    Hour=decodes['hour'],
                                    PostTotal=decodes['first_post_total'],
                                    Fenzi=decodes['first_suc_total'])
            first_obj.save()
            

            # first offline info
            first_offline_obj=connect_ratio(Date=create_date,
                                    Version=ver,
                                    ConnectType=3,
                                    Hour=decodes['hour'],
                                    PostTotal=decodes['first_post_total'],
                                    Fenzi=decodes['first_fail_total'])
            first_offline_obj.save()

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
