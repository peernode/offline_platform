# Create your views here.
# -*- coding: utf-8 -*- 

import logging
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from vod.models import *

logger=logging.getLogger('flashVoD.debug_view')
def home(request):
    logger.debug("home request!!!")
    return render_to_response("vod_index.html")

def nav(request):
    return render_to_response("nav.html")

def panel(request):
    return render_to_response("panel.html")