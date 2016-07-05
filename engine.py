#################################################~~~~~Author: Krishna Nagaraja~~~~~~############################################################
'''This module contains two classes utility and login.Utility miscellaneous functions which the login class has to use. Login class will take
the user name and will continue in user mode or if no user name is given, then it will continue in guest mode. It has functions like getquestin() which will select a question from the database based on a certain paameters, and also keeps track of the questions asked so that the questions are not repeated.Once an object of this class is created ,it acts like the backend. Once the user logs in, an object of the login class will be 
created in the front end, and its various functions like highscores() etc. will be used by the front end to access the database. The database of this game is spread over several files.
1.As soon as a new user is created, a file of his name will be creates in which data will be stored in the format,
#########FORMAT##########
name
score
Question_to_be_asked status_of_lifeline_1 status_of_lifeline_2 status_of_lifeline_3 status_of_lifeline_4
milestone
id's of questions asked
#########################
If the game is played in guest mode, the name will be guest and this file will be overwritten everytime.
2.Questions are stored in questions.dat which has the format:
########FORMAT###########
%no_of_questions The_question_numbers_for_which_this_data_can_be_referred_to
id question option1 option2 option3 option4 answer category
#########################
Eg: %1 1 2
    1-2:1 who is the prime ministe of india? manmohan_singh Narendra_Modi Jawaharlal_Nehru Indira_gandhi B POL
here, this part of the database contains one question ,which can be referred to for asking either the first or second question in the game
1-2:1 is the id of the question

3.Scores are stored in scores.dat file whic has the format,
########FORMAT###########
name score
#########################

4.The data of experts is stored in experts.dat, in the format,
########FORMAT###########
slno name description categories_of_questions_he_can_handle
#########################

5.The data about some friends who can be referred to while using the lifeline "phone a friend" is stored in phone_a_friend.dat int he format,
########FORMAT###########
slno name job categories_of_questions_he_can_handle
#########################

6.If the user logs in with his name, then his name will be stored in a file details.dat, which has the format,
########FORMAT###########
name
#########################'''
import os
import random
class utility:
	@staticmethod
	#This function will check whether the name is registered or not
	def validateusername(name,password):
		detailsfile=open("details.dat","r")
		for line in iter(detailsfile):
			if(line.split()[0]==name): #and line.split[1]==password):
				detailsfile.close()
				return True
		detailsfile.close()
		return False
	@staticmethod
	#This function will register a new user
	def createuser(name,password=""):
		detailsfile=open("details.dat","r+")
		count=0
		for line in iter(detailsfile):
			if(line.split()[0]==name):
				print name,"*************"
				raise Exception("Username already exists")
				count=count+1
		if(count==0):
			detailsfile.write(name+" "+password+"\n")
			newfile=open(name+".dat","w")
			newfile.write(name+"\n")
			newfile.write("0\n")
			newfile.write("1 _ _ _ _\n")
			newfile.write("0\n")
			newfile.close()
	@staticmethod
	#Each Quetion in the database will be having a unique ID which will be 
	#based on the range of questions for which this can be chosen.
	#The number [resent after the colon (:) is the serial number of the question
	#Ex: ID of 1-2:1 means this particular question is the first question 
	#which falls under the category of being able to be chosen as either the first or the second question in the game WHO WANTS TO BE A MILLIONAIRE.
	def deduce_question_ID(rangelist,number):
		qid=str(rangelist[0])
		qid+=("-"+str(rangelist[-1]))
		qid+=(":"+str(number))
		return qid
	@staticmethod
	def replace_underscore(stringlist,replaceitem):
		for i in range(len(stringlist)):
			temp=""
			for j in range(len(stringlist[i])):
				if(stringlist[i][j]=="_"):
					temp+=replaceitem
				else:
					temp+=stringlist[i][j]
			stringlist[i]=temp
					
		return stringlist
		
			
