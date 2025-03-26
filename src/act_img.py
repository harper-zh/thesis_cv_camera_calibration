from pathlib import Path
from data_manager import DataManager
from camera_calib import cam_calib
from pixel_processing import corner_pixel_extract
from image_cut_warp import warp_perspective
import cv2
import numpy as np
from PIL import Image
import piexif
# 获取当前脚本所在的目录
base_dir = Path(__file__).parent

# 定义输入和输出文件夹
img4calib = base_dir / "image4calib"
chessboard_corner = base_dir / "chessboard_corner"
img4pnp = base_dir / "image4pnp"
draw_corner = base_dir / "draw_corner"
warped_img = base_dir / "warped_img"
imgmassive = base_dir / "images"
img_with_exif = base_dir / "exif_img"
# 确保输出文件夹存在
chessboard_corner.mkdir(exist_ok=True)
draw_corner.mkdir(exist_ok=True)
warped_img.mkdir(exist_ok=True)



def main():
    # 1. 初始化数据管理器
    data = DataManager()
    imgs4pixel = list(imgmassive.glob("*_0*.JPG"))
    imgs4warp = list(imgmassive.glob("*.JPG"))
    
    for img in imgs4pixel:
        #提取角点像素坐标并储存
        pixel = corner_pixel_extract(img)
        if pixel:
            pts = np.array(pixel, dtype=np.float32)
            if pts.shape != (4, 2):  # 确保有 4 个点
                print(
                    f"Error: Expected 4 points, but got {pts.shape}. Skipping {img.name}."
                )
                continue

            id = img.stem.split("_")[0]
            print("id是:", id)
            data.add_pixel_coords(id, pixel)

            # 切割图像计算，透视变换矩阵
            match_imgs = [
                match for match in imgs4warp if match.stem.split("_")[0] == id
            ]
            print(match_imgs)

            for match in match_imgs:
                #读取原图像EXIF数据
                original_pil = Image.open(match)
                exif_dict = piexif.load(original_pil.info.get("exif", b""))

                image = cv2.imread(str(match))
                if image is None:
                    print(f"Error: Image {match} could not be loaded.")
                    continue  # 跳过处理

                warped, M = warp_perspective(image,
                                             pts,
                                             output_size=(800, 800))
                if warped is None:
                    print(
                        f"Error: Warped image is None for {match}. Skipping save."
                    )
                    continue

                output_path = warped_img / match.name
                exif_path = img_with_exif / match.name
                cv2.imwrite(str(output_path), warped)
                # 用 PIL 重新加载 OpenCV 保存的图片
                warped_pil = Image.open(output_path)

                # 重新写入 EXIF 数据
                exif_bytes = piexif.dump(exif_dict)
                warped_pil.save(exif_path, "jpeg", exif=exif_bytes)
                print(" 继承 EXIF 数据！")

                #保存变换矩阵数据
                data.add_warp_matrix(id, M)
        else:
            print("没有提取到角点")
            continue
    return data


if  __name__ == "__main__":
    data = None

    try:
        data = main()
    except KeyboardInterrupt:
        print("\n⚠️ 检测到 Ctrl+C，中断前先保存数据...")
    finally:
        if data:  # 只有 data 不为空才执行保存
            data.save("data.pkl")
            print("✅ 数据已保存！")
        else:
            print("❌ 没有数据可保存，可能 main() 没有执行完成。")
