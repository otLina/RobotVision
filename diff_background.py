# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# スクショしたかどうかを保存する変数 (まだ撮っていないのでFalse)
screenshot = False
# スクショを保存する変数
photo = None

# 実行
while True:

    # Webカメラのフレーム取得
    ret, frame = cap.read()

    # 画像をRGBからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # スクショがあるなら差分を出力
    if screenshot:
        # 背景差分のクラスを定義(リセット)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        # 背景画像を指定(スクショ)
        background = fgbg.apply(photo)
        # 差分画像(カメラの入力フレーム)
        fg_mask = fgbg.apply(frame)
        cv2.imshow("fg_mask", fg_mask)
        

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
            blur_mask = cv2.cvtColor(blur_mask, cv2.COLOR_GRAY2BGR)
            blur_mask = (blur_mask / 255* np.array([255, 0, 0])).astype("uint8")

            cv2.imshow("blur_mask", blur_mask)

    cv2.imshow('window', frame)
    cv2.setMouseCallback('window', click_pos)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    # フレームを保存 (スクショ)
    elif k == ord("s"):
        photo = frame
        screenshot = True

cap.release()
cv2.destroyAllWindows()
