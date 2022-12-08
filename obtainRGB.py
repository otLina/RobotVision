# ライブラリのインポート
import cv2
import numpy as np

# -----------以下記述-----------
cap = cv2.VideoCapture(0)

while(True):
    ret,frame = cap.read()
    #img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    def click_pos(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            img2=np.copy(frame)
            cv2.circle(img2,center=(x,y),radius=5,color=(0,0,0),thickness=-1)
            B,G,R=frame[y,x,:]
            bgr_str='(B,G,R)=('+str(B)+','+str(G)+','+str(R)+')'
            print(bgr_str)

    cv2.imshow('window', frame)
    cv2.setMouseCallback('window', click_pos)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
