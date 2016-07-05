import pygame
import time
import random
import time

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



pygame.init()
pygame.font.init()
clock=pygame.time.Clock()


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
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Kon Banega Crorepati?')
#pygame.display.update()
FPS=10
box_c=([80,620],[290,620],[330,655],[290,690],[80,690],[40,655])
box_d=([410,620],[620,620],[660,655],[620,690],[410,690],[370,655])
box_a=([80,540],[290,540],[330,575],[290,610],[80,610],[40,575])
box_b=([410,540],[620,540],[660,575],[620,610],[410,610],[370,575])
box_ques=([80,400],[620,400],[660,460],[620,520],[80,520],[40,460])
box_amt=([410,310],[620,310],[660,345],[620,380],[410,380],[370,345])
msg_pos=([80,575],[410,575],[80,655],[410,655],[80,440],[410,340],[245,338],[245,638],[250,645])
box_amount=([245,315],[455,315],[495,350],[455,385],[245,385],[205,350])
box_back=([[245,620],[455,620],[495,655],[455,690],[245,690],[205,655]])
box_lifeline=([30,5],[300,5],[450,5],[600,5])
lifelines=("walkaway","Poll","Phone","expert")
timer_circle=[(350,615),38,25]
for i in range(len(msg_pos)-1):
	msg_pos[i][1]-=10
ans_seq=["A","B","C","D"]
amount=['0','5,000','10,000','20,000','40,000','80,000','1,60,000','3,20,000','6,40,000','12,50,000','25,00,000','50,00,000','1,00,00,000','2,00,00,000','5,00,00,000','10,00,00,000']

def display_timer(t):
	if(type(t)==int):
		t=str(t)
		if(len(t)==1):
			t=" "+t
	pygame.draw.circle(gameDisplay,black,timer_circle[0],timer_circle[1],0)
	pygame.draw.circle(gameDisplay,white,timer_circle[0],timer_circle[1],2)
	msg_to_screen(str(t),white,(timer_circle[0][0]-25,timer_circle[0][1]-20),60)
	pygame.display.update()

def display_lifelines():
	for j in range(len(lifelines)):
		img=pygame.image.load(lifelines[j]+".png")
		gameDisplay.blit(img, box_lifeline[j])

def if_in_lifeline(mouse_pos):
	lifelineNo=-1
	k=0
	for j in box_lifeline:
		if(mouse_pos[0]<=j[0]+100 and mouse_pos[0]>=j[0] and mouse_pos[1]<=j[1]+100 and mouse_pos[1]>=j[1]):
			lifelineNo=k
			break
		k+=1
	Template()
	if(lifelineNo!=-1):
		pygame.draw.rect(gameDisplay,light_yellow,[box_lifeline[lifelineNo][0],box_lifeline[lifelineNo][1],100,100],2)
	return lifelineNo

def template_status(quesNo,milestone):
	msg_x=250
	msg_y=11
	size=30
	clear_screen()
	for j in range(1,len(amount)):
		color=yellow
		if(j==len(amount)-quesNo):
			pygame.draw.rect(gameDisplay,light_yellow,[msg_x-10,msg_y-5,300,size])
		if(j==len(amount)-milestone or j==1):
			color=white
		msg=str(len(amount)-j)+" \t "+"Rs."+amount[len(amount)-j]
		if(len(amount)-j<=9):
			msg=" "+msg
		msg_to_screen(msg,color,[msg_x,msg_y],size)
		msg_y+=11+size
		color_box(box_back,yellow)
	pygame.display.update()

	
def display_status(quesNo,milestone):
	back=False
	timer=MyTime(31)
	template_status(quesNo,milestone)
	while back!=True:
		if(timer.time_left<=0):
			back=True
		for event in pygame.event.get():
			mouse_pos=pygame.mouse.get_pos()
			if is_in_box(mouse_pos,box_back) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				back=True
			elif is_in_box(mouse_pos,box_back):
				color_box(box_back,light_yellow)
			else:
				color_box(box_back,yellow)
			msg_to_screen("Continue",white,msg_pos[8],40)
		pygame.display.update()
	clear_screen()
			
		
def timeOver():
	msg_to_screen("Times Up!",orange,(200,250),50)
	pygame.display.update()
	time.sleep(1)

