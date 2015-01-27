# -*- coding: utf-8 -*- 
from baseobj import *

class video_type_obj(baseobj):
    """clarity_type_obj"""
    @staticmethod
    def get_update_api():
        return 'update/video_type'

if __name__ == '__main__':
    import post_tools
    video_obj=video_type_obj()

    items={"0":"all", "1":"movie", "2":"tv", "3":"cartoon", "4":"variety", "5":"micro", "6":"other", "7":"vfilm"}
    for key in items.keys():
        video_obj.append_item(key, items[key])
    print video_obj.get_json_str()
    post_tools.post_data(video_obj.get_update_api(), video_obj.get_json_str())

