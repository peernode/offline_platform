from django.http import HttpResponse
import json
import liveBackend.models
# Create your views here.

def update_ver_info(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        for key in decodes.keys():
            try:
                vft=liveBackend.models.version_info(VType=key, Version=decodes[key])
                vft.save()
            except BaseException, e:
                result = "save error:"+ e.message
                break
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_infohash_info(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        infohashid = decodes['infohash']
        infohashname = decodes['name']
        infohashrate = decodes['rate']
        try:
            vft=liveBackend.models.infohash_info(Infohash=infohashid,Name=infohashname,Rate=infohashrate)
            vft.save()
        except BaseException, e:
            result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")
    
def update_flow_type(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        try:
            version = liveBackend.models.version_info.get_version_type(decodes['ver'])
            infohash = liveBackend.models.infohash_info.objects.get(Infohash=decodes['infohash'])

            vft=liveBackend.models.flow_infohash_type(FType=decodes['type'], Ver=version, Infohash=infohash)
            vft.save()
        except BaseException, e:
            result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_isp_info(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        for key in decodes.keys():
            try:
                vft=liveBackend.models.isp_info(IType=key, ISP=decodes[key])
                vft.save()
            except BaseException, e:
                result = "save error:"+ e.message
                break
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_loc_info(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        for key in decodes.keys():
            try:
                vft=liveBackend.models.loc_info(LType=key, Location=decodes[key])
                vft.save()
            except BaseException, e:
                result = "save error:"+ e.message
                break
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_flow_by_hour(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            fdate = decodes['date']
            flow_type = liveBackend.models.flow_infohash_type.get_flowtype_id(decodes['ver'], decodes['infohash'])
            ftime = decodes['timestamp']

            count = 0
            vlen = len(decodes['isp'])
            while count < vlen:
                ispid = liveBackend.models.isp_info.get_isp_id(decodes['isp'][count]['name'])
                p2p = decodes['isp'][count]['P2P']
                cdn = decodes['isp'][count]['CDN']
                count = count + 1
                vft=liveBackend.models.flow_by_hour(Infohash_type=flow_type,ISP_type=ispid,Date=fdate,Timestamp=ftime,P2P=p2p,CDN=cdn)
                vft.save()
        except BaseException, e:
           result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_flow_loc_by_hour(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        try:
            fdate = decodes['date']
            flow_type = liveBackend.models.flow_infohash_type.get_flowtype_id(decodes['ver'], decodes['infohash'])
            ftime = decodes['timestamp']

            count = 0
            vlen = len(decodes['loc'])
            while count < vlen:
                locid = liveBackend.models.loc_info.get_loc_id(decodes['loc'][count]['name'])
                p2p = decodes['loc'][count]['P2P']
                cdn = decodes['loc'][count]['CDN']
                count = count + 1
                vft=liveBackend.models.flow_loc_by_hour(Infohash_type=flow_type,Loc_type=locid,Date=fdate,Timestamp=ftime,P2P=p2p,CDN=cdn)
                vft.save()
        except BaseException, e:
           result = "save error:"+ e.message
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_connect_type(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        for key in decodes.keys():
            try:
                vft=liveBackend.models.connect_type(ConnectType=key, Description=decodes[key])
                vft.save()
            except BaseException, e:
                result = "save error:"+ e.message
                break
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

def update_rate_type(request):
    result="ok"
    if request.method == 'POST':
        decodes = json.loads(request.body)
        #print decodes
        for key in decodes.keys():
            try:
                vft=liveBackend.models.rate_type(RateType=key, Description=decodes[key])
                vft.save()
            except BaseException, e:
                result = "save error:"+ e.message
                break
    else:
        result="error"

    respStr=json.dumps({"result":result})
    return HttpResponse(respStr, content_type="text/html")