def to_next_ques_template(quesNo,milestone):
	bg = pygame.image.load("bluew.jpg")
	gameDisplay.blit(bg, (0,0))
	#pygame.draw.lines(gameDisplay,white,True,box_amount,2)
	msg_to_screen('Lets move to next Question',white,(180,50),40)
	msg_to_screen('You have won',white,(250,250),40)
	color_box(box_amount,yellow)
	msg_to_screen('Rs.'+amount[quesNo],white,msg_pos[6],40)
	color_box(box_back,yellow)
	msg_to_screen('Continue',white,msg_pos[7],40)
	pygame.display.update()

def to_next_ques(quesNo,milestone):
	timer=MyTime(7)
	back=False
	to_next_ques_template(quesNo,milestone)
	while back!=True:
		if(timer.time_left<=0):
			back=True
		mouse_pos=pygame.mouse.get_pos()
		#quit
		for event in pygame.event.get():
			if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
				if(is_in_box(mouse_pos,box_amount)):
					timer.pause()
					display_status(quesNo,milestone)
					to_next_ques_template(quesNo,milestone)
					timer.play()
				elif(is_in_box(mouse_pos,box_back)):
					back=True
			if(is_in_box(mouse_pos,box_amount)):
				color_box(box_amount,light_yellow)
			else:
				color_box(box_amount,yellow)
				
			if(is_in_box(mouse_pos,box_back)):
				color_box(box_back,light_yellow)
			else:
				color_box(box_back,yellow)
			msg_to_screen("Continue",white,msg_pos[7],40)
			msg_to_screen('Rs.'+amount[quesNo-1],white,msg_pos[6],40)
			pygame.display.update()

def ques_to_screen(box_ques,ques):
	decolor_box(box_ques)
	msg_to_screen('Q: '+ques,white,msg_pos[4],40)

def ans_to_screen(box_ques,ans,ques):
	ques_to_screen(box_ques,ques)
	for j in range(len(ans)):
			msg_to_screen(ans_seq[j]+": "+ans[j],white,msg_pos[j])

def flash_answer(ans,correct_ans,user_ans_no,box_ques,ques):
	box=[box_a,box_b,box_c,box_d]
	correct_ans_no=-1
	for j in range(len(box)):
		if ans[j]==correct_ans: correct_ans_no=j
	if(correct_ans_no!=user_ans_no and user_ans_no!=-1):
		color_box(box[user_ans_no],red)
	color_box(box[correct_ans_no],green)
	ans_to_screen(box_ques,ans,ques)
	pygame.display.update()
	time.sleep(1)
	
def getQues():
	return 'Who won the FIFA World Cup 2014?',["Brazil","Spain","Germany","Argentina"],"Germany"
	
def msg_to_screen(msg,color,pos,size=25):
	font=pygame.font.SysFont(None,size)
	screen_text=font.render(msg,True,color)
	gameDisplay.blit(screen_text,pos)

def is_in_box(loc,box):
	if(loc[0]>box[0][0] and loc[0]<box[1][0] and loc[1]>box[1][1] and loc[1]<box[4][1]):
		return True
	elif((loc[0]<box[0][0] and loc[0]>=box[5][0])or (loc[0]>=box[1][0] and loc[0]<box[2][0])):
		if(loc[1]<=box[3][1] and loc[1]>=box[0][1]):
			if(is_in_tri((loc[0],loc[1]),(box[0],box[5],box[4])) or is_in_tri((loc[0],loc[1]),(box[1],box[2],box[3]))):
				return True
	return False
	
def is_in_tri(loc,tri):
	if(loc[1]>tri[1][1]):
		loc=(loc[0],tri[2][1]-loc[1]+tri[0][1])
	if(abs((loc[1]-tri[0][1])*(tri[0][0]-tri[1][0]))>=abs((loc[0]-tri[0][0])*(tri[0][1]-tri[1][1]))):
		return True
	return False

def color_box(box,color):
	pygame.draw.polygon(gameDisplay,color, box)
	pygame.draw.lines(gameDisplay,white,True,box,2)
		
def decolor_box(box):
	color_box(box,black)
	
def if_in_box(mouse_pos,box,color=orange):
	if is_in_box(mouse_pos,box):
		color_box(box,color)
	else:
		decolor_box(box)

def clear_screen():
	pygame.draw.rect(gameDisplay,black,[0,0,display_width,display_height])
	pygame.display.update()
		
