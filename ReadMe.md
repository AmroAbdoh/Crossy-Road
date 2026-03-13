# Crossy Road AI Agent

An AI system that learns to play **Crossy Road** automatically using reinforcement learning and computer vision.

The project combines:

* Object detection using YOLOv8
* Reinforcement learning (Deep Q-Network)
* Screen capture from an Android emulator
* Game control through ADB

---

## Architecture

Game Screen
↓
Screen Capture
↓
YOLOv8 Object Detection
↓
State Extraction
↓
DQN Agent
↓
ADB Controls

---

## State Representation

The agent observes three features:

* `player_y` – normalized vertical player position
* `nearest_car_dist` – distance to closest car
* `on_log` – whether the player is standing on a log

These features are used as input to the neural network.

---

## Action Space

The agent can perform 5 actions:

0 – Move forward
1 – Move backward
2 – Move left
3 – Move right
4 – Wait

---

## Technologies

* Python
* PyTorch
* YOLOv8
* OpenCV
* ADB
* LDPlayer

---

## Installation

```
pip install -r requirements.txt
```

---

## Training the Agent

```
python src/agent/train_rl.py
```

---

## Running the AI

```
python src/run/play_ai.py
```

---

## Notes

YOLO weights must be placed in:

```
models/crossy_yolo.pt
```

DQN model will be saved to:

```
models/crossy_dqn3.pt
```
