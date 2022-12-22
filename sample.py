# ライブラリのインポート
import cv2
import numpy as np

# -----------以下記述-----------
cap = cv2.VideoCapture(0)
grayscale = False

while(True):
    ret,frame = cap.read()
    if grayscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    cv2.imshow('camera',frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('g'):
        grayscale = True
    
cap.release()
cv2.destroyAllWindows()