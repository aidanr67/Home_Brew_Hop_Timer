#==============================================================================================
# Home Brew Hop Timer, Multiple instance timers
#----------------------------------------------------------------------------------------------
# This is the initial window, where timers can be created
#==============================================================================================
#===========Includes===========================================================================
import sys
from os.path import expanduser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from boil import *
from timer_window import *
from timer_thread import *
from database import *
#==============================================================================================

# Initial Window class
class InitialWindow(QMainWindow): # Inherits from QMainWindow
	#Class variables
	__timerList = list()

	#Constructor
	def __init__(self):
		super(QMainWindow, self).__init__() #Super class constructor
		self.boil = Boil() #create and set Boil object
		self.boil.setBoil(3600, False) #default 60min boil
		# create timer and timer thread
		self.timer = TimerThread()
		self.timer.start()
		self.initInitialWindow()
		self.initMenuBar()
		self.createMasterTime() # Master timer
		self.setConnections()

	def initInitialWindow(self):
		self.setWindowTitle("Home Brew Hop Timer")
		self.setGeometry(100,100, 900, 300)
		self.createInitialLayout()
	
		#Set central widget
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.initialGrid)
		self.setCentralWidget(self.central_widget)

	def createInitialLayout(self):
		#This is the initial layout of the window
		self.addButton = QPushButton("Add Timer")
		self.setBoilTimeLabel = QLabel("Set Boil Time (mins): ")
		self.setBoilTime = QSpinBox()
		self.setBoilTime.setValue(60)
		self.startButton = QPushButton("Start")
		self.stopButton = QPushButton("Stop")
		self.stopButton.setDisabled(True)
		self.resetButton = QPushButton("Reset")
		self.resetButton.setVisible(False)
		
		#create layout to hold widgets
		self.initialGrid = QGridLayout()
		self.initial_layout = QVBoxLayout()
		self.initialGrid.addWidget(self.addButton, 0, 0, 1, 2)
		self.initialGrid.addWidget(self.setBoilTimeLabel, 1, 0)
		self.initialGrid.addWidget(self.setBoilTime, 1, 1)
		self.initialGrid.addWidget(self.startButton, 2, 0, 1, 2)
		self.initialGrid.addWidget(self.stopButton, 3, 0, 1, 2)
		self.initialGrid.addWidget(self.resetButton, 3, 0, 1, 2)
		
		self.initialWidget = QWidget()
		self.initialWidget.setLayout(self.initial_layout)

	def initMenuBar(self):
		self.menu = QMenuBar(self)
		self.fileMenu = QMenu("&File", self)
		self.menu.addMenu(self.fileMenu)
		#Quit action	
		self.quit = QAction("&Quit", self)
		self.fileMenu.addAction(self.quit)
		#Load Recipe action
		self.recipe = QAction("&Load BrewTarget Recipe", self)
		self.fileMenu.addAction(self.recipe)
		

	def setConnections(self):
		#connections
		self.addButton.clicked.connect(self.newTimer)
		self.setBoilTime.valueChanged.connect(self.setNewBoilTime)
		self.startButton.clicked.connect(self.startTimers)
		self.connect(self, SIGNAL('triggered()'), self.closeEvent)
		self.stopButton.clicked.connect(self.stopTimers)
		self.resetButton.clicked.connect(self.resetTimers)
		self.connect(self.quit, SIGNAL("triggered()"), self.close) 
		self.connect(self.recipe, SIGNAL("triggered()"), self.addRecipe)	
		#Connect timer emit
		self.connect(self.timer, self.timer.signal, self.decrement)

	def createMasterTime(self):
		#Master timer widget
		self.masterTimeDisplay = QLCDNumber(self)
		self.masterTimeDisplay.setNumDigits(8)
		self.initialGrid.addWidget(self.masterTimeDisplay, 0, 3, 4, 12)
		self.displayTime()

	def displayTime(self):
		time = intToTime(self.boil.getTime())
		self.masterTimeDisplay.display(time)
		

	#add button clicked
	def newTimer(self):
		self.timerWindow = TimerWindow(self.boil, self.timer)
		self.timerWindow.show()
		self.__timerList.append(self.timerWindow)
	
	def setNewBoilTime(self):
		#set the boil time variable
		self.boil.setTime(self.setBoilTime.value()*60)
		self.displayTime()

	def startTimers(self):
		self.timer.startTimer()
		self.startButton.setDisabled(True)
		self.stopButton.setDisabled(False)
		self.setBoilTime.setDisabled(True)
		self.resetButton.setVisible(False)
		self.stopButton.setVisible(True)

	def resetTimers(self):
		if QMessageBox.warning(self,"Warning", "Are you sure you want to reset all timers.", "Reset", "Cancel") is 0:
			self.setNewBoilTime()
			self.setTimers()
			self.resetButton.setVisible(False)
			self.stopButton.setVisible(True)
			self.setBoilTime.setDisabled(False)

	def setTimers(self):
		for timer in self.__timerList:
			timer.setTime()
		
	#When main window is closed
	def closeEvent(self, event):
		if self.timer.isActive():
			if QMessageBox.warning(self,"Warning", "There are still timers running.", "Quit", "Cancel") is 1:
				event.ignore()
			else:
				self.timer.exit(0)
				self.setTimerState(False)
				self.closeAllTimers()
		else:
			self.timer.exit(0)
			self.setTimerState(False)
			for timer in self.__timerList:
				timer.close()

	def closeAllTimers(self):
		for timer in self.__timerList:
			timer.close()

	#Stop all timers
	def stopTimers(self):
		self.timer.stopTimer()
		self.startButton.setDisabled(False)
		self.stopButton.setDisabled(True)
		self.stopButton.setVisible(False)
		self.resetButton.setVisible(True)

	def decrement(self):
		if self.boil.getTime() > 0:
			self.boil.decrementTime()
			self.displayTime()
		else:
			self.timeout()

	def timeout(self):
		self.timer.stopTimer()
		self.masterTimeDisplay.display('KNOCKOUT')

	#Set all timers as started/stopped
	def setTimerState(self, isStarted):
		self.boil.setStarted(isStarted)

	#Load recipe from Brewtarget
	def addRecipe(self):
		home = expanduser("~")
		home = home + '/.config/brewtarget/database.sqlite'
		db = Database(home)
		if not db.connect(): 
			QMessageBox.warning(self, "Error", '''Failed to open BrewTarget database. This is most likely because BrewTarget is using it.
If BrewTarget is open please close it.''')
			
		else:
			indexedRecipes = db.getRecipes()
			recipes = indexedRecipes[1]
			selection, isSelected = QInputDialog.getItem(self, "Select Brewtarget Recipe", "Brewtarget Recipes",
							recipes, 0, False)
			#get recipe index
			if isSelected and selection:
				i = recipeIndex = 1 
				for recipe in recipes:
					if recipe == selection:
						recipeIndex = i
					i = i + 1
			# set boil time
				boilTime = db.getBoilTime(recipeIndex)
				if boilTime != self.setBoilTime.value():
					self.setBoilTime.setValue(boilTime)
		
