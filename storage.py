# -*- coding: utf-8 -*-
import urllib
import json
from base import Base
import updatesql
#import DBmanager
import readclass 

class Storage(object):
    def getPic(self, accessToken, off):
	postJson = {"type":'image',"offset":off,"count":1}
	postJson = json.dumps(postJson)
        getUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % accessToken
        if isinstance(postJson, unicode):
            postJson = postJson.encode('utf-8')
        urlResp = urllib.urlopen(url=getUrl, data=postJson)
        return urlResp.read()
	
    def parse_to_list(self, urlResp):
	urlResp = json.loads(urlResp)

	img_list = []
	for items in urlResp['item']:
		sub_list = []
		sub_list.append(items.get('name').split('.',1)[0].upper())
		sub_list.append(items.get('media_id'))
		sub_list.append(items.get('url'))
		img_list.append(sub_list)

	return json.dumps(img_list)


if __name__ == '__main__':
    
    sto = Storage()
    accessToken = Base().get_access_token()

    #myMenu.delete(accessToken)
    offset = 0
    while offset < 1:
    	imgList = sto.parse_to_list(sto.getPic(accessToken, offset))
    	print "@@@@", imgList
	offset += 1
    	updatesql.courseupdate(eval(imgList))