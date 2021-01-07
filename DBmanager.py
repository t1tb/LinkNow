import pyodbc
from datetime import datetime
from time import strftime, gmtime

import inspect, os, csv
import logging
#from LoggerManager import NewLogger
import numpy as np
from OCRread import OCRread


class DBmanager:
    
    def __init__(self, server_name,database,logger_file_name=''):
        self.conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:'+server_name+',1433;Database='+database+';Uid=Wechat;Pwd={AzureDB1!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        self.database = database
#        self.logger_file_name = logger_file_name
#        self.database_logger = NewLogger('DBmanager',self.logger_file_name)
        self.cursor = self.conn.cursor()
  
    def select_table(self, table):
#        logging_info('select run on' + self.database)
        table = self.cursor.execute('select * from ' + table)
        table = self.cursor.fetchall()
        return table
        
   
    # def insert_student(self,OCR):
    #     self.year = datetime.now().strftime('%Y')
    #     self.month = datetime.now().strftime('%m')
    #     self.date = datetime.now().strftime('%d')
    #     timestamp = [self.year,self.month,self.date]
    #     courselst = []
    #     try:
    #         cursor = self.conn.cursor()
    #         print('this is OCR: ',OCR.classtable)
    #         counter = 0
    #         for row in OCR.classtable:
    #             counter = counter + 1
    #         for i in range(counter):
    #             try:
    #                 courseID = cursor.execute('select top 1 CourseID from Course where ClassName = ? and ClassNum = ?;',OCR.classtable[i][0],OCR.classtable[i][1]).fetchall()[0][0]
    #                 courselst.append(courseID)
    #                 print('inserting {} {} {} for {}'.format(courseID, OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))
    #                 cursor.execute('insert into Student(CourseID,WxId,year,month,date) values (?,?,?,?,?);',courseID,OCR.studentID,self.year,self.month,self.date)
    #                 cursor.commit()
    #             except:
    #                 print('NO SUCH COURSE YET!')
    #                 newCourseID = self.insert_newCourse(OCR.classtable[i])
    #                 print('inserting {} {} {} for {}'.format(newCourseID, OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))
    #                 cursor.execute('insert into Student(CourseID,WxId,year,month,date) values (?,?,?,?,?);',newcourseID,OCR.studentID,self.year,self.month,self.date)
    #                 cursor.commit()
    #                 print('NOW WE WILL GENERATE QR CODE for new course: {} {} {} for student {}.'.format(newCourseID,OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))                    
    #         cursor.close()
    #         return courselst
    #     except pyodbc.Error as ex:
    #         logging.error('Insert new student on Student error msg: '+ str(ex))
    #         cursor.close()
        
    
    def insert_student(self,OCR):
        self.year = datetime.now().strftime('%Y')
        self.month = datetime.now().strftime('%m')
        self.date = datetime.now().strftime('%d')
        timestamp = [self.year,self.month,self.date]
        
        try:
            courselst = []
            cursor = self.conn.cursor()
            print('this is OCR: ',OCR.classtable)
            counter = 0
            for row in OCR.classtable:
                counter = counter + 1
            for i in range(counter):

                if cursor.execute('select top 1 ClassID from Course where ClassName = ? and ClassNum = ?;',OCR.classtable[i][0],OCR.classtable[i][1]).fetchall() != []:

                    classID,url = cursor.execute('select top 1 ClassID,Url from Course where ClassName = ? and ClassNum = ?;',OCR.classtable[i][0],OCR.classtable[i][1]).fetchall()[0]
                    cursor.commit()
                    print('@@@@@@@@@@@@@@@@@',i)
                    courselst.append(url)
                    print(courselst)
                    print('inserting {} {} {} for {}'.format(classID, OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))
                    cursor.execute('insert into Student(CourseID,WxId,year,month,date) values (?,?,?,?,?);',classID,OCR.studentID,self.year,self.month,self.date)
                    cursor.commit()
                else:
                    print('NO SUCH COURSE YET!')
                    newCourseID = self.insert_newCourse(className = OCR.classtable[i][0],classNum = OCR.classtable[i][1])
                    print('@@@inserting {} {} {} for {}'.format(newCourseID, OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))
                    cursor.execute('insert into Student(CourseID,WxId,year,month,date) values (?,?,?,?,?);',newCourseID,OCR.studentID,self.year,self.month,self.date)
                    cursor.commit()
                    print('NOW WE WILL GENERATE QR CODE for new course: {} {} {} for student {}.'.format(newCourseID,OCR.classtable[i][0],OCR.classtable[i][1],OCR.studentID))                    
            cursor.close()
            print(courselst)
            return courselst
        except pyodbc.Error as ex:
            logging.error('Insert new student on Student error msg: '+ str(ex))
            cursor.close()
        
    
    def insert_member(self,clubName,wx):
        '''
        insert student member on student table 
        must ensure that the club is listed and stored in our database
        this method will run into error if search for a club unknown        
        '''
        clubID = None        
        query = """
            insert into Student (WxId, ClubID) values (?,?);         
        """
        cursor = self.conn.cursor()
        try:
            clubID = cursor.execute('select top 1 ClubID from Club where ClubName = ?;',clubName).fetchall()[0][0]
            print('inserting {} on Club table'.format(clubName))
            cursor.execute(query,wx,clubID)
            cursor.commit()
            cursor.close()
            print('successfully inserted {} as club id {} for {}'.format(clubName,clubID,wx))            
            return clubID
        except pyodbc.Error as ex:
            logging.error('Insert new member on student error msg: '+ str(ex))
            cursor.close()
           
    
    def insert_newClub(self,clubName,url=None,mediaID=None):
        '''
        take club name string and QR code
        return new club id once created
        '''
        query = """
                insert into Club(ClubName,Url,MediaID) output inserted.ClubID values (?,?,?);
            """
        try:
            cursor = self.conn.cursor()
            newClubID = cursor.execute(query,clubName,url,mediaID)
            cursor.commit()
            cursor.close()
            return newClubID
        except pyodbc.Error as ex:
            logging.error('Insert new club on Club error msg: '+ str(ex))
            cursor.close()


    def insert_newCourse(self,className,classNum,url=None,mediaID=None):
 
        query = """
                insert into Course(ClassName,ClassNum,Url,MediaID) output inserted.ClassID values (?,?,?,?);
            """
        try:
            cursor = self.conn.cursor()
            newClassID = cursor.execute(query,className,classNum,url,mediaID).fetchall()[0][0]
            cursor.commit()
            cursor.close()
            return newClassID
        except pyodbc.Error as ex:
            logging.error('Insert new course on Course error msg: '+ str(ex))
            cursor.close()
            
            
    # def insert_newCourse(self,classNN,QRcode=None):
    #     '''
    #     classNN is a list of {class name and class number}
    #     insert new course name and number, maybe QRcode
    #     return the new course ID
    #     '''
    #     try:
            
    #         className = classNN[0]
    #         classNum = classNN[1]
    #         cursor = self.conn.cursor()
            
    #         query = """
    #             insert into Course(ClassName,ClassNum,QRcode) output inserted.CourseID values (?,?,Cast(? As varbinary(max)));
    #         """
    #         # QRcode = pyodbc.Binary(QRcode)
            
    #         cursor.execute(query,(className,classNum,QRcode))
    #         newCourseID = cursor.fetchall()[0][0]
    #         cursor.commit()
    #         cursor.close()
    #         print('insert new course now')
    #         return newCourseID
    #     except pyodbc.Error as ex:
    #         logging.error('Insert new course on Course error msg: '+ str(ex))
    #         cursor.close()
            
            
            
            
    def outCourseQR(self,courselst):
        '''
        take a list of course ID and then return a list of QRcode
        '''
        lst = []
        query = """
            select top 1 QRcode from Course where CourseID = ?;
        """
        cursor = self.conn.cursor()
        try:
            for ind in courselst:
                cursor.execute(query,ind)
                QRcode = cursor.fetchall()[0][0]
                print('FOUND QRcode for CourseID {}'.format(ind))
                lst.append(QRcode)                
            
        except:
            print('Something wrong in outCourseQR! Partial outcome')
        return lst
        
        
    def outClubQR(self,clubID):
        '''
        take a list of course ID and then return a list of QRcode
        '''
        clubQR = []
        query = """
            select top 1 QRcode from Club where ClubID = ?;
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute(query,clubID)
            QRcode = cursor.fetchall()[0][0]
            print('FOUND QRcode for ClubID {}'.format(clubID))
            clubQR = bytes(QRcode)
            return clubQR
        except pyodbc.Error as ex:
            print('Something wrong in outClubQR!')
            logging.error('findQR on '+ table + ' error msg: '+ str(ex))
            
                
 
    def findQR(self,SQLinput,table):
        '''
            need to change the SQLinput to OCR class
        '''
        try:
            cursor = self.conn.cursor()
            if table == 'Course':
                className = SQLinput[0]
                classNum = SQLinput[1]
                cursor.execute('select top 1 QRcode from ' +table+ ' where ClassName = ? and ClassNum = ?;', (className,classNum))
                QRcode = cursor.fetchall()[0][0]
                # print(QRcode)
                cursor.commit()
                cursor.close()
                return QRcode
                
            elif table == 'Club':
                clubName = SQLinput
                cursor.execute('select top 1 QRcode from ' +table+ ' where ClubName = ? ;',clubName)
                QRcode = cursor.fetchall()[0][0]
                # print('this is the QRcode for {}: {}'.format(clubName,QRcode))
                cursor.commit()
                cursor.close()
                return QRcode
                
        except pyodbc.Error as ex:
            print('NOT FOUND!')
            logging.error('findQR on '+ table + ' error msg: '+ str(ex))
            
    
    
            
    def update_allQRtable(self,QRcode,table,file_name):
        '''
        this method reads all QR from server and store them into datebase
        take QRcode, table in string, file name read in string        
        create new instance if not exist 
        otherwise, update the QRcode
        '''
        QRcode = pyodbc.Binary(QRcode)
        try:
            cursor = self.conn.cursor()
            if table == 'Course':
                className = file_name.split()[0]
                classNum = file_name.split()[1]
                
                if cursor.execute('select * from Course where ClassName = ? and ClassNum = ?',className, classNum).fetchall()==[]:
                    print('inserting new class')
                    self.insert_newCourse([className,classNum],QRcode)
                    print('inserted')
                    
                else:
                    print('update Course QRcode')
                    cursor.execute("""
                        update Course set QRcode = ? where ClassName = ?  and ClassNum = ?
                    """, QRcode,className,classNum)
                    cursor.commit()
                    print('updated')                   
                    
            elif table == 'Club':
                clubName = file_name
                if cursor.execute('select * from Club where ClubName = ?;',clubName).fetchall()==[]:
                    self.insert_newClub(clubName,QRcode)
                else:
                    print('update Club QRcode')
                    cursor.execute("""                     
                        update Club set QRcode = ? where ClubName = ?
                    """, QRcode,clubName)
                    cursor.commit()
                    print('updated')
                    
            cursor.close()
        except pyodbc.Error as ex:
            logging.error('update the QRcode on '+ table + ' error msg: '+ str(ex))
            cursor.close()
            
    
            
            