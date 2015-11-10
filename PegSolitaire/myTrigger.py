import argparse
import time
import search
import config
import pegSolitaireUtils
import readGame

tic = time.clock()
gameItrObject = pegSolitaireUtils.game('./original.txt')
#gameItrObject = pegSolitaireUtils.game('./game.txt')
search.ItrDeepSearch(gameItrObject)
search.aStarOne(gameItrObject)
search.aStarTwo(gameItrObject)
toc = time.clock()
toc = time.clock()
timeItr = toc - tic

print "Itr Deepening Search:"
print "Execution Time: " + str(timeItr)
print "Nodes Expanded: " + str(gameItrObject.nodesExpanded)
print "Trace: " + str(gameItrObject.trace)+ '\n'
	
