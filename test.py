import pygame
import time
import random
import lifelines
import util
import KBC
from engine import *

#This module contains the GUI of the basic game
'''Some global variables are defined here that are needed throughout this module.
There are different box over here each of which has the coordintaes of their corresponding hexagon.'''
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
blue=(0,0,255)
green=(0,175,0)
black=(0,0,0)
yellow=(100,100,0)
light_yellow=(200,200,0)
orange=(230,130,0)
display_width=700
display_height=700
lifeline_size=100
gameDisplay=None
#pygame.display.update()
FPS=10
box_c=([80,620],[290,620],[330,655],[290,690],[80,690],[40,655])
box_d=([410,620],[620,620],[660,655],[620,690],[410,690],[370,655])
box_a=([80,540],[290,540],[330,575],[290,610],[80,610],[40,575])
box_b=([410,540],[620,540],[660,575],[620,610],[410,610],[370,575])
box_ques=([80,400],[620,400],[660,460],[620,520],[80,520],[40,460])
box_amt=([410,310],[620,310],[660,345],[620,380],[410,380],[370,345])
msg_pos=([80,565],[410,565],[80,645],[410,645],[80,430],[410,330],[245,328],[245,628],[250,635])
box_amount=([245,315],[455,315],[495,350],[455,385],[245,385],[205,350])
box_back=([[245,620],[455,620],[495,655],[455,690],[245,690],[205,655]])
box_lifeline=([30,5],[300,5],[450,5],[600,5])
timer_circle=[(350,615),38,25]
amount2=[0,5000,10000,20000,40000,80000,160000,320000,640000,1250000,2500000,5000000,10000000,20000000,30000000,50000000]
amount=['0','5,000','10,000','20,000','40,000','80,000','1,60,000','3,20,000','6,40,000','12,50,000','25,00,000','50,00,000','1,00,00,000','2,00,00,000','3,00,00,000','5,00,000,00']
lifeline=['walkaway','Phone_a_friend','Expert_Advice','Audience_Poll']
ob1=None
ob2=None
ans_seq=["A","B","C","D"]	


'''This MyTime class is used to create an object that acts as the timer.
When the object is created the timer is started.
The time_left property is used to find the reamining time of the timer.
pause() is used to pause the timer at any given point of time
play() is used to resume the timer again'''
class MyTime():
	def __init__(self,t):
		self.start=time.time()
		self.pause_time=0
		self.timer=t
		self.pause_at=0

	@property	
	def time_left(self):
		current=time.time()
		if(self.timer<0):
			return 1
		return int(self.timer-current+self.start+self.pause_time)
	
	def pause(self):
		self.pause_at=time.time()
		
	def play(self):
		self.pause_time+=(time.time()-self.pause_at)

'''This class Lifeline is created to handle the display of lifelines as well as their event handling.
display lifelines displays the lifeline and also puts a cross on those lifelines that are used by the user'''
class Lifeline:
	def __init__(self,lf,box,used=[]):
		self.lifelines=lf
		self.box_lifeline=box
		self.used=used
		
	def display_lifelines(self,gameDisplay):
		for j in range(len(self.lifelines)):
			image_to_screen(gameDisplay,self.lifelines[j]+".png",self.box_lifeline[j])
			'''img=pygame.image.load(self.lifelines[j]+".png")
			gameDisplay.blit(img, self.box_lifeline[j])'''
			for i in self.used:
				image_to_screen(gameDisplay,"x.png",self.box_lifeline[i])
			
	def if_in_lifeline(self,gameDisplay,mouse_pos):
		lifelineNo=-1
		k=0
		for j in self.box_lifeline:
			if(mouse_pos[0]<=j[0]+100 and mouse_pos[0]>=j[0] and mouse_pos[1]<=j[1]+100 and mouse_pos[1]>=j[1]):
				lifelineNo=k
				break
			k+=1
		bg = pygame.image.load("bgHalf.jpg")
		gameDisplay.blit(bg, (1,0))
		self.display_lifelines(gameDisplay)
		if(lifelineNo!=-1 and lifelineNo not in self.used):
			pygame.draw.rect(gameDisplay,light_yellow,[box_lifeline[lifelineNo][0],box_lifeline[lifelineNo][1],100,100],2)
		return lifelineNo

	def use_lifeline(self,lifelineNo):
		pass
		
