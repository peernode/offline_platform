# -*- coding: utf-8 -*-
from baseobj import *

class version_info_obj(baseobj):
    """version info obj"""
    @staticmethod
    def get_update_api():
        return 'update/version'

if __name__ == '__main__':
    import post_tools
    version_obj = version_info_obj()

    items={"0":"all", "1":"master", "2":"beta", "3":"VIP"}
    for key in items.keys():
        version_obj.append_item(key, items[key])

    print version_obj.get_json_str()
    post_tools.post_data(version_obj.get_update_api(), version_obj.get_json_str())