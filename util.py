from Tkinter import *
import pygame
import engine
class Credits():
	def __init__(self):
		self.master=Tk()
		self.master.resizable(width=FALSE, height=FALSE)
		self.master.minsize(width=500, height=200)
		
	#changes the title of the indow as required
	@property
	def windowTitle(self):
		self.master.wm_title("Game Credits")
	
	#reads the instructions from a file and displays them on the window
	def display(self, fileName):
		with open(fileName, "r") as creditFile:
			s=creditFile.read()
		#showing the instructions
		label1=Message(self.master, text=s)
		label1.pack()
	
	#function to insert the button on the window
	@property
	def button(self):
		#helper function to ok button
		def close_window():
			self.master.destroy()
		#button to quit this window
		kButton=Button(self.master, text="OK", command=close_window)
		kButton.pack(side=BOTTOM)
	
	#main function to call other functions
	def main(self):
		self.windowTitle
		self.button
		self.display("credits.txt")
		self.master.mainloop()
		
#function which can be called from other modules to access the class highscore
def showCredits():
	sc=Credits()
	sc.main()
	


class highscore():
	def __init__(self):
		self.master=Tk()
		self.master.minsize(width=250, height=100)
		self.master.resizable(width=FALSE, height=FALSE)

	#function to change the title of the window
	@property		
	def windowTitle(self):
		self.master.wm_title("High Scores")
	
	#function which reads high scores from a file and displays them
	def display(self, fileName):
		#reading the high sc from a fileores
		#with open(fileName, "r") as highscoreFile:
		#	s=highscoreFile.read()
		#showing the high scores
		sp = engine.login.gethighscores()
		s = "".join([str(i[0]) + " : " + str(i[1]) + "\n" for i in sp])
		if s=="":
			s="No High Scores to display!!!\n"
		label1=Message(self.master, text=s)
		label1.pack()
	
	#inserts the button on the window
	@property
	def button(self):
		#helper funtion
		def close_window():
			self.master.destroy()
		#button to quit this window
		kButton=Button(self.master, text="OK", command=close_window)
		kButton.pack(side=BOTTOM)
	
	#main function which calls other functions
	def main(self):
		self.windowTitle
		self.display("high_scores.txt")
		self.button
		self.master.mainloop()
		
#function which can be called from other modules to access the class highscore
def HighScore():
	hs=highscore()
	hs.main()
	
	
	
	
class instructions():
	def __init__(self):
		self.master=Tk()
		self.master.resizable(width=FALSE, height=FALSE)
		
	#changes the title of the indow as required
	@property
	def windowTitle(self):
		self.master.wm_title("Instructions to play")
	
	#reads the instructions from a file and displays them on the window
	def display(self, fileName):
		with open(fileName, "r") as instructFile:
			s=instructFile.read()
		#showing the instructions
		label1=Message(self.master, text=s)
		label1.pack()
	
	#function to insert the button on the window
	@property
	def button(self):
		#helper function to ok button
		def close_window():
			self.master.destroy()
		#button to quit this window
		kButton=Button(self.master, text="OK", command=close_window)
		kButton.pack(side=BOTTOM)
	
	#main function to call other functions
	def main(self):
		self.windowTitle
		self.button
		self.display("instructions.txt")
		self.master.mainloop()
		
#function which can be called from other modules to access the class highscore
def Instructions():
	i=instructions()
	i.main()
	
	
	
	
class Music:
	def __init__(self, fileName):
		self.musicFile=fileName
		
	#function plays a music file in the background when it is called	
	@property
	def play(self):
		#pygame object is created but a window is not thrown
		#this is done so that the music remains in the background itself
		pygame.init()
		pygame.mixer.music.load(self.musicFile)
		pygame.mixer.music.play()
		
def musicCall(musicFile):
	m=Music(musicFile)
	m.play	
