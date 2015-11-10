class Board:
    """ Initiating the board in the constructor"""

    def __block_check(self, cellrow, cellcol, value):
        """ """
        """TODO"""
        rowstart = cellrow/self.blockmaxrow
        colstart = cellcol/self.blockmaxcol

        rowstart = rowstart*self.blockmaxrow
        colstart = colstart*self.blockmaxcol

        for x in self.board[rowstart:rowstart + self.blockmaxrow]:
            self.consistent_check_count += 1
            if value in x[colstart:colstart + self.blockmaxcol]:
                return False
        return True

    def __row_check(self, cellrow, value):
        """ """
        self.consistent_check_count += 1
        if value in self.board[cellrow]:
            return False
        return True

    def __col_check(self, cellcol, value):
        """ """
        self.consistent_check_count += 1
    
        if value in [x[cellcol] for x in self.board]:
            return False
        return True

    def get_first_free(self):
    
       for x in self.board:
         for y in x:
            row = self.board.index(x)
            col = x.index(y)
            if self.board[row][col] is '-':
                return ((row,col))
       return (-1,-1)

    def get_all_free(self):
       freecoords = list()
       for row, x in enumerate(self.board):
         for col, y in enumerate(x):
            if self.board[row][col] is '-':
                freecoords.append((row,col))
       return freecoords
       
    def get_next_min_val(self):
       """ """
       coordinates = self.get_all_free()
       if len(coordinates) is 0:
           return (-1, -1)
       count = {}
      
       for cell in coordinates:
           for value in range(1, self.size + 1):
               if self.__row_check(cell[0], value) and \
                  self.__col_check(cell[1], value) and \
                  self.__block_check(cell[0], cell[1], value):
                      c = count.get(cell)
                      if c is None:
                          count[cell] = 1
                      else:
                          count[cell] = c + 1
       min_val = 10000
       min_cell = None
       for key in count:
           if count[key] < min_val:
               min_val = count[key]
               min_cell = key

       return min_cell

    def get_next_min_val_forward_check(self):
       """ """
       coordinates = self.get_all_free()
       if len(coordinates) is 0:
           return (-1, -1)
       count = {}
      
       for cell in coordinates:
           for value in range(1, self.size + 1):
               if self.__row_check(cell[0], value) and \
                  self.__col_check(cell[1], value) and \
                  self.__block_check(cell[0], cell[1], value):
                      c = count.get(cell)
                      if c is None:
                          count[cell] = 1
                      else:
                          count[cell] = c + 1
       min_val = 10000
       min_cell = None
       if len(count) != len(coordinates):
           return None
       for key in count:
           if count[key] < min_val:
               min_val = count[key]
               min_cell = key

       return min_cell


    def get_next_mrv_cp(self):

        mrv_cell = self.get_next_min_val()

        mrv_cell_values = []
        for value in range(1,self.size+1):
            if self.__row_check(mrv_cell[0],value) and \
               self.__col_check(mrv_cell[1],value) and \
               self.__block_check(mrv_cell[0],mrv_cell[1],value):
                   mrv_cell_values.append(value)

        row_accept_values = []

        for index_x, x in enumerate(self.board[mrv_cell[0]]):
            tmp = []
            if x is not '-':
                row_accept_values.append([x])
                continue
            for value in range(1,self.size+1):
                if self.__row_check(mrv_cell[0],value) and\
                   self.__col_check(mrv_cell[1],value) and \
                   self.__block_check(mrv_cell[0],mrv_cell[1],value):
                      tmp.append(value)
            row_accept_values.append([tmp])

        col_accept_values = []
        for index_x,x in enumerate(self.board):
            tmp = []
            if self.board[index_x][mrv_cell[1]] is not '-':
                col_accept_values.append([self.board[index_x][mrv_cell[1]]])
                continue

            for value in range(1,self.size+1):
                if self.__row_check(index_x,value) and\
                   self.__col_check(mrv_cell[1],value) and \
                   self.__block_check(index_x,mrv_cell[1],value):
                       tmp.append(value)
            col_accept_values.append([tmp])

        rowstart = mrv_cell[0]/self.blockmaxrow
        colstart = mrv_cell[1]/self.blockmaxcol

        rowstart = rowstart*self.blockmaxrow
        colstart = colstart*self.blockmaxcol

        block_accept_values = []
        for index_x,x in enumerate(self.board[rowstart:rowstart + self.blockmaxrow]):
            tmp = []            
            for index_y,y in enumerate(x[colstart:colstart + self.blockmaxcol]):
                if self.board[index_x][index_y] is not '-':
                   tmp.append(self.board[index_x][index_y])
                   break
                if self.__row_check(index_x,value) and\
                   self.__col_check(index_y,value) and \
                   self.__block_check(index_x,index_y,value):
                       tmp.append(value)
            block_accept_values.append([tmp])
        
        for row_values in row_accept_values:
            for value in mrv_cell_values:
                if value in row_values and len(row_values) is 1:
                    mrv_cell_values.remove(value)
                    break

        for col_values in col_accept_values:
            for value in mrv_cell_values:
                if value in col_values and len(col_values) is 1:
                    mrv_cell_values.remove(value)
                    break

        for block_values in block_accept_values:
            for value in mrv_cell_values:
                if value in block_values and len(block_values) is 1:
                    mrv_cell_values.remove(value)
                    break

        if len(mrv_cell_values) is 0:
            return None
        return (mrv_cell,mrv_cell_values)

    def check_free(self, cellrow, cellcol):
        """ """ 
        return self.board[cellrow][cellcol] == '-'

    def __check_bound(self, cellrow, cellcol):
        """ """
        return not (cellrow < 0 or cellcol < 0 or 
                     cellrow >= self.size or cellcol >= self.size)


    def __check_constraint(self, cellrow, cellcol, value):
        """ """
        return self.__check_bound(cellrow, cellcol) and \
               self.__row_check(cellrow, value) and     \
               self.__col_check(cellcol, value) and     \
               self.__block_check(cellrow, cellcol, value)

    def insert(self, row, col, val):
        """ """

        if self.__check_constraint(row, col, val):
            """update board"""
            self.board[row][col] = val
            return True
        return False

    def is_goal(self):

        for x in self.board:
            for y in x:
                if self.check_free(self.board.index(x), x.index(y)):
                    return False
        return True

    def fill_board(self):

        import copy
        new_board = copy.deepcopy(self.board)
        import random
        self.original_values = set()
        for index_x,row in enumerate(self.board):
            for index_y,cell in enumerate(row):
                if cell is '-':                    
                    new_board[index_x][index_y] = random.randint(1,self.size)
                else:
                    self.original_values.add((index_x,index_y))
        self.board = copy.deepcopy(new_board)

    def __count_block_check(self, cellrow, cellcol, value):
        """ """
        """TODO"""
        count = 0
        rowstart = cellrow/self.blockmaxrow
        colstart = cellcol/self.blockmaxcol

        rowstart = rowstart*self.blockmaxrow
        colstart = colstart*self.blockmaxcol

        for x in self.board[rowstart:rowstart + self.blockmaxrow]:
            self.consistent_check_count += 1
            count += x[colstart:colstart + self.blockmaxcol].count(value)

        return count 

    def __count_row_check(self, cellrow, value):
        """ """
        self.consistent_check_count += 1
        return self.board[cellrow].count(value) 

    def __count_col_check(self, cellcol, value):
        """ """
        self.consistent_check_count += 1
        return [x[cellcol] for x in self.board].count(value) 


    def get_next_min_conflict(self,row,col):

        conflict_map = {}
        for value in range(1,self.size + 1):

            temp = 0
            if self.board[row][col] == value:
                temp = -3
            conflict_map[value] = self.__count_row_check(row,value) +     \
                             self.__count_col_check(col,value) +     \
                             self.__count_block_check(row,col,value) + temp
        return_val = min(conflict_map,key=conflict_map.get)

        if len(set(conflict_map.values())) == 0:
            return -1
        return return_val

    def get_constraining_list(self):
        constraining_list = []

        for index_x, x in enumerate(self.board):
            for index_y, y in enumerate(x):
                value = self.board[index_x][index_y]
                if (index_x, index_y) in self.original_values:
                    continue
                self.board[index_x][index_y] = '-'

                if self.__row_check(index_x,value) is False or self.__col_check(index_y,value) is False or self.__block_check(index_x,index_y,value) is False:
                    constraining_list.append((index_x,index_y))

                self.board[index_x][index_y] = value
        return constraining_list    

    def is_min_conflict_goal(self):

        for i in range(0,self.size):
            for j in range(0,self.size):
                temp = self.board[i][j]                
                self.board[i][j] = '-'
                if self.__row_check(i,temp) is False or \
                   self.__col_check(j,temp) is False or \
                   self.__block_check(i,j,temp) is False:
                       self.board[i][j] = temp
                       return False
                self.board[i][j] = temp
        return True

    def get_next_cell_fn(self):
        return self.get_next_cell_function()

    def __init__(self, filename, mode):
        if filename is None:
            print "No file name passed"
            exit()
        self.board = list()
        fp = open(filename, "r")
        lines = fp.readlines()
        fp.close()
        vals = lines[0]
        vals = str(vals)
        vals = vals.partition(";") #
        vals = str(vals[0])
        vals = vals.split(",")
        vals = list(vals)
        self.size = int(vals[0])   
        self.blockmaxrow = int(vals[1])   #m rows in a block
        self.blockmaxcol = int(vals[2])   #k columns in a block
        self.consistent_check_count = 0
            
        for line in lines[1:]:
            vals = line.partition(";") #
            vals = vals[0]
            vals = vals.split(",") 
          
            for cell in vals:
                if cell is not '-':
                    vals[vals.index(cell)] = int(cell)
            
            self.board.append(vals)

        if mode is 'Backtracking':
            self.get_next_cell_function = self.get_first_free
        if mode is 'MRV':
            self.get_next_cell_function = self.get_next_min_val
        if mode is 'MRVFWD':
            self.get_next_cell_function = self.get_next_min_val_forward_check
        if mode is 'MRVCP':
            self.get_next_cell_function = self.get_next_mrv_cp
        if mode is 'MINCONFLICT':
            self.get_next_cell_function = self.get_next_min_conflict
