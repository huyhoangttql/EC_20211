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

def add_sur(xa,xb,ya,yb):
    for i in range (int(xa*5),int(xb*5)+1,1):
        vor.add_points([[i/5,ya]])
        vor.add_points([[i/5,yb]])
    for i in range (int(ya*5),int(yb*5)+1,1):
        vor.add_points([[xa,i/5]])
        vor.add_points([[xb,i/5]])

#tạo ra các điểm ban đầu để khởi tạo voronoi map
points = np.array([[0, 0], [0, 5], [5, 6], [0, 6]])

vor = Voronoi(points, incremental=True)


def line_create(dynX, dynY, speedX, speedY, lower_limit, upper_limit):
    x = np.linspace(lower_limit/100, upper_limit/100, 5)
    y = -speedX/speedY * x + (speedX*dynX/100 + speedY*(600-dynY)/100)/speedY
    # y1 = 4/5 * x - 7/5 - 0.1
    for i in range(5):
        vor.add_points([[x[i], y[i]]])
    # vor.add_points([[x[i], y1[i]]])

line_create(300, 500, -4, 5, 280, 300)

add_point(1,2,4,5)
add_point(2,2.5,2,3)
add_point(1.5,2,1,1.5)
add_point(4,4.5,3.5,4.5)
add_point(3,3.5,3,4)
# add_point(2.8,3.5,0.8,1)
# add_point(2.8,2.8,1,2)

# add_point(2,2.5,3,3.7)
# add_point(2.25,2.85,2.7,3)
add_sur(0,5,0,6)

#tạo một numpy array mới từ vor.vertices, thêm 1 cột toàn 0
#nếu một điểm là bên trong hình của mình, thì cột [2] của nó sẽ là 1
vor_check = np.hstack((vor.vertices, np.zeros((vor.vertices.shape[0], 1), dtype=vor.vertices.dtype)))

#hàm kiểm tra nếu một điểm là bên trong thì vor_check[i][2] sẽ là 1
def checkinside(xa,xb,ya,yb):
    for i in range(vor.vertices.shape[0]):
        if (vor_check[i][0] > xa) and (vor_check[i][0] < xb) and (vor_check[i][1] > ya) and (vor_check[i][1] < yb):
            vor_check[i][2] = 1

checkinside(1,2,4,5)
checkinside(2,2.5,2,3)
checkinside(1.5,2,1,1.5)
checkinside(4,4.5,3.5,4.5)
checkinside(3,3.5,3,4)
# checkinside(2.8,3.5,0.8,1)




# checkinside(2,2.5,3,3.7)
# checkinside(2.25,2.85,2.7,3)
# print(vor_check)

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
    if vpair[0] >= 0 and vpair[1] >= 0 and (vor_check[vpair[0]][2] != 1) and (vor_check[vpair[1]][2] != 1):
        graph.add_edge(vpair[0], vpair[1], distance(vor.vertices[vpair[0]], vor.vertices[vpair[1]]))
        graph.add_edge(vpair[1], vpair[0], distance(vor.vertices[vpair[0]], vor.vertices[vpair[1]]))

#điểm bắt đầu và kết thúc, biểu thị bởi chấm hồng
start = [2.5, 0.62]
end = [3, 4.3]

def distance_list(start, end):
    return np.sqrt(np.abs((start[0] - end[0])**2 - (start[1] - end[1])**2))

start_end = distance_list(start,end)
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
    if (distance(start, vor_node[i]) < min_dist_start) and (vor_check[i][2] != 1 and (start_end > distance(vor_node[i], end))) :
        # and (distance(start,end) > distance(vor_node[i], end))
        min_dist_start = distance(start, vor_node[i])
        start_graph = i
    if (distance(end, vor_node[i]) < min_dist_end) and (vor_check[i][2] != 1):
        min_dist_end = distance(end, vor_node[i])
        end_graph = i
    
#nối từ điểm start và end đến điểm gần nhất trong voronoi vertices
plt.plot([start[0], vor_node[start_graph][0]], [start[1], vor_node[start_graph][1]], 'k', linewidth=2)
plt.plot([end[0], vor_node[end_graph][0]], [end[1], vor_node[end_graph][1]], 'k', linewidth=2)

#liệt kê các đỉnh đi qua từ start_graph đến end_graph
node_list = find_path(graph, start_graph, end_graph).nodes
# print(node_list)
# print(vor_node[node_list[0]])
for i in node_list:
    plt.plot([vor.vertices[i][0]] , [vor.vertices[i][1]], marker='o', markersize=10, color="red")
list_vertices1 =[]
for i in node_list:
    list_vertices1.append([round(100*vor_node[i][0],1),round(600-100*vor_node[i][1],1)])
list_vertices1.append([end[0]*100, 600 - end[1]*100])
list_vertices1.insert(0,[270.0,526.0])
# list_vertices1.insert(0,[250,548])
print(list_vertices1)
plt.show()
list_node1 = []
for i in range(len(vor_node)):
    list_node1.append([round(100*vor_node[i][0],1),round(600-100*vor_node[i][1],1)])
# print(list_node1)
# plt.show()

def toofarpoint(list_vertices):
    i = len(list_vertices) -1
    while (i >= 1):
    # for i in range(len(list_vertices) - 1):
        ver_dist = distance_list(list_vertices[i], list_vertices[i-1])
        # print(ver_dist)
        if (ver_dist > 10):
            x = np.linspace(list_vertices[i-1][0], list_vertices[i][0], int(ver_dist/10))
            y = np.linspace(list_vertices[i-1][1], list_vertices[i][1], int(ver_dist/10))
            for j in range(int(ver_dist/10)):
                # print(i+j)
                list_vertices.insert(i+j, [x[j], y[j]])
            # if i > 5: 
            #     i = i - 4
        i = i - 1

toofarpoint(list_vertices1)
# print(distance_list(list_vertices1[0], list_vertices1[1]))
print("--------------------------------")
print(list_vertices1)
# for i in range(len(list_vertices1) - 1):
# print(distance_list(list_vertices1[30], list_vertices1[31]))
    