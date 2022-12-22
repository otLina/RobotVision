# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
file_path = "./8.jpg"

class mouseEventHandler:
    def __init__(self): 
        self.prevColor = []
        self.nextColor = []
        self.prevColorChosen = False
        self.showResult = False

    # window上でクリックされた位置の色を取得
    def getPrevColor(self, hsv, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            H,S,V=hsv[y,x,:]
            self.prevColor = hsv[y,x,:]
            self.prevColorChosen = True
            print(self.prevColor)
            
    # パレット上でクリックされた位置の色を取得
    def getNextColor(self, img, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            H,S,V=hsv[y,x,:]
            self.nextColor = hsv[y,x,:]
            print(self.nextColor)
            self.showResult = True

    # frameのprevColorをnextColorに変更
    def changeColor(self, frame):
        """
        grubcutで前景maskを生成
        """
        # grabCut処理が重いのでwindowサイズを圧縮
        frame_resize = cv2.resize(frame, (int(frame.shape[1] / 8), int(frame.shape[0] / 8)))
        # windowの高さ、幅
        frame_h, frame_w = frame_resize.shape[0], frame_resize.shape[1]
        # 前景部分を指定(引数 : x座標, y座標, 幅, 高さ)
        cut_rect = (1, 1, frame_w, frame_h)
        # grabCutに必要なmaskや座標を格納するための配列の準備
        frame_mask = np.zeros((frame_h, frame_w), np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        # grubcutの実行
        cv2.grabCut(frame_resize, frame_mask, cut_rect, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_RECT)
        # maskを用意
        mask = np.where((frame_mask == 0) | (frame_mask == 2), 1, 0).astype("uint8")
        mask_print = np.where((frame_mask == 0) | (frame_mask == 2), 0, 255).astype("uint8")
        # サイズを元に戻す
        mask = cv2.resize(mask, (int(mask.shape[1] * 8), int(mask.shape[0] * 8)))
        mask_print = cv2.resize(mask_print, (int(mask_print.shape[1] * 8), int(mask_print.shape[0] * 8)))

        """
        frameのprevColorをnextColorに変更
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hmax = self.prevColor[0] + 10
        hmin = self.prevColor[0] - 10
        h = hsv[:,:,0]
        h_mask = hsv[:,:,0] * mask
        h = np.where((h < hmax) & (h > hmin) & (h_mask == 0), self.nextColor[0], h)
        hsv[:,:,0] = h
        
        smax = self.prevColor[1] + 1
        smin = self.prevColor[1] - 1
        s = hsv[:,:,1]
        s_mask = hsv[:,:,1] * mask
        s = np.where((s < smax) & (s > smin) & (s_mask == 0), self.nextColor[1], s)
        hsv[:,:,1] = s

        vmax = self.prevColor[2] + 0
        vmin = self.prevColor[2] - 0
        v = hsv[:,:,2]
        v_mask = hsv[:,:,2] * mask
        v = np.where((v < vmax) & (v > vmin) & (v_mask == 0), self.nextColor[2], v)
        hsv[:,:,2] = v

        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return mask_print, frame

# 実行
m = mouseEventHandler()
while True:
    ret, frame = cap.read()
    img = cv2.imread(file_path)

    # 画像をRGBからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('frame', frame)
    cv2.imshow('palette', img)
    cv2.setMouseCallback('frame', 
                        lambda event, x, y, flags, param: 
                        m.getPrevColor(hsv, event, x, y, flags, param))
    cv2.setMouseCallback('palette',
                        lambda event, x, y, flags, param: 
                        m.getNextColor(img, event, x, y, flags, param))
    
    if(m.showResult and m.prevColorChosen):
        cv2.imshow('mask_print', m.changeColor(frame)[0])
        cv2.imshow('result', m.changeColor(frame)[1])

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("m"):
        m = mouseEventHandler()
    if k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
