#!/usr/bin/python

#import matplotlib.pyplot as plt
from random  import *
import math
''' 
First attempt at the ant algorithm to solve some simple TSP problems.  
Note: The TSP Matrices are fed in to this program as a full Matrix inthe form of a text file
'''

def readFile(libfile):
  #open the supplied file
  with open(libfile) as f:
    #content variable assumes list, with each item pandtaining a line.
    content = f.readlines()
    f.close()
    return content

def makeHananGraph(content):

  #Initialize lists for the following;

  #List of coordinates in order divided into (index,xcoord,ycoord)
  split_list = []

  x_coords = []
  y_coords = []


  #Hannan graph
  hannan_graph = []
  count_map = []

  #Make a list for each term.
  for term in content:
    split_list.append(term.split())

  #Find the x and y coordinates.
  for coordinate in split_list:
    x_coords.append(int(coordinate[1]))
    y_coords.append(int(coordinate[2]))

  #initialize a count map and real map that contains all zeros
  for x in range(max(x_coords) + 1):
    count_map.append([])
    hannan_graph.append([])
    for y in range(max(y_coords) + 1):
      hannan_graph[x].append(0)
      count_map[x].append((0,0))

  #for each coordinate, if there is a city, mark a 1 in the map.
  for i in range(len(x_coords)):
    hannan_graph[ x_coords[i]][ y_coords[i]] = 1

  #iterate through the mapa and find all points
  for i in range(len(hannan_graph)):
    for j in range(len(hannan_graph[i])):
      if hannan_graph[i][j] == 1:
        #Find new points at the intersection of horizontal and vertical lines
        #from the already existing points on the map i.e. Find Hanan Graph
        for h in range(len(hannan_graph)):
          for k in range(len(hannan_graph[h])):
            #At the points of intersection create the Steiner points
            if hannan_graph[h][k] == 1:
              if hannan_graph[i][k] != 1:
                hannan_graph[i][k] = 2
              if hannan_graph[h][j] != 1:
                hannan_graph[h][j] = 2
                break

  #print (hannan_graph) 
  #print(count_map)
  return (hannan_graph, count_map)

def reduceHananGraph(hannan_graph):
  #Use the convex hull reduction algorithm to reduce the number of steiner points
  for i in range(len(hannan_graph)):
    for j in range(len(hannan_graph[i])):
      #If the point is a Steiner point...
      if hannan_graph[i][j] == 2:

        left = (i - 1)
        right = (i + 1)
        up = (j - 1)
        down = (j + 1)

        foundLeft = False
        foundRight = False
        foundUp = False
        foundDown = False
        keep = False

        while (foundLeft == False and left >= 0):
          point = hannan_graph[left][j]
          if point == 2:
            foundLeft = True
          elif point == 1:
            keep = True
            foundLeft = True
          else:
            left = left - 1

        if not keep:

          while (foundRight == False and right < len(hannan_graph)):
            point = hannan_graph[right][j]
            if point == 2:
              foundRight = True
            elif point == 1:
              keep = True
              foundRight = True
            else:
              right = right + 1

          if not keep:
            while (foundUp == False and up >= 0):
              point = hannan_graph[i][up]
              if point == 2:
                foundUp = True
              elif point == 1:
                keep = True
                foundUp = True
              else:
                up = (up - 1)

            if not keep:
              while (foundDown == False and down < len(hannan_graph[i])):
                point = hannan_graph[i][down]
                if point == 2:
                  foundDown = True
                elif point == 1:
                  keep = True
                  foundDown = True
                else:
                  down = (down + 1)

        '''
        If the adjacent points to current Steiner point are ALL steiner points,
        find the points of intersection of these points on the horizontal axes.
        If these points are also steiner we may delete the original point.
        '''
        if (not keep) and (foundLeft or foundRight) and (foundUp or foundDown):

          if (foundLeft and foundUp):
            if hannan_graph[left][up] == 2:
              hannan_graph[i][j] = 0
          elif (foundRight and foundUp):
            if hannan_graph[right][up] == 2:
              hannan_graph[i][j] = 0
          elif (foundLeft and foundDown):
            if hannan_graph[left][down] == 2:
              hannan_graph[i][j] = 0
          elif (foundRight and foundDown):
            if hannan_graph[right][down] == 2:
              hannan_graph[i][j] = 0

  #print(hannan_graph)
  return hannan_graph


