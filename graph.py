from Tkinter import *
import random
import tkFont
from engine import utility,login
from PIL import Image, ImageTk
from playgif import *
class phone_a_friend_gui(Frame):
    def __init__(self, master,ans,category,names,jobs,categories,*pargs):
        Frame.__init__(self, master, *pargs)
	self.category=category
	self.answer=ans	
	self.b1=Image.open("call1.png")
	self.button_image=ImageTk.PhotoImage(self.b1)
	self.c=Canvas(self,width=600,height=550,bg='black')
	options=['A','B','C','D']
	options.remove(self.answer)
	dont_know_string="Umm.. I don't exactly know the answer, but I think the answer is ..\n option.. "
	know_string="I can surely say that the answer is \n option .. "
	self.display=["","",""]
	for i in range(len(categories)):
		if(category in categories[i]):
			self.display[i]=know_string
		else:
			self.display[i]=dont_know_string
		self.display[i]+=" "+self.answer
		
	call1=Button(self,text="call",bd=0,image=self.button_image,bg='black',activebackground='honeydew2',command=(lambda: self.call_friend(1,master)))
	call2=Button(self,text="call",bd=0,image=self.button_image,bg='black',activebackground='honeydew2',command=(lambda: self.call_friend(2,master)))
	call3=Button(self,text="call",bd=0,image=self.button_image,bg='black',activebackground='honeydew2',command=(lambda: self.call_friend(3,master)))
	call1.config(highlightbackground='black')
	call2.config(highlightbackground='black')
	call3.config(highlightbackground='black')
	call1.place(x=500,y=20)
	call2.place(x=500,y=200)
	call3.place(x=500,y=400)
	self.c.place(x=0,y=0)
	size=20
	tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
        self.c.create_text(10,40, text=names[0],font=tempfont,fill="honeydew2",anchor=W)
	self.c.create_text(10,80, text=jobs[0],font=tempfont,fill="honeydew2",anchor=W)
        self.c.create_text(10,230, text=names[1],font=tempfont,fill="honeydew2",anchor=W)
	self.c.create_text(10,270, text=jobs[1],font=tempfont,fill="honeydew2",anchor=W)
        self.c.create_text(10,410, text=names[2],font=tempfont,fill="honeydew2",anchor=W)
	self.c.create_text(10,450, text=jobs[2],font=tempfont,fill="honeydew2",anchor=W)
    def call_friend(self,friend_no,window):
	self.destroy()
	new=Frame(window)
	
	def display_answer():
		anim.destroy()
		new.config(bg="black")
		size=40
		tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
		newcanvas=Canvas(window,width=600,height=550,bg='black')
		newcanvas.place(x=0,y=0,relheight=1,relwidth=1)
		newcanvas.create_text(250,225,text=self.display[friend_no-1],font=tempfont,fill="honeydew2",width=400)
		quit_button=Button(window,text="QUIT",bd=2,bg="honeydew2",command=window.destroy)
		quit_button.place(x=300,y=510)
	new.place(x=0,y=0,relheight=1,relwidth=1)
	new.after(3000,display_answer)
	anim=MyLabel(new,"loadbar.gif")
	anim.place(x=100,y=250)
	size=20
	tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
	text=Label(window,text="CONNECTING....",width=80)
	text.place(x=25,y=225)
	
#this function gives true if all the values in the passed dictionary are unequal else gives falsei
def allunequal(given_dict):
	values=given_dict.values()
	for i in values:
		values.remove(i)
		if(i in values):
			return False
	return True	
def remove_underscore(string):
	new=""
	for i in range(len(string)):
		if(string[i]=="_"):
			new+=" "
		else:
			new+=string[i]
	return new