'''Class is used to display the status of the current user ie how many questions user has answered, where is the milestone, and it also does event handling.
This class is an abstract class as it uses some features of its sub-classes
template_status() is used to display the basic template of the status, while display_status is used in event handling of the status'''
class Status:

	def template_status(self,gameDisplay,quesNo):
		msg_x=250
		msg_y=11
		size=30
		clear_screen(gameDisplay)
		for j in range(1,len(self.amount)):
			color=yellow
			if(j==len(self.amount)-quesNo):
				pygame.draw.rect(gameDisplay,light_yellow,[msg_x-10,msg_y-5,300,size])
			if(j==len(self.amount)-self.milestone or j==1):
				color=white
			msg=str(len(self.amount)-j)+" \t "+"Rs."+self.amount[len(self.amount)-j]
			if(len(self.amount)-j<=9):
				msg=" "+msg
			msg_to_screen(gameDisplay,msg,color,[msg_x,msg_y],size)
			msg_y+=11+size
			color_box(gameDisplay,self.box_back,yellow)
		pygame.display.update()
		
	def display_status(self,gameDisplay,quesNo):
		back=False
		timer=MyTime(10)
		self.template_status(gameDisplay,quesNo)
		while back!=True:
			if(timer.time_left<=0):
				back=True
			for event in pygame.event.get():
				mouse_pos=pygame.mouse.get_pos()
				if is_in_box(mouse_pos,self.box_back) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					back=True
				elif is_in_box(mouse_pos,self.box_back):
					color_box(gameDisplay,self.box_back,light_yellow)
				else:
					color_box(gameDisplay,self.box_back,yellow)
				msg_to_screen(gameDisplay,"Continue",white,msg_pos[8],40)
			pygame.display.update()
		clear_screen(gameDisplay)
		
'''Next_Question class is also an abstract class that is also the sub-class of Status and super-class of Display.
to_next_ques_template() is used for creating the template for the intermediate process between two questions
to_next_ques() is used for event handling of this screen'''		
class Next_Question(Status):

	def to_next_ques_template(self,gameDisplay,quesNo):
		bg = pygame.image.load("bluew.jpg")
		gameDisplay.blit(bg, (0,0))
		#pygame.draw.lines(gameDisplay,white,True,box_amount,2)
		msg_to_screen(gameDisplay,'Lets move to next Question',white,(180,50),40)
		msg_to_screen(gameDisplay,'You have won',white,(250,250),40)
		color_box(gameDisplay,self.box_amount,yellow)
		msg_to_screen(gameDisplay,'Rs.'+self.amount[quesNo],white,msg_pos[6],40)
		color_box(gameDisplay,self.box_back,yellow)
		msg_to_screen(gameDisplay,'Continue',white,self.msg_pos[7],40)
		pygame.display.update()

	def to_next_ques(self,quesNo,milestone):
		timer=MyTime(7)
		back=False
		self.to_next_ques_template(gameDisplay,quesNo)
		while back!=True:
			if(timer.time_left<=0):
				back=True
			mouse_pos=pygame.mouse.get_pos()
			#quit
			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
					if(is_in_box(mouse_pos,self.box_amount)):
						timer.pause()
						self.display_status(gameDisplay,quesNo)
						self.to_next_ques_template(gameDisplay,quesNo)
						timer.play()
					elif(is_in_box(mouse_pos,self.box_back)):
						back=True
				if(is_in_box(mouse_pos,self.box_amount)):
					color_box(gameDisplay,self.box_amount,light_yellow)
				else:
					color_box(gameDisplay,self.box_amount,yellow)
					
				if(is_in_box(mouse_pos,self.box_back)):
					color_box(gameDisplay,self.box_back,light_yellow)
				else:
					color_box(gameDisplay,self.box_back,yellow)
				msg_to_screen(gameDisplay,"Continue",white,self.msg_pos[7],40)
				msg_to_screen(gameDisplay,'Rs.'+self.amount[quesNo-1],white,self.msg_pos[6],40)
				pygame.display.update()	
