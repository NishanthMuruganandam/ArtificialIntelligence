import readGame
import config
#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
	def __init__(self, filePath):
        	self.gameState = readGame.readGameState(filePath)
		self.startState = readGame.readGameState(filePath)
		self.numberOfPegs = self.computeNumberOfPegs()
                self.nodesExpanded = 0
		self.trace = []	
	
	def computeNumberOfPegs(self):
		n = 0
		for row in self.gameState:
			for value in row:
				if value == 1:
					n+=1
		return n

	def is_corner(self, pos):
		########################################
		# You have to make changes from here
		# check for if the new positon is a corner or not
		# return true if the position is a corner
				
		return (self.gameState[pos[0]][pos[1]] == -1) 
		
	def alreadyOccupied(self,pos):
		return self.gameState[pos[0]][pos[1]] == 1
	
	def outsideBoard(self,pos):
		return ((pos[0] < 0) or (pos[1]<0) or (pos[0]>6) or (pos[1]>6))
	def getNextPosition(self, oldPos, direction):
		#########################################
		# YOU HAVE TO MAKE CHANGES HERE
		# See DIRECTION dictionary in config.py and add
		# this to oldPos to get new position of the peg if moved
		# in given direction , you can remove next line
		newX = 2*config.DIRECTION[direction][0] + oldPos[0]
		newY = 2*config.DIRECTION[direction][1] + oldPos[1]
		newPos  = (newX,newY)
		return newPos
	
	def getMiddlePeg(self,oldPos,newPos):
		""" gets the index of the position between old position and new position"""
		middlePos = ((oldPos[0]+newPos[0])/2,(oldPos[1]+newPos[1])/2)
		return middlePos
	
	def pegBetweenIt(self,oldPos,newPos):
		""" Checks if there is a peg between two positions"""
		#print ("Checking for middle")
		middlePos = self.getMiddlePeg(oldPos,newPos)
		if self.gameState[middlePos[0]][middlePos[1]] != 1:
			return False
		#print ("Middle Test success")
		return True
	
	def is_validMove(self, oldPos, direction):
		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		newPos = self.getNextPosition(oldPos, direction)
		#print ("OLD POS : " + str(oldPos) + " New Pos: " + str(newPos))
		if self.outsideBoard(newPos):
			#print("outside board")
			return False
		if self.is_corner(newPos):
			#print ("It is a corner")
			return False	
		#########################################
		
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		# or new move is outside peg Board
		# Remove next line according to your convenience
		if self.alreadyOccupied(newPos):
			#print ("Already Occupied")
			return False
		return self.pegBetweenIt(oldPos,newPos)
	
	def getNextState(self, oldPos, direction):
		###############################################
		# DONT Change Things in here
		self.nodesExpanded += 1
		if not self.is_validMove(oldPos, direction):
			print "Error, You are not checking for valid move"
			exit(0)
		###############################################
		
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1
		#print ("Updating the state!!!")
		newPos = self.getNextPosition(oldPos,direction)
	        self.gameState[newPos[0]][newPos[1]] = 1
		self.gameState[oldPos[0]][oldPos[1]] = 0	
		middlePos = self.getMiddlePeg(oldPos,newPos)
		self.gameState[middlePos[0]][middlePos[1]] = 0
		#print ("OLD POS : " + str(oldPos) + " New Pos: " + str(newPos))
		return self.gameState	
	
	def isGoalState(self):
		pegInCenter = False
		if self.gameState[3][3] == 1:
			pegInCenter = True
		onlyOnePeg = True
		for x in range(7):
			for y in range(7):
				if x == 3 and y == 3:
					continue
				if self.gameState[x][y] == 1:
					onlyOnePeg = False
					break;
		return pegInCenter and onlyOnePeg

	def distFromCentre(self,pos):
	 	distance = abs(pos[0]-3)+abs(pos[1]-3)
		return distance

	def countPossibleMoves(self,pos):	
		count = 0
		for key in config.DIRECTION:
			if self.is_validMove(pos,key):
				count+=1		
		return count 
		
	def displayState(self):

		f = open('myOutput.txt','a')
		f.write ("The game state is :\n")
		for row in self.gameState:
			f.write(str(row))
			f.write("\n")
		f.close()
