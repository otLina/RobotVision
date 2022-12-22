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

    def getPrevColor(self, hsv, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            H,S,V=hsv[y,x,:]
            self.prevColor = hsv[y,x,:]
            self.prevColorChosen = True
            #self.prevColor='prev(H,S,V)=('+str(H)+','+str(S)+','+str(V)+')'
            print(self.prevColor)

    def getNextColor(self, img, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            H,S,V=hsv[y,x,:]
            self.nextColor = hsv[y,x,:]
            #self.nextColor='next(H,S,V)=('+str(H)+','+str(S)+','+str(V)+')'
            print(self.nextColor)
            self.showResult = True
    
    def changeColor(self, frame):
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
        mask = np.where((frame_mask == 0) | (frame_mask == 2), 1, 0).astype("uint8")
        mask2 = np.where((frame_mask == 0) | (frame_mask == 2), 0, 255).astype("uint8")
        # サイズを元に戻す
        mask_resize = cv2.resize(mask, (int(mask.shape[1] * 4), int(mask.shape[0] * 4)))
        mask_resize2 = cv2.resize(mask2, (int(mask2.shape[1] * 4), int(mask2.shape[0] * 4)))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        v = hsv[:,:,2]
        v_copy = hsv[:,:,2] * mask_resize

        hmax = self.prevColor[0] + 10
        hmin = self.prevColor[0] - 10
        h = hsv[:,:,0]
        h = np.where((h < hmax) & (h > hmin) & (v_copy == 0), self.nextColor[0], h)
        hsv[:,:,0] = h
        
        smax = self.prevColor[1] + 1
        smin = self.prevColor[1] - 1
        s = hsv[:,:,1]
        s = np.where((s < smax) & (s > smin) & (v_copy == 0), self.nextColor[1], s)
        hsv[:,:,1] = s

        vmax = self.prevColor[2] + 0
        vmin = self.prevColor[2] - 0
        v = np.where((v < vmax) & (v > vmin) & (v_copy == 0), self.nextColor[2], v)
        hsv[:,:,2] = v

        frame2=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return frame2, mask_resize2


# 実行
m = mouseEventHandler()
while True:
    ret, frame = cap.read()
    img = cv2.imread(file_path)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
        cv2.imshow('result', m.changeColor(frame)[0])
        cv2.imshow('mask_resize2', m.changeColor(frame)[1])

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("m"):
        m = mouseEventHandler()
    if k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()







# class mouseeventHandler {
#     value {
#         prevColor,
#         nextColor,
#     }

#     methods {
#         init, 
#         getColor(return Color)
#             クリックされた位置の色をとる
#         getPrevColor(return 動画からとった色の値 prevColor {H, S, V}),
#             frameに対してクリックされた値をとってくる
#             getColor
#         getNextColor(return カラーパレットからとった色の値 nextColor {H, S,V}),
#             paletteに対してクリックされた値をとってくる
#             getColor
#         changeColor(引数：prevColor, nextColor)
#             frameのprevColorをnextColorに変える
#     }
# }