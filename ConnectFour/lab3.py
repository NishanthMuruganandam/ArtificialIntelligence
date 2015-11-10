######################################
#FirstName #  LastName	 #Student ID #
######################################
#Basavaraj #  Kaladagi 	 # 110562162 #
#Nishanth  # Muruganandam# 110276247 #
######################################

from util import INFINITY



from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player1, human_player)
#run_game(new_player, human_player)
#run_game(human_player,new_player)
#run_game(new_player,new_player)
## Or watch the computer play against itself:
#run_game(basic_player, basic_player)
## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
#quick_to_win_player = lambda board: minimax(board, depth=4,
#                                            eval_fn=focused_evaluate)


def alpha_beta_search_helper(board,depth,level,eval_fn,get_next_moves_fn,is_terminal_fn,alpha,beta):

	""" 
	Actual implementation of Alpha-Beta pruning search. It returns the score of the move to the alpha_beta_search(..) which acts as a 
	wrapper which returns the desired index to the actual caller.
	It inverts the score accordingly to maintain the consistency of the search algorithm.
	Pruning is done if alpha greater than or equal to beta.	
	"""

	#print('Alpha: ' +str(alpha) + ' Beta: ' + str(beta) + 'level:' + str(level))
#	raw_input('waiting')
	if alpha >= beta:
		return None

	if is_terminal_fn(depth,board):
		if board.is_game_over():
			if level is "MIN":
				return 1000
			else:
				return -1000
		score = eval_fn(board)
		return score

	nextLevel = "MIN" if level == "MAX" else "MAX"
	scores = []
	alpha_beta_search_helper.nodesExpanded += 1

	for i in range(7):
		try:
			newBoard = board.do_move(i)
			score = alpha_beta_search_helper(newBoard,depth-1,nextLevel,eval_fn,get_next_moves_fn,is_terminal_fn,alpha,beta)
			#print ('score' + str(score))
			if score is None:
				#print "PRUNED MACHI"
				#print ('level is' + str(level))
				break
			elif level is "MAX" and score > alpha:
				#print ('setting alpha' + str(level))
				alpha = score
			elif level is "MIN" and score < beta:
				#print ('setting beta' + str(level))
				beta = score
			#print('Appending score: ' + str(score))
			#raw_input('Waiting')
			scores.append(score)
		except Exception:#TODO: Make it InvalidMoveException!!
			scores.append("ERROR")

	if level == "MAX":
		max = -sys.maxint-1
		for i in range(len(scores)):
			if scores[i] is "ERROR" :
				continue
			if max < scores[i]:
				max = scores[i]
		#print ('Level is ' + str(level) + 'returngin ' + str(max))
		return max
	else:
		min = sys.maxint
		for i in range(len(scores)):
			if scores[i] is "ERROR":
				continue
			if min > scores[i]:
				min = scores[i]
		#print ('Level is ' + str(level) + 'returngin ' + str(min))
		return min


alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=basic_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    """ Entry point for Alpha Beta Search. """

    import time
    start = time.time()
    moves = [move for move,newBoard in get_all_next_moves(board)]
    scores = {}
    
    alpha = -sys.maxint - 1
    beta = sys.maxint
    for move in moves:
        newBoard = board.do_move(move)
	score = (alpha_beta_search_helper(newBoard,depth-1,'MIN',eval_fn,get_next_moves_fn,is_terminal_fn,alpha,sys.maxint))
	if score > alpha:
		alpha = score
        scores[move] = score
    from operator import itemgetter
    alpha_beta_search.time += (time.time() - start)
    return max(scores.iteritems(),key=itemgetter(1))[0]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)



minimax.time = 0.0
minimaxHelper.nodesExpanded = 0
alpha_beta_search.time = 0.0
alpha_beta_search_helper.nodesExpanded = 0

run_game(basic_player,human_player,gameToken=True)


#run_game(alphabeta_player,human_player)
#run_game(basic_player,human_player)
#run_game(alphabeta_player,basic_player)
#run_game(new_player,human_player)
#run_game(basic_player,new_player)
#run_game(alphabeta_player,new_player)

if minimaxHelper.nodesExpanded != 0:
	print ('Nodes expanded for Minimax : ' + str(minimaxHelper.nodesExpanded))

if minimax.time != 0.0:
	print ('Total Execution time for Minimax : ' + str(minimax.time))

if alpha_beta_search_helper.nodesExpanded != 0:
	print ('Nodes expanded for AlphaBeta search : ' + str(alpha_beta_search_helper.nodesExpanded))

if alpha_beta_search.time != 0.0:
	print ('Total Execution time for AlphaBeta search : ' + str(alpha_beta_search.time))
#if totalExecutionTimeAlpha != 0.0:
#	print('Total Execution Time for AlphaBeta is ' + str(totalExecutionTimeAlpha))

#if numberOfNodesExpandedAlphaBeta != 0:
#	print('Total Nodes expanded for AlphaBeta is ' + str(numberOfNodesExpandedAlphaBeta))




## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
#ab_iterative_player = lambda board: \
 #   run_search_function(board,
  #                      search_fn=alpha_beta_search,
   #                     eval_fn=focused_evaluate, timeout=5)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
 #   print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
  #  print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
#your_player = lambda board: run_search_function(board,
 #                                               search_fn=alpha_beta_search,
  #                                              eval_fn=better_evaluate,
   #                                             timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
