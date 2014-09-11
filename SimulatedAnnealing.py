'''
Created on Dec 18, 2012

@author: Mike
'''

import csv
import math
import random
import sys
import time
import operator

# TODO: Define a function to get the distance between two chimneys

# TODO: Try some sort of "Tabu search" technique to keep from repeatedly falling into the same
# traps

# TODO: Modify the algorithm so that it preferentially finds improvements for the better of
# the two algorithms.

# TODO: Think about ways to get around the fact that one path restricts the other from making.
# potentially useful intermediate transitions.

def dist(chimneys, point1, point2):
    # Given the indices of two chimneys, compute the distance between them.
    d = math.sqrt((chimneys[point1][0]-chimneys[point2][0])**2 + (chimneys[point1][1]-chimneys[point2][1])**2)
    return d

# Taken from online at "Psychic Origami"
def P(prev_score,next_score,temperature):
    if next_score < prev_score:
        return 1.0
    else:
        # TODO: Adjust this function to allow a higher probability of more "radical" transitions.
        return math.exp( -abs(next_score-prev_score)/temperature )
    
def update_temp(temp):
        return temp
        #return temp*(0.99999999)
    
def energy(chimneys, route):
    total_dist = 0
    for i in range(len(route)-1):
        d = math.sqrt((chimneys[route[i]][0] - chimneys[route[i+1]][0])**2 + \
                (chimneys[route[i]][1] - chimneys[route[i+1]][1])**2)
        total_dist += d
    return total_dist

def tweak_path(route,dct1,dct2,NN,chimneys):
    
    # Make a modification to the given path. Return the new path and the resulting change in score.
    
    # TODO: Modify this algorithm so that it uses the 2-opt technique instead.

    while True:
        
        #start = time.clock()

        #print "1.0", time.clock()-start
        r1 = random.randint(1,len(route)-3) # Think it over to verify if it really should be -3.
        #print "1.1", time.clock()-start
        point1 = route[r1]
        #print "1.2", time.clock()-start
        point2 = NN[point1][random.randint(0,99)]  # TODO: Tweak the number of neighbors used to improve results.
        #print "1.3", time.clock()-start
        # TODO: Fix the error that will occur if the randomly selected point is at the END of the full route!
        r2 = dct1[point2]
        vertices1 = route[r1-1:r1+2]
        vertices2 = route[r2-1:r2+2]
        
        if r2 == len(route)-1 or r2 == 0:
            continue
        
#        print r1, r2
#        print point1, point2
#        print vertices1, vertices2
#        print dct2[vertices1[0]],dct2[vertices1[1]],dct2[vertices1[2]]
#        print dct2[vertices2[0]],dct2[vertices2[1]],dct2[vertices2[2]]
#        
        #print "2", time.clock()-start
        
        if (abs(dct2[vertices1[0]]-dct2[vertices2[1]])==1 or \
            abs(dct2[vertices1[2]]-dct2[vertices2[1]])==1 or \
            abs(dct2[vertices2[0]]-dct2[vertices1[1]])==1 or \
            abs(dct2[vertices2[2]]-dct2[vertices1[1]])==1):
            continue
        
        #print "3", time.clock()-start
        
        # TODO: Verify that this special case handling actually works!        
        if r2-r1==1:
            old_energy = dist(chimneys, vertices1[0],vertices1[1]) + dist(chimneys, vertices2[1],vertices2[2])
            new_energy = dist(chimneys, vertices1[0],vertices1[2]) + dist(chimneys, vertices2[0],vertices2[2])
        elif r1-r2==1:
            old_energy = dist(chimneys, vertices1[1],vertices1[2]) + dist(chimneys, vertices2[0],vertices2[1])
            new_energy = dist(chimneys, vertices1[0],vertices1[2]) + dist(chimneys, vertices2[0],vertices2[2])
        else:        
            old_energy = dist(chimneys, vertices1[0], vertices1[1]) + dist(chimneys, vertices1[1], vertices1[2]) + \
                         dist(chimneys, vertices2[0], vertices2[1]) + dist(chimneys, vertices2[1], vertices2[2])
            
            new_energy = dist(chimneys, vertices1[0], vertices2[1]) + dist(chimneys, vertices1[1], vertices2[2]) + \
                        dist(chimneys, vertices2[0], vertices1[1]) + dist(chimneys, vertices2[1], vertices1[2])
        
        #print "4", time.clock()-start
        