class lifelines:
  def __init__(self,obj):
	self.obj=obj
	experts=open("experts.dat","r")
	self.expertname=""
	self.experdetails=""
	self.expertimage=""
	self.expertcategory=[]
	for line in iter(experts):
		print line.split()
		print self.obj.expert
		if(line.split()[0]==str(self.obj.expert)):
			print "*********************************************"
			
			self.expertname=remove_underscore(line.split()[1])
			self.expertimage=line.split()[2]
			self.expertdetails=remove_underscore(line.split()[3])
			self.expertcategory.extend(line.split()[4:])
			break
  def audiencepoll(self,ans,qno):
	options={'A':0,'B':0,'C':0,'D':0}
	l=options.keys()
        if(qno<8): 
	  l.remove(ans)
	  while(not(allunequal(options))):
		options[ans]=random.randint(40,50)
		options[l[0]]=random.randint(10,30)
		while(True):
			options[l[1]]=random.randint(5,25)
			if(options[ans]+options[l[0]]+options[l[1]]<=95):
				break
        else:
	 l.remove(ans)
	 options[ans]=random.randint(30,47)
	 options[l[0]]=random.randint(10,30)
         while(True):
			options[l[1]]=random.randint(5,35)
			if(options[ans]+options[l[0]]+options[l[1]]<=95):
				break
	options[l[2]]=100-(options[ans]+options[l[0]]+options[l[1]])
	data = [options['A'],options['B'],options['C'],options['D']]
	root = Tk()
	root.title("Audience poll")
	c_width = 350
	c_height = 450
	c = Canvas(root, width=c_width, height=c_height, bg= 'black',bd=2)
	y_stretch = 10
	# gap between lower canvas edge and x axis
	y_gap = 45
	# stretch enough to get all data items in
	x_stretch = 100
	x_width = 30
	# gap between left canvas edge and y axis
	x_gap =20
	lx0=[20,95,170,245]
	lx1=[80,155,230,305]
	c.create_line(0,405,350,405,fill="honeydew2",width=2)
	c.create_line(0,45,350,45,fill="honeydew2",width=2)
	c.create_line(0,45+36*10,350,45+36*10,fill="honeydew2",width=1)
	c.create_line(0,45+36*9,350,45+36*9,fill="honeydew2",width=1)
	c.create_line(0,45+36*8,350,45+36*8,fill="honeydew2",width=1)
	c.create_line(0,45+36*7,350,45+36*7,fill="honeydew2",width=1)
	c.create_line(0,45+36*6,350,45+36*6,fill="honeydew2",width=1)
	c.create_line(0,45+36*5,350,45+36*5,fill="honeydew2",width=1)
	c.create_line(0,45+36*4,350,45+36*4,fill="honeydew2",width=1)
	c.create_line(0,45+36*3,350,45+36*3,fill="honeydew2",width=1)
	c.create_line(0,45+36*2,350,45+36*2,fill="honeydew2",width=1)
	c.create_line(0,45+36,350,45+36,fill="honeydew2",width=1)
	text=["A","B","C","D"]
	size=20
	tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
	def click(event):
		if(event.x>100 and event.x<230 and event.y>406 and event.y<450):
			root.quit()
		else:
			pass
	for x, y in enumerate(data):
		x0=lx0[x]
        	y0 = c_height -3.6*y-y_gap
		x1=lx1[x]
        	y1 = c_height - y_gap
        	rect=c.create_rectangle(x0, y0, x1, y1, fill="orange2",outline="honeydew2",width=2)
		c.tag_raise(rect)
        	c.create_text(x0+15,46,anchor=SW, text=str(y)+"%",font=tempfont,fill="honeydew2")
        	c.create_text(x0+15,409,anchor=SW, text=text[x],font=tempfont,fill="honeydew2")
        c.create_rectangle(100,406,230,450,outline="black",fill="honeydew2")
	c.create_text(160,430,text="OK",font=tempfont,fill="black")
	c.bind("<Button-1>", click)
	c.grid()
	root.mainloop()
	try:
		self.obj.lifelineused("audience poll")
	except:
		raise Exception("Life line already used")