'''This class is the main display class that displays the question screen.
It is sub-class of Next_Question and indirectly the sub-class of Status
display_timer() is used to display the timer on the screen, if it is given the time t and the timer_circle which contains radius and coordintaesof centre of the circle
Template() is used to create the template of question and the answers
ques_to_screen() is used to display the question to the screen
ans_to_screen() as the name suggests is used to display the answers to the screen
timeOver() is used in case if the lime limit is exceeded for answering the question. It display the times up followed by the correct answer
flash_answer() is used to flash the correct answer as well as the wrong answer if user gives a wrong answer
end_screen() is used display the last screen to the user showing the amount he has won. If he won nothing, it does not show amount'''		
class Display(Next_Question):

	def __init__(self,bg,all_box,amt,ms,mp):
		self.box_a=all_box[0]
		self.box_b=all_box[1]
		self.box_c=all_box[2]
		self.box_d=all_box[3]
		self.box_ques=all_box[4]
		self.box_amt=all_box[5]
		self.box_amount=all_box[6]
		self.box_back=all_box[7]
		self.amount=amt
		self.milestone=ms
		self.msg_pos=mp
		self.bg=bg
	
	def display_timer(self,gameDisplay,timer_circle,t):
		t=str(t)
		if(len(t)==1):
				t=" "+t
		pygame.draw.circle(gameDisplay,black,timer_circle[0],timer_circle[1],0)
		pygame.draw.circle(gameDisplay,white,timer_circle[0],timer_circle[1],2)
		msg_to_screen(gameDisplay,t,white,(timer_circle[0][0]-25,timer_circle[0][1]-20),60)
		pygame.display.update()
	
	def Template(self,gameDisplay,display_width,display_height,lfl,ans=None,ques=None):
		#bg = pygame.image.load("bg.jpg")
		bg= pygame.image.load(self.bg)
		gameDisplay.blit(bg, (0, 0))
		pygame.draw.line(gameDisplay,white,(0,box_c[2][1]),(display_width,box_c[2][1]))
		pygame.draw.line(gameDisplay,white,(0,box_a[2][1]),(display_width,box_a[2][1]))
		decolor_box(gameDisplay,self.box_a)
		decolor_box(gameDisplay,self.box_b)
		decolor_box(gameDisplay,self.box_c)
		decolor_box(gameDisplay,self.box_d)
		'''pygame.draw.line(gameDisplay,white,(0,655),(40,655),2)
		pygame.draw.line(gameDisplay,white,(330,655),(370,655),2)
		pygame.draw.line(gameDisplay,white,(660,655),(700,655),2)
		pygame.draw.line(gameDisplay,white,(0,575),(40,575),2)
		pygame.draw.line(gameDisplay,white,(330,575),(370,575),2)
		pygame.draw.line(gameDisplay,white,(660,575),(700,575),2)
		pygame.draw.lines(gameDisplay,white,True,box_ques,2)
		pygame.draw.line(gameDisplay,white,(0,460),(40,460))
		pygame.draw.line(gameDisplay,white,(660,460),(700,460))'''
		color_box(gameDisplay,box_amt,yellow)
		pygame.draw.line(gameDisplay,white,(655,345),(700,345))
		lfl.display_lifelines(gameDisplay)
		if(ques!=None and ans!=None):
			self.ans_to_screen(gameDisplay,ans,ques)
		
	def ques_to_screen(self,gameDisplay,ques):
		decolor_box(gameDisplay,self.box_ques)
		ques_pos=[msg_pos[4]]
		if(len(ques)<48):
			msg_to_screen(gameDisplay,'Q: '+ques,white,self.msg_pos[4],33)
			return
		else:
			#print [ques_pos[0][0],ques_pos[0][1]+38]
			ques_pos.append([ques_pos[0][0],ques_pos[0][1]+38])
			c=' '
			if(len(ques)>52):
				if(ques[52]!=' '):
					c='-'
				msg_to_screen(gameDisplay,'Q: '+ques[:52:]+c,white,ques_pos[0],25)
				if(len(ques)>102):
					ques_pos.append([ques_pos[0][0],ques_pos[1][1]+38])
					msg_to_screen(gameDisplay,ques[52:103:]+c,white,ques_pos[1],25)
					msg_to_screen(gameDisplay,ques[103::],white,ques_pos[2],25)
				else:
					msg_to_screen(gameDisplay,ques[52::],white,ques_pos[1],25)
			else:
				msg_to_screen(gameDisplay,ques,white,ques_pos[1],30)

	def ans_to_screen(self,gameDisplay,ans,ques):
		self.ques_to_screen(gameDisplay,ques)
		ans_seq=['A','B','C','D']
		for j in range(len(ans)):
				msg_to_screen(gameDisplay,ans_seq[j]+": "+ans[j],white,self.msg_pos[j])

	def timeOver(self,gameDisplay):
		msg_to_screen(gameDisplay,"Times Up!",orange,(200,250),50)
		pygame.display.update()
		time.sleep(1)
	
	def flash_answer(self,gameDisplay,ans,correct_ans,user_ans_no,box_ques,ques):
		box=[box_a,box_b,box_c,box_d]
		correct_ans_no=-1
		for j in range(len(box)):
			if ans[j]==correct_ans: correct_ans_no=j
		if(correct_ans_no!=user_ans_no and user_ans_no!=-1):
			color_box(gameDisplay,box[user_ans_no],red)
		color_box(gameDisplay,box[correct_ans_no],green)
		self.ans_to_screen(gameDisplay,ans,ques)
		pygame.display.update()
		time.sleep(1)
	
	def end_screen(self,gameDisplay,amt):
		image_to_screen(gameDisplay,"Brick.jpg")
		if(amt==0):
			msg=["Thanks","for Playing.","Better Luck,","Next Time."]
			msg_pos=[(300,100),(260,150),(260,400),(260,450)]
			for i in range(len(msg)):
				msg_to_screen(gameDisplay,msg[i],(255,255,255),msg_pos[i],40)
		else:
			msg=["You won","Rs. "+str(amt),"Thanks for Playing"]
			msg_pos=[(300,100),(300,150),(260,400),(260,450)]
			for i in range(len(msg)):
				msg_to_screen(gameDisplay,msg[i],(255,255,255),msg_pos[i],40)
		pygame.display.update()
		time.sleep(2)
		try:
			kbc=KBC.startscreen("kbc.jpg")
			kbc.main()
		except:
			pass
		

