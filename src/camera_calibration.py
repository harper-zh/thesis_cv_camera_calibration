from camera_calib import cam_calib
import cv2
from pathlib import Path


# 获取当前脚本所在的目录
base_dir = Path(__file__).parent
img_folder = base_dir / "image4calib"
output_path = base_dir / "chessboard_corner"

#标定相机内参
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100,
            0.0001)
camera_matrix, distortion_coeffs = cam_calib(w=9,
                                             h=11,
                                             square_size=45,
                                             criteria=criteria,
                                             path=img_folder,
                                             outpath=output_path)
