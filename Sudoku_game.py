import numpy as np
import random 

class Cell:
    
    def __init__(self, row, col):
        
        self.x = row  
        self.y = col
        self.sub = (self.x // 3, self.y // 3) #Subgrid that the cell contains
        self.posibilities = [num for num in range(1,10)] #Posibilities of digits that can be put to the cell
        self.setCheck = False
        
    def setvalue(self, value):
        self.posibilities = [value]
        
    def resetcell(self):
        self.posibilities = [num for num in range(1,10)]
        
    def posi_length(self):
        return len(self.posibilities)
    
    def update(self, row, col, value):
        # Updating the postibilities
        if (self.x == row or self.y == col or self.sub == (row // 3, col // 3)) and (value in self.posibilities):
            self.posibilities.remove(value)
            

class gridGenerate:
    
    def __init__(self):
        
        self.grid = [Cell(i, j) for i in range(9) for j in range(9)]
        cor = [(i, j) for i in range(9) for j in range(9)]
        self.map = {tup : id for id, tup in enumerate(cor)}
        
        
        for _ in range(9):
            for num in range(1,10):
                self._ShowGrid()
                print('updating number',num)
                Indx = self._eligibale(num)
                
                Indx = self._leastPos(Indx)
                print("random selction range",Indx)
                
                ranCell = self.grid[random.choice(Indx)]
                if num in ranCell.posibilities:
                    ranCell.setvalue(num)
                    ranCell.setCheck = True
                    self._updateGrid(ranCell)      
                
                # for cell in self.grid:
                #     if (cell.setCheck == False) and cell.posi_length() == 1:
                #         self._updateGrid(cell)
                #         cell.setCheck = True
                        
                    
    def _leastPos(self, idx):
        pos = []
        for i in idx:
            cell = self.grid[i]
            pos.append(cell.posi_length())
        
        Minimum = min(pos)
        valid = []
        for id, value in enumerate(pos):
            if value == Minimum:
                valid.append(idx[id])
        
        return valid
                        
        
    
    def _eligibale(self, value):
        dummyGrid = []
        idx = []
        for cell in self.grid:
            if cell.posi_length() > 1 and (value in cell.posibilities):
                dummyGrid.extend(self._Copygrid())
                
                
                # a1= []
                # for i1 in dummyGrid:
                #     a1.append(i1.posi_length())
                    
                # print('Ori',a1)
                
                
                # a= []
                # for i in dummyGrid:
                #     print(i.posibilities)
                    # a.append(i.posi_length())
                    
                # print('dummy',a)
                
                dummyCell = dummyGrid[self.map[(cell.x, cell.y)]]
                dummyCell.setvalue(value)
                self._updateDummyGrid(dummyCell, dummyGrid)
                # for cell1 in dummyGrid:
                #     if (cell1.setCheck == False) and cell1.posi_length() == 1:
                #         self._updateDummyGrid(cell1, dummyGrid)
                #         cell1.setCheck = True
                
                if self._checker(dummyGrid):
                    idx.append(self.grid.index(cell))
        return idx
        
                
    def _Copygrid(self):
        dummy = [Cell(i, j) for i in range(9) for j in range(9)]
        for cell in self.grid:
            dummyCell = dummy[self.map[(cell.x, cell.y)]]
            dummyCell.posibilities = cell.posibilities.copy()
            dummyCell.setCheck = cell.setCheck
            
        return dummy
    
    
    def _checker(self, grid):
        ar = np.zeros((9,9), dtype=int)
        for i in grid:
            if i.posi_length() == 1:
                ar[i.x, i.y] = i.posibilities[0]
        for r in range(9):
            row = ar[r, :]
            idx1 = np.where(row == 0)
            if len(idx1[0]) != 0:
                row = list(set(row.tolist()))
                row = row[1:]
                    
                MissingValues = list(set([1,2,3,4,5,6,7,8,9]) - set(row))
                
                pool = []
                
                for i in idx1[0]:
                    cordinate = (r, i)
                    pos = grid[self.map[cordinate]].posibilities
                    print(cordinate, pos)
                    pool.extend(pos)
                
                pos = list(set(pool))

                for m in MissingValues:
                    if not m in pos:
                        print('missing valuse', MissingValues)
                        print('posibility pool', pos)
                        print('raw check fail', r)
                        self._showDummy(grid=grid)
                        return False
                        
                        
        for c in range(9):
            col = ar[:, c]
            idx2 = np.where(col == 0)
            if len(idx2[0]) != 0:
                col = list(set(col.tolist()))
                col = col[1:]
                    
                MissingValues = list(set([1,2,3,4,5,6,7,8,9]) - set(col))
                
                pool = []
                for i in idx2[0]:
                    cordinate = (r, i)
                    pos = grid[self.map[cordinate]].posibilities
                    pool.extend(pos)
                
                pos = list(set(pool))

                for m in MissingValues:
                    if not m in pos:
                        print('missing valuse', MissingValues)
                        print('posibility pool', pos)
                        print('column check fail', c)
                        self._showDummy(grid=grid)
                        return False
        
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = ar[row:row+3, col:col+3].flatten()
                idx3 = np.where(subgrid == 0)
                if len(idx3[0]) != 0:
                    subgrid = list(set(subgrid.tolist()))
                    subgrid = subgrid[1:]
                        
                    MissingValues = list(set([1,2,3,4,5,6,7,8,9]) - set(subgrid))
                    
                    pool = []
                    for i in idx3[0]:
                        cordinate = (r, i)
                        pos = grid[self.map[cordinate]].posibilities
                        pool.extend(pos)
                    
                    pos = list(set(pool))

                    for m in MissingValues:
                        if not m in pos:
                            print('missing valuse', MissingValues)
                            print('posibility pool', pos)
                            print('subgrid checck fail', row, col)
                            self._showDummy(grid=grid)
                            return False
        
        return True
                    
                
            
        
    
    
    def _updateGrid(self, item):
        # print(f"Item : ({item.x},{item.y}) value: {item.posibilities[0]}")
        for i in self.grid:
            if i != item and i.posi_length() > 1:
                # print(i.x, i.y, i.posibilities)
                i.update(item.x, item.y, item.posibilities[0])
                # print( i.posibilities)
                
                
    def _updateDummyGrid(self, item, grid):
        # print(f"Item : ({item.x},{item.y}) value: {item.posibilities[0]}")
        for i in grid:
            if i != item and i.posi_length() > 1:
                # print(i.x, i.y, i.posibilities)
                i.update(item.x, item.y, item.posibilities[0])
                # print( i.posibilities)
                
        for cell in grid:
            if (cell.setCheck == False) and cell.posi_length() == 1:
                self._updateGrid(cell)
                cell.setCheck = True
                
    def _ShowGrid(self):
        ar = np.zeros((9,9), dtype=int)
        for i in self.grid:
            if i.posi_length() == 1:
                ar[i.x, i.y] = i.posibilities[0]
                
        print(ar)
        # if self._is_valid_sudoku(ar) == True:
        #     print('Correct', ar)
            
        # else:
        #     print("Wrong", ar)
        
    def _showDummy(self, grid):
        ar = np.zeros((9,9), dtype=int)
        for i in grid:
            if i.posi_length() == 1:
                ar[i.x, i.y] = i.posibilities[0]
                
        print(ar)
        
    def is_valid_sudoku(self, sudoku):
        # Check rows and columns
        for i in range(9):
            if len(set(sudoku[i, :])) != 9 or len(set(sudoku[:, i])) != 9:
                return False
        
        # Check 3x3 subgrids
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = sudoku[row:row+3, col:col+3].flatten()
                if len(set(subgrid)) != 9:
                    return False
                    
        return True
        

if __name__ == "__main__":
    
    gen = gridGenerate()
    