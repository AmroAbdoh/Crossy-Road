import pygetwindow

# window = pygetwindow.getWindowsWithTitle("LDPlayer")[0]
# print(window.left , window.top , window.width , window.height)

def getWindowsDetails():
    window = pygetwindow.getWindowsWithTitle("LDPlayer")[0]
    # print(window.left , window.top , window.width , window.height)
    return window.left , window.top , window.width , window.height

# print(getWindowsDetails())