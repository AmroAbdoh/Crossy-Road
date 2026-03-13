# adb_control.py
import subprocess

DEVICE_ID = "emulator-5554"

# connect to the device
adb = subprocess.Popen( 
    f"adb -s {DEVICE_ID} shell",
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

def pressKey(key_code):
    adb.stdin.write(f"input keyevent {key_code}\n")
    adb.stdin.flush()

def action_up():
    pressKey(19)

def action_down():
    # pressKey(20)
    # swipe from somewhere above to (900, 820)
    x_start, y_start = 900, 600
    x_end, y_end = 900, 820
    duration = 50  # milliseconds

    adb.stdin.write(f"input touchscreen swipe {x_start} {y_start} {x_end} {y_end} {duration}\n")
    adb.stdin.flush()

def action_left():
    pressKey(21)

def action_right():
    pressKey(22)

def action_wait():
    pass

def tap_screen(x, y):
    adb.stdin.write(f"input tap {x} {y}\n")
    adb.stdin.flush()

def tap_space():
    # Press space key (keycode 62)
    adb.stdin.write("input keyevent 62\n")
    adb.stdin.flush()
    # time.sleep(0.1)  # short delay between taps

# while True: 
#     inpt = input()
#     if(inpt == "w"):
#         action_up()
#     elif inpt == 's':
#         action_down()