'''These are some utility function that do not belong to any class'''

'''Get question is used to get the question as well as the answers from the engine module that are then converted in their required format
[question,answer_a,answer_b,answer_c,answer_d,correct option,category,audio file name] is the format in which the engine module gives me the list
which is converted to the format required by my module [question,[list of answers],correct_ans_no,category,audiofile]'''
def getQues():
	list=ob1.getquestion()
	k=1
	if(len(list)==7):
		list.append(None)
	for i in 'ABCD':
		if(i==list[5]):
			k=ord(i)-64
	return list[0],list[1:5:],list[k],list[5],list[6],list[7]

'''This function is used to display an image onto the screen.'''
def image_to_screen(gameDisplay,img,pos=(0,0)):
	img=pygame.image.load(img)
	gameDisplay.blit(img, pos)

'''This function is used to blit the message to the screen ,in the required position and the size'''	
def msg_to_screen(gameDisplay,msg,color,pos,size=25):
	font=pygame.font.SysFont(None,size)
	screen_text=font.render(msg,True,color)
	gameDisplay.blit(screen_text,pos)

'''It is used to find if the mouse is in the given hexagon box or not'''
def is_in_box(mouse_pos,box):
	if(mouse_pos[0]>box[0][0] and mouse_pos[0]<box[1][0] and mouse_pos[1]>box[1][1] and mouse_pos[1]<box[4][1]):
		return True
	elif((mouse_pos[0]<box[0][0] and mouse_pos[0]>=box[5][0])or (mouse_pos[0]>=box[1][0] and mouse_pos[0]<box[2][0])):
		if(mouse_pos[1]<=box[3][1] and mouse_pos[1]>=box[0][1]):
			if(is_in_tri((mouse_pos[0],mouse_pos[1]),(box[0],box[5],box[4])) or is_in_tri((mouse_pos[0],mouse_pos[1]),(box[1],box[2],box[3]))):
				return True
	return False

