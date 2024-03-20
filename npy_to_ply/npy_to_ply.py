import numpy as np
from scipy import interpolate
from plyfile import PlyData, PlyElement

data = np.load("/Users/mrniu/Desktop/GitHub/vessel_tree_generator/npy_to_ply/data/1000points.npy") 
print(data.shape)   

reshaped_data = data.reshape(-1, 3)

print(reshaped_data)
print(reshaped_data.shape)

ply_data = np.array([tuple(x) for x in reshaped_data], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])

vertex = PlyElement.describe(ply_data, 'vertex')

ply_data = PlyData([vertex])

#这里需要先保存为中转文件，然后再将这个文件转换为ascii格式的ply文件
ply_data.write('output1.ply')

import open3d as o3d


pcd = o3d.io.read_point_cloud("output1.ply")

#设置颜色为血红色，RGB值为[153, 0, 0]
pcd.paint_uniform_color([153 / 255, 0, 0])

pcd.estimate_normals()

o3d.io.write_point_cloud("output.ply", pcd, write_ascii=True)

#删除中转文件
import os
os.remove("output1.ply")


o3d.visualization.draw_geometries([pcd])