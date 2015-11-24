#===================================================================================
# Home Brew Hop Timer. multiple instance timers
# ---------------------------------------------
# This is the GUI - creates instances of timerinstance - objects of type Timer.
#===================================================================================

# Includes =========================================================================
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from initial_window import *
#===================================================================================

# Variables ========================================================================
#timerList = [] #hold timers
#===================================================================================

hopTimer = QApplication(sys.argv)
mainWindow = InitialWindow() 
mainWindow.show()
mainWindow.raise_()
hopTimer.exec_()
