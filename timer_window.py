#===================================================================================
# Home Brew Hop Timer. Multiple instance timers
# ---------------------------------------------
# This is the timer instances.
#===================================================================================
#===Includes========================================================================
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time_conversion import *
from initial_window import *
from boil import *
from play_alarm import *
#===================================================================================
	
# Timer window class
class TimerWindow(QMainWindow): #Inherits from QMainWindow super class
	#Constructer
	def __init__(self, boil, timer):
		super(QMainWindow, self).__init__() #Super class constructer
		self.timer = timer
		self.boil = boil
		self.alarmRinging = False
		self.time = 60 
		self.initTimerWindow()
	
	def initTimerWindow(self):
		self.setWindowTitle("Home Brew Timer")
		self.create_timer_layout()

		# Set central widget
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.timer_grid)
		self.setCentralWidget(self.central_widget)
		
	#define layout
	def create_timer_layout(self):
		self.setLabel = QLabel("Set Time (mins): ")
		self.setNumber = QSpinBox(self)
		self.setNumber.setFocus(True)
		self.setNumber.selectAll()
		self.timeLabel = QLabel("Time to addition: ")
		self.timeDisplay = QLCDNumber(self)
		self.timeDisplay.setSegmentStyle(QLCDNumber.Flat)
		self.timeDisplay.setStyleSheet('color: black')
		self.noteLabel = QLabel("Notes: ")
		self.noteEdit = QLineEdit(self)
		#For after alarm
		self.stopButton = QPushButton("Stop")
		self.stopButton.setVisible(False)
		

		#Create initial layout
		self.timer_grid = QGridLayout()
		self.timer_grid.addWidget(self.setLabel, 0, 0, 1, 2)
		self.timer_grid.addWidget(self.setNumber, 0, 3)
		self.timer_grid.addWidget(self.timeLabel, 1, 0, 1, 2)
		self.timer_grid.addWidget(self.timeDisplay, 1, 3, 2, 2)
		self.timer_grid.addWidget(self.noteLabel, 3, 0)
		self.timer_grid.addWidget(self.noteEdit, 3, 1, 1, 3)
		#For after alarm
		self.timer_grid.addWidget(self.stopButton, 0, 0, 2, 3)
	
		#connections
		self.setNumber.valueChanged.connect(self.setTime)
		self.stopButton.clicked.connect(self.alarmStopped)
		#Connect timer emit
		self.connect(self.timer, self.timer.signal, self.decrement)

	def setTimeDisplay(self):
		#set timer to display
		timeDisplay = intToTime(self.time)
		self.timeDisplay.display(timeDisplay)

	def decrement(self):
		if self.time > 0:
			self.time = self.time - 1
			self.setTimeDisplay()
		else:
			if not self.alarmRinging:
				self.timeout()

	def setTime(self):
		time = self.setNumber.value() * 60 #Store time is seconds
		if time > self.boil.getTime():
			QMessageBox.warning(self, "Error", "Addition time cannot be larger than remaining boil time.")
		else:
			#Invert time as per home brewing convention
			time = self.boil.getTime() - time
			self.time = time
			self.setTimeDisplay()
		self.alarmRinging = False

	def timeout(self):
		alarmStyle ="""
		QPushButton{
		background-color: red;
		}
		"""
		self.alarmLayout()
		self.setStyleSheet(alarmStyle)
		self.alarm = WavePlayerLoop('./')
		self.alarm.play()
		self.alarmRinging = True 

	def alarmLayout(self):
		self.setLabel.setVisible(False)
		self.setNumber.setVisible(False)
		self.timeLabel.setVisible(False)
		self.timeDisplay.setVisible(False)
		self.stopButton.setVisible(True)
		
	def alarmStopped(self):
		self.alarm.stop()
		self.setLabel.setVisible(True)
		self.setNumber.setVisible(True)
		self.timeLabel.setVisible(True)
		self.timeDisplay.setVisible(True)
		self.stopButton.setVisible(False)
		normalStyle="""
		QPushButton{
		background-color: #F2F2F2;
		}
		"""
		self.setStyleSheet(normalStyle)
