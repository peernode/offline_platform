# -*- coding: utf-8 -*- 
from baseobj import *

class Location_info_obj(baseobj):
    """ISP info obj"""
    @staticmethod
    def get_update_api():
        return 'update/Location_info'

if __name__ == '__main__':
    import post_tools
    Location_obj=Location_info_obj()

    items={"0":u"所有", "1":u"广东", "2":u"上海", "3":u"北京"}
    for key in items.keys():
        Location_obj.append_item(key, items[key])
    print Location_obj.get_json_str()
    post_tools.post_data(Location_obj.get_update_api(), Location_obj.get_json_str())