# environment.py
import time
import numpy as np

from src.control.adb_control import action_up, action_down, action_left, action_right, action_wait , tap_space , tap_screen
from src.capture.screen_capture import capture_frame
from src.perception.detector import Detector
from src.perception.state_extractor import extract_state

class CrossyEnv:
    def __init__(self):
        self.detector = Detector(
            r"models/crossy_yolo.pt"
        )
    
        self.last_y = 0
        self.missing_player_frames = 0


    def reset(self):
        # tap restart button
        adb_restart_x, adb_restart_y = 1114, 934  # adjust once correctly

        from adb_control import pressKey
        import subprocess

        # tap restart
        subprocess.call(
            f"adb -s emulator-5554 shell input tap {adb_restart_x} {adb_restart_y}",
            shell=True
        )

        time.sleep(1.5)  # wait for animation

        frame = capture_frame()
        detections = self.detector.detect(frame)
        state = extract_state(detections, frame.shape)
        self.last_y = state[0]
        return state

    def step(self, action):
        forwardReward = 11
        reward = 0
        if action == 0:
            # action_up()     
            tap_screen(900, 820)    
            reward += forwardReward
            # if delta < 0.05 :        # small threshold to ignore noise
                # reward -= 5
        elif action == 1:
            action_down()
            reward -= (forwardReward - 1)
        elif action == 2:
            action_left()
            # reward -= 0.1
        elif action == 3:
            action_right()
            # reward -= 0.1
        else:
            action_wait()

        time.sleep(0.14)

        frame = capture_frame()
        detections = self.detector.detect(frame)
        state = extract_state(detections, frame.shape)
        delta = state[0] - self.last_y
        done = False

        if action == 0 and delta < 0.02 :
            reward -= forwardReward


        #  Forward movement
        # if delta > 0.05:        # small threshold to ignore noise
        #     reward += 100

        # #  Backward movement
        # elif delta < -0.01:
        #     reward -= 9

        

        # if action in [2, 3]:   # left or right
            # reward -= 0.05

        # death detection (player missing)

        # player_exists = any(d["class"] == 0 for d in detections)   OLD
        PLAYER_CLASS = 0
        
        PLAYER_CONF_THRESHOLD = 0.60

        player_exists = any(
            d["class"] == PLAYER_CLASS and d["conf"] >= PLAYER_CONF_THRESHOLD
            for d in detections
        )

        # 🟢 Alive bonus
        if player_exists : 
            reward += 0.5


        if not player_exists:
            self.missing_player_frames += 1
        else:
            self.missing_player_frames = 0


        if self.missing_player_frames >= 3:
            reward -= 90
            done = True
            print("Game Over , new Game : ")            
            # time.sleep(2.5)
            # tap_screen(900, 820)
            time.sleep(2)
            tap_screen(900, 820)
            # tap_screen(900, 790)
            # time.sleep(0.2)
            # tap_screen(890 , 800)
            

        self.last_y = state[0]
        return state, reward, done


