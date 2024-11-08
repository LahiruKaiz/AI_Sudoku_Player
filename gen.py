import numpy as np
import random

class Cell:
    
    def __init__(self, row, col):
        
        self.value = None
        self.x = row  
        self.y = col
        self.sub = (self.x // 3, self.y // 3) #Subgrid that the cell contains
        self.posibilities = [num for num in range(1,10)] #Posibilities of digits that can be put to the cell
        
    def setvalue(self, value):
        self.value = value
        self.posibilities = []
        
    def resetcell(self):
        self.posibilities = [num for num in range(1,10)]
        self.value = None
        
    def posi_length(self):
        return len(self.posibilities)
    
    def update(self, row, col, value):
        # Updating the postibilities
        if (self.x == row or self.y == col or self.sub == (row // 3, col // 3)) and (value in self.posibilities):
            self.posibilities.remove(value)
            

class gridGenerate():
    
    def __init__(self):
        
        self.pool = [num for _ in range(9) for num in range(1,10)]
        self.grid_array = [[0 for _ in range(9)] for _ in range(9)]
        
        try:
            while True:
                
                remain = self._GetRemain()
                
                if len(remain) == 0:
                    raise StopIteration
                
                Select_num = random.choice(remain)
                Eligible_Pos = self._Eligible(Select_num)
                Least_Pos = self._LeastPosibilties(Eligible_Pos)
                Filling_Pos = random.choice(Least_Pos)
                i, j = Filling_Pos
                self.grid_array[i][j] = Select_num
                self._CheckSinglePos()
                
                a = np.array(self.grid_array)
                print(a)
                
        except StopIteration:
            print("Grid generation is complete.")
            
            
    def _CheckSinglePos(self):
        ActiveGrid = []
        for x in range(9):
                for y in range(9):
                    ActiveGrid.append(Cell(x, y))
        
        self._UpdatingFromArray(ActiveGrid)
        
        for item in ActiveGrid:
            if len(item.posibilities) == 1:
                self.grid_array[item.x][item.y] = item.posibilities[0]
    
    
    def _LeastPosibilties(self, Positions):
        ActiveGrid = []
        for x in range(9):
                for y in range(9):
                    ActiveGrid.append(Cell(x, y))
                    
        map = {}
        for id, item in enumerate(ActiveGrid):
            map.update({(item.x, item.y): id})
                  
        self._UpdatingFromArray(ActiveGrid)
        
        Posibilties = []
        for pos in Positions:
            cell = ActiveGrid[map[pos]]
            Posibilties.append(len(cell.posibilities))
            
        Minimum = min(Posibilties)
        valid = []
        for id, value in enumerate(Posibilties):
            if value == Minimum:
                valid.append(Positions[id])
        
        return valid
    
    
    def _Eligible(self, number):
        Positions = []
        
        for i in range(len(self.grid_array)):
            for j in range(len(self.grid_array[i])):
                if self.grid_array[i][j] == 0:
                    Positions.append((i,j))
                    
        for pos in Positions:
            ActiveGrid = []
            
            for x in range(9):
                for y in range(9):
                    ActiveGrid.append(Cell(x, y))
       
            self._UpdatingFromArray(ActiveGrid)

            self._PositionUpdate(ActiveGrid, pos, number)

            if not self._GridCheck(ActiveGrid):
                Positions.remove(pos)
        
        return Positions
    
    
    def _PositionUpdate(self, grid, position, number):
        
        i,j = position
        for item in grid:
            if (item.x, item.y) == position:
                continue
            
            item.update(i, j, number)
            
            
    
    def _GridCheck(self, Grid):
        map = {}
        for id, item in enumerate(Grid):
            map.update({(item.x, item.y): id})
        
        ar = np.zeros((9,9), dtype=int)
        for i in Grid:
            if i.value != None:
                ar[i.x, i.y] = i.value
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
                    pos = Grid[map[cordinate]].posibilities.copy()
                    pool.extend(pos)
                
                pos = list(set(pool))

                for m in MissingValues:
                    if not m in pos:
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
                    pos = Grid[map[cordinate]].posibilities.copy()
                    pool.extend(pos)
                
                pos = list(set(pool))

                for m in MissingValues:
                    if not m in pos:
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
                        pos = Grid[map[cordinate]].posibilities.copy()
                        pool.extend(pos)
                    
                    pos = list(set(pool))

                    for m in MissingValues:
                        if not m in pos:
                            return False
        
        return True
    
    
    def _UpdatingFromArray(self, grid):
        map = {}
        for id, item in enumerate(grid):
            map.update({(item.x, item.y): id})
        
        for i in range(len(self.grid_array)):
            for j in range(len(self.grid_array[i])):
                if self.grid_array[i][j] != 0:
                    pos = grid[map[(i,j)]]
                    pos.setvalue(self.grid_array[i][j])
                    self._PositionUpdate(grid= grid, position=(i,j), number=self.grid_array[i][j])

                    # if not self._GridCheck(grid):
                    #     print("Error while updating from main array")
                        
    
    
    def _GetRemain(self):
        
        ls = self.pool.copy()
        
        for raws in self.grid_array:
            for item in raws:
                if item != 0:
                    ls.remove(item)
                    
        return ls
            
            
if __name__ == '__main__':
    
    g = gridGenerate()