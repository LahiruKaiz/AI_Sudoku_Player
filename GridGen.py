import random
import numpy as np
import copy

class GridGenerate():
    
    def __init__(self):
        while True:  # Start an infinite loop to retry the process
            # Initialize a 9x9 grid with lists of possible numbers (1-9)
            self.MainGrid = [[[num for num in range(1, 10)] for _ in range(9)] for _ in range(9)]
            # Create a pool of numbers from 1 to 9, each number appearing 9 times
            self.NumPool = [num for _ in range(9) for num in range(1, 10)]

            # Start the grid generation process
            num = self.NumPool[0]  
            self.NumPool.pop(0)  

            # Randomly select a position in the grid to place the number
            i, j = random.randint(0, 8), random.randint(0, 8)

            # Place the number in the selected position and update the grid
            self.MainGrid[i][j] = num
            self._UpdateArray(self.MainGrid, i, j, num)

            try:
                # Continue filling the grid until the number pool is empty
                while len(self.NumPool) > 0:
                    # Check for cells that can only have one possibility
                    for x in range(9):
                        for y in range(9):
                            if isinstance(self.MainGrid[x][y], list) and len(self.MainGrid[x][y]) == 1:
                                num = self.MainGrid[x][y][0]  # Get the only possible number
                                self.MainGrid[x][y] = num  # Assign it to the grid
                                self._UpdateArray(self.MainGrid, x, y, num)  # Update the grid
                                self.NumPool.remove(num)  # Remove the number from the pool

                    # Check if the grid is complete
                    if self._CheckComplete():
                        raise StopIteration  # Exit the loop if complete
                    
                    num = self.NumPool[0]  # Get the next number from the pool
                    Positions = self._Eligible(num)  # Find eligible positions for this number

                    if not Positions:  # If there are no eligible positions, restart the process
                        break

                    # Find the positions with the least possibilities for the next number
                    MinimumPos = self._LeastPosi(Positions)
                    RandPos = random.choice(MinimumPos)  
                    i, j = RandPos  
                    self.MainGrid[i][j] = num  
                    self._UpdateArray(self.MainGrid, i, j, num)  
                    self.NumPool.pop(0) 

            except StopIteration:
                break  # Exit the infinite loop when the grid is complete
            
        
    
    def _CheckComplete(self):
        # Check if the grid is complete by ensuring all cells are filled
        for i in range(9):
            for j in range(9):
                if isinstance(self.MainGrid[i][j], list):
                    return False  # Found an empty cell
        return True  # All cells are filled
    
    def GridShow(self):
        # Display the grid in a 2D numpy array format
        a = np.zeros((9,9))
        
        for i in range(9):
            for j in range(9):
                if not isinstance(self.MainGrid[i][j], list):
                    a[i,j] = self.MainGrid[i][j]  # Fill the array with numbers
        
        print(a)  # Print the grid to the console
    
    def _LeastPosi(self, positions: list) -> list:
        # Find the positions with the least number of possibilities
        min_length = min(len(self.MainGrid[i][j]) for i, j in positions)
        
        # Return positions that have the minimum length of possibilities
        return [(i, j) for i, j in positions if len(self.MainGrid[i][j]) == min_length]
    
    def _Eligible(self, number: int) -> list:
        # Find all positions eligible for a specific number
        Positions = []
        
        for i in range(9):
            for j in range(9):
                if isinstance(self.MainGrid[i][j], list) and (number in self.MainGrid[i][j]):
                    Positions.append((i,j))  # Add position if the number is a possibility
        
        # Validate positions by checking if placing the number would keep the grid valid
        for pos in Positions:
            Dummy = copy.deepcopy(self.MainGrid)  # Create a copy of the grid
            x, y = pos  
            self._UpdateArray(Dummy, x, y, number)  
            if not self._GridCheck(Dummy):  # Check if the grid remains valid
                Positions.remove(pos)  # Remove invalid positions
                
        return Positions  # Return the list of valid positions
            
    def _GridCheck(self, array: list) -> bool:
        # Check if the grid is valid by verifying rows, columns, and subgrids
        # Check rows
        for i in range(9):
            if not self._check_units(array[i]):
                return False  # Invalid row

        # Check columns
        for j in range(9):
            column = [array[i][j] for i in range(9)]
            if not self._check_units(column):
                return False  # Invalid column

        # Check 3x3 subgrids
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = []
                for r in range(row, row + 3):
                    for c in range(col, col + 3):
                        subgrid.append(array[r][c])  # Collect elements of the subgrid
                if not self._check_units(subgrid):
                    return False  # Invalid subgrid

        return True  # The grid is valid

    def _check_units(self, unit: list) -> bool:
        # Check if a unit (row, column, or subgrid) contains valid numbers
        seen = set()  # Set to track seen numbers
        for item in unit:
            if isinstance(item, list):
                seen.update(item)  # Add possibilities to seen set
            else:
                if item in seen or item < 1 or item > 9:
                    return False  # Duplicate or out of range
                seen.add(item)  # Add the number to seen set

        expected_values = set(range(1, 10))  # Set of expected values (1-9)
        return expected_values.issubset(seen)  # Check if all expected values are present
                        
    def _UpdateArray(self, array: list, x: int, y: int, number: int):
        # Update the grid by removing the number from the corresponding row, column, and subgrid
        for item in array[x]:
            if isinstance(item, list) and (number in item):
                item.remove(number)  # Remove number from the possibilities
        
        for i in range(9):
            if isinstance(array[i][y], list) and (number in array[i][y]):
                array[i][y].remove(number)  # Remove number from the possibilities
                
        # Determine the starting indices of the 3x3 subgrid
        subgrid_row_start = (x // 3) * 3
        subgrid_col_start = (y // 3) * 3

        # Remove the number from the corresponding subgrid
        for row in range(subgrid_row_start, subgrid_row_start + 3):
            for col in range(subgrid_col_start, subgrid_col_start + 3):
                if isinstance(array[row][col], list) and (number in array[row][col]):
                    array[row][col].remove(number)  # Remove number from the possibilities

if __name__ == '__main__':
    pass