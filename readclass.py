

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