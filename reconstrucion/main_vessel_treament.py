#处理的是主血管，思路是将主血管看成分支血管，然后将分支血管在主血管中的三个洞给挖空，这样分支血管就能插进来
import numpy as np
branch_surface_inside = []

import open3d as o3d
for file_number in range(2, 5):
    # 加载主血管和分支血管的中心线和半径
    branch_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_1.npy')
    main_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_{}.npy'.format(file_number))

    # 加载主血管和分支血管的表面点坐标
    branch_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_1.npy')
    main_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_{}.npy'.format(file_number))

    # 提取主血管的中心线坐标和半径
    main_centerline = main_vessel[:, :3]
    main_radius = main_vessel[:, 3]

    # 创建一个空的列表来存储不在主血管内部的点
    branch_surface_outside = []

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
branch_surface_intside = np.array(branch_surface_inside)

main_vessel = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_1.npy')
main_surface = np.load('/Users/mrniu/Desktop/vessel_data/surface_points_1.npy')
#将inside的点在main_surface点云中删除


# 找出 main_surface 中存在于 branch_surface_inside 的点
mask = np.isin(main_surface, branch_surface_inside).all(axis=1)

# 使用布尔索引来删除这些点
main_surface = main_surface[~mask]


np.save('/Users/mrniu/Desktop/vessel_data/processed_surface_points1.npy', main_surface)

import matplotlib.pyplot as plt


main_cloud = o3d.geometry.PointCloud()

main_cloud.points = o3d.utility.Vector3dVector(main_surface)

o3d.visualization.draw_geometries([main_cloud])