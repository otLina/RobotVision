# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

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
            # HSVからマスクを作成
            hsv_mask = cv2.inRange(hsv, HSVRange["lower"], HSVRange["upper"])
            # medianblurを用いてノイズ成分を除去
            blur_mask = cv2.medianBlur(hsv_mask, ksize=3)
            cv2.imshow("hsv_mask", blur_mask)

    cv2.imshow('window', frame)
    cv2.setMouseCallback('window', click_pos)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
