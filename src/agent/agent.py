# agent.py
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
import os

class DQNAgent:
    def __init__(self, state_size, action_size, model_path="models/crossy_dqn3.pt"):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=5000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05
        self.lr = 0.001

        self.model_path = model_path

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.build_model().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

        
        if os.path.exists(self.model_path):
            checkpoint = torch.load(self.model_path, map_location=self.device)

            self.model.load_state_dict(checkpoint["model"])
            self.optimizer.load_state_dict(checkpoint["optimizer"])
            self.epsilon = checkpoint["epsilon"]

            print("✅ MODEL + OPTIMIZER + EPSILON LOADED")
        else:
            print("🆕 NO MODEL FOUND — TRAINING FROM SCRATCH")

    def build_model(self):
        return nn.Sequential(
            nn.Linear(self.state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_size)
        )

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)

        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state)
        return int(torch.argmax(q_values).item())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)

        states, targets = [], []

        for state, action, reward, next_state, done in batch:
            state_t = torch.FloatTensor(state).to(self.device)
            next_state_t = torch.FloatTensor(next_state).to(self.device)

            target = reward
            if not done:
                target += self.gamma * torch.max(
                    self.model(next_state_t.unsqueeze(0))
                ).item()

            target_f = self.model(state_t).detach().cpu().numpy()
            target_f[action] = target

            states.append(state)
            targets.append(target_f)

        states = torch.FloatTensor(states).to(self.device)
        targets = torch.FloatTensor(targets).to(self.device)

        self.optimizer.zero_grad()
        loss = self.loss_fn(self.model(states), targets)
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save(self):
        torch.save({
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon
        }, self.model_path)
