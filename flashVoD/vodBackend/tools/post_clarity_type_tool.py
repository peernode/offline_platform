# -*- coding: utf-8 -*- 
from baseobj import *

class clarity_type_obj(baseobj):
    """clarity_type_obj"""
    @staticmethod
    def get_update_api():
        return 'update/clarity_type'

if __name__ == '__main__':
    import post_tools
    clarity_obj=clarity_type_obj()

    items={"0":u"所有", "1":u"流畅", "2":u"标清", "3":u"高清", "4":u"超清"}
    for key in items.keys():
        clarity_obj.append_item(key, items[key])
    print clarity_obj.get_json_str()
    post_tools.post_data(clarity_obj.get_update_api(), clarity_obj.get_json_str())