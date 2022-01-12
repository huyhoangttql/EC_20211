import numpy as np
import matplotlib.pyplot as plt
import json
from dijkstar import Graph, find_path
from dijkstar.algorithm import PathInfo
from scipy.spatial import Voronoi, voronoi_plot_2d

def vor(start, end, json_file):

    #hàm để add point bị giới hạn bởi (xa,xb) và (ya,yb)
    def add_point(xa,xb,ya,yb):
        for i in range (int(xa*6),int(xb*6)+1,1):
            vor.add_points([[i/6,ya]])
            vor.add_points([[i/6,yb]])
        for i in range (int(ya*6),int(yb*6)+1,1):
            vor.add_points([[xa,i/6]])
            vor.add_points([[xb,i/6]])

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
    # add_point(1,2,4,5)
    # add_point(2,2.5,2,3)
    # add_point(1.5,2,1,1.5)
    # add_point(4,4.5,3.5,4.5)
    # add_point(3,3.5,3,4)

    f = open(json_file)
    data = json.load(f)
    for i in data:
        if (i["Dynamic"] == "0"):
            xa = int(i["startpointX"])/100
            xb = xa + int(i["length"])/100
            ya = 6 - int(i["startpointY"])/100
            yb = ya - int(i["width"])/100
            if(xa > xb):
                xa, xb = xb, xa
            if(ya > yb):
                ya, yb = yb, ya
            print(xa, xb, ya, yb)
            add_point(xa, xb, ya, yb)
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

    # checkinside(1,2,4,5)
    # checkinside(2,2.5,2,3)
    # checkinside(1.5,2,1,1.5)
    # checkinside(4,4.5,3.5,4.5)
    # checkinside(3,3.5,3,4)
    for i in data:
        if (i["Dynamic"] == "0"):
            xa = int(i["startpointX"])/100
            xb = xa + int(i["length"])/100
            ya = 6 - int(i["startpointY"])/100
            yb = ya - int(i["width"])/100
            if(xa > xb):
                xa, xb = xb, xa
            if(ya > yb):
                ya, yb = yb, ya
            checkinside(xa, xb, ya, yb)
    f.close()
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
    # start = [2, 0]
    # end = [3, 4.3]
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
        if (distance(start, vor_node[i]) < min_dist_start) and (vor_check[i][2] != 1):
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

    # plt.show()
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


    return list_vertices, list_node

# vor([2, 1], [3, 4.3], 'input4.json')