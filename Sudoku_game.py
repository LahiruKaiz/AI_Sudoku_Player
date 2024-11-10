import pygame
from GridGen import GridGenerate

pygame.init()
font = pygame.font.SysFont('arial', 25)


class Sudoku:
    
    def __init__(self, Solved_grid):
        
        # self.display = pygame.display.set_mode((500, 500))
        # pygame.display.set_caption('Sudoku')
        
        self.Solved_grid = Solved_grid
        
if __name__ == '__main__':
    
    g = GridGenerate()
    game = Sudoku(g.MainGrid)
    
    # while True:
    #     pass