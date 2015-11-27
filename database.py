#============================================================================================
# Home Brew Hop Timer -- Multiple instance timer
#--------------------------------------------------------------------------------------------
# This is the database class -- handles database access to Brewtarget DB
#============================================================================================
#================Includes====================================================================
import sys
import sqlite3
#============================================================================================

class Database():
	def __init__(self, dbName):
		self.dbName = dbName
		self.conn = None

	def connect(self):
		self.conn = sqlite3.connect(self.dbName)
		cur = self.conn.cursor()
		#Test db
		try:				
			cur.execute('SELECT 1 FROM recipe')
		except sqlite3.OperationalError:
			print "Unable to open Database."
			return False
		else:
			return True

	def disconnect(self):
		self.conn.close()

	#retuen list of recipes
	def getRecipes(self):
		recipes = list()
		recipes.append([])
		recipes.append([])
		cur = self.conn.cursor()
		index = 1
		for row in cur.execute('SELECT id, name FROM recipe'):
			recipes[0].append(row[0])
			recipes[1].append(row[1])
			index = index + 1
		return recipes
	def getBoilTime(self, recipe):
		boilTime = 0
		cur = self.conn.cursor()
		boilTime = cur.execute('SELECT boil_time FROM recipe WHERE id=:recipe',
				 {"recipe": recipe}).fetchone()[0]
		return boilTime
	
	# return 2D list with discriptions and times
	def getHopAdditions(self, recipe):
		hopAddition = list()
		hopAddition.append([])
		hopAddition.append([])
		hopAddition.append([])
		cur = self.conn.cursor()
		for row in cur.execute(''' SELECT time, name, amount FROM hop
					INNER JOIN hop_in_recipe ON
					hop.id = hop_in_recipe.hop_id
					WHERE hop_in_recipe.recipe_id =:recipe AND hop.use = "Boil"''', {"recipe": recipe}):
			hopAddition[0].append(row[0])
			hopAddition[1].append(row[1])
			hopAddition[2].append(row[2])
		return hopAddition 
