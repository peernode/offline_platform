# -*- coding: utf-8 -*- 
from baseobj import *

class connect_type_obj(baseobj):
    """connect type obj"""
    @staticmethod
    def get_update_api():
        return 'update/connect_type'

if __name__ == '__main__':
    import post_tools
    connect_obj=connect_type_obj()

    items={"0":u"所有投递", "1":u"首次投递", "2":u"所有下线比例", "3":u"首次下线比例"}
    for key in items.keys():
        connect_obj.append_item(key, items[key])
    print connect_obj.get_json_str()
    post_tools.post_data(connect_obj.get_update_api(), connect_obj.get_json_str())

