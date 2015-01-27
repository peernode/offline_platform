from django.test import TestCase

# Create your tests here.

import urllib2
import json


class PostDataTest(TestCase):
    
    def test_post_data(self):
        
        url = "http://127.0.0.1:8000/update/vod/playtm"
        
        request = {}
        request['isp'] = "1"
        request['loc'] = '0'
        request['ver'] = '20056'
        request['hour'] = '0'
        request['date'] = '2000-01-01'
        request['pchoke_ratio'] = 0.99
        request['ptr1'] = 0.01
        request['ptr2'] = 0.005
        
        
        req = urllib2.Request(url, headers={'Content-Type': 'application/json; charset=utf-8'},
                              data = json.dumps(request))
        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        
        response = opener.open(req)
        
        print response.read()
        
        self.assertEqual(response.status_code, 200)
