# Create your views here.
from django.http import HttpResponse
import json
from delay.models import *

# Create your views here.

def update_delay(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            ddate = decodes['date']
            dinfohash = infohash_info.objects.get(Name=decodes['infoname'])

            count = 0
            dlen = len(decodes['infohash'])
            while count < dlen:
                dguid = decodes['infohash'][count]['guid']
                flow_type = flow_infohash_type.get_flowtype_id(decodes['infohash'][count]['ver'], dinfohash.Infohash)
                disp = isp_info.get_isp_id(decodes['infohash'][count]['isp'])
                dstart = decodes['infohash'][count]['start']
                dend = decodes['infohash'][count]['end']
                delay = decodes['infohash'][count]['delay']
                play = decodes['infohash'][count]['play']
                vft=delay_by_play(Infohash_type=flow_type, ISP_type=disp, Date=ddate, Guid=dguid, Delay_chunks=delay, Play_counts=play, Play_start=dstart, Play_end=dend)
                vft.save()
                count = count + 1
        except BaseException, e:
            result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_delay_record(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            ddate = decodes['date']
            dinfohash = infohash_info.objects.get(Name=decodes['infohash'])
            flow_type = flow_infohash_type.get_flowtype_id(decodes['ver'], dinfohash.Infohash)
            count = 0
            dlen = len(decodes['isp'])
            while count < dlen:
                disp = isp_info.get_isp_id(decodes['isp'][count]['name'])
                record = decodes['isp'][count]['record']
                vrecord = decodes['isp'][count]['vrecord']
                vft=delay_records(Infohash_type=flow_type, ISP_type=disp, Date=ddate, Records=record, ValidRecords=vrecord)
                vft.save()
                count = count + 1
        except BaseException, e:
            result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")