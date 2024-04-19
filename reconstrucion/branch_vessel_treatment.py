#处理分支血管，将分支血管插入主血管后多余的点云部分给删除

import numpy as np

file_number = 2
# 加载主血管和分支血管的中心线和半径
main_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_1.npy')
branch_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_{}.npy'.format(file_number))

# 加载主血管和分支血管的表面点坐标
main_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_1.npy')
branch_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_{}.npy'.format(file_number))

# 提取主血管的中心线坐标和半径
main_centerline = main_vessel[:, :3]
main_radius = main_vessel[:, 3]

# 创建一个空的列表来存储不在主血管内部的点
branch_surface_outside = []

#核心处理思路是遍历分支血管每个表面点，对于每个表面点如果在主血管里面就选中为inside点不在就是outside点
#判断是否在主血管中的思路是将该点到中心线的最短路距离和离中心线最近点的距离比较，大就是outside小就是inside
# 对于分支血管的每一个表面点
for point in branch_surface:
    # 计算它到主血管中心线上每一段线段的最短距离
    distances = np.sqrt(np.sum((main_centerline - point)**2, axis=1))
    # 找到最近的主血管中心线上的点
    nearest_point_index = np.argmin(distances)
    # 如果这个距离大于最近点的半径，那么这个点就不在主血管内部
    if distances[nearest_point_index] > main_radius[nearest_point_index]:
        branch_surface_outside.append(point)

# 将列表转换为NumPy数组
branch_surface_outside = np.array(branch_surface_outside)

# 保存结果
np.save('/Users/mrniu/Desktop/vessel_data/branch_surface_outside{}.npy'.format(file_number),branch_surface_outside)
#画出npy文件
import open3d as o3d
# 创建PointCloud对象
pcd_main = o3d.geometry.PointCloud()
pcd_main.points = o3d.utility.Vector3dVector(main_surface)

pcd_branch = o3d.geometry.PointCloud()
pcd_branch.points = o3d.utility.Vector3dVector(branch_surface_outside)

# 显示点云
o3d.visualization.draw_geometries([pcd_main, pcd_branch])