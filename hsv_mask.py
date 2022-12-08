# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# 実行
while True:

    # Webカメラのフレーム取得
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    # 画像をRGBからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # 色の範囲
    HSVRange = {
        "lower": np.array([50, 50, 30]), 
        "upper": np.array([70, 120, 70])
    }

    # HSVからマスクを作成
    hsv_mask = cv2.inRange(hsv, HSVRange["lower"], HSVRange["upper"])
    cv2.imshow("hsv_mask", hsv_mask)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
