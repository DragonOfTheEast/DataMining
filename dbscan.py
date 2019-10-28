#DBSCAN
import numpy as np
import math


import time

min_pts = [2,4,6]
epsilon = [1,2,3,4]


#This function gets the input from the input data
#param out_filename: name of original file
#return: array of data
def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            temp = line[:-1].split('\t')
            lines.append(temp)
        file.close()
    return np.array(lines)


# This function returns the Euclidean distance between two data points x and y
# param x: A data point
# param y: A data point
# return: The Euclidean distance between x and y
def distance(x, y):
    dis = 0
    for i in range(1, len(x)):
        dis += math.pow((float(x[i]) - float(y[i])), 2)
    dis = math.sqrt(dis)
    return float(format(dis, '.4f'))


# This function generates a matrix of distance between each pair of points
# param data: An array of data points
# return: A distance matrix
def generate_distance_matrix(data):
    distance_matrix = []
    count = 0
    #getting distances between every pair of points
    for i in data:
        arr = []
        for  j in data:
            arr.append(distance(i,j))
        distance_matrix.append(arr)
    return np.array(distance_matrix)


#This function returns the neighbours of a point
#param data: An array of data points
#param point: the data point
#param min_dis: epsilon
#param distance_matrix: n by n matrix of distances
def get_neighbours(data, point, min_dis, distance_matrix):
    neighbours = []
    for i in range(len(data)):
        if distance_matrix[point][i] <= min_dis:
            neighbours.append(i)
    return neighbours

#This function runs the actual dbscan algorithm
#param data: An array of data points
#param clusters:an n array of the data points
#param idx: index of point
#param neighbours: neighbours of idx
#param new_idx: new possible index
#param min_pt: minimum number of points
#param eps: epsilon
#param distance_matrix: A matrix of distance between each pair of points

def get_sub_cluster(data, clusters, idx, neighbours, new_idx, min_pt, eps, distance_matrix):
    clusters[idx] = new_idx
    count = 0
    while count < len(neighbours):
        j = neighbours[count]
        if clusters[j] == 0:
            clusters[j] = new_idx
            new_neighbours = get_neighbours(data, j,eps, distance_matrix)
            if len(new_neighbours) >= min_pt:
                neighbours += new_neighbours
        elif clusters[j] == -1:
            clusters[j] = new_idx
        count+=1

#This function extracts the clusters for the data points
#param data: input data
#param esp: epsilon
#param distance_matrix: A matrix of distance between each pair of points
def extract_clusters(data, eps, min_pt, distance_matrix):
    clusters = [0] * len(data)
    idx = 0
    for i in range(len(data)):
        if clusters[i] != 0:
            continue
        neighbours = get_neighbours(data,i,eps, distance_matrix)
        if len(neighbours) >= min_pt:
            idx += 1
            get_sub_cluster(data, clusters,i,neighbours,idx,min_pt,eps, distance_matrix)
        else:
            clusters[i] = -1
    for i in range(len(clusters)):
        if clusters[i] != -1:
            clusters[i] -= 1
    return clusters

def output_to_file(clusters, string,data):
    with open("output.txt", "w") as file:
        file.write("Size of data set: " + str(len(data)) + "\n")
        for i in range(len(clusters)):
            file.write("Epsilon: " + string[i][0] + " Minimum Points: " + string[i][1] + "\n")
            for j in clusters[i]:
                file.write(str(j) + " ")
            file.write("\n\n")
        file.close()


def main():
    data = get_input("assignment3_input.txt")
    ans = []
    points = [ ]
    start_time = time.time()
    distance_matrix  = generate_distance_matrix(data)
    for i in min_pts:
        for j in epsilon:
            ans.append(extract_clusters(data,j,i, distance_matrix))
            string = str(j) + str(i)
            points.append(string)
    output_to_file(ans, points,data)



if __name__ == "__main__":
    main()
