# Research Progress
一边解决毕业论文里标定相机位置的问题，一边学习计算机视觉里相机标定的知识。记录一下进度
### 2025.03.08
相机内参标定的结果有些奇怪，畸变系数比较大，但重投影误差很小。
发现了手眼标定的AX=ZB问题，完全符合我的需求，对应cv2库里的 calibrateRobotWorldHandEye。先马一下，明天来看。
https://robotics.stackexchange.com/questions/20437/understanding-types-of-hand-eye-calibration
