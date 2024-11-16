import numpy as np
import random
import torch
from Model import NeuralNEt, Trainer
from collections import deque
from SudokuGame import SudokuAI
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = NeuralNEt(162, 8)
        self.trainer = Trainer(self.model, lr = LR, gamma= self.gamma)
        
        
    def GetState(self, game):
        
        state1 = [game.sudoku_grid[i][j] + game.filling_space[i][j] for i in range(9) for j in range(9)]

        state2 = [[1 if (x, y) in game.Empty else 0 for y in range(9)] for x in range(9)]
        
        state = state1 + [item for sublist in state2 for item in sublist]

        return np.array(state, dtype=int)
    
    def GetAction(self, state, game):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - game.attempts
        if random.randint(0, 200) < self.epsilon:
            valid = False
            while not valid:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                
                pos = (x, y)
                if pos in game.Empty:
                    valid = True
            num = random.randint(1, 9)
            
            action = ((pos), num)
            
            
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            pred1, pred2, pred3 = self.model(state0)
            x = torch.argmax(pred1).item()
            y = torch.argmax(pred2).item()
            num = torch.argmax(pred3).item() + 1
            
            action = ((x, y), num)

        return action
    
    
    def TrainShortMemory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
        
    
    def Remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
        
    def TrainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
        
def train():
    plot_scores = []
    record = 0
    agent = Agent()
    game = SudokuAI()
    while True:
        # get old state
        state_old = agent.GetState(game)

        # get move
        final_move = agent.GetAction(state_old)

        # perform move and get new state
        reward, done, score = game.PlayStep(final_move)
        state_new = agent.GetState(game)

        # train short memory
        agent.TrainShortMemory(state_old, final_move, reward, state_new, done)

        # remember
        agent.Remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            score = game.attempts
            game.reset()
            agent.TrainLongMemory()

            if score < record:
                record = score
                agent.model.save()

            plot_scores.append(score)
            plot(plot_scores)


if __name__ == '__main__':
    train()