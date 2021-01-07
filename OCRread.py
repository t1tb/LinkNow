
#DO NOT SHARE THIS TO OUTSIDERS CONTAINS API CREDENTIAL
#DO NOT SHARE THIS 
#SENSITIVE CREDENCIAL

import requests
import os, json


class OCRread:
    '''
    This Class reads a picture of class table then returns a 2d array of course taken

    self.classtable : course taken of a student
    self.img        : image directory
    self.studentID  : sturent ID, currently get from image name
    self.RAWJson    : JSON result form AZURE OCR
    self.classlist  : List of Subject name

    '''


    def __init__(self):
        self.classtable = []
        self.img = ''
        self.studentID =''
        self.RAWJson = ''
        with open('CLASSLIST') as f:  # get list of class for reading 
            self.classlist = f.readlines()
            self.classlist = [x.strip() for x in self.classlist]
    def AzureOCR(self,img):
        '''
        extract text forom an image by AZURE OCR

        usage: AzureOCR('image_DIR')

        may need to set up Ocp-Apim-Subscription-Key and request URL if API credencial changed

        '''
        self.img = img
        self.studentID = img.split('/')[5].split('.')[0]
    
        body= open(img,"rb").read()
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '79ecb88bc7814e74b344a8ada2071069',
            }
        params = {
            # Request parameters
            'language': 'unk',
            'detectOrientation': 'true',
            }
        try:
            response = requests.post('https://classtableocr.cognitiveservices.azure.com/vision/v3.0/ocr', headers=headers, params=params, data=body)
            response.raise_for_status()
            data = response.json()
            self.RAWJson = data
        #    print(data)
        except:
            print('AZURE OCR READ FAIL')

        

    def JSONPhrasor(self,RAWJson):


        '''
        Flat out and extract word dict from OCR, then look for subject name then find class name's next word for class number



        '''
        self.RAWJson = RAWJson
        #jsonstore= json.dumps(self.RAWJson)
        #jsondict =json.loads(self.RAWJson)
        jsondict= self.RAWJson
        line_infos = [region["lines"] for region in jsondict["regions"]]# read each line of the json
        word_infos = []
        for line in line_infos: #flat out the word here
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        for x in word_infos:  #look for each word
            if x['text'] in self.classlist: #look word is in the list of subject name
                course =[]
                course.append(x['text'])
                course.append(word_infos[word_infos.index(x)+1]['text']) # read next word
                if course[1] == 'IOO' or course[1] == '1OO' or course [1] == 'I00' : # fix OCR reading error
                    course [1] = '100'
                elif '-' in course [1]:  # fix classtable with -
                    course[1] = course[1].split('-')[0]
                
                if course[1][:2] == '00':   #change class number '00x' to 'x'
                    course [1] = course [2]


                if course not in self.classtable:
                    self.classtable.append(course)
	
	return json.dumps(self.classtable)


    def ReadClass(self,img):
        ''' 
        output for this method: 
        self.classtable = [['ECON','302'],['English','202C'],['MATH','141']]
        self.studentID = 'aaaaaa'
        '''
        self.img = img
        self.AzureOCR(self.img)
        self.JSONPhrasor(self.RAWJson)
    

'''
this is left for testing of this class don't use


def run():
	return OCRread();


read = OCRread()
read.ReadClass('WeChat Image_20200822223711.jpg')
print(*read.classtable)
'''
