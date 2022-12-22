# ライブラリのインポート
import cv2
import numpy as np

# -----------以下記述-----------
cap = cv2.VideoCapture(0)
grayscale = False

while(True):
    ret,frame = cap.read()
    cv2.imshow('camera',frame)

    # グレースケール変換
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    # 方法2(OpenCVで実装)
    dst = cv2.Canny(img, 150, 250)
    dst = 255 - dst

    # カーネルを作成する。
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    # 2値画像を膨張する。
    dst = cv2.erode(dst, kernel)
    dst = cv2.erode(dst, kernel)
    dst = cv2.erode(dst, kernel)

    # medianblurを用いてノイズ成分を除去
    dst = cv2.medianBlur(dst, ksize=3)

    cv2.imshow('dst', dst)



    """
    ここからラベリングを行う
    """
    # ラベリング結果書き出し用に二値画像をカラー変換 (枠や座標をカラー表示したい！)
    src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    # ラベリング処理
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # 領域(stats[:, 4])が3つ以上ある場合(そのうち1つは背景)だけ処理
    if nlabels >= 3:
        # 面積でソート(今回は面積が上位２つの領域を利用)
        top_idx = stats[:, 4].argsort()[-3:-1]

        # 各領域において...
        for i in top_idx:
            # 領域の外接矩形の角座標を入手
            x0 = stats[i, 0]
            y0 = stats[i, 1]
            x1 = x0 + stats[i, 2]
            y1 = y0 + stats[i, 3]
            # 長方形描画 (引数 : 描画画像、 長方形の左上角、 長方形の右下角、 色(BGR)、 線の太さ)
            # 長方形以外を使いたい時はURL参照→(http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html)
            cv2.rectangle(src, (x0, y0), (x1, y1), (0, 0, 255), 5)

            # 領域の重心座標、サイズを表示 (引数 : 描画画像、 書き込む文字列、 書き込む座標、 フォント、 サイズ、 色、 太さ)
            cv2.putText(
                src,
                "Center X: " + str(int(centroids[i, 0])),
                (x1 - 30, y1 + 15),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                src,
                "Center Y: " + str(int(centroids[i, 1])),
                (x1 - 30, y1 + 30),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                src,
                "Size: " + str(int(stats[i, 4])),
                (x1 - 30, y1 + 45),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 255, 255),
                2,
            )

    cv2.imshow('contours', src)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()