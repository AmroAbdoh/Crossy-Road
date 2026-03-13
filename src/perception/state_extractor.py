# state_extractor.py
import numpy as np

# class IDs must match your YOLO training
CAR = 0
LOG = 1
PLAYER = 2
TRAIN_LIGHT = 3
LILY = 4

def extract_state(detections, frame_shape):
    h, w, _ = frame_shape

    player_y = 0
    nearest_car_dist = 1.0
    on_log = 0

    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        if d["class"] == PLAYER:
            player_y = cy / h

        if d["class"] == CAR:
            dist = abs(cy - player_y * h) / h
            nearest_car_dist = min(nearest_car_dist, dist)

        if d["class"] == LOG:
            if abs(cy - player_y * h) < 40:
                on_log = 1

    return np.array([
        player_y,
        nearest_car_dist,
        on_log
    ], dtype=np.float32)
