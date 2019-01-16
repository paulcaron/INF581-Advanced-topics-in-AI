from numpy import *
from utils import tile2pos, pos2tile
from copy import *

red_squares = [0, 3, 6, 8, 14, 18, 20]
green_squares = [0, 5, 6, 7, 11, 18, 19]

def get_neighbors(i):
    if i==-1.:
        return [10, 4]
    neighbors = []
    pos = tile2pos(i)
    x = pos[0]
    y = pos[1]
    if x>0:
        neighbors.append(pos2tile(array([x-1, y])))
    if y>0:
        neighbors.append(pos2tile(array([x, y-1])))
    if x<4:
        neighbors.append(pos2tile(array([x+1, y])))
    if y<4:
        neighbors.append(pos2tile(array([x, y+1])))

    return neighbors

def get_two_neighbors(i):
    neighbors = get_neighbors(i)
    neighbors2 = [get_neighbors(j) for j in neighbors]
    neighbors2_to_return = []
    for neighbor2_set in neighbors2:
        for neighbor2 in neighbor2_set:
            neighbors2_to_return.append(neighbor2)
    return unique(neighbors2_to_return)

def get_conditional_probability(i, x):
    if i in red_squares:
        if x[0]==0.:
            p1 = 0.1
        else:
            p1 = 0.9
    else:
        if x[0]==0.:
            p1 = 1
        else:
            return 0
    if i in green_squares:
          if x[1]==0.:
              p2 = 0.2
          else:
              p2 = 0.8
    else:
        if x[1]==0.:
            p2 = 1
        else:
            return 0  
    return p1*p2

def explore_paths(paths,X,y,p=1.,t=0):
    '''
        Explore paths.
                          
        Explore all possible paths that the target may take, store them in 'paths' with an associated score (probability).

        Parameters
        ----------

        X: the T observations
        y: the path, of length T,
        p: score/probability of the path y.
        t: time-step of the path
        paths: reference to a list, when t = T - 1, then add (y,p) to this list, else update y and p 
               and recursively call the function with (paths,X,y,p,t+1)
    '''
    T = X.shape[0]

    # if path complete, add it and return
    # ...
    if t==T:
        paths.append((y,p))
        return

    # if probability 0, return
    # ...
    if p==0:
        return

    # for each state i:
    #   y_new <- mark it into the path y (N.B. good to make a copy(.) of the path here)
    #   p_new <- get the probabilitiy associated with it
    #   call the same function: explore_paths(paths,X,y_new,p_new,t+1) ...
    neighbors = get_neighbors(y[-1])
    if y[-1] == -1.:
        y = []
    n = len(neighbors)
    p_new = [get_conditional_probability(i,X[t]) for i in neighbors]
    s = sum(p_new)
    if s!=0:
        p_new_2 = [p_new[i]/s for i in range(n)]
        p_new = p_new_2
    for i in range(n):
        y_new = list(y.copy())
        y_new.append(neighbors[i])
        explore_paths(paths,X,array(y_new),p*p_new[i],t+1)

        
        
#####################################

# Load some paths and their observations
X = loadtxt('X.dat')
y = loadtxt('y.dat', dtype=int)

seed = 0
X = X[seed:seed+5,:]
print(X)
y = y[seed:seed+5]

# Obtain all *possible* paths and a relative score (probability) associated with each
T,D = X.shape
paths = []
explore_paths(paths,X,y=-ones(T))

# Print out these paths and their joint-mode score (normalized to a distribution, st they sum to 1) ...
# (TODO), e.g.,  
#   [  4   3   8  13  18], 0.8   (equiv. grid path : [(0, 4), (0, 3), (1, 3), (2, 3), (3, 3)])
#   [  4   9   8  7  6],   0.2   (equiv. grid path : [(0, 4), (1, 4), (1, 3), (1, 2), (1, 1)])

# Print out the marginas dist. of the final node and associated scores (normalized to a distribution, st they sum to 1)
# (TODO), e.g.,
# 6,  0.95 (equiv. grid square: 1,1)
# 18, 0.05 (equiv. grid square: 3,3)

neighbors2 = get_two_neighbors(2)
min_p = (sqrt(3)-1) / (sqrt(10)-1)
prob = zeros(25)
for path in paths:
    prob[path[0][4]] += path[1]
res = [0,0]
for i in neighbors2:
    if prob[i]>res[0]:
        res[0] = prob[i]
        res[1] = i
        
"""
if res[0]>min_p:
    print("Yes " + str(res[1]))
else:
    print("No")
"""
# Decide whether to 'pounce' or not
# (TODO), e.g., 'Yes'
if res[0]>min_p:
    print("Yes " + str(res[1]))
else:
    print("No")
# Compare to the true path (Evaluation):
print("y = %s, i.e., tile path: %s, finishing at y = %d (tile: %s)" % (str(y), str([(tile2pos(y[i])[0],tile2pos(y[i])[1]) for i in range(len(y))]),y[-1],str(tile2pos(y[-1]))))

