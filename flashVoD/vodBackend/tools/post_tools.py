# -*- coding: utf-8 -*- 

import urllib
import urllib2

def post_data(url, json_str):
    url='http://127.0.0.1:8000/%s'%url
    req=urllib2.Request(url, json_str, {'Content-Type': 'application/json'})
    f=urllib2.urlopen(req)
    s=f.read()
    print s

