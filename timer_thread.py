#=============================================================================================
# Home Brew Hop Timer. Multimple instance timers
# --------------------------------------------------------------------------------------------
# This is the Timer class
#=============================================================================================
#==========Inlcudes===========================================================================
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#=============================================================================================

class TimerThread(QThread):
	def __init__(self):
		super(QThread, self).__init__()
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.setSingleShot(False)
		self.timer.timeout.connect(self.decrement)
		self.signal = SIGNAL('decrement')
	
	def startTimer(self):
		self.timer.start()
	
	def stopTimer(self):
		self.timer.stop()

	def decrement(self):
		self.emit(self.signal)

	def isActive(self):
		return self.timer.isActive()
