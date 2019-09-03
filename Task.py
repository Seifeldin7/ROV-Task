import cv2
import numpy as np
import math
recr_length = 0.0
recb_length = 0
recr_real = 15.0
recb_real = 0
loc_x=0
loc_y=0
def nothing(x):
    pass


#cv2.namedWindow("Tracking")
#cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
#cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
#cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

######decrease resolution######
resized = cv2.imread('rect2.jpg')


#l_h = cv2.getTrackbarPos("LH", "Tracking")
#l_s = cv2.getTrackbarPos("LS", "Tracking")
#l_v = cv2.getTrackbarPos("LV", "Tracking")
    #
#u_h = cv2.getTrackbarPos("UH", "Tracking")
#u_s = cv2.getTrackbarPos("US", "Tracking")
#u_v = cv2.getTrackbarPos("UV", "Tracking")

######Mask for blue and red rectangles######
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
l_r = np.array([170,50,50])
u_r = np.array([180,255,255])
l_b = np.array([110,50,50])
u_b = np.array([130,255,255])
mask_blue = cv2.inRange(hsv, l_b, u_b)
mask_red = cv2.inRange(hsv, l_r, u_r)

res_red = cv2.bitwise_and(resized, resized, mask=mask_red)
res_blue= cv2.bitwise_and(resized, resized, mask=mask_blue)
######Contours######
#blurred = cv2.pyrMeanShiftFiltering(res_red,91,111)
imgGrey = cv2.cvtColor(res_red, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 0, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(str(len(contours)))
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(resized, [approx], 0, (0, 0, 0), 5)
    rotatedRect = cv2.minAreaRect(contour)
    angle = rotatedRect[2]
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    #if len(approx) == 4:
    x1 ,y1, w, h = cv2.boundingRect(approx)
    if w < 50 or h <50: #noise
        continue
    if angle >= -92 and angle <= -80 or angle >=-1 and angle <=1 or angle <=90.0 and angle >=85:

        if w > h:
            recr_length =recr_length + w + 40
        else:
            recr_length =recr_length + h +40
    else:
        recr_length += math.sqrt(math.pow(w,2)+math.pow(h,2))


cv2.drawContours(res_red,contours,0,(0,255,0),3)
cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
cv2.imshow('Contours',res_red)
imgGrey = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 0, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(str(len(contours)))
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(resized, [approx], 0, (0, 0, 0), 5)
    rotatedRect = cv2.minAreaRect(contour)
    angle = rotatedRect[2]
    #print(angle)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    #if len(approx) == 4:
    x1 ,y1, w, h = cv2.boundingRect(approx)

    if w < 80 or h <80: #noise
        continue
    else:
        loc_x=x1
        loc_y=y1
    if angle >= -92 and angle <= -80 or angle >=-1 and angle <=1 or angle <=90.0 and angle >=85:

        if w > h:
            recb_length += w
        else:
            recb_length += h
    else:
        recb_length += math.sqrt(math.pow(w,2)+math.pow(h,2))


#cv2.drawContours(res_red,contours,0,(0,255,0),3)
#cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
#cv2.imshow('Contours',res_red)
#cv2.imshow("imgGrey", imgGrey)
#cv2.imshow("mask", mask)
#cv2.imshow("res", res)

recb_real = (recr_real*recb_length)/recr_length
print(recb_real)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(resized,str(recb_real),(loc_x,loc_y),font,3,(255,255,255),10)
cv2.namedWindow("Resized image", cv2.WINDOW_NORMAL)
cv2.imshow("Resized image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
