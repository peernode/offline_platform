# -*- coding: utf-8 -*- 
from baseobj import *

class ISP_info_obj(baseobj):
    """ISP info obj"""
    @staticmethod
    def get_update_api():
        return 'update/ISP_info'

if __name__ == '__main__':
    import post_tools
    ISP_obj=ISP_info_obj()

    items={"0":u"所有", "1":u"电信", "2":u"联通", "3":u"其他"}
    for key in items.keys():
        ISP_obj.append_item(key, items[key])
    print ISP_obj.get_json_str()
    post_tools.post_data(ISP_obj.get_update_api(), ISP_obj.get_json_str())