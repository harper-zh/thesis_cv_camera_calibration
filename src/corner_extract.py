import numpy as np
import cv2
import os

def corner_pixel_extract(file,file_path,output_path):
    """
    检测样品的四个角点，并返回角点的像素坐标
    file是照片的名字
    file_path是照片所处文件夹的路径
    output_path是绘制四边形后照片的保存路径
    """
    points = []
    img = cv2.imread(file_path)  
    # 转为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊（减少噪声）
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 二值化处理
    retval, threshold_img = cv2.threshold(blurred, 35, 255, cv2.THRESH_BINARY)
    # 形态学操作，去除小噪点
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)
    # 轮廓检测
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        peri = cv2.arcLength(contour, True)  # 计算轮廓周长
        # print(peri)
        if peri> 100:
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)  # 轮廓逼近

            if len(approx) == 4:  # 只保留四边形
                print("检测到四边形，顶点坐标：")
                
                
                for point in approx:
                    x, y = point[0]
                    points.append([x, y])
                    print(f"({x}, {y})")
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 标记四边形顶点（红色）
                cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)  # 绿色绘制四边形
            # 保存检测结果
    
                cv2.imwrite(f'{output_path}\\{file}', img)

                print(f"处理完成，结果已保存: {output_path}")
    return points