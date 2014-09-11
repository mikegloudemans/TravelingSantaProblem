'''
Created on Jan 2, 2013

@author: Mike
'''

import csv
import math
import random
import sys
import time
import operator

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
    # Define energy computation function (if same data structure is used, may be same as previous one.)
    pass

def tweak_path(route,dct1,dct2,NN,chimneys):
    # Make a modification to the given path. Return the new path and the resulting change in score.
    
    # TODO: Use the 2-opt technique.
    pass
    
def initialize_routes(subset, start, end1, end2):
    # Idea: store edges as two dictionaries - a forward direction and backwards direction dictionary. Or one
    # dict that contains a tuple with the previous and next edges would probably be even better.
    
    route1 = [s for s in subset if s != end1 and s != start]
    route1 = [start] + route1 + [end1]
    
    #route2 = [s for s]
    dRoute1 = {}
    # TODO: Update dictionary data structure
    
    pass
    

def compute_route(chimneys, subset, start, end1, end2):
    # Compute an efficient route through a subset of the chimneys using simulated annealing.
    
    init_routes = initialize_routes(subset, start, end1, end2)
    
    pass

if __name__ == '__main__':
    xdim = 10
    ydim = 10
    
    all_chimneys = {}
    with open("santa_cities.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ',')
        next(cr)
        for row in cr:
            all_chimneys[int(row[0])] = [int(row[1]),int(row[2])]
            
    # Load nearest neighbors list

    nearest_neighbors = []    
    with open("Neighbors.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ",")
        for row in cr:
            nearest_neighbors.append([int(r.strip())-1 for r in row])

    for i in range(ydim):
        for j in range(xdim):
            # Depending on the bin that we are in, determine a starting and ending point for each of the
            # two paths. (Only the ending point should be different.) Then, find the subset of chimneys
            # belonging to this bin and pass the chimneys and endpoints to a compute_route function, which generates
            # two disjoint routes traversing the points using simulated annealing.
            
            # First, determine chimneys that are actually in this bin.
            
            chimney_subset = []            
            for chim in all_chimneys.keys():
                if all_chimneys[chim][0] > i * (20000.0/xdim) and all_chimneys[chim][0] <= (i+1)*(20000.0/xdim) \
                    and all_chimneys[chim][1] > j * (20000.0/ydim) and all_chimneys[chim][1] <= (j+1)*(20000.0/ydim):
                    chimney_subset.append((chim, all_chimneys[0], all_chimneys[1]))
            
            # TODO: Fix cases in which the start and end chimneys are selected to be the same thing!
            
            
            if (i % 2 == 0):
                # Move to the right along even-numbered rows
                if (j == 0):
                    # We're at the start of the row
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(2))
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(1), reverse = True)
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
                elif (j == xdim-1):       
                    # We're at the end of the row           
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(1))
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(2), reverse = True)
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
                else:
                    # We're in the middle of the row 
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(1))
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(1), reverse = True)
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
            else:
                # Move to the left along odd-numbered rows.
                if (j == 0):
                    # We're at the end of the row (moving left)
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(1), reverse = True)
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(2), reverse = True)
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
                elif (j == xdim-1):       
                    # We're at the start of the row (moving right)         
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(2))
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(1))
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
                else:
                    # We're in the middle of the row 
                    chimney_subset = sorted(chimney_subset, key = operator.itemgetter(1), reverse = True)
                    start = chimney_subset[0][0]
                    remaining = [c for c in chimney_subset if c != start]
                    remaining = sorted(remaining, key = operator.itemgetter(1))
                    end1 = remaining[0][0]
                    end2 = remaining[1][0]
                    
            compute_route(all_chimneys, chimney_subset, start, end1, end2)