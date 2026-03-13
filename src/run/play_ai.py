import numpy as np
from environment import CrossyEnv
from agent import DQNAgent

env = CrossyEnv()

state_size = 3
action_size = 5

agent = DQNAgent(state_size, action_size)

state = env.reset().flatten()

while True:

    action = agent.act(state)

    next_state, reward, done = env.step(action)

    state = next_state.flatten()

    if done:
        state = env.reset().flatten()