'''	It is used to find if the mouse pointer is in given triangle or not
It is a helper method to is_in_box()'''
	
def is_in_tri(mouse_pos,tri):
	if(mouse_pos[1]>tri[1][1]):
		mouse_pos=(mouse_pos[0],tri[2][1]-mouse_pos[1]+tri[0][1])
	if(abs((mouse_pos[1]-tri[0][1])*(tri[0][0]-tri[1][0]))>=abs((mouse_pos[0]-tri[0][0])*(tri[0][1]-tri[1][1]))):
		return True
	return False

'''color_box() is its name suggests is used to color a given hexagon box to the color we want'''	
def color_box(gameDisplay,box,color):
	pygame.draw.polygon(gameDisplay,color, box)
	pygame.draw.lines(gameDisplay,white,True,box,2)
'''It is similar to color box, and uses color_box().
It is derived used color_box(), but instead of coloring the hexagon box the color we want, the colors the  hexagon box to black.'''			
def decolor_box(gameDisplay,box):
	color_box(gameDisplay,box,black)
	
def if_in_box(gameDisplay,mouse_pos,box,color=orange):
	if is_in_box(mouse_pos,box):
		color_box(gameDisplay,box,color)
	else:
		decolor_box(gameDisplay,box)

'''This is used to cover the screen to black any any given point'''
def clear_screen(gameDisplay):
	pygame.draw.rect(gameDisplay,black,[0,0,display_width,display_height])
	pygame.display.update()
		

	
