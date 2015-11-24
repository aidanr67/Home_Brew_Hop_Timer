#============================================================================================
# Home Brew Hop Timer -- Multiple instance timers
# ------------------------------------------------------------------------------------------
# This class stores Boil state and time information
#============================================================================================

class Boil():
	def __init__(self):
		self.boilTime = 0
		self.started = False

	def setBoil(self, time, isStarted):
		self.boilTime = time
		self.started = isStarted

	def setTime(self, time):
		self.boilTime = time

	def setStarted(self, isStarted):
		self.started = isStarted

	def getTime(self):
		return self.boilTime

	def isStarted(self):
		return self.started

	def decrementTime(self):
		self.boilTime = self.boilTime - 1
