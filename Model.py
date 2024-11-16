import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os 


class NeuralNEt(nn.Module):
    
    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, 2*input_size)
        self.linear2 = nn.Linear(2*input_size, output_size)
        self.linear3 = nn.Linear(2*input_size, output_size)
        self.linear4 = nn.Linear(2*input_size, output_size)
        
        
    def forward(self, x):
        x = F.relu(self.linear1(x))
        
        x1 = self.linear2(x)
        x2 = self.linear3(x)
        x3 = self.linear4(x)
        
        return x1, x2, x3
        
        
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
        


class Trainer:
    
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion1 = nn.MSELoss()
        self.criterion2 = nn.MSELoss()
        self.criterion3 = nn.MSELoss()
        
        
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred1, pred2, pred3 = self.model(state)

        target1 = pred1.clone()
        target2 = pred2.clone()
        target3 = pred3.clone()
        
        for idx in range(len(done)):
            
            Q_new1 = reward[idx]
            Q_new2 = reward[idx]
            Q_new3 = reward[idx]
            if not done[idx]:
                temp1, temp2, temp3 = self.model(next_state[idx])
                Q_new1 = reward[idx] + self.gamma * torch.max(temp1)
                Q_new2 = reward[idx] + self.gamma * torch.max(temp2)
                Q_new3 = reward[idx] + self.gamma * torch.max(temp3)

            target1[idx][action[idx][0][0].item()] = Q_new1
            target2[idx][action[idx][0][1].item()] = Q_new2
            target3[idx][action[idx][-1].item() - 1] = Q_new3
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss1 = self.criterion(target1, pred1)
        loss2 = self.criterion(target2, pred2)
        loss3 = self.criterion(target3, pred3)
        loss = loss1 + loss2 + loss3
        loss.backward()

        self.optimizer.step()