class login:
	def __init__(self,login="user",name="",password=""):
		self.login=login
		if(login=="guest"):
			self.name="guest"
			newfile=open("new.dat","w")
			newfile.write(self.name+"\n")
			newfile.write("0\n")
			newfile.write("1 _ _ _ _\n")
			newfile.write("0\n")
			newfile.close()
			os.system("cp new.dat guest.dat")
			os.system("rm new.dat")
			self.currentplayer=open("guest.dat","r")
		elif(login=="user" and name !=""):
			if(utility.validateusername(name,password="")):
			 self.currentplayer=open(name+".dat","r")
			 self.name=name	
			else:
				utility.createuser(name)
				self.currentplayer=open(name+".dat","r")
				self.name=name	
		else:
			raise Exception("No user like that");
		 
		self.questionnumber=1
		self.milestone=self.getmilestone()
		self.expert=random.randint(1,10)
		if(self.questionnumber>13):
			self.questionnumber=1
#This function sets the milestone (i.e after the milestone question, the timer would not be actiive)
	def setmilestone(self,milestone):
		temp=open("temp.dat","w")
		count=0
		for line in iter(self.currentplayer):
			if(count==3):
				temp.write(str(milestone)+"\n")
			else:
				temp.write(line)
			count+=1
		temp.close
		name=self.currentplayer.name
		self.currentplayer.close()
		os.system("cp temp.dat "+name)
		os.sysem("rm temp,dat")
		self.currentplayer=open(name,"r")
#This functions checks the file and returns the milestone selected by the player
	def getmilestone(self):
		count=0
		milestone=0
		for line in iter(self.currentplayer):
			if(count==3):
				milestone=(int)(line)
				break
			count+=1
		name=self.currentplayer.name
		self.currentplayer.close()
		self.currentplayer=open(name,"r")
		return milestone
	@staticmethod
	def sortscores(slist):
		for i in range(len(slist)):
			smax=slist[i]
			pos=i
			for j in range(i+1,len(slist)):
				if((int)(slist[j][1])>(int)(smax[1])):
					smax=slist[j]
					pos=j
			slist[pos]=slist[i]
			slist[i]=smax
		return slist
#This method checks the scores database and returns the list of top ten highscores
	@staticmethod	
	def gethighscores():
		scoreslist=[]
		highscores=[]
		scores=open("scores.dat","r")
		for line in iter(scores):
			scoreslist.append(line.split())
		highscores=login.sortscores(scoreslist)[:11]
		scores.close()
		return highscores
#This method returns the number of the question which is to be asked to the user
	def getquestno(self):
		question=0
		count=0
		for line in iter(self.currentplayer):
			if(count==2):
				question=(int)(line.split()[0])
			count+=1
		name=self.currentplayer.name
		self.currentplayer.close()
		self.currentplayer=open(name,"r")
		return question	
#This function updates the score of the user in the scores.dat file and in the username.dat file
	def submitfinalscore(self,score):
		scorelist=open("scores.dat","a")
		scorelist.write(self.name+" "+str(score)+"\n")
		scorelist.close()
		self.submitscore(score)
#This only updates the score in user.dat file
	def submitscore(self,score):
		tempfile=open("temp.dat","w")
		count=0
		for line in iter(self.currentplayer):
			if(count==1):
				tempfile.write(str(score)+"\n")
			else:
				tempfile.write(line)
			count+=1
		tempfile.close()
		self.currentplayer.close()
		os.system("cp temp.dat "+self.name+".dat")
		os.system("rm temp.dat")
		self.currentplayer=open(self.name+".dat","r")
	def save_and_quit(self):
		self.currentplayer.close()
		exit()
