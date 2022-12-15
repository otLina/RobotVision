# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
file_path = "./color_picker.png"
offset = 20

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

    def getNextColor(self, hsv, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            H,S,V=hsv[y,x,:]
            self.nextColor = hsv[y,x,:]
            #self.nextColor='next(H,S,V)=('+str(H)+','+str(S)+','+str(V)+')'
            print(self.nextColor)
            self.showResult = True
    
    def changeColor(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hmax = self.prevColor[0] + offset
        hmin = self.prevColor[0] - offset
        h = hsv[:,:,0]
        h = np.where((h < hmax) & (h > hmin), self.nextColor[0], h)
        hsv[:,:,0] = h
        smax = self.prevColor[1] + offset
        smin = self.prevColor[1] - offset
        s = hsv[:,:,1]
        s = np.where((s < smax) & (s > smin), self.nextColor[1], s)
        hsv[:,:,1] = s

        vmax = self.prevColor[2] + offset
        vmin = self.prevColor[2] - offset
        v = hsv[:,:,2]
        v = np.where((v < vmax) & (v > vmin), self.nextColor[2], v)
        hsv[:,:,2] = v

        frame2=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return frame2 


# 実行
m = mouseEventHandler()
while True:
    ret, frame = cap.read()
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 画像をRGBからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('frame', frame)
    cv2.imshow('palette', img)
    cv2.setMouseCallback('frame', 
                        lambda event, x, y, flags, param: 
                        m.getPrevColor(hsv, event, x, y, flags, param))
    cv2.setMouseCallback('palette',
                        lambda event, x, y, flags, param: 
                        m.getNextColor(hsv, event, x, y, flags, param))
    
    if(m.showResult and m.prevColorChosen):
        cv2.imshow('result', m.changeColor(frame))

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