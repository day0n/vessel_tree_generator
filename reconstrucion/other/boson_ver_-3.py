#这个代码用于处理重建后泊松表面顶点，将分支血管中插入主血管的顶点提取出来作为branch_surface_inside文件


import numpy as np
import open3d as o3d

file_number = 2
# 加载主血管和分支血管的中心线和半径
main_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_1.npy')
branch_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_{}.npy'.format(file_number))



# 加载主血管和分支血管的表面点坐标
main_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_1.npy')


#加载泊松重建得到的表面所有点
# 加载PLY文件
mesh = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_{}.ply".format(file_number))
# 获取顶点
vertices = np.asarray(mesh.vertices)
# 保存为npy文件
np.save('/Users/mrniu/Desktop/vessel_data/vessel_boson_vertices_{}.npy'.format(file_number),vertices)
branch_surface = np.load("/Users/mrniu/Desktop/vessel_data/vessel_boson_vertices_{}.npy".format(file_number))

# 提取主血管的中心线坐标和半径
main_centerline = main_vessel[:, :3]
main_radius = main_vessel[:, 3]

# 创建一个空的列表来存储不在主血管内部的点
branch_surface_outside = []

# 创建一个列表存储在血管内的点
branch_surface_inside = []

# 对于分支血管的每一个表面点
for point in branch_surface:
    # 计算它到主血管中心线上每一段线段的最短距离
    distances = np.sqrt(np.sum((main_centerline - point)**2, axis=1))
    # 找到最近的主血管中心线上的点
    nearest_point_index = np.argmin(distances)
    # 如果这个距离大于最近点的半径，那么这个点就不在主血管内部
    if distances[nearest_point_index] > main_radius[nearest_point_index]:
        branch_surface_outside.append(point)
    else:
        branch_surface_inside.append(point)

# 将列表转换为NumPy数组
branch_surface_outside = np.array(branch_surface_outside)
#将列表中的点存储到npy文件
np.save('/Users/mrniu/Desktop/vessel_data/branch_surface_inside{}.npy'.format(file_number),branch_surface_inside)



import open3d as o3d

pcd_inside = o3d.geometry.PointCloud()
pcd_inside.points = o3d.utility.Vector3dVector(branch_surface_inside)

# pcd_main = o3d.geometry.PointCloud()
# pcd_main.points = o3d.utility.Vector3dVector(main_surface)

# pcd_branch = o3d.geometry.PointCloud()
# pcd_branch.points = o3d.utility.Vector3dVector(branch_surface_outside)



o3d.visualization.draw_geometries([pcd_inside])