#        new_route[r1] = point2
#        new_route[r2] = point1
        
        swap = (point1, point2)
        
        # Technically I don't think it's really even necessary to pass back the indices.
        # Fix this later.
        indices = (r1,r2)
           
        delta_energy = new_energy - old_energy
        
        #print "5", time.clock()-start
              
        return (indices, delta_energy, swap)



if __name__ == '__main__':
    
    
    # Specify parameters:
    
    kmax = 100000000       # Number of iterations to run
    T = 5           # Starting temperature - at the moment this is arbitrary
    
    # Load stuff:
    
    # Load chimneys 
    
    all_chimneys = {}
    with open("santa_cities.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ',')
        next(cr)
        for row in cr:
            all_chimneys[int(row[0])] = [int(row[1]),int(row[2])]
   
    # Load routes
    route1 = []
    route2 = []    
    with open("results/Annealed_results.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ",")
        next(cr)
        for row in cr:
            route1.append(int(row[0]))
            route2.append(int(row[1]))
            
    # Load nearest neighbors list

    nearest_neighbors = []    
    with open("Neighbors.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ",")
        for row in cr:
            nearest_neighbors.append([int(r.strip())-1 for r in row])
    
    print "Starting simulated annealing:"
    
    profile_x = []
    profile_y = []
    
    # Dictionaries to store the index of each chimney in either array
    s1_d = {}
    s2_d = {}
    for i in range(len(route1)):
        s1_d[route1[i]] = i
        s2_d[route2[i]] = i
            
    s1 = route1                     # Initialize state 1
    s2 = route2                     # Initialize state 2
    e1 = energy(all_chimneys, route1)             # Compute initial energy
    e2 = energy(all_chimneys, route2)
    sbest = [route1, route2]        # Initial best solution
    ebest = max(e1, e2)
    k = 0                           # Number of iterations completed
    while k < kmax:
        start = time.clock()
        T = update_temp(T)
        if (e1 > e2):
            (indices1, delta_e1, swaps1) = tweak_path(s1,s1_d,s2_d,nearest_neighbors,all_chimneys)
            e1new = e1 + delta_e1
            if P(e1, e1new, T) > random.random():
                e1 = e1new
                # Swap items in s1
                tmp1 = s1[indices1[0]]
                s1[indices1[0]] = s1[indices1[1]]
                s1[indices1[1]] = tmp1
                # Swap indices of the two list elements in the dictionary.
                temp1 = s1_d[swaps1[0]]
                s1_d[swaps1[0]] = s1_d[swaps1[1]]
                s1_d[swaps1[1]] = temp1
        else:
            (indices2, delta_e2, swaps2) = tweak_path(s2,s2_d,s1_d,nearest_neighbors, all_chimneys)
            e2new = e2 + delta_e2
            if P(e2, e2new, T) > random.random():
                e2 = e2new
                # Swap items in s2
                tmp2 = s2[indices2[0]]
                s2[indices2[0]] = s2[indices2[1]]
                s2[indices2[1]] = tmp2
                # Swap indices of the two list elements in the dictionary.
                temp2 = s2_d[swaps2[0]]
                s2_d[swaps2[0]] = s2_d[swaps2[1]]
                s2_d[swaps2[1]] = temp2
        if max(e1,e2) < ebest:
            sbest = [s1, s2]
            ebest = max(e1,e2)
        k = k + 1
        if k % 10000 == 0:
            profile_x.append(k)
            profile_y.append(ebest)
            print "Iterations:", k, "Best so far:", ebest
            if k%100000 == 0:
                print "Path 1 score:", energy(all_chimneys, s1)
                print "Path 2 score:", energy(all_chimneys, s2)
                print "Temp:", T
                
            # Debugging: check validity of current solution (dictionaries)

#            for i in range(149999):
#                if abs(s2_d[s1[i]] - s2_d[s1[i+1]])==1:
#                    print "Num iterations:", k
#                    print "Path invalid. Duplicate edges:"
#                    print s1[i], s1[i+1]
#                    sys.exit()
                    

    
    with open('results/Annealed_results4.csv', 'wb') as csvfile:
        cw = csv.writer(csvfile, delimiter=',')
        cw.writerow(['path1', 'path2'])
        for i in range(len(s1)):
            cw.writerow([s1[i],s2[i]])   

    with open('profiles/Annealed_results4.csv', 'wb') as csvfile:
        cw = csv.writer(csvfile, delimiter=',')
        for i in range(len(profile_x)):
            cw.writerow([profile_x[i],profile_y[i]])
    
    #TODO: Proofread code to make sure functions are doing what I want them to do.