def graphToMatrix(hannan_graph, count_map):

  two_d_plane = []
  necessary_points = []
  x1_coords = []
  y1_coords = []
  x2_coords = []
  y2_coords = []
  node_degree = []

  #Assign each point in the graph an ordered number. This is used later.
  count = 0
  for i in range(len(hannan_graph)):
    for j in range(len(hannan_graph[i])):
      coord = hannan_graph[i][j]
      if coord == 1: 
        x1_coords.append(i)
        y1_coords.append(j)
        count_map[i][j] = (coord,count)
        necessary_points.append(count_map[i][j][1])
        count = count +  1
      elif coord == 2:
        x2_coords.append(i)
        y2_coords.append(j)
        count_map[i][j] = (coord,count)
        count = count +  1

  #Initialize the 2D plane
  for i in range(count):
    node_degree.append(0)
    two_d_plane.append([])
    for j in range(count):
      two_d_plane[i].append(None)

  for i in range(len(hannan_graph)):
    for j in range(len(hannan_graph[i])):
      if hannan_graph[i][j] != 0:

        left = (i - 1)
        right = (i + 1)
        up = (j - 1)
        down = (j + 1)

        foundLeft = False
        foundRight = False
        foundUp = False
        foundDown = False 
        while (foundLeft == False and left >= 0):
          point = hannan_graph[left][j]
          if point != 0:
            foundLeft = True
          else:
            left = left - 1

        while (foundRight == False and right < len(hannan_graph)):
          point = hannan_graph[right][j]
          if point != 0:
            foundRight = True
          else:
            right = right + 1
  
        while (foundUp == False and up >= 0):
          point = hannan_graph[i][up]
          if point != 0:
            foundUp = True
          else:
            up = (up - 1)
    
        while (foundDown == False and down < len(hannan_graph[i])):
          point = hannan_graph[i][down]
          if point != 0:
            foundDown = True
          else:
            down = (down + 1)

        fromPoint = count_map[i][j][1]

        if foundLeft:
          toPoint = count_map[left][j][1]
          distance = i - left
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
          node_degree[fromPoint] += 1

        if foundRight:
          toPoint = count_map[right][j][1]
          distance = right - i
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
          node_degree[fromPoint] += 1

        if foundUp:
          toPoint = count_map[i][up][1]
          distance = j - up
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
          node_degree[fromPoint] += 1

        if foundDown:
          toPoint = count_map[i][down][1]
          distance = down - j
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
          node_degree[fromPoint] += 1

  return (count_map, two_d_plane, necessary_points, node_degree, x1_coords, x2_coords, y1_coords, y2_coords)
  

def shortestPathByManhattan(two_d_plane, count_map):

  shortest_distance = []
  total_points = len(two_d_plane)
  for i in range(total_points):
    shortest_distance.append([])
    for j in range(total_points):
      shortest_distance[i].append(None)
  count = 0
  for i in range(len(count_map)):
    for j in range(len(count_map[i])):
      
      if count_map[i][j][0] == 1 or count_map[i][j][0] == 2:
        
          count += 1
          for k in range(len(count_map)):
            for l in range(len(count_map[k])):
              if count_map[k][l][0] == 1 or count_map[k][l][0] == 2:
                shortest_distance[count_map[i][j][1]][count_map[k][l][1]] = \
                        abs(i - k) +  abs(j - l)

  return shortest_distance

def placeAnt(ant_tour, source_node):
  ant_tour.append([])
  ant_tour[-1].append(source_node)
  return ant_tour



