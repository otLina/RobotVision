# ライブラリのインポート
import cv2
import numpy as np
# -----------以下記述-----------
cap = cv2.VideoCapture(0)
changeColor = np.array([255, 255, 255], dtype="uint8")

while(True):
    ret,frame = cap.read()
    #frame = cv2.imread('color_picker.png')
    cv2.imshow('window', frame)
    #img = np.copy(frame)

    #img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    def click_pos(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # img = np.copy(frame)
            img = frame
            #img = cv2.resize(img, (256, 256))
            B,G,R = frame[y,x,:]
            # targetColor = np.array([B, G, R]).astype(np.uint8)
            # bgr_str = '(B,G,R)=('+str(B)+','+str(G)+','+str(R)+')'
            # print(bgr_str)
            # print(targetColor)
            # print(f"{targetColor.dtype = }")
            # print(f"{changeColor.dtype = }")
            # cv2.imshow('window3', img.astype(np.uint8))
            #img = np.where((img == targetColor), changeColor, np.array([0, 0, 0], dtype="uint8"), )
            # print(f"{img.dtype = }")
            # print(f"{img.max() = }")

            cv2.imshow('window2', img)

    cv2.setMouseCallback('window', click_pos)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
