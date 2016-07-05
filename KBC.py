from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import sys
import util
import welcome

class startscreen:
	def __init__(self, imageFile):
		self.master=Tk()
		self.master.resizable(width=FALSE, height=FALSE)
		#widget to insert buttons 
		self.frame=Frame(self.master)
		self.frame.pack()
		#widget to insert button at the bottom of the frame
		self.bottomframe=Frame(self.master)
		self.bottomframe.pack(side=BOTTOM)
		#creates a canvas on which other items can be put
		self.canvas=Canvas(self.master, bg="white", height=500, width=800)
		self.canvas.pack()
		#puts an image on the canvas
		self.photo=ImageTk.PhotoImage(Image.open(imageFile))
		self.canvas.create_image(385, 200, image=self.photo)
		
	#function changes the title of the window to the app name
	@property	
	def windowTitle(self):
		self.master.wm_title("Kon Banega Crorepati?")
		
	#function inserts all the necessary buttons and text field in the window at appropriate places
	def buttons(self):
		#asks for user name
		name1=Label(self.frame, text="Name")
		name1.pack(side=LEFT)
		name2=Entry(self.frame, bd=5, justify=CENTER)
		name2.pack(side=LEFT)
		def Name():
			n=name2.get()
			self.master.destroy()
			welcome.Welcome(n)
		#button to go to next module after entering the name
		okButton=Button(self.frame, text="OK", command=Name)
		okButton.pack(side=TOP)

		#button to show the credits of the game
		cButton=Button(self.bottomframe, text="Credits", command=util.showCredits)
		cButton.pack(side=LEFT)

		#button for instructions
		htpButton=Button(self.bottomframe, text="How to play?", command=util.Instructions)
		htpButton.pack(side=LEFT)

		#high scores button
		hsButton=Button(self.bottomframe, text="High Scores", command=util.HighScore)
		hsButton.pack(side=LEFT)

		#helper function which assists the quit button
		def quit():
			val=tkMessageBox.askquestion("Quit Game!", "Are You Sure?", icon="warning")
			if val=='yes':
				sys.exit()	
		#button to quit	
		quitButton=Button(self.bottomframe, text="Quit Game!", fg="red", command=quit)
		quitButton.pack()

	#main only throws the window
	def main(self):
		util.musicCall("kbc.mp3")
		self.windowTitle
		self.buttons()
		self.master.mainloop()
if __name__=="__main__":
#object of the class is created
	kbc=startscreen("kbc.jpg")
#only the main function is invoked which in turn calls the other functions
	kbc.main()
