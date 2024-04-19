import numpy as np
import open3d as o3d


centerline_and_radius = np.load('/Users/mrniu/Desktop/vessel_data/centerline_and_radius_combined.npy')
surface_points = np.load("/Users/mrniu/Desktop/vessel_data/data_combined.npy")


pcd_centerline = o3d.geometry.PointCloud()
pcd_centerline.points = o3d.utility.Vector3dVector(centerline_and_radius[:, :3])

pcd_surface = o3d.geometry.PointCloud()
for surface in surface_points:
    print(type(slice))
    print(np.shape(slice))
    for slice in surface:
        pcd_surface.points.extend(o3d.utility.Vector3dVector(slice))

# 设置点的颜色
pcd_centerline.paint_uniform_color([1, 0, 0])  # 红色表示中心线的点
pcd_surface.paint_uniform_color([0, 1, 0])  # 绿色表示表面的点


vis = o3d.visualization.Visualizer()
vis.create_window()


vis.add_geometry(pcd_centerline)
vis.add_geometry(pcd_surface)

# 设置点的大小
render_option = vis.get_render_option()
render_option.point_size = 0.01  # 可以调整这个值来改变点的大小


vis.run()


vis.destroy_window()