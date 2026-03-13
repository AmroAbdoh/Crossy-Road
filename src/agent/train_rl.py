# train_rl.py
from src.environment import CrossyEnv
from agent import DQNAgent
import os

env = CrossyEnv()

state_size = 3
action_size = 5

os.makedirs("models", exist_ok=True)

agent = DQNAgent(
    state_size,
    action_size,
    model_path="models/crossy_dqn3.pt"
)

episodes = 999999   # train until YOU stop
batch_size = 32
SAVE_EVERY = 10

episode = 0
while True:
    episode += 1
    state = env.reset().flatten()
    done = False
    total_reward = 0

    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = next_state.flatten()

        agent.remember(state, action, reward, next_state, done)
        agent.replay(batch_size)

        state = next_state
        total_reward += reward

    if episode % SAVE_EVERY == 0:
        agent.save()
        print("💾 Model saved")

    print(
        f"Episode {episode} | "
        f"Reward: {total_reward:.1f} | "
        f"Epsilon: {agent.epsilon:.3f}"
    )