#------------------------- get hop additions and create timers ------------------
				#close existing timers
				if self.__timerList:
					if QMessageBox.warning(self,"Warning", "This will overwrite existing timers and stop timer if running.", "OK", "Cancel") is 0:
						if self.timer.isActive():
							self.stopTimers()
						self.closeAllTimers()	
						del self.__timerList[:] #empty list
					else:
						return
				# Get recipe hop additions
				hopAdditions = db.getHopAdditions(recipeIndex)
				i = 0
				for hopAddition in hopAdditions[0]:
					match = False
					hopAddition = int(hopAddition)
					if not self.__timerList: #create first timer
						self.timerFromRecipe(hopAddition, hopAdditions[1][i], hopAdditions[2][i])
						match = True
					else:
						for timer in self.__timerList:
							if timer.getTime() == hopAddition:
								self.addToTimer(timer, hopAdditions[1][i], hopAdditions[2][i])
								match = True
					if not match:
						self.timerFromRecipe(hopAddition, hopAdditions[1][i], hopAdditions[2][i])
					i = i + 1
			db.disconnect()
			
	def addToTimer(self, timer, name, amount):
		timer.addNoteInfo(name, amount)
		
	def timerFromRecipe(self, time, name, amount):
		self.timerWindow = TimerWindow(self.boil, self.timer)
		self.timerWindow.setTimeBox(time)
		self.timerWindow.setNote(name, amount)
		self.timerWindow.show()
		self.__timerList.append(self.timerWindow)
					