'''
Method to move an ant to the next available city, based on some 
probabilities.
'''
def move(ant):

  #find a list of free cities
  free_cities = [] 

  for city in range(len(two_d_plane[ant[-1]])):
    if two_d_plane[ant[-1]][city] != None and city not in ant:
      free_cities.append(city)
  if len(free_cities) == 0:
    ant_dead = True
  else:
    next_city = pickNext(free_cities, ant)
    if(next_city in ant):
      ant_dead = True
      print(next_city)
      #update_trails(ant, 0)
    else:
      ant.append(next_city)
      ant_dead = False

  return ant, ant_dead


'''
Method for picking random city using formula or otherwise.
'''
def pickNext(free_cities, ant):

   #Initialize denominator variable
   denominator = 0.0 
   #Make a list of the probabilites to go to the next city
   prob_next = []
   #Initialize total cost of the trails
   total_cost_of_trails = 0.0
   #Initialize the trail intensity for the next trail
   total_prime_trail_intensity = 0.0
   #let the current city be last element in the list of places the ant has visited
   current_city = ant[-1]
   #Find the values for the denominator - Pheramone of all unvisited cities from current node & pheramone
   for i in free_cities:
     trail_cost = two_d_plane[current_city][i]['length']
     pheramone = two_d_plane[current_city][i]['pheramone']

     total_cost_of_trails = pow((1.0 / (trail_cost)), alpha)
     total_prime_trail_intensity = pheramone

     denominator += total_cost_of_trails * total_prime_trail_intensity

   #for each free city....
   for i in free_cities:
     trail_cost = two_d_plane[current_city][i]['length']
     pheramone = two_d_plane[current_city][i]['pheramone']

     #Let the numerator be the current city to the power of alpha by the current 
     numerator = (pow(( 1.0 / (trail_cost)), alpha)) * (pheramone)
     prob = numerator / denominator
     #List of probabilities of travelling to the each city
     prob_next.append(prob)

   #Get the random number between 0 and the total probability
   index_number = uniform(0.0, 1.0)
     
   #Initialize the current index i.e the lower bound of the probability of choosing the given city
   current_index = 0.0

   #iterate through the list of probabilities...
   for j in range(0, len(prob_next)):
     #upper bound for P(choosing a path)
     next_index = prob_next[j] + current_index

     if current_index <= index_number and index_number <= next_index:
       next_city = free_cities[j]
     current_index = next_index
   return next_city

'''
Method for updating the trails of the ants.
'''
def updateTrails(tree_cost, unique_edges):
  for i in range(0, len(two_d_plane)):
    for j in range(0, len(two_d_plane)):
      if two_d_plane[i][j] != None:
        if ((i,j) in unique_edges):
          included_cost = evaporation_rate * (10000/tree_cost)
        else:
          included_cost = 0

        two_d_plane[i][j]['pheramone'] = ((1 - evaporation_rate) * two_d_plane[i][j]['pheramone']) \
                                         + included_cost







#Initialize all class parameters

  #Random Number for local trail updating
local = 0

  #Random number for global trail updating
globe = 0

  #Evaporation Rate.
evaporation_rate = 0.5

  #contribution factor
pheramone_factor = 1.0

  #Random probability of the equation being discarded
random_prob = 1

  #Trail intensity variable - open to fiddling and testing
mew = 1.0

  #Weight of the Pheramone of the agorithm
alpha = 5.0

content = readFile("eil51.tsp")

hannan_graph, count_map = makeHananGraph(content)

hannan_graph = reduceHananGraph(hannan_graph)

count_map, two_d_plane, necessary_points, node_degree, x1_coords, x2_coords, y1_coords, y2_coords  \
                     = graphToMatrix(hannan_graph, count_map)

SSSD = shortestPathByManhattan(two_d_plane, count_map)


length_of_shortest_path = 1000000000
smallest_tree = []
tree_costs = [0]
destination_node = necessary_points[randint(0, len(necessary_points)-1)]
source_node = necessary_points[randint(0, len(necessary_points)-1)]

ant_tour = []

ant_tour = placeAnt(ant_tour, source_node)
ant_dead = False
print(source_node)
print(destination_node)
while (not ant_dead) and (ant_tour[-1][-1] != destination_node):
  ant_tour[-1], ant_dead = move(ant_tour[-1])
print(ant_tour[-1])
print(ant_dead)
