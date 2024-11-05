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
        
        for _ in range(9):
            for num in range(1,10):
                self._ShowGrid()
                MinPos, Indx = self._leastPosi(num)
                check = False
                if MinPos == 9:
                    
                    while not check:
                        ranCell = random.choice(self.grid)
                        if num in ranCell.posibilities:
                            check = True
                            ranCell.setvalue(num)
                            self._updateGrid(ranCell)
                
                else:
                    
                    while not check:
                        ranCell = self.grid[random.choice(Indx)]
                        if num in ranCell.posibilities:
                            check = True
                            ranCell.setvalue(num)
                            self._updateGrid(ranCell)
                    
        
    
    def _leastPosi(self, value):
        leastpos = []
        for cell in self.grid:
            if cell.posi_length() == 1 or (not value in cell.posibilities):
                leastpos.append(10)
                
            else:
                leastpos.append(cell.posi_length())
                
            if (cell.setCheck == False) and cell.posi_length() == 1:
                self._updateGrid(cell)
                cell.setCheck = True
        
        
        Minimum  = min(leastpos)
        
        idx = []
        for id, item in enumerate(leastpos):
            if item == Minimum:
                idx.append(id)
                
        return Minimum, idx
    
    
    def _updateGrid(self, item):
        print(f"Item : ({item.x},{item.y}) value: {item.posibilities[0]}")
        for i in self.grid:
            if i != item and i.posi_length() > 1:
                # print(i.x, i.y, i.posibilities)
                i.update(item.x, item.y, item.posibilities[0])
                # print( i.posibilities)
                
                
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
    
    Gen = gridGenerate()
    Gen._ShowGrid()
    