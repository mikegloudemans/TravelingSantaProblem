'''
Created on Dec 20, 2012

@author: Mike
'''

import csv
import operator
import sys

if __name__ == '__main__':
    
    srcfile = "results/Annealed_results.csv"
    
    # Load routes
    route1_indices = {}
    route2_indices = {}  
    with open(srcfile) as csvfile:
        cr = csv.reader(csvfile, delimiter = ",")
        next(cr)
        i = 0
        for row in cr:
            route1_indices[int(row[0])] = i
            route2_indices[int(row[1])] = i
            i += 1
            
    for i in range(150000):
        if not (i in route1_indices and i in route2_indices):
            print "Path invalid. Not all elements are included in both paths."
            print i
            sys.exit()
    
    items1 = sorted(route1_indices.items(), key = operator.itemgetter(1))
            
    for i in range(149999):
        if abs(route2_indices[items1[i][0]] - route2_indices[items1[i+1][0]])==1:
            print "Path invalid. Duplicate edges:"
            print items1[i][0], items1[i+1][0]
            sys.exit()
            
    print "Path is valid."
            
            
    