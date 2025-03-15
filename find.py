import cv2
import numpy as np

# 读取图像
img = cv2.imread('bg.jpg')

# 转为灰度图
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


# 返回值：1.得到的阈值，2.阈值化后的图像
retval,threshold_img = cv2.threshold(gray_img,20,255,cv2.THRESH_BINARY)


cv2.imshow("img",img)
#cv2.imshow("gray_img",gray_img)
cv2.imshow("threshold_img",threshold_img)



contours, hierarchy = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (255, 0, 0), 2)

cnt_len = cv2.arcLength(contours[0], True)
cnt = cv2.approxPolyDP(contours[0], 0.02*cnt_len, True)
if len(cnt) == 4:
    cv2.drawContours(img, [cnt], -1, (255, 255, 0), 3 )
for point in cnt:
        x, y = point[0]
        cv2.circle(img, (x, y), 8, (0,0,255), -1)
cv2.imshow("img1",img)


cv2.waitKey(0)
cv2.destroyAllWindows()