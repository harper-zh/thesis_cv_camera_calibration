import itertools
import numpy as np
from scipy.spatial.transform import Rotation as R

euler = np.array([-20,-10,0,10,20])
#欧拉角组合
euler_combos = list(itertools.product(euler,repeat = 3))
# print(euler_combos)

#生成网格点
grid_size = 50
grid_extend = [-2,-1,0,1,2]
grid = np.array([(i*grid_size,j*grid_size) for i in grid_extend for j in grid_extend])
grid_reshaped = grid.reshape(len(grid_extend), len(grid_extend),2)
for i in range(len(grid_extend)):
    if i % 2 == 1:  # 奇数列从上到下
        grid_reshaped[i,:] = grid_reshaped[i,::-1]
grid_3d = np.insert(grid_reshaped, 2, 0, axis=2)
grid_flatten = grid_3d.reshape(-1, 3)
#倒序的网格点
reverse_grid = grid_flatten[::-1]
# print(reverse_grid)

#旋转矩阵
rotations = [
    R.from_euler('zyx', angles, degrees=True) for angles in euler_combos
]

T_list = []
for rotation in rotations:
    R_matrix = rotation.as_matrix()

    i = rotations.index(rotation)  #第i种姿态
    T = np.eye(4)
    T[:3, :3] = R_matrix
    if i % 2 == 0:
        translation = grid_flatten
    else:
        translation = reverse_grid
    for g in translation:
        T[:3, 3] = g
        T_list.append(T)
print(len(T_list))


def object_points_calculate(T_ref, T_pose, point_board):
    """
    说明：计算某一位姿下棋盘格点在参考坐标系下的3d坐标
    T_ref:参考坐标系相对于base的变换矩阵
    T_pose该位姿下tcp相对于base的变换矩阵
    point_board：棋盘格点在tcp坐标系里的坐标
    """
    # 将3D点转换为齐次坐标
    origin_points_h = np.hstack(
        [point_board, np.ones((point_board.shape[0], 1))])
    # 使用矩阵乘法进行坐标变换
    #去掉齐次坐标中的最后一列，转换回普通的3D坐标
    object_points_base_inv = np.dot(T_pose, origin_points_h.T)
    object_points_o1 = np.dot(np.linalg.inv(T_ref), object_points_base_inv).T
    return object_points_o1[:, :3]