#This function takes the questionID as the parameter and appends that to the user.dat file so that the same question will not be asked to that user again 
	def update(self,questionID):
		name=self.currentplayer.name
		self.currentplayer.close()
		updatefile=open(name,"a")
		updatefile.write(questionID+"\n")
		updatefile.close()
		self.currentplayer=open(name,"r")
		tempfile=open("temp.dat","w")
		count=0
		for line in iter(self.currentplayer):
			if(count==2):
				s=str(self.questionnumber)
				for i in line.split()[1:]:
					s+=(" "+i)
				tempfile.write(s+"\n")
			else:
				tempfile.write(line)
			count+=1
		tempfile.close()
		self.currentplayer.close()
		os.system("cp temp.dat "+name)
		os.system("rm temp.dat")
		self.currentplayer=open(self.name+".dat","r")
#This function checks the questions.dat file and returns the question and answer in the following format
#[question,option1,option2,option3,option4,answer,category]
#This generation of the question depends on number of the question that is being asked to the user in the game, it chooses easier questions for 1st and 2nd question, and relatively tougher for further questions and so on
	def getquestion(self):
		database=open("questions.dat","r")
		no_of_questions=0
		qrange=[]
		for line in iter(database):
			if(line.split()[0][0]=="%" and (str(self.questionnumber) in line.split()[1:])):
				no_of_questions=(int)(line.split()[0][1:])
				qrange=[(int)(i) for i in line.split()[1:]]
				break;
		count=0
		questionsasked=[]
		for line in iter(self.currentplayer):
			if(count>3):
				questionsasked.extend(line.split())
			count=count+1
		count=0
		x=random.randint(1,no_of_questions)
		while(count<1000):
			x=random.randint(1,no_of_questions)
			if(utility.deduce_question_ID(qrange,x) not in questionsasked):
				break;
			count=count+1
		question_to_be_asked=utility.deduce_question_ID(qrange,x)
		for line in iter(database):
			if(line.split()[0]==question_to_be_asked):
				self.questionnumber+=1
				if(self.questionnumber >18):
					raise Exception("Game over")
					self.questionnumber=1
				self.update(question_to_be_asked)
				database.close()
				return utility.replace_underscore(line.split()[1:]," ")
		raise Exception("something went wrong")
#This function checks whether the lifeline is available or not
	def lifeline_available(self,lifeline):
		count=0	
		availability=True
		name=self.currentplayer.name
		self.currentplayer.close()
		self.currentplayer=open(name,"r")
		for line in iter(self.currentplayer):
			if(count==2):
				if(lifeline[0] in line.split()[1:]):
					availability=False
				else:
					pass
				break
			count+=1
		name=self.currentplayer.name
		self.currentplayer.close()
		self.currentplayer=open(name,"r")
		return availability
#This functions updates in the username.dat file that the particular lifeline(passed as parameter) has been used by the user	
	def lifelineused(self,lifeline):
		temp=open("temp.dat","w")
		name=self.currentplayer.name
		count=0
		if(not(self.lifeline_available(lifeline))):
			raise Exception("Life line is used")
		self.currentplayer.close()
		self.currentplayer=open(name,"r")
		for line in iter(self.currentplayer):
			if(count==2):
				s=""
				s+=(line.split()[0]+" ")
				for i in line.split()[2:]:
					s+=(i+" ")
				s+=(lifeline[0]+"\n")
				temp.write(s)
			else:
				temp.write(line)
			count+=1
		name=self.currentplayer.name
		self.currentplayer.close()
		temp.close()
		os.system("cp temp.dat "+name)
		os.system("rm temp.dat")
		self.currentplayer=open(name,"r")
#restart function sets the question that is to be asked to the user to 1 ,and updates the score to 0 and updates the milestone to not set.
	def restart(self):
		temp=open("temp.dat","w")
		count=0
		name=self.currentplayer.name
		for line in iter(self.currentplayer):
			if(count==1):
				temp.write("0\n")
			elif(count==2):
				temp.write("1 _ _ _ _\n")
			elif(count==3):
				temp.write(0)
			else:
				temp.write(line)
		temp.close()
		self.currentplayer.close()
		os.system("cp temp.dat "+name)
		os.system("rm temp.dat")
		self.currentplayer=open(name,"r") 
