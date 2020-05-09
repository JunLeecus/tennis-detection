import cv2 as cv
import numpy as np

imagename = '1.jpg'

#read image
img = cv.imread(imagename, cv.IMREAD_COLOR)

#Convert to hsv colorspace because that works better
hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#Define thresholds
#True value for white in HSV is (0-255,0-255, 255) only Value matters for white
# 只需要调整【x, x, x】中第三个参数
white_lower = np.array([0, 0, 30])
white_upper = np.array([330, 255, 100])

#Threshold the HSV image to get only white colors
#Image is a mask of only colors in the threshold values
mask = cv.inRange(hsvimg, white_lower, white_upper)
cv.imshow('Result', mask)
k = cv.waitKey(0)

#Find circles in the masked image
circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, 20,
                          param1=50, param2=30, minRadius=0, maxRadius=0)

if circles is None:
    #This displays text if no ball is detected
    text = 'no ball detected'
    textsize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
    rows, columns, channels = img.shape
    
    #Finds origin to center text
    textorigin = ((columns//2)-(textsize[0][0]//2), textsize[0][1]+10)

    #Draw a Rectangle to help text stand out
    bottomleftvertex = (textorigin[0]-5, textorigin[1]+5)
    toprightvertex = (textorigin[0]+textsize[0][0]+5, 5)
    cv.rectangle(img, bottomleftvertex, toprightvertex, [255, 255, 255], cv.FILLED)
    
    #Draw text
    cv.putText(img, text, textorigin, cv.FONT_HERSHEY_SIMPLEX, 2, [0,0,0], 2, cv.FILLED, False)
    
else: #Ball is detected
    #Round number to whole numbers
    circles = np.uint16(np.around(circles))
    print(circles)
    
    #Draw circle around the image
    #The "best" circle is the first one in the array so that one is used
    center_x = circles[0][0][0]
    center_y = circles[0][0][1]
    radius = circles[0][0][2]
    cv.rectangle(img, (center_x-radius, center_y-radius), (center_x+radius, center_y+radius), (0, 0, 255), 2)

#Show image
cv.imshow('Result', img)

k = cv.waitKey(0)
cv.destroyAllWindows()
