
import cv2 as cv
import imutils as imutils
import numpy as np
import matplotlib.pyplot as plt


# 调用opencv函数开启摄像头，判断是否成功打开。
#video_path = './1.mp4'
video_path = 0
template = cv.imread('./template.jpg')
cap = cv.VideoCapture(video_path)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

center = []
while True:
    found = None
    # 获取摄像头桢照片，isframeread返回bool类是否获取到图片，frame返回图片数据
    isframeread, frame = cap.read()

    # isframeread 为false则没有获取到图片
    if not isframeread:
        print("Can't receive frame. Exiting ...")
        break

# 将图像变换到hsv空间
    if video_path == 0:
        hsvimg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        (H, S, V) = cv.split(hsvimg)
        HH = cv.equalizeHist(H)
        SH = cv.equalizeHist(S)
        VH = cv.equalizeHist(V)
        equimage = cv.merge((HH, SH, VH))
        #filtimage = cv.bilateralFilter(equimage, 9, 75, 75)

    else:
        hsvimg = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
        (H, S, V) = cv.split(hsvimg)
        HH = cv.equalizeHist(H)
        SH = cv.equalizeHist(S)
        VH = cv.equalizeHist(V)
        equimage = cv.merge((HH, SH, VH))
        #filtimage = cv.bilateralFilter(equimage, 9, 75, 75)

    # 定义阈值
    # 检测白色的HSV值为(0-255,0-255, 255) ，只需要调整S和V两个参数
    balck_lower = np.array([0, 0, 10])
    black_upper = np.array([255, 255, 50])

    # 将图像做阈值化处理，只保留白色和黑色
    # 生成图像掩码，避免影像原图

    mask = cv.inRange(equimage, balck_lower, black_upper)
    #mask = cv.blur(mask, (10, 10))
    #cv.imshow('Result', mask)
    #cv.waitKey(0)

    hsvtemplate = cv.cvtColor(template, cv.COLOR_RGB2GRAY)

    # 获得模板图片的高宽尺寸
    theight, twidth = hsvtemplate.shape[:2]
    # resize the image according to the scale, and keep track
    # of the ratio of the resizing
    for scale in np.linspace(0.5, 3, 4)[::-1]:
        resized = imutils.resize(mask, width=int(twidth * scale))
        r = mask.shape[1] / float(resized.shape[1])
    # if the resized image is smaller than the template, then break
    # from the loop
        if resized.shape[0] < theight or resized.shape[1] < twidth:
            break
    # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv.matchTemplate(resized, hsvtemplate, cv.TM_CCORR)
    # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # check to see if the iteration should be visualized

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable
        if found is None or max_val > found[0]:
            if max_loc[0] is 0:
                break
            else:
                found = (max_val, max_loc, r)

    (_, max_loc, r) = found
    (startX, startY) = (int(max_loc[0] * r), int(max_loc[1] * r))
    (endX, endY) = (int((max_loc[0] + twidth) * r), int((max_loc[1] + theight) * r))
    (center_x, center_y) = (int((startX + endX)/2), int((startY + endY)/2))
    center.append((center_x, center_y))
    for i in range(1, len(center)):
        if center[i - 1] is None or center[i] is None:
            continue
        cv.line(frame, center[i - 1], center[i], (0, 255, 255), 1)

    # 绘制矩形边框，将匹配区域标注出来
    # min_loc：矩形定点
    # (min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
    # (0,0,225)：矩形的边框颜色；2：矩形边框宽度
    #mask = cv.cvtColor(mask, cv.COLOR_GRAY2RGB)
    cv.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

    # 显示图片
    cv.imshow('Result', frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