#This function takes the answer for the question and the category of the question as parameters and invokes the phone a friend lifeline
#Friend names and jobs are stored in phone_a_friend.dat in the format,
# slno name job categories_he_is_capable_of_answering
  def phone_a_friend(self,ans,category):	
	root = Tk()
	root.title("Phone a friend")
	root.geometry("600x550")
	root.configure(background="black")
	friendnames=[]
	friendjobs=[]
	friend_category=[]
	database=open("phone_a_friend.dat","r")
	random1=random.randint(1,6)
	random2=random.randint(7,12)
	random3=random.randint(13,18)
	for line in iter(database):
		if(line.split()[0]==random1 or line.split()[0]==random2 or line.split()[0]==random3):
			friendnames.append(remove_underscore(line.split()[1]))
			friendjobs.append(remove_underscore(line.split()[2]))
			friendcategory.append(line.split()[3:])
	database.close()
#	obj=phone_a_friend_gui(root,ans,category,friendnames,friendjobs,friend_category)
	obj=phone_a_friend_gui(root,'A',"MY",["vinay","Aravind","Krishna"],["Scientist","Astronaught","software Engineer"],[["SC","GEO"],["MY","GEO"],["MY","GEO","SC"]])
	obj.pack(fill=BOTH,expand=YES)
	
	root.mainloop()
	try:
		self.obj.lifelineused("phone_a_friend")
	except:	

		raise Exception("Life line already used")
#This function shows the user who is the expert for this game
  def view_expert(self):
		root=Tk()
		root.title("Expert For Today")
		root.configure(background="white")
		root.geometry("500x600")
		im=Image.open(self.expertimage)
		image=ImageTk.PhotoImage(im)
		size=12
		tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
		newcanvas=Canvas(root,width=500,height=500,bg='white')
		size=15
		tempfont1 = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
		size=35
		tempfont2 = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
		newcanvas.place(x=0,y=0,relheight=1,relwidth=1)
		newcanvas.create_text(250,250,text="The Expert \nfor today is ....",font=tempfont2)
		def display_image():
		 newcanvas.configure(bg='black')
		 newcanvas.create_image(225,150,image=image)
		 newcanvas.create_text(150,40,text=self.expertname,anchor=W,font=tempfont1,fill="honeydew2",justify=CENTER,width=200)
		def display_text():
			 newcanvas.create_text(40,250,anchor=NW,text=self.expertdetails,font=tempfont,fill="honeydew2",width=430)
		root.after(3000,display_text)
		root.after(1500,display_image)
		root.mainloop()
#expert_advice function takes the answer for the question and its category as parameters and invoke the expert's advice lifeline
  def expert_advice(self,ans,category):
	displaystring=""
	if(category in self.expertcategory):
		displaystring="\nGo for option..  "
	else:
		displaystring="I can't definitely say,\n but I think you can go with\noption .. "
	displaystring+=ans
	root=Tk()
	root.title("Expert's Advice")
	root.configure(background="white")
	root.geometry("500x500")
	im=Image.open(self.expertimage)
	image=ImageTk.PhotoImage(im)
	size=12
	tempfont = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
	newcanvas=Canvas(root,width=500,height=500,bg='white')
	size=15
	tempfont1 = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
	size=20
	tempfont2 = tkFont.Font(family='Helvetica',size=size,name="font%s" %size)
	newcanvas.place(x=0,y=0,relheight=1,relwidth=1)
	newcanvas.create_image(225,120,image=image)
	newcanvas.create_text(250,300,text=self.expertname+"\nSays..,\n"+displaystring,font=tempfont2)	
	quit_button=Button(root,text="QUIT",bd=2,bg="honeydew2",command=root.destroy)
	quit_button.place(x=300,y=450)
	root.mainloop()	
l=login("guest")
obj=lifelines(l)
obj.phone_a_friend('B',14)
obj.view_expert()
obj.expert_advice('A',"MY")
obj.audiencepoll('C',12)
#l.currentplayer.close()

