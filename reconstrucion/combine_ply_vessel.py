import open3d as o3d


mesh1 = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_1.ply")
mesh2 = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_2.ply")
mesh3 = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_3.ply")
mesh4 = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_4.ply")


mesh_combined = mesh1 + mesh2 + mesh3 + mesh4

# 保存合并后的PLY文件，使用ASCII编码
o3d.io.write_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel.ply", mesh_combined, write_ascii=True)

o3d.visualization.draw_geometries([mesh_combined])