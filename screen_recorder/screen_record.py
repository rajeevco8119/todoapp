import cv2
import pyautogui
from win32api import GetSystemMetrics
import numpy as np
import time


# Get screen resolution
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

dim = (width,height)

f = cv2.VideoWriter_fourcc(*"XVID")

output = cv2.VideoWriter("C:/Users/rajeevmahajan/Desktop/test.mp4",f,30.0,dim)   # 30 is the no of frames per second, can be changed

now_start_time = time.time()   # Time right now

# Give duration in seconds for which screen is to be recorded
duration = 10

end_time = now_start_time+duration  # End time is current time+ duration

while True:
    image = pyautogui.screenshot()
    frame_1 = np.array(image)
    frame = cv2.cvtColor(frame_1,cv2.COLOR_BGR2RGB)

    output.write(frame)

    c_time = time.time()
    if c_time > end_time:
        break

output.release()
print('-----END------')
