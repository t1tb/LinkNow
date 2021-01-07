# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
#import web
import lxml
import time
import os
import reply
import receive
import urllib
import cv2
import numpy as np
import OCRread
import pyodbc
from OCRread import OCRread
from DBmanager import DBmanager
from datetime import datetime
import json



class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "mywechat" #你的暗号

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self, webData):
        try:
            
            print webData
            recMsg = receive.parse_xml(webData)

            toUser = recMsg.FromUserName 
            fromUser = recMsg.ToUserName
            menu = "以下为菜单，输入“菜单”重新获取：\n ⭐ 如果您在寻找同一节课的兄弟姐妹们，请回复”1“\n ⭐ 如果您对Penn State各大社团感兴趣，请回复“2”"
            
            if recMsg.MsgType == 'event':
                if recMsg.EventType == 'subscribe':

       	    		content = "你要关注我，我有什么办法。随便发点什么试试吧" + '\n\n' + menu
		
			replyMsg = reply.TextMsg(toUser, fromUser, content)

            		return replyMsg.send()
		elif recMsg.EventType == 'CLICK':
			if recMsg.Eventkey == 'lookFor':
				content = '感谢使用我们的OCR功能，请以图片格式发送您的课表。\n 👉请尽量截图以保证图片质量 \n 👉目前功能还处于试验阶段，还不能保证100%识别准确率 \n 👉 可以选择手动输入课程名称和课号，例如，ECON 102'

            elif  recMsg.MsgType == 'image':
                mediaId = recMsg.MediaId
                picUrl = recMsg.PicUrl
                print('image processing..')
                courselst, ocrOut = self.Match_Class(self.savePic(toUser,picUrl))
                print('insert succeed \n')
                content = '识别出结果：\n'
                couter = 0
                if courselst !=[]:
                    for i in ocrOut:
                        content = content + "<a href = '"+ bytes(courselst[couter]).encode('utf-8') + "'>" + bytes(i[0]) +" "+ bytes(i[1]) + "</a> "
                        # content = content + "<a href = 'http://40.76.91.78/img?id=" + str(courselst[couter])+ " '>" + bytes(i[0]) +" "+ bytes(i[1]) + "</a> "
                        # print(courselst[couter],i[0],i[1])
                        content = content + '\n'
                        couter = couter + 1
                content = content + '点击课名就可以加入对应课友群啦~'
                print '回复用户：'+ toUser + '\n内容：'+ content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                content = recMsg.Content
                if content == '1':
                    content = '感谢使用我们的OCR功能，请以图片格式发送您的课表。\n 👉请尽量截图以保证图片质量 \n 👉目前功能还处于试验阶段，还不能保证100%识别准确率 \n 👉 可以选择手动输入课程名称和课号，例如，ECON 102'
                elif content == '2':
                    content = """       社团招新群列表🌈
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNyDn8zxWH3uJmDMtjvqPDQTPAx5DmlpiaibjiayOTh3sWsUukK6PIXib4Og/0?wx_fmt=jpeg'>👉PSU CSSA</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNkEuFYrx3FHmrk2DCTX8MphpJ9woNVa2SHRz7O5nZNeoWtzow4s4Aicw/0?wx_fmt=jpeg'>👉NP摄影社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpN5vGzibickxMo1A6RmpicLY9PMC43yCSlR2ibC8ALOO4ozjgm0PNxVATr8Q/0?wx_fmt=jpeg'>👉心家团契</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNzZv8M3VrtUbJWiamdoRhUv5tHhnED0xWAkpgcDk9nIc9FSm7D2kuTnw/0?wx_fmt=jpeg'>👉RoboX</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNEoezsrhl71TgUeKmhx0My3QYzhyWIwicMLXPOxicE5cWe7Cl0WOvjVog/0?wx_fmt=jpeg'>👉Bounce街舞社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNvDjQD2EZDnEXj4Jkp3cMeZs0qTlMBXnkCKY4djrc3ZSn1ZZWxN6aOQ/0?wx_fmt=jpeg'>👉ECO环境保护社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNBlR8BMWWKshYibyphHaPE0bpicK2GgiapXbktnIZYU7kcV8fY2q3hqX3g/0?wx_fmt=jpeg'>👉中国象棋社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNdfiatdhpe4YYMB1kRMBepy9pCicdlqDlHxy9L7aPIicZ3SrnVzFn3OPUQ/0?wx_fmt=jpeg'>👉ACMC民乐社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNlASmE8QHeLIhdNP7Ho2plVs3lAkrKFwoiaicT5gXoyLpeKzBAr8qraOA/0?wx_fmt=jpeg'>👉华人网球社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNoXrn1TGtxJeLlCVWiaTibAHOTVgFVrRkjxLFrnkP7diatsZia7XyJBrxxg/0?wx_fmt=jpeg'>👉PSU CUSA</a>\n更多社团介绍 <a href = 'https://zhuanlan.zhihu.com/p/61912110'>👉点击这里</a>  """
                    	

                elif content == '3':
                    content = '感谢您的回复，目前功能还在开发，敬请期待'
                elif content == '菜单':
                    content = menu
                else:
                    read = ReadClass(recMsg.Content)

		    print '@@@@@'
            if read.check_if_classMsg():
		    	course_list, course_with_no_num = read.find_course()
            print '@@@@@'
			url_list = self.find_url(course_list,toUser)
			print url_list
            print '@@@@@'
            		url_list = eval(json.dumps(url_list))
                    print '@@@@@'
			content = '检测到您发送的消息包含以下课程：\n'
			for i, j in zip(course_list, url_list):
				#print('h =@@@@@@@@@@ ',i)
                if not j == '':
				    content += "<a href = '" + j + "'>👉" + i[0]+ ' ' + i[1]+ '</a>\n'
                else:
                    content +=  "👉" + i[0]+ ' ' + i[1]+ '\n'
			content += '点击对应课程名称就可以加入课友群啦~\n如果点击没有出现二维码说明我们目前还没有对应的课友群，我们会尽快更新，感谢您的支持！'
			if not course_with_no_num == []:
				content += '\n我们还识别出了一些未提供课号的课程，如下：\n'
				for i in course_with_no_num:
					content += i + '  '
				content += '\n请您检查后按我们提供的格式带上课号再发送一次，谢谢。'
				print url_list
		    else:
			content = '本机器人目前还不会聊天哦，'+menu           
	    replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        except Exception as e:
            print(e)
            return 'success'


    # def Match_Class(self,imgDir):
    #     try:
    #         OCRreader=OCRread()
    #         OCRreader.ReadClass(str(imgDir))
    #         print 'read succeed'
    #         server_name = 'wechatnameserver.database.windows.net'
    #         database = 'MyWeChat'
    #         conn = DBmanager(server_name = server_name, database = database)
    #         print 'connect server'
    #         courselst = conn.insert_student(OCRreader)
    #         print 'insert succeed'
    #         return courselst, OCRreader.classtable
    #     except Exception as e:
    #         print(err)

    def Match_Class(self,imgDir):
    	server_name = 'wechatnameserver.database.windows.net'
    	database = 'MyWeChat'
        try:
            OCRreader=OCRread()
            OCRreader.ReadClass(str(imgDir))
            print 'read succeed'
            
            conn = DBmanager(server_name = server_name, database = database)
            print 'connect server'
            OCRreader.classtable = self.checkNum(OCRreader.classtable)
            print(OCRreader.classtable)
            courselst = conn.insert_student(OCRreader)
            print 'insert succeed'
            return courselst, OCRreader.classtable
        except Exception as err:
            print(err)


    def find_url(self,arr,toUser):
        studentID = toUser
        '''run in testing database'''
        server_name = 'wechatnameserver.database.windows.net'
        database = 'MyWeChat'
        conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:'+server_name+',1433;Database='+database+';Uid=Wechat;Pwd={AzureDB1!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        

        year = datetime.now().strftime('%Y')
        month = datetime.now().strftime('%m')
        date = datetime.now().strftime('%d')
        
        try:
            courselst = []
            cursor = conn.cursor()
            print('this is OCR: ',arr)
            counter = 0
            for row in arr:
                counter = counter + 1
            for i in range(counter):

                if cursor.execute('select top 1 ClassID from Course where ClassName = ? and ClassNum = ?;',arr[i][0],arr[i][1]).fetchall() != []:

                    classID,url = cursor.execute('select top 1 ClassID,Url from Course where ClassName = ? and ClassNum = ?;',arr[i][0],arr[i][1]).fetchall()[0]
                    
                    cursor.commit()
                    courselst.append(url)
                    
                    
                    cursor.execute('insert into Student(CourseID,WxId,year,month,date) values (?,?,?,?,?);',classID,studentID,year,month,date)
                    print('inserting {} {} {} for {}'.format(classID, arr[i][0],arr[i][1],studentID))
                    cursor.commit()
                else:
                    print('NO SUCH COURSE YET!')
                    
                    num_request = cursor.execute('select top 1 num_requested from course_to_update where ClassName = ? and ClassNum = ?;',arr[i][0],arr[i][1]).fetchall()
                    
                    if num_request != []:
                        for (quantity,) in num_request:
                    	   cursor.execute('update course_to_update set num_requested = ? where ClassName = ? and ClassNum = ?;',int(quantity)+1,arr[i][0],arr[i][1])
                		
                    	cursor.commit()	
                    else:
                    	cursor.execute('insert into course_to_update(ClassName,ClassNum,num_requested) values (?,?,?);',arr[i][0],arr[i][1],1)
                    	cursor.commit()
                    
                    
                    courselst.append(None)
                    

                    #newCourseID = self.insert_newCourse(className = arr[i][0],classNum = arr[i][1])
                    # print('@@@inserting {} {} {} for {}'.format(newCourseID, OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))
                    
                    # print('NOW WE WILL GENERATE QR CODE for new course: {} {} {} for student {}.'.format(newCourseID,OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))                    
            cursor.close()
            # print(courselst)
            return courselst
        except pyodbc.Error as ex:
            logging.error('Insert new student on Student error msg: '+ str(ex))
            cursor.close()

    def savePic(self, userID, picUrl):
        path = '/home/AzureUser/WeChat/userImage'
        try:
            url_response = urllib.urlopen(picUrl)
            img_array = np.array(bytearray(url_response.read()), dtype = np.uint8)
            img = cv2.imdecode (img_array, -1)
            tmp = userID+'.png'
            print '++ Saving the image', tmp
            file_path = os.path.join(path,tmp)
            cv2.imwrite(file_path, img)
            print 'image saved!'
            return file_path
        except Exception as e:
            print(1,e)
        
    def checkNum(self,classArray):
    # '''
    #   OCR classArray is a 2D list, contains 0:className 1:classNum
    # '''

        for row in classArray:
            row[0] = row[0].upper()
            row[1] = row[1].replace('I','1')
            row[1] = row[1].replace('O','0')
        return classArray

	#def record_courseNotFound(self,classArray):


class ReadClass:
    def __init__(self, msg):
        self.msg = msg
        with open('CLASSLIST') as f:
                self.classlist = f.readlines()
                self.classlist = [x.strip() for x in self.classlist]
                self.classlist = filter(None, self.classlist)
    

    def find_course(self):
        

        classFound = []
        class_no_num = []
        for i in self.classlist:
            n = 0
            while n < len(self.msg):
                if self.msg[n:len(self.msg)].upper().find(i) == -1:
                    
                    break
                #if not self.msg[n:len(self.msg)].upper().find(i) == -1:
                classNum = ''
                
                n += self.msg[n:len(self.msg)].upper().find(i)
                n = n + len(i)
                
                while n<len(self.msg) and self.msg[n] == ' ':
                    n += 1
                    
                tmp = n

                while n<len(self.msg) and self.msg[n] in ['0','1','2','3','4','5','6','7','8','9']:
                    
                    classNum = classNum + self.msg[n]
                    n += 1
                if not n == tmp:
                    if n<len(self.msg) and self.msg[n].isalpha(): 
                        if n+1>=len(self.msg) or not self.msg[n+1].isalpha(): 
                            classNum = classNum + self.msg[n].upper()

                    #print i,classNum
                    classFound.append([i, classNum])
                else:
                    class_no_num.append(i)
                    print i +': class number not found'


        for i in classFound:
            for j in classFound:                
            	if j[0].find(i[0])!=-1 and len(i[0]) < len(j[0]) and i[1] == j[1]:
                    classFound.remove(i)

        print 'Class found:'
	print classFound
	
	for i in class_no_num:
            for j in class_no_num:
                #str = 
                if j.find(i)!=-1 and len(i) < len(j):
                    class_no_num.remove(i)
	print 'Class with no class number:'
	print class_no_num
        return classFound, class_no_num

    def check_if_classMsg(self):
        for i in self.classlist:
                if not self.msg.upper().find(i) == -1:
                    return True


if __name__ == "__main__":
    xml = """<xml><ToUserName><![CDATA[gh_5bbceda1db81]]></ToUserName>
<FromUserName><![CDATA[oiRDG6TUBJivzafkFJztQQ8Ft0ZA]]></FromUserName>
<CreateTime>1598220501</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[ee 302 math 140]]></Content>
<MsgId>22881014693836433</MsgId>
</xml>"""
    handle = Handle()
    print handle.POST(xml)