'''This function contains the event handling of the game.
It coordinates the working of different components of the game'''	
def gameLoop():
	curr_amt=0
	left=False
	#pygame.display.update()
	gameExit=False
	questionOver=True
	quesNo=0
	quit=False
	milestone=6
	mouse_pos=0
	lfl=Lifeline(lifeline,box_lifeline,[])
	while gameExit!=True:
		if(quesNo==16):
				break
		obj=Display("bg.jpg",[box_a,box_b,box_c,box_d,box_ques,box_amt,box_amount,box_back],amount,milestone,msg_pos)
		while questionOver==True:
			quesNo+=1
			if(quesNo==16):
				break
			questionOver=False
			if(quesNo==0):
				milestone=6
			elif(quesNo>milestone):
				curr_amt=amount2[milestone]
			ob1.submitscore(amount[quesNo-1])
			ques,ans,correct_ans,ansNo,cat,fname=getQues()
			#print ques
			if(quesNo!=1):
				clear_screen(gameDisplay)
				obj.to_next_ques(quesNo,milestone)
				clear_screen(gameDisplay)
				#time.sleep(1)
			obj.Template(gameDisplay,700,700,lfl,ans,ques)
			timer=MyTime(31)
			msg_to_screen(gameDisplay,"Rs."+str(amount[quesNo]),white,msg_pos[5],40)
			pygame.display.update()
			if(fname!=None):
				util.musicCall(fname)
		if(timer.time_left<0 and quesNo<=milestone):
			obj.timeOver(gameDisplay)
			obj.flash_answer(gameDisplay,ans,correct_ans,-1,box_ques,ques)
			gameExit=True
		if(quesNo==16):
			break
		current_time=timer.time_left
		if(current_time<0):
			current_time=0
		if(quesNo<=milestone):
			obj.display_timer(gameDisplay,timer_circle,current_time)
		
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
				left=True
			mouse_pos=pygame.mouse.get_pos()
			user_ans=-1;
			if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
				timer.pause()
				lno=lfl.if_in_lifeline(gameDisplay,mouse_pos)
				if(is_in_box(mouse_pos,box_a)):
					user_ans=0
				elif(is_in_box(mouse_pos,box_b)):
					user_ans=1
				elif(is_in_box(mouse_pos,box_c)):
					user_ans=2
				elif(is_in_box(mouse_pos,box_d)):
					user_ans=3
				elif(is_in_box(mouse_pos,box_amt)):
					obj.display_status(gameDisplay,quesNo)
					obj.Template(gameDisplay,700,700,lfl,ans,ques)
				elif(lno==0):
					left=True
					curr_amt=amount2[quesNo-1]
					quit=True
					gameExit=True
					obj.flash_answer(gameDisplay,ans,correct_ans,user_ans,box_ques,ques)
					ob1.submitfinalscore(curr_amt)					
					obj.end_screen(gameDisplay,amount2[quesNo-1])				
					break
				elif(lno==1 and lno not in lfl.used):
					ob2.phone_a_friend(ansNo,cat)
					lfl.used.append(1)
				elif(lno==2 and lno not in lfl.used):
					ob2.expert_advice(cat,ansNo)
					lfl.used.append(2)
				elif(lno==3 and lno not in lfl.used):
					ob2.audiencepoll(ansNo, quesNo)
					lfl.used.append(3)
				timer.play()
			
			lfl.if_in_lifeline(gameDisplay,mouse_pos)
			if_in_box(gameDisplay,mouse_pos,box_a)
			if_in_box(gameDisplay,mouse_pos,box_b)
			if_in_box(gameDisplay,mouse_pos,box_c)
			if_in_box(gameDisplay,mouse_pos,box_d)
			
			if(is_in_box(mouse_pos,box_amt)):
				color_box(gameDisplay,box_amt,light_yellow)
			else:
				color_box(gameDisplay,box_amt,yellow)
			obj.ans_to_screen(gameDisplay,ans,ques)
			msg_to_screen(gameDisplay,"Rs."+str(amount[quesNo]),white,msg_pos[5],40)
			
			current_time=timer.time_left
			if(current_time<0):
				current_time=0
			if(quesNo<=milestone):
				obj.display_timer(gameDisplay,timer_circle,current_time)
			
			pygame.display.update()
			
			if(user_ans!=-1):
				obj.flash_answer(gameDisplay,ans,correct_ans,user_ans,box_ques,ques)
				if(ans[user_ans]!=correct_ans):
					gameExit=True
				else:
					questionOver=True
					
	if(quesNo==15 and left!=True):
		curr_amt=50000000
	if(left!=True):
		ob1.submitfinalscore(curr_amt)
		obj.end_screen(gameDisplay,curr_amt)
		
	
def UI(eng):
	global ob1,ob2,gameDisplay
	ob1=eng
	#print ob1
	ob2=lifelines.lifelines(ob1)
	ob2.view_expert()
	gameDisplay=pygame.display.set_mode((display_width,display_height))
	pygame.display.set_caption('Kon Banega Crorepati?')
	pygame.init()
	pygame.font.init()
	clock=pygame.time.Clock()
	gameLoop()	
	pygame.quit()
	quit()
