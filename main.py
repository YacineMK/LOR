import socket
import cv2
import numpy as np

#returns true if color is present in image
#frame should be in brg format
def detect_color(frame,lower_color,upper_color,display_output=False,display_name='output',sentivity=0.8):
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_color,upper_color)
    filtered = cv2.bitwise_and(frame,frame,mask=mask)
    if display_output:
     cv2.imshow(display_name,filtered)
    if 1- sentivity <= np.sum(mask.flatten()) / len(mask.flatten()) / 255:
     return True
    
    return False
    
    
print("Creating server...")
s = socket.socket()
s.bind(('0.0.0.0', 10000))
s.listen(0)
cam = cv2.VideoCapture(0)

  

while True:
        client, addr = s.accept()
        while True:
          ret,frame = cam.read()
          cv2.imshow("Real Image",frame)
          red = detect_color(frame,np.array([0,100,100]),np.array([10 ,255,255]),display_name='red filter')
          blue = detect_color(frame,np.array([120,100,100]),np.array([180,255,255]),display_name='blue filter')
          green = detect_color(frame,np.array([20,50,50]),np.array([110,255,255]),display_name='green filter')
          result = -1
          if red:
              print('Red sign')
              result = 0
          elif blue:
              print('Blue sign')
              result = 1
          elif green:
              print('green sign')
              result = 2
          client.sendall((str(result) + '\n').encode('utf8'))
          cv2.waitKey(1)
        print("Closing connection")
        client.close()
