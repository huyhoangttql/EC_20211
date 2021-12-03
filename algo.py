import numpy as np
import matplotlib.pyplot as plt
from dijkstar import Graph, find_path
from dijkstar.algorithm import PathInfo
from scipy.spatial import Voronoi, voronoi_plot_2d

#hàm để add point bị giới hạn bởi (xa,xb) và (ya,yb)
def add_point(xa,xb,ya,yb):
    for i in range (int(xa*10),int(xb*10)+1,1):
        vor.add_points([[i/10,ya]])
        vor.add_points([[i/10,yb]])
    for i in range (int(ya*10),int(yb*10)+1,1):
        vor.add_points([[xa,i/10]])
        vor.add_points([[xb,i/10]])

#tạo ra các điểm ban đầu để khởi tạo voronoi map
points = np.array([[0, 0], [0, 5], [5, 6], [0, 6]])

vor = Voronoi(points, incremental=True)
add_point(1,2,4,5)
add_point(2,2.5,2,3)
add_point(1.5,2,1,1.5)
add_point(4,4.5,3.5,4.5)
# add_point(2,2.5,3,3.7)
# add_point(2.25,2.85,2.7,3)
add_point(0,5,0,6)

fig = voronoi_plot_2d(vor)

#hàm tính khoảng cách euclid
def distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))   

#khởi tạo 1 cái graph
#kiểm tra cái ridge_vertices đều >= 0 thì thêm vào edge vào graph
#mình phải thêm edge [0][1] và edge [1][0] để tạo thành đồ thị vô hướng
#còn nếu chỉ thêm edge 1 lần thì nó là đồ thị có hướng
graph = Graph()
for vpair in vor.ridge_vertices:
    if vpair[0] >= 0 and vpair[1] >= 0:
        graph.add_edge(vpair[0], vpair[1], distance(vor.vertices[vpair[0]], vor.vertices[vpair[1]]))
        graph.add_edge(vpair[1], vpair[0], distance(vor.vertices[vpair[0]], vor.vertices[vpair[1]]))

#điểm bắt đầu và kết thúc, biểu thị bởi chấm hồng
start = [2, 0]
end = [4, 3]
plt.plot([start[0]],[start[1]], marker='o', markersize=15, color="pink")
plt.plot([end[0]],[end[1]], marker='o', markersize=15, color="pink")

#điểm bắt đầu và kết thúc trong số vertices của voronoi
#ở đây mình sẽ tìm node gần nhất với start và node gần nhất với end
vor_node = vor.vertices
start_graph = 0
end_graph = 0
min_dist_start = 100000
min_dist_end = 100000
for i in range(len(vor_node)):
    if distance(start, vor_node[i]) < min_dist_start:
        min_dist_start = distance(start, vor_node[i])
        start_graph = i
    if distance(end, vor_node[i]) < min_dist_end:
        min_dist_end = distance(end, vor_node[i])
        end_graph = i
    
#nối từ điểm start và end đến điểm gần nhất trong voronoi vertices
plt.plot([start[0], vor_node[start_graph][0]], [start[1], vor_node[start_graph][1]], 'k', linewidth=2)
plt.plot([end[0], vor_node[end_graph][0]], [end[1], vor_node[end_graph][1]], 'k', linewidth=2)

#liệt kê các đỉnh đi qua từ start_graph đến end_graph
node_list = find_path(graph, start_graph, end_graph).nodes
for i in node_list:
    plt.plot([vor.vertices[i][0]] , [vor.vertices[i][1]], marker='o', markersize=10, color="red")
# print(node_list)
list_vertices =[]
for i in node_list:
    list_vertices.append([round(100*vor_node[i][0],1),round(600-100*vor_node[i][1],1)])
# print(list_vertices)
# plt.show()
list_node = []
for i in range(len(vor_node)):
    list_node.append([round(100*vor_node[i][0],1),round(600-100*vor_node[i][1],1)])
# print(list_node)