#=============================================================================================
# Home brew Hop Timer -- Multiple instance timers
#---------------------------------------------------------------------------------------------
# Time conversion functions
#=============================================================================================
#===================Includes==================================================================
#=============================================================================================


def intToTime(intTime):
	seconds = intTime 
	minutes = 0
	hours = 0
	if seconds > 59:	
		minutes = seconds/60
		seconds = seconds%60
		if minutes > 59:
			hours = minutes/60
			minutes = minutes%60
	if seconds < 10:
		secs = str('0' + str(seconds))
	else:
		secs = str(seconds)
	if minutes < 10:
		mins = str('0' + str(minutes))
	else:
		mins = str(minutes)
	if hours < 10:
		hrs = str('0' + str(hours))
	else:
		hrs = str(hours)
	return hrs + ':' + mins + ':' + secs