def Template():
	bg = pygame.image.load("bg.jpg")
	gameDisplay.blit(bg, (0, 0))
	decolor_box(box_a)
	decolor_box(box_b)
	decolor_box(box_c)
	decolor_box(box_d)
	pygame.draw.line(gameDisplay,white,(0,655),(40,655),2)
	pygame.draw.line(gameDisplay,white,(330,655),(370,655),2)
	pygame.draw.line(gameDisplay,white,(660,655),(700,655),2)
	pygame.draw.line(gameDisplay,white,(0,575),(40,575),2)
	pygame.draw.line(gameDisplay,white,(330,575),(370,575),2)
	pygame.draw.line(gameDisplay,white,(660,575),(700,575),2)
	pygame.draw.lines(gameDisplay,white,True,box_ques,2)
	pygame.draw.line(gameDisplay,white,(0,460),(40,460))
	pygame.draw.line(gameDisplay,white,(660,460),(700,460))
	color_box(box_amt,yellow)
	pygame.draw.line(gameDisplay,white,(660,345),(700,345))
	display_lifelines()

def get_milestone():
	pass

def gameLoop():
	#pygame.display.update()
	gameExit=False
	questionOver=True
	quesNo=0
	milestone=6
	mouse_pos=0
	while gameExit!=True:
	
		while questionOver==True:
			questionOver=False
			quesNo+=1
			if(quesNo==0):
				milestone=get_milestone()
			else:
				pass
			ques,ans,correct_ans=getQues()
			if(quesNo!=1):
				clear_screen()
				to_next_ques(quesNo,milestone)
				clear_screen()
				#time.sleep(1)
			Template()
			timer=MyTime(31)
			pygame.display.update()
		if(timer.time_left<0):
			timeOver()
			flash_answer(ans,correct_ans,-1,box_ques,ques)
			gameExit=True
		
		
		current_time=timer.time_left
		if(current_time<0):
			current_time=0
		if(quesNo<=milestone):
			display_timer(current_time)
		
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
			mouse_pos=pygame.mouse.get_pos()
			user_ans=-1;
			if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
				if(is_in_box(mouse_pos,box_a)):
					user_ans=0
				elif(is_in_box(mouse_pos,box_b)):
					user_ans=1
				elif(is_in_box(mouse_pos,box_c)):
					user_ans=2
				elif(is_in_box(mouse_pos,box_d)):
					user_ans=3
				elif(is_in_box(mouse_pos,box_amt)):
					display_status(quesNo,milestone)
					Template()
			
			if_in_lifeline(mouse_pos)
			if_in_box(mouse_pos,box_a)
			if_in_box(mouse_pos,box_b)
			if_in_box(mouse_pos,box_c)
			if_in_box(mouse_pos,box_d)
			
			
			if(is_in_box(mouse_pos,box_amt)):
				color_box(box_amt,light_yellow)
			else:
				color_box(box_amt,yellow)
			ans_to_screen(box_ques,ans,ques)
			msg_to_screen("Rs."+str(amount[quesNo]),white,msg_pos[5],40)
			
			current_time=timer.time_left
			if(current_time<0):
				current_time=0
			if(quesNo<=milestone):
				display_timer(current_time)
			
			pygame.display.update()
			
			if(user_ans!=-1):
				flash_answer(ans,correct_ans,user_ans,box_ques,ques)
				if(ans[user_ans]!=correct_ans):
					gameExit=True
				else:
					questionOver=True
			clock.tick(10)
			
					
gameLoop()					
pygame.quit()
quit()


'''def is_in_tri(loc,points):
	x=loc[0]-points[0][0]
	y=loc[0]-points[0][1]
	xb=points[1][0]-points[0][0]
	yb=points[1][1]-points[0][1]
	xc=points[2][0]-points[0][0]
	yc=points[2][1]-points[0][1]
	d=(xb*yc-xc*yb)*1.0
	wa=(x*(yb-yc)+y*(xc-xb)+xb*yc-xc*yb)/d
	wb=(x*yc-y*xc)/d
	wc=(y*xb-x*yb)/d
	print(wa,wb,wc)
	if(wa>=0 and wa<=1 and wb>=0 and wb<=1 and wc>=0 and wc<=1):
		return True
	return False'''
