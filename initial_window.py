#==============================================================================================
# Home Brew Hop Timer, Multiple instance timers
#----------------------------------------------------------------------------------------------
# This is the initial window, where timers can be created
#==============================================================================================
#===========Includes===========================================================================
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from boil import *
from timer_window import *
from timer_thread import *
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
		self.createMasterTime() # Master timer

	def initInitialWindow(self):
		self.setWindowTitle("Home Brew Hop Timer")
		self.setGeometry(100,100, 900, 150)
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
		
		#create layout to hold widgets
		self.initialGrid = QGridLayout()
		self.initial_layout = QVBoxLayout()
		self.initialGrid.addWidget(self.addButton, 0, 0, 1, 2)
		self.initialGrid.addWidget(self.setBoilTimeLabel, 1, 0)
		self.initialGrid.addWidget(self.setBoilTime, 1, 1)
		self.initialGrid.addWidget(self.startButton, 2, 0, 1, 2)
		self.initialGrid.addWidget(self.stopButton, 3, 0, 1, 2)
		
		self.initialWidget = QWidget()
		self.initialWidget.setLayout(self.initial_layout)
		self.setConnections()

	def setConnections(self):
		#connections
		self.addButton.clicked.connect(self.newTimer)
		self.setBoilTime.valueChanged.connect(self.setNewBoilTime)
		self.startButton.clicked.connect(self.startTimers)
		self.connect(self, SIGNAL('triggered()'), self.closeEvent)
		self.stopButton.clicked.connect(self.stopTimers) 
		
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

	#When main window is closed
	def closeEvent(self, event):
		if self.timer.isActive():
			if QMessageBox.warning(self,"Warning", "There are still timers running.", "Quit", "Cancel") is 1:
				event.ignore()
			else:
				self.timer.exit(0)
				self.setTimerState(False)
				for timer in self.__timerList:
					timer.close()
		else:
			self.timer.exit(0)
			self.setTimerState(False)
			for timer in self.__timerList:
				timer.close()


	#Stop all timers
	def stopTimers(self):
		self.timer.stopTimer()
		self.startButton.setDisabled(False)
		self.stopButton.setDisabled(True)

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
