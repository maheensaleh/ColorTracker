import cv2
import numpy as np

#bgr sequence

color = np.uint8([[[0,255,255 ]]]) # give bgr value here to get its hsv range
hsv_color = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
hsv_color = hsv_color[0][0]
print("hsv of ",color," is ",hsv_color)

lower = (hsv_color[0]-10,100,100)  ## reduce the value 100 to 75 or 50 to incresae the range of detection
upper = (hsv_color[0]+10,255,255)

print("lower ",lower)
print("upper",upper)