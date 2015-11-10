import board
from random import randint
###########################################
# you need to implement five funcitons here
###########################################

WINNING_BOARD = None
def backtracking_helper(board):
    """ Does the DFS and checks constraints while doing that"""

    if board.is_goal():
        global WINNING_BOARD
        import copy
        WINNING_BOARD = copy.deepcopy(board)
        return True

    import copy
    old_board = copy.deepcopy(board)
    cordinates = board.get_next_cell_fn()

    if cordinates is None:
        return False

    for value in range(1,board.size+1):
        
        if board.insert(cordinates[0],cordinates[1],value):
            if backtracking_helper(board):
                return True
        board = copy.deepcopy(old_board)

    return False

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board_obj = board.Board(filename, 'Backtracking')
    if backtracking_helper(board_obj):
        print "Backtracking succeeded:"
    global WINNING_BOARD 
    return (WINNING_BOARD.board, WINNING_BOARD.consistent_check_count)

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board_obj = board.Board(filename, 'MRV')
    if backtracking_helper(board_obj):
        print 'success MRV'
    global WINNING_BOARD 
    return (WINNING_BOARD.board, WINNING_BOARD.consistent_check_count)

def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board_obj = board.Board(filename, 'MRVFWD')
    global WINNING_BOARD
    if backtracking_helper(board_obj):
        print 'success MRV FWD'
    return (WINNING_BOARD.board, WINNING_BOARD.consistent_check_count)

def backtracking_mrv_cp_helper(board):
    """ Does the DFS and checks constraints while doing that"""
    if board.is_goal():
        global WINNING_BOARD
        import copy
        WINNING_BOARD = copy.deepcopy(board)
        return True
    import copy
    old_board = copy.deepcopy(board)
    result = board.get_next_cell_fn()

    if result is None:
        return False

    for value in result[1]:
        
        if board.insert(result[0][0],result[0][1],value):
            if backtracking_mrv_cp_helper(board):
                return True
        board = copy.deepcopy(old_board)

    return False

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board_obj = board.Board(filename, 'MRVCP')
    global WINNING_BOARD
    WINNING_BOARD = None
    if backtracking_mrv_cp_helper(board_obj):
        print 'success MRVCP'
    
    return (WINNING_BOARD.board, WINNING_BOARD.consistent_check_count)

def pick_random_cell(constraining_list):
    centry = randint(0,len(constraining_list) - 1)
    return constraining_list[centry]

def min_conflict_helper(board,step=100):

    for i in range(step):

        if board.is_min_conflict_goal():
            global WINNING_BOARD
            import copy
            WINNING_BOARD = copy.deepcopy(board)
            return True
        constraining_list = []
        constraining_list = board.get_constraining_list()
        #coords = constraining_list[len(constraining_list)/2]# pick_random_cell(constraining_list)
        for coords in constraining_list:
            temp = board.get_next_min_conflict(coords[0],coords[1])
            board.board[coords[0]][coords[1]] = temp
    print 'Failed board : ' +str(board.board)

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board_obj = board.Board(filename, 'MRVCP')
    global WINNING_BOARD
    WINNING_BOARD = None

    board_obj.fill_board()
    min_conflict_helper(board_obj,100000)
    
    if WINNING_BOARD is None:
        print 'Min conflict failed! Try again probably with a bigger step count'
        return ([[]],0)
    else:    
        print('Success MINCONFLICT')

    return (WINNING_BOARD.board, WINNING_BOARD.consistent_check_count)
