#将处理好的主血管和分支血管表面点云构造法线并且重建表面
#处理法线思路是对于一个中心线上的点，我们首先在点云找到以这个点的半径r为圆的一圈点，对于这些点他们和中心线改点连线就是表面点的法线
#这里我们使用了KD树加快了搜索时间
#法向量是通过将这个点的坐标减去给定点（x, y, z）的坐标得到的。
#我们将这个法向量归一化（即除以它的模长），然后添加到normals列表中。归一化是为了得到一个长度为1的单位向量，这样可以方便后续的计算
#

import numpy as np
import open3d as o3d
from scipy.spatial import KDTree


file = 2
# data_center_r = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_{}.npy'.format(file))
# data_surface = np.load('/Users/mrniu/Desktop/vessel_data/branch_surface_outside{}.npy'.format(file))
# 将data_surface转换为一维数组
data_center_r = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_combined.npy')
data_surface = np.load('/Users/mrniu/Desktop/vessel_data/data_combined.npy')

data_surface = data_surface.reshape(-1, 3)


# 创建KDTree  用于快速查找点 极大减少了时间复杂度
tree = KDTree(data_surface)


result = []
normals = []


for i, point in enumerate(data_center_r.reshape(-1, 4)):
    x, y, z, r = point
  
    indices = tree.query_ball_point([x, y, z], r)
    # 排除中心线上的点
    indices = [index for index in indices if index != i]
    
    for index in indices:
        
        dist = np.linalg.norm(data_surface[index] - np.array([x, y, z]))
        
        if np.isclose(dist, r, atol=0):
            #
            result.append(data_surface[index])
            
            normal = data_surface[index] - np.array([x, y, z])
            normals.append(normal / np.linalg.norm(normal))  # 归一化

# 将结果列表和法线列表转换为NumPy数组
result = np.array(result)
normals = np.array(normals)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(result)
pcd.normals = o3d.utility.Vector3dVector(normals)

pcd.paint_uniform_color([0, 0, 1])
o3d.visualization.draw_geometries([pcd])


pcd.paint_uniform_color([0.5, 0, 0])

# 泊松重建表面
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

o3d.io.write_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel.ply".format(file),mesh, write_ascii=True)


o3d.visualization.draw_geometries([mesh])
