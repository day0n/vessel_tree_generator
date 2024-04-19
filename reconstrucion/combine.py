#合并分支血管中心线半径文件和表面点云文件
#合并中心线半径文件用于法线构造
#将处理好的主血管和分支血管表面点云合并成一整个血管，用于之后的泊松重建
#都是为了将小的血管合并成总的重建做准备

import numpy as np

data1 = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_1.npy')
data2 = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_2.npy')
data3 = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_3.npy')
data4 = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_4.npy')


data_combined = np.concatenate((data1, data2, data3, data4), axis=0)



np.save('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_combined.npy', data_combined)


print(data_combined.shape)


data1 = np.load('/Users/mrniu/Desktop/vessel_data/processed_surface_points1.npy')
data2 = np.load('/Users/mrniu/Desktop/vessel_data/branch_surface_outside2.npy')
data3 = np.load('/Users/mrniu/Desktop/vessel_data/branch_surface_outside3.npy')
data4 = np.load('/Users/mrniu/Desktop/vessel_data/branch_surface_outside4.npy')


data_combined = np.concatenate((data1, data2, data3, data4), axis=0)


np.save('/Users/mrniu/Desktop/vessel_data/data_combined.npy', data_combined)

#画出data_combined.npy和centerline_and_radius_combined.npy
import open3d as o3d


pcd_centerline = o3d.geometry.PointCloud()
pcd_centerline.points = o3d.utility.Vector3dVector(data_combined[:, :3])

# 设置点的颜色
pcd_centerline.paint_uniform_color([1, 0, 0])  


vis = o3d.visualization.Visualizer()
vis.create_window()


vis.add_geometry(pcd_centerline)

# 设置点的大小
render_option = vis.get_render_option()
render_option.point_size = 0.01  # 可以调整这个值来改变点的大小


vis.run()


vis.destroy_window()



print(data_combined.shape)