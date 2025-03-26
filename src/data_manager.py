import pickle


class DataManager:

    def __init__(self):

        self.pixel_coords = {}  # 像素坐标 {(img_name): [(u,v), (u,v)]}
        self.world_coords = {}  # ref坐标系下的点3d坐标 {(img_name): [(X,Y,Z), (X,Y,Z)]}
        self.camera_coords = {}  #相机相对于样品的变换矩阵{(img_name): M}
        self.euler_matrices = {}  # 该位姿的变换矩阵 {(img_name): M}
        self.warp_matrices = {}  #变换到正方形图片的矩阵{{img:M}}
        self.pose = {}  #机器人的六点位姿{(img_name): [x,y,z,a,b,c]}

    def add_pixel_coords(self, img_name, coords):
        self.pixel_coords[img_name] = coords  #像素坐标

    def add_3d_points(self, img_name, points):
        self.world_coords[img_name] = points

    def add_camera(self, img_name, matrix):
        self.camera_coords[img_name] = matrix

    def add_euler_matrix(self, img_name, matrix):
        self.euler_matrices[img_name] = matrix

    def add_warp_matrix(self, img_name, matrix):
        self.warp_matrices[img_name] = matrix
    def add_pose(self,img_name,pose):
        self.pose[img_name] = pose
    def save(self, filename="data.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)  # 保存整个对象

    @staticmethod
    def load(filename="data.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)  # 加载对象
        except FileNotFoundError:
            print("No previous data found, creating new DataManager.")
            return DataManager()  # 如果文件不存在，返回新对象
