import pygame
import random
import copy
from GridGen import GridGenerate

pygame.init()
font = pygame.font.SysFont('arial', 35)
font1 = pygame.font.SysFont('arial', 30)
font2 = pygame.font.SysFont('arial', 42)


class SudokuAI:
    
    def __init__(self):
        self.display = pygame.display.set_mode((500, 500))
        self.display.fill((255, 255, 255))
        pygame.display.set_caption('Sudoku')
        self.reset()
        
    
    def reset(self):
        GridGen = GridGenerate()
        self.Solved_grid = GridGen.MainGrid
        self.sudoku_grid, self.Empty = self._PrepGrid()
        self.filling_space = [[0 for _ in range(9)] for _ in range(9)]
        self.game_over = False
        self.completed = 0
        self.attempts = 0
        self.UiUpdate()
    
    
    def DrawLines(self):
        
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.display, (0,0,0), (25 + i*50, 25), (25 + i*50, 475), 3)
                pygame.draw.line(self.display, (0,0,0), (25, 25 + i*50), (475, 25 + i*50), 3)
                
            else:
                pygame.draw.line(self.display, (0,0,0), (25 + i*50, 25), (25 + i*50, 475), 1)
                pygame.draw.line(self.display, (0,0,0), (25, 25 + i*50), (475, 25 + i*50), 1)

        
        
    def DrawPreoccupiedBoxes(self):
        Preoccupied = [(i, j) for i in range(9) for j in range(9) if not (i, j) in self.Empty]
        
        for x, y in Preoccupied:
            pygame.draw.rect(self.display, (145, 144, 140), pygame.Rect((25 + x*50,25 + y*50),(50,50)))
            num = font.render(str(self.sudoku_grid[x][y]), True, (0,0,0))
            self.display.blit(num, (42 + x*50,30 + y*50))
                
        
    
    def _PrepGrid(self):
        Number_of_empty_cells = 37
        Positions = [(i, j) for i in range(9) for j in range(9)]
        
        Random_Positions = random.sample(Positions, Number_of_empty_cells)
        grid = copy.deepcopy(self.Solved_grid)
        
        for x, y in Random_Positions:
            grid[x][y] = 0
            
        return grid, Random_Positions
    
    
    def is_fill_pos(self, position):
        x, y = position
        if (x,y) in self.Empty:
                return True
            
        return False
    
    
#     def is_button_pos(self, position):
#         x, y = position
#         if x > 5 and x < 495 and y > 525 and y < 575:
#             return True
            
#         return False
    

    
    def UiUpdate(self):
        self.display.fill((255, 255, 255))
        self.DrawPreoccupiedBoxes()
        self.DrawDucplicateBoxes()
        self.DrawLines()
        self.DrawFillSpace()
        
        if self.game_over == True:
            pygame.draw.rect(self.display, (0,0,0), pygame.Rect((100,225),(300,75)))
            num = font2.render("Sudoku Completed", True, (225,225,225))
            self.display.blit(num, (105, 233))
        
        pygame.display.update()
        
        
    def update_filling_space(self, position, number):
        x, y = position
        if number in range(1,10):
            self.filling_space[x][y] = number
            
    
    def DrawFillSpace(self):
        for pos in self.Empty:
            x, y = pos
            if self.filling_space[x][y] == 0:
                continue
            
            else:
                num = font.render(str(self.filling_space[x][y]), True, (0,0,0))
                self.display.blit(num, (42 + x*50,30 + y*50))
                
    def _FindDuplicatePositions(self):
        complete = 0
        duplicate_positions = []
        num_of_zeros = 0
        sudoku = [[self.sudoku_grid[i][j] + self.filling_space[i][j] for j in range(9)] for i in range(9)]
        
        # Check rows for duplicates
        for r in range(9):
            seen = {}
            Fill = True
            for c in range(9):
                num = sudoku[r][c]
                if num != 0:  # Ignore zeros
                    if num not in seen:
                        seen[num] = []
                    seen[num].append((r, c))
                
                else:
                    num_of_zeros += 1
                    Fill = False

            # Add positions of duplicates to the list
            for positions in seen.values():
                if len(positions) > 1:
                    duplicate_positions.extend(positions)
                    Fill = False
                
            if Fill:
                complete += 1
                

        # Check columns for duplicates
        for c in range(9):
            seen = {}
            Fill = True
            for r in range(9):
                num = sudoku[r][c]
                if num != 0:  # Ignore zeros
                    if num not in seen:
                        seen[num] = []
                    seen[num].append((r, c))
                    
                else:
                    Fill = False

            # Add positions of duplicates to the list
            for positions in seen.values():
                if len(positions) > 1:
                    duplicate_positions.extend(positions)
                    Fill = False
                    
            if Fill:
                complete += 1
            

        # Check subgrids for duplicates
        for grid_row in range(3):
            for grid_col in range(3):
                seen = {}
                Fill = True
                for r in range(3):
                    for c in range(3):
                        num = sudoku[grid_row * 3 + r][grid_col * 3 + c]
                        if num != 0:  # Ignore zeros
                            if num not in seen:
                                seen[num] = []
                            seen[num].append((grid_row * 3 + r, grid_col * 3 + c))
                            
                        else:
                            Fill = False

                # Add positions of duplicates to the list
                for positions in seen.values():
                    if len(positions) > 1:
                        duplicate_positions.extend(positions)
                        Fill = False
                        
                if Fill:
                    complete += 1
                
        
        if num_of_zeros == 0 and len(list(set(duplicate_positions))) == 0:
            self.game_over = True

        return list(set(duplicate_positions)), complete
    
    
    def DrawDucplicateBoxes(self):
        positions, _ = self._FindDuplicatePositions()
        
        for pos in positions:
            if pos in self.Empty:
                x, y = pos
                pygame.draw.rect(self.display, (214, 2, 2), pygame.Rect((25 + x*50,25 + y*50),(50,50)))
                
    
    def PlayStep(self, action):
        pos, num = action
        reward = 0
        
        if self.is_fill_pos(pos):
            self.update_filling_space(pos, num)
            self.attempts += 1
            dup, com = self._FindDuplicatePositions()
            
            if len(dup) != 0:
                reward += -27
            
            if self.completed < com:
                reward += (com - self.completed)
                self.completed = com
                
        self.UiUpdate()
        
        return reward, self.game_over
        
                        
        
if __name__ == '__main__':
    
    game  = SudokuAI()
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            string = input("pos and num: ")
            ls= string.split(',')
            v = []
            for i in ls:
                v.append(int(i))
            
            act= ((v[0], v[1]), v[-1])
            
            re, done = game.PlayStep(act)
            print(act, re)
            
            if done:
                running = False
        
        
    

#     game = Sudoku()
#     game.DrawPreoccupiedBoxes()
#     game.DrawLines()
#     game.DrawFillSpace()
    
    
    
#     pygame.display.update()
#     running = True
    
#     while running:
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
                
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#             # Check if left mouse button (button 1) is clicked
#                 if event.button == 1:
#                     # Get the position of the click
#                     click_position = event.pos
#                     x,y = click_position
                    
#                     if game.is_button_pos(click_position):
                        
#                         i = (x - 5)//49
                        
#                         game.buttun_value = i + 1
                            
#                         game.UiUpdate()
                        
#                     if game.is_fill_pos(click_position):
#                         i, j = ((x - 25) // 50), ((y - 25) // 50)
#                         game.update_filling_space(i, j)
#                         game.DrawFillSpace()
#                         game.UiUpdate()
#                         print(game.game_over)
                        
#                     if game.game_over:
#                         game.UiUpdate()
                        
                        
                            
                        
                    
                