# screen_capture.py
from windowDetection import getWindowsDetails
import mss
import numpy as np
import cv2

left, top, width, height = getWindowsDetails()

top    += 40
# left   += 25
# width  -= 8
# height -= 500

monitor = {
    "top": top,
    "left": left,
    "width": width,
    "height": height
}

sct = mss.mss() # screen capture 

def capture_frame():
    img = sct.grab(monitor)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

# capture_frame()

if __name__ == "__main__":
    while True:
        frame = capture_frame()
        cv2.imshow("Game Screen", frame)

        # ESC to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
