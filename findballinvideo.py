import cv2 as cv
import numpy as np

# 创建滑动条需要的操作
def doNothing(x):
    pass

# 调用opencv函数开启摄像头，判断是否成功打开。
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 创建参数调成界面和滑动条，窗口显示不支持中文
cv.namedWindow('Adjustments')
# HSV空间的V--value值的下阈值和上阈值，检测白色下阈值在200左右，上阈值255，可根据实际调整
cv.createTrackbar('White Lower Threshold Value', 'Adjustments', 0, 255, doNothing)
cv.createTrackbar('White Upper Threshold Value', 'Adjustments', 0, 255, doNothing)
# HSV空间的S--Saturation值的下阈值和上阈值，检测白色下阈值在0左右，上阈值255，可根据实际调整
cv.createTrackbar('White Lower Threshold Saturation', 'Adjustments', 0, 255, doNothing)
cv.createTrackbar('White Upper Threshold Saturation', 'Adjustments', 0, 255, doNothing)
# 霍夫变换检测的圆的最小和最大圆半径，检测半径下阈值在0左右，上阈值255，可根据实际调整
cv.createTrackbar('Min Radius', 'Adjustments', 0, 255, doNothing)
cv.createTrackbar('Max Radius', 'Adjustments', 0, 255, doNothing)


while True:
    # 获取摄像头桢照片，isframeread返回bool类是否获取到图片，frame返回图片数据
    isframeread, frame = cap.read()
    
    # isframeread 为false则没有获取到图片
    if not isframeread:
        print("Can't receive frame. Exiting ...")
        break
    
    # 由滑动条给参数赋值
    low_threshv = cv.getTrackbarPos('White Lower Threshold Value', 'Adjustments')
    high_threshv = cv.getTrackbarPos('White Upper Threshold Value', 'Adjustments')
    low_threshs = cv.getTrackbarPos('White Lower Threshold Saturation', 'Adjustments')
    high_threshs = cv.getTrackbarPos('White Upper Threshold Saturation', 'Adjustments')
    minradius = cv.getTrackbarPos('Min Radius', 'Adjustments')
    maxradius = cv.getTrackbarPos('Max Radius', 'Adjustments')
    
    # 将图像变换到hsv空间
    hsvimg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 定义阈值
    # 检测白色的HSV值为(0-255,0-255, 255) ，只需要调整S和V两个参数
    white_lower = np.array([0, low_threshs, low_threshv])
    white_upper = np.array([255, high_threshs, high_threshv])
    
    # 将图像做阈值化处理，只保留白色和黑色
    # 生成图像掩码，避免影像原图
    mask = cv.inRange(hsvimg, white_lower, white_upper)
    
    # 通过霍夫变换检测掩码图像中的圆
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, 20,
                              param1=50, param2=30, minRadius=minradius, maxRadius=maxradius)
    
    if circles is None:
        # 检测不到圆则显示未检测到
        text = 'no ball detected'
        textsize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
        rows, columns, channels = frame.shape
        
        # 处理文本显示位置
        textorigin = ((columns//2)-(textsize[0][0]//2), textsize[0][1]+10)
    
        # 绘制文本方框
        bottomleftvertex = (textorigin[0]-5, textorigin[1]+5)
        toprightvertex = (textorigin[0]+textsize[0][0]+5, 5)
        cv.rectangle(frame, bottomleftvertex, toprightvertex, [255, 255, 255], cv.FILLED)
        
        # 绘制文本
        cv.putText(frame, text, textorigin, cv.FONT_HERSHEY_SIMPLEX, 2, [0, 0, 0], 2, cv.FILLED, False)
        
    else: # 检测到球？
        # 打印圆坐标
        circles = np.uint16(np.around(circles))
        print(circles)
        
        # 绘制圆的外接矩形
        # 只保留最佳矩形
        center_x = circles[0][0][0]
        center_y = circles[0][0][1]
        radius = circles[0][0][2]
        cv.rectangle(frame, (center_x - radius, center_y - radius), (center_x + radius, center_y + radius), (0, 0, 255),
                     2)
    
    # 显示图片
    cv.imshow('Result', frame)
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows() 
