# -*- coding: utf-8 -*- 
import json

class baseobj(object):
    """base table: key - value"""
    def __init__(self):
        self.info={}

    def append_item(self, info_key, description):
        self.info[info_key]=description

    def get_json_str(self):
        json_str=json.dumps(self.info)
        return json_str