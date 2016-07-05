from Tkinter import *
import util
from PIL import Image, ImageTk
import engine
import test

class welcome:
	def __init__(self, n, image):
		self.master=Tk()
		self.master.resizable(width=FALSE, height=FALSE)
		self.name=n
		self.logIn=""
		if n=="": 
			self.name="guest"
			self.LogIn=engine.login("guest")
		
		else:
			#try:
				self.LogIn=engine.login(name=self.name)
			#except:
				#try:
				#engine.utility.createuser(self.name)
				#self.LogIn=engine.login(name=self.name)
				#except:
				#	pass
		#creating a canvas to put an image on it
		self.canvas=Canvas(self.master, bg="white", height=500, width=800)
		self.canvas.pack()
		#putting a background image on the canvas
		self.photo=ImageTk.PhotoImage(Image.open(image))
		self.canvas.create_image(385, 200, image=self.photo)
	
	#changes title of the window 
	@property
	def windowTitle(self):
		s="Welcome, "+self.name
		self.master.wm_title(s)
	
	#function to insert the button
	@property
	def button(self):
		def close_window():
			self.master.destroy()		
			test.UI(self.LogIn)
		#button to quit this window
		kButton=Button(self.master, text="Start Game", command=close_window)
		kButton.pack(side=BOTTOM)
		
	#main function to invoke other functions
	def main(self):
		util.musicCall("KBC intro.mp3")
		self.windowTitle
		self.button
		self.master.mainloop()
	
#function which can be called from other modules to access the class highscore
def Welcome(Name):
	w=welcome(Name, "kbc.jpg")
	w.main()
