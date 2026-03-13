from src.capture.screen_capture import capture_frame
from src.perception.detector import Detector

detector = Detector(r"models/crossy_yolo.pt")
frame = capture_frame()
detections = detector.detect(frame)
print(detections)
