# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
hdelta = 150
sdelta = 50
vdelta = 50 

# 実行
while True:

    # Webカメラのフレーム取得
    ret, frame = cap.read()

    # 画像をRGBからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def click_pos(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            H,S,V=hsv[y,x,:]
            hsv_str='(H,S,V)=('+str(H)+','+str(S)+','+str(V)+')'
            print(hsv_str)
            # 色の範囲
            HSVRange = {
                "lower": np.array([int(H)-10, int(S)-20, int(V)-20]), 
                "upper": np.array([int(H)+10, int(S)+20, int(V)+20])
            }
            # # HSVからマスクを作成
            # hsv_mask = cv2.inRange(hsv, HSVRange["lower"], HSVRange["upper"])
            # # medianblurを用いてノイズ成分を除去
            # blur_mask = cv2.medianBlur(hsv_mask, ksize=3)
            # blur_mask = cv2.cvtColor(blur_mask, cv2.COLOR_GRAY2BGR)
            # blur_mask = (blur_mask / 255* np.array([255, 0, 0])).astype("uint8")
            
            #cv2.imshow("blur_mask", blur_mask)

            

            hmax = int(H) + 20
            hmin = int(H) - 20
            h = hsv[:,:,0]
            h = np.where((h < hmax) & (h > hmin), h + hdelta, h)
            hsv[:,:,0] = h

            smax = int(S) + 20
            smin = int(S) - 20
            s = hsv[:,:,1]
            s = np.where((s < smax) & (s > smin), s + sdelta, s)
            hsv[:,:,1] = s

            vmax = int(V) + 20
            vmin = int(V) - 20
            v = hsv[:,:,2]
            v = np.where((v < vmax) & (v > vmin), v + vdelta, v)
            hsv[:,:,2] = v

            img2=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('change_color.jpg',img2)


    cv2.imshow('window', frame)
    cv2.setMouseCallback('window', click_pos)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
