#!/usr/bin/python

x_coords = []
y_coords = []
real_map = []
count_map = []
two_d_plane = []

mew = 1.0

def readFile(libfile):

  #open the supplied file
  with open(libfile) as f:
    #content variable assumes list, with each item pandtaining a line.
    content = f.readlines()
    f.close()

  split_list = []
  resulting_map = []
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
    real_map.append([])
    for y in range(max(y_coords) + 1):
      real_map[x].append(0)
      count_map[x].append((0,0))

  #for each coordinate, if there is a city, mark a 1 in the map.
  for i in range(len(x_coords)):
    real_map[ x_coords[i]][ y_coords[i]] = 1
  
  #iterate through the mapa and find all points
  for i in range(len(real_map)):
    for j in range(len(real_map[i])):
      if real_map[i][j] == 1:
        #Find new points at the intersection of horizontal and vertical lines
        #from the already existing points on the map i.e. Find Hanan Graph
        for h in range(len(real_map)):
          for k in range(len(real_map[h])):
            #At the points of intersection create the Steiner points
            if real_map[h][k] == 1:
              if real_map[i][k] != 1:
                real_map[i][k] = 2
              if real_map[h][j] != 1:
                real_map[h][j] = 2
                break

  #Use the convex hull reduction algorithm to reduce the number of steiner points
  for i in range(len(real_map)):
    for j in range(len(real_map[i])):
      #If the point is a Steiner point...
      if real_map[i][j] == 2:

        left = (i - 1)
        right = (i + 1)
        up = (j - 1)
        down = (j + 1)

        foundLeft = False
        foundRight = False
        foundUp = False
        foundDown = False 
        keep = False       

        '''
        search left, right, up and down for the next point on 
        horizontal and vertical axes. If the next point in any direction
        is not a steiner point keep the steiner point.
		'''
		while (foundLeft == False and left >= 0):
          point = real_map[left][j]
          if point == 2:
            foundLeft = True
          elif point == 1:
            keep = True
            foundLeft = True
          else:
            left = left - 1

        if not keep:

          while (foundRight == False and right < len(real_map)):
            point = real_map[right][j]
            if point == 2:
              foundRight = True
            elif point == 1:
              keep = True
              foundRight = True
            else:
              right = right + 1
  
          if not keep:
            while (foundUp == False and up >= 0):
              point = real_map[i][up]
              if point == 2:
                foundUp = True
              elif point == 1:
                keep = True
                foundUp = True
              else:
                up = (up - 1)
    
            if not keep:
              while (foundDown == False and down < len(real_map[i])):
                point = real_map[i][down]
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
            if real_map[left][up] == 2:
              real_map[i][j] = 0
          elif (foundRight and foundUp):
            if real_map[right][up] == 2:
              real_map[i][j] = 0
          elif (foundLeft and foundDown):
            if real_map[left][down] == 2:
              real_map[i][j] = 0
          elif (foundRight and foundDown):
            if real_map[right][down] == 2:
              real_map[i][j] = 0

  count = 0
  for i in range(len(real_map)):
    for j in range(len(real_map[i])):
      coord = real_map[i][j]
      if coord == 1 or coord == 2:
        count_map[i][j] = (coord,count)
        count = count +	1
		
  for i in range(count):
    two_d_plane.append([])
    for j in range(count):
      two_d_plane[i].append(None)

  for i in range(len(real_map)):
    for j in range(len(real_map[i])):
      if real_map[i][j] != 0:

        left = (i - 1)
        right = (i + 1)
        up = (j - 1)
        down = (j + 1)

        foundLeft = False
        foundRight = False
        foundUp = False
        foundDown = False 

        while (foundLeft == False and left >= 0):
          point = real_map[left][j]
          if point != 0:
            foundLeft = True
          else:
            left = left - 1

        while (foundRight == False and right < len(real_map)):
          point = real_map[right][j]
          if point != 0:
            foundRight = True
          else:
            right = right + 1
  
        while (foundUp == False and up >= 0):
          point = real_map[i][up]
          if point != 0:
            foundUp = True
          else:
            up = (up - 1)
    
        while (foundDown == False and down < len(real_map[i])):
          point = real_map[i][down]
          if point != 0:
            foundDown = True
          else:
            down = (down + 1)

        fromPoint = count_map[i][j][1]

        if foundLeft:
          toPoint = count_map[left][j][1]
          distance = i - left
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
		  
        if foundRight:
          toPoint = count_map[right][j][1]
          distance = right - i
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}
		
        if foundUp:
          toPoint = count_map[i][up][1]
          distance = j - up
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}

        if foundDown:
          toPoint = count_map[i][down][1]
          distance = down - j
          two_d_plane[fromPoint][toPoint] = {'length' : distance,'pheramone' : mew}


readFile("eil15.tsp")
for i in real_map:
  print(i)
  
for j in count_map:
  print(j)
  
for k in two_d_plane:
  for u in k:
    if u != None:
      print(u)
  print("--------------")