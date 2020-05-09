# -*- coding: UTF-8 -*-

import cv2 as cv
import numpy as np

# 创建滑动条需要的操作
def doNothing(x):
    pass

video_path = "./1.mp4"
# 检测本地视频用上边代码，如果调用摄像头，用以下代码
# video_path = 0
template = cv.imread('./template.jpg')
cap = cv.VideoCapture(video_path)
if not cap.isOpened():
    print 'Cannot open camera'
    exit()


# 创建参数调成界面和滑动条，窗口显示不支持中文
cv.namedWindow('Adjustments', 0)
cv.resizeWindow('Adjustments', 600, 600)
# 灰度空间的V--value值的下阈值和上阈值，检测黑色下阈值在0左右，上阈值70，可根据实际调整
cv.createTrackbar('Lower', 'Adjustments', 0, 255, doNothing)
cv.createTrackbar('Upper', 'Adjustments', 60, 255, doNothing)
# 模版缩放尺寸
cv.createTrackbar('Zoom', 'Adjustments', 6, 10, doNothing)

center = []
while True:
    found = None
    isframeread, frame = cap.read()
    print frame.shape
    print template.shape

    if not isframeread:
        print "Can't receive frame. Exiting ..."
        break

    img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    equimage = cv.equalizeHist(img)

    # 由滑动条给参数赋值
    balck_lower = cv.getTrackbarPos('Lower', 'Adjustments')
    black_upper = cv.getTrackbarPos('Upper', 'Adjustments')
    scale = cv.getTrackbarPos('Zoom', 'Adjustments') / 10.0

    mask = cv.inRange(equimage, balck_lower, black_upper)

    cv.putText(mask, str(balck_lower), (-20, 500), cv.FONT_HERSHEY_SIMPLEX, 2, [255, 0, 0], 2, cv.FILLED, False)
    # cv.imshow('Result', mask)
    # cv.waitKey(0)

    Gray_template = cv.cvtColor(template, cv.COLOR_RGB2GRAY)
    theight, twidth = Gray_template.shape[:2]

    resized = cv.resize(Gray_template, (int(theight * scale), int(twidth * scale)), interpolation=cv.INTER_NEAREST)

    result = cv.matchTemplate(resized, Gray_template, cv.TM_CCORR)

    (min_val, max_val, min_loc, max_loc) = cv.minMaxLoc(result)

    (startX, startY) = (int(max_loc[0]), int(max_loc[1]))
    (endX, endY) = (int(max_loc[0] + theight),
                    int(max_loc[1] + twidth))

    (center_x, center_y) = (int(((startX + endX) / 2)), int(((startY + endY) / 2)))
    center.append((center_x, center_y))

    for i in range(1, len(center)):
        if (center[(i - 1)] is None) or (center[i] is None):
            continue
        cv.line(frame, center[(i - 1)], center[i], (0, 255, 255), 1)
    cv.rectangle(mask, (startX, startY), (endX, endY), (0, 0, 255), 2)

    cv.imshow('Adjustments', mask)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
