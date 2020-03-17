import cv2
import matplotlib.pyplot as plt

cam = cv2.VideoCapture(0)

#while True:
ret, img = cam.read()
plt.imshow(img)
plt.show()
    
