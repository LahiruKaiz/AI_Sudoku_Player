import random
import numpy as np
import copy

class GridGenerate():
    
    def __init__(self):
        
        self.MainGrid = [[[num for num in range(1,10)] for _ in range(9)] for _ in range(9)]
        self.NumPool = [num for _ in range(9) for num in range(1,10)]
        
        num = self.NumPool[0]
        self.NumPool.pop(0)
        
        i, j = random.randint(0,8), random.randint(0,8)
        
        self.MainGrid[i][j] = num
        
        self._UpdateArray(self.MainGrid, i, j, num)
        
        try:
            while len(self.NumPool) > 0:
                for x in range(9):
                    for y in range(9):
                        if isinstance(self.MainGrid[x][y], list) and len(self.MainGrid[x][y]) == 1:
                            num = self.MainGrid[x][y][0]
                            self.MainGrid[x][y] = num
                            self._UpdateArray(self.MainGrid, x, y, num)
                            self.NumPool.remove(num)
                
                if self._CheckComplete():
                    raise StopIteration
                
                self._GridShow()
                print(self.NumPool)
                num = self.NumPool[0]
                Positions = self._Eligible(num)
                MinimumPos = self._LeastPosi(Positions)
                RandPos = random.choice(MinimumPos)
                i, j = RandPos
                self.MainGrid[i][j] = num
                self._UpdateArray(self.MainGrid, i, j, num)
                self.NumPool.pop(0)
            
        except StopIteration:
            self._GridShow()
            
            
                        
        a = np.array(self.MainGrid)
        print(a)
    
    def _CheckComplete(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.MainGrid[i][j], list):
                    return False
        return True
    
    def _GridShow(self):
        a = np.zeros((9,9))
        
        for i in range(9):
            for j in range(9):
                if not isinstance(self.MainGrid[i][j], list):
                    a[i,j] = self.MainGrid[i][j]
        
        print(a)
    
    
    def _LeastPosi(self, positions):
        # Use a list comprehension to find the minimum length of possibilities
        min_length = min(len(self.MainGrid[i][j]) for i, j in positions)
        
        # Return positions with the minimum length
        return [(i, j) for i, j in positions if len(self.MainGrid[i][j]) == min_length]
    
    
    def _Eligible(self, number):
        
        Positions = []
        
        for i in range(9):
            for j in range(9):
                if isinstance(self.MainGrid[i][j], list) and (number in self.MainGrid[i][j]):
                    Positions.append((i,j))
        
        for pos in Positions:
            Dummy = copy.deepcopy(self.MainGrid)
            x, y = pos
            self._UpdateArray(Dummy, x, y, number)
            if not self._GridCheck(Dummy):
                Positions.remove(pos)
                
        return Positions
            
            
    def _GridCheck(self, array):
        # Check rows
        for i in range(9):
            if not self._check_units(array[i]):
                return False

        # Check columns
        for j in range(9):
            column = [array[i][j] for i in range(9)]
            if not self._check_units(column):
                return False

        # Check 3x3 subgrids
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = []
                for r in range(row, row + 3):
                    for c in range(col, col + 3):
                        subgrid.append(array[r][c])
                if not self._check_units(subgrid):
                    return False

        return True

    def _check_units(self, unit):
        seen = set()
        for item in unit:
            if isinstance(item, list):
                seen.update(item)
            else:
                if item in seen or item < 1 or item > 9:
                    return False  # Duplicate or out of range
                seen.add(item)

        expected_values = set(range(1, 10))
        return expected_values.issubset(seen)
                        
        
        
    def _UpdateArray(self, array, x, y, number):
        
        for item in array[x]:
            if isinstance(item, list) and (number in item):
                item.remove(number)
        
        for i in range(9):
            if isinstance(array[i][y], list) and (number in array[i][y]):
                array[i][y].remove(number)
                
        subgrid_row_start = (x // 3) * 3
        subgrid_col_start = (y // 3) * 3

        for row in range(subgrid_row_start, subgrid_row_start + 3):
            for col in range(subgrid_col_start, subgrid_col_start + 3):
                if isinstance(array[row][col], list) and (number in array[row][col]):
                    array[row][col].remove(number)
                    

            
if __name__ == '__main__':
    
    GridGenerate()