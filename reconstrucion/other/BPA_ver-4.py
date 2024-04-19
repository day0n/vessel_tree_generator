#用于生成处理泊松重建生成的模型，将模型中的一部分删除
import numpy as np
import open3d as o3d
from scipy.spatial import KDTree
file = 2
# 加载PLY文件
mesh = o3d.io.read_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_{}.ply".format(file))

# 加载要删除的顶点
to_delete_vertices = np.load('/Users/mrniu/Desktop/vessel_data/branch_surface_inside{}.npy'.format(file))

# 创建KDTree
tree = KDTree(np.asarray(mesh.vertices))

# 找到要删除的顶点在原始顶点列表中的索引
to_delete = tree.query(to_delete_vertices, k=1)[1]

# 创建新的顶点列表
new_vertices = [v for i, v in enumerate(mesh.vertices) if i not in to_delete]

# 创建新的三角形列表
new_triangles = [t for t in mesh.triangles if not any(v in to_delete for v in t)]

# 更新三角形的顶点索引
for t in new_triangles:
    for i in range(3):
        t[i] -= sum(v < t[i] for v in to_delete)

# 更新网格
mesh.vertices = o3d.utility.Vector3dVector(new_vertices)
mesh.triangles = o3d.utility.Vector3iVector(new_triangles)

#颜色设置为血红色
mesh.paint_uniform_color([1, 0, 0])

# 显示新的网格
o3d.visualization.draw_geometries([mesh])

o3d.io.write_triangle_mesh("/Users/mrniu/Desktop/vessel_data/vessel_{}.ply".format(file),mesh, write_ascii=True)