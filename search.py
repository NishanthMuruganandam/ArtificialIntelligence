import pegSolitaireUtils
import config
import copy

def ItrDeepSearch(pegSolitaireObject):
""" This function is the entry point for Iterative Deepening Search algorithm. It calls a recursive function ITRDeepSearch(arg1,arg2,depthLimit) 
which is found below, for every value of depthLimit starting from 0 to NumberOfPegs. 
The upperLimit for depth is chosen as NumberOfPegs on the board as the that is the maximum number of moves one can make in any configuration
of the board."""

	#print ("Number of Pegs : " + str(pegSolitaireObject.numberOfPegs))	
	pegSolitaireObject.displayState()#This is for debugging purposes. It writes the state to a file.
		#startState = pegSolitaireObject #Do a deep copy. Assure this statement does that. 
		# That stmt doesnt do that. 
	for depth in range(pegSolitaireObject.numberOfPegs):
		#print ("Iteration : " + str(depth))
		#f = open('myOutput.txt','a')
		#f.write("Iteration "+ str(depth) + "\n");
		#f.close()
		pegSolitaireObject.gameState = copy.deepcopy(pegSolitaireObject.startState)#Every iteration, we have to start from the root as per 
		# definition of the Iterative Deepening Algorithm. So, an attribute is added to the pegSolitaireObject which acts as a restore point.
		pegSolitaireObject.trace = []
		if itrDeepSearch(pegSolitaireObject,0,depth):
			return True
	pegSolitaireObject.trace = []
	print ("No possible moves")
	return False

def itrDeepSearch(pegSolitaireObject,i,depthLimit):
	
	if i == depthLimit:#If the depth limit is reached, we abort the recursion.		
		return pegSolitaireObject.isGoalState() 
	if pegSolitaireObject.isGoalState():#If goal is found, we abort the recursion.
		return True
	pegSolitaireObject.displayState()#Debugging purposes.
	if i < depthLimit:
		#Iteration is over every position in the board.
		for x in range(7):
			for y in range(7):
				#print ("Processing " + str(x) +"  " +  str(y))
				#If the position is an invalid place(corner) or unoccupied, we ignore it.
				if pegSolitaireObject.gameState[x][y] in [-1,0]:
					continue
				oldState = copy.deepcopy(pegSolitaireObject.gameState)#the state is saved to act as a restore point. 
				for key in config.DIRECTION:#For every possible direction, we explore the tree
					if not pegSolitaireObject.is_validMove((x,y),key):#If it is not a valid move, we prune that path. 
						continue
					pegSolitaireObject.getNextState((x,y),key) #This is where the next node is created exactly.
					if itrDeepSearch(pegSolitaireObject,i+1,depthLimit): #Start of recursion.
						transition = [(x,y),pegSolitaireObject.getNextPosition((x,y),key)]#getNextPosition() is a method
						# in class 'game' which returns the destination coordinates on moving in direction 'key' from (x,y).
						pegSolitaireObject.trace.insert(0,transition[1])
						pegSolitaireObject.trace.insert(0,transition[0])
						return True #If one state is found, it is returned as the goal state.
					pegSolitaireObject.gameState = copy.deepcopy(oldState) #If the explored subtree doesn't lead to a goal, we 
					#restore the saved state and try another direction from that state. 
	return False

								
def aStarOne(pegSolitaireObject):

	if pegSolitaireObject.isGoalState():
		return True
	
	fringeList = heuristicOne(pegSolitaireObject)
	oldState = copy.deepcopy(pegSolitaireObject.gameState)#The old state is retained to backtract if explored branch doesn't lead to goal state.
	
	for step in fringeList:
		for key in config.DIRECTION:
			#print ("Going in direction : " + str(key))
			if not pegSolitaireObject.is_validMove(step,key):
				#print("Validity test failed")
				continue
			pegSolitaireObject.getNextState(step,key)
			if aStarOne(pegSolitaireObject):
				transition = [step,pegSolitaireObject.getNextPosition(step,key)]
				pegSolitaireObject.trace.insert(0,transition[1])
				pegSolitaireObject.trace.insert(0,transition[0])
				return True
			pegSolitaireObject.gameState = copy.deepcopy(oldState)	
	
	return False	


def heuristicOne(pegSolitaireObject):
"""
Heuristic one: For every peg in board, compute the Manhattan Distance from the centre(3,3) and order by the farthest first.
The intuition behind: The ones that are far from centre, have the objective of moving to centre. If we try to eliminate the farthest
one with the one closer to it, we isolate a peg and eventually it might to a state where that peg can never be reached by any move of the other pegs.
So, the best bet is to clear off the ones in the far and move inwards towards the goal rather than going the opposite way.

Admissibility: h(n) is nothing but the measure of number of moves of the relaxed version of the problem - a peg can move to a tile next to it, if empty. So, h(n) will always be lesser than the actual cost h*(n).

Consistency: h(n) just finds the measure of the relaxed problem. Any c(n1) >> h(n), so the condition c(n1) + h(n1) >> h(n) which makes the heuristic a consistent one
""" 
	dictionary={}
	for x in range(7):
		for y in range(7):
			if pegSolitaireObject.gameState[x][y] in [-1,0]:
				continue
			dictionary[(x,y)] = pegSolitaireObject.distFromCentre((x,y))
	values = sorted(dictionary,key=lambda key:dictionary[key],reverse=True)
	return values

def aStarTwo(pegSolitaireObject):
""" Implementation idea is very much similar to aStarOne()"""

	if pegSolitaireObject.isGoalState():
		#print("goal state found")
		pegSolitaireObject.displayState();
		return True

	fringeList = heuristicTwo(pegSolitaireObject)
	oldState = copy.deepcopy(pegSolitaireObject.gameState)
		
	for step in fringeList:
		for key in config.DIRECTION:
			#print ("Going in direction : " + str(key))
			if not pegSolitaireObject.is_validMove(step,key):
				#print("Validity test failed")
				continue
			pegSolitaireObject.getNextState(step,key)
			if aStarTwo(pegSolitaireObject):
				transition = [step,pegSolitaireObject.getNextPosition(step,key)]
				pegSolitaireObject.trace.insert(0,transition[1])
				pegSolitaireObject.trace.insert(0,transition[0])
				return True
			pegSolitaireObject.gameState = copy.deepcopy(oldState)	
	return False

def heuristicTwo(pegSolitaireObject):
"""
Heuristic Two: For every peg, the number of possible moves it can take is calculated(Max is 4 for any peg). The one with the higher value is explored first compared to others. If there is a tie, the one farther is chosen.

Intuition behind the heuristic: It is more of a probabilistic determination. Assume that two pegs have 3 and 2 possible moves each. Without considering any other extra parameters, the probability of reaching the goal using the one with '3' possible moves is more compared to the other. So, this heuristic takes a calculated risk by exploring that node.

Admissibility: h(n) takes into only the account the number of moves available. But, the original cost function takes into account the actual move cost which 1 in each step. So, the original cost function from n will be greater than h(n) which can never cross 4. For every increase in h(n), the h*(n) will increase since the increase in h(n) indirectly means that there are more pegs to be removed thus increasing the actual cost. 

Consistency: The actual cost of moving from one state to the immediate next one is 1. The maximum value	of h(n) = h(n1) = 4. So, h(N) is always less than sum of both h(n1) and c(n1).

"""
	dictionary={}
	for x in range(7):
		for y in range(7):
			if pegSolitaireObject.gameState[x][y] in [-1,0]:
				continue
			dictionary[(x,y)] = pegSolitaireObject.countPossibleMoves((x,y))
	values = sorted(dictionary,key=lambda key:dictionary[key],reverse=True)
	return values

