# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(True):
    ret,frame = cap.read()
    cv2.imshow("frame", frame)

    """
    grubcutの準備・実行
    """
    # windowサイズを圧縮
    frame_resize = cv2.resize(frame, (int(frame.shape[1] / 4), int(frame.shape[0] / 4)))
    # windowの高さ、幅
    frame_h, frame_w = frame_resize.shape[0], frame_resize.shape[1]
    # 前景部分を指定(引数 : x座標, y座標, 幅, 高さ)
    # x,y座標は0を指定するとエラーとなるため1を指定
    cut_rect = (1, 1, frame_w, frame_h)
    # grubcutに必要なmaskや座標を格納するための配列の準備
    frame_mask = np.zeros((frame_h, frame_w), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # grubcutの実行
    cv2.grabCut(frame_resize, frame_mask, cut_rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    """
    [grubcutの実行結果について]
    frame_maskでは各画素が0~3で分類される。
    それぞれ...
    0.背景
    1.前景
    2.背景らしい
    3.前景らしい
    である。
    そこで、0,2,3の画素は0として、1の画素は255とするようなmaskを用意
    """
    # maskを用意
    mask = np.where((frame_mask == 0) | (frame_mask == 2), 0, 255).astype("uint8")
    # サイズを元に戻す
    mask_resize = cv2.resize(mask, (int(mask.shape[1] * 4), int(mask.shape[0] * 4)))
    cv2.imshow("mask", mask_resize)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()