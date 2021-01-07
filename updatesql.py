from DBmanager import DBmanager
import pyodbc
# import os
import glob
# import re
import readclass
server_name = 'wechatnameserver.database.windows.net'
database = 'MyWeChat'
# conn = DBmanager(server_name = server_name, database = database)




'''
the method ge all filenames under the subdir
'''


path = '/home/AzureUser/WeChat/img'

# def getlst(table):
# 	path = '/home/AzureUser/WeChat/img'
# 	lst = []
# 	filename = []
# 	if table == 'Course':
# 		location = path + '/course/*.jpg'
# 		lst = glob.glob(location)
# 		for i in range(len(lst)):
# 			filename.append(lst[i].split('/')[6].split('.')[0])
# 	else:
# 		location = path + '/club/*.jpg'
# 		lst = glob.glob(location)
# 		for i in range(len(lst)):
# 			filename.append(lst[i].split('/')[6].split('.')[0])
# 	return filename

# print(getlst('Course'))

'''
update the sql DB
'''

# def clubupdate():
# 	table  = "Club"
# 	lst = getlst(table)
# 	conn = DBmanager(server_name = server_name, database = database)
# 	for ind in range(len(lst)):
# 		root = path+'/club/'+lst[ind]+'.jpg'
# 		print(root)
# 		with open(root,'rb') as f:
# 			body = f.read()
# 		conn.insert_newClub(clubName = lst[ind], QRcode = body)
# 	print('update done! \n')


def courseupdate(courselst):
	conn = DBmanager(server_name = server_name, database = database)
	cursor = conn.cursor
	for ind in courselst:
		reader = readclass.ReadClass(ind[0])
		if reader.check_if_classMsg():
			if cursor.execute('select * from Course where ClassName = ? and ClassNum = ?;',ind[0].split()[0],ind[0].split()[1]).fetchall() == []:
				conn.insert_newCourse(className = ind[0].split()[0],classNum = ind[0].split()[1],url = ind[2], mediaID = ind[1])
				print('inserting {}'.format(ind[0]))
			else:
				cursor.execute('update Course set Url = ?, MediaID = ? where ClassName = ? and ClassNum = ?;',ind[2], ind[1],ind[0].split()[0],ind[0].split()[1])
				print('update {}'.format(ind[0]))
				
'''
def out_math():
	conn = DBmanager(server_name = server_name, database = database)
	cursor = conn.cursor
	outcome = cursor.execute("""select ClassName,ClassNum,Url from Course where ClassName = 'MATH';""").fetchall()
	return outcome
'''

