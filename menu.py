# -*- coding: utf-8 -*-
import urllib
from base import Base

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()
        
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

if __name__ == '__main__':
    
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "view",
                "name": "找组织",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "社团大汇总",
                        "url": "https://zhuanlan.zhihu.com/p/61912110"
                    },
                    {
                        "type": "click",
                        "name": "找课友",
                        "key":  "lookFor"
                    },

                ]
            },
            {   
                "type": "view"
                "name": "七夕限定",
                "url": "https://forms.gle/dNRceDQ2pThs7cuk7"
                
            },
            {
                "type": "media_id",
                "name": "PSU百亿社团",
                "media_id": "IifbnE4gVaqd8CBPBIVoDoEAjXk7kxyNbci86FI1C_Q"
            }
        ]
    }
    """
    accessToken = Base().get_access_token()
    #myMenu.delete(accessToken)

    myMenu.create(postJson, accessToken)
