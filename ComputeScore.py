'''
Created on Dec 17, 2012

@author: Mike
'''
import csv
import math

def path_length(chimneys, route):
    total_dist = 0
    for i in range(len(route)-1):
        dist = math.sqrt((chimneys[route[i]][0] - chimneys[route[i+1]][0])**2 + \
                (chimneys[route[i]][1] - chimneys[route[i+1]][1])**2)
        total_dist += dist
    return total_dist

if __name__ == '__main__':
    all_chimneys = {}
    with open("C:\\Users\\Mike\\Desktop\\Santa_Cities\\santa_cities.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ',')
        next(cr)
#        i = 0
        for row in cr:
#            if i > 999:
#                break
#            if (int(row[1])>2000 or int(row[2])>2000):
#                continue
            all_chimneys[int(row[0])] = [int(row[1]),int(row[2])]
#            i += 1

    route1 = []
    route2 = []
    
    with open("Annealed_results10_10milliontrials_50NN_temp10.csv") as csvfile:
        cr = csv.reader(csvfile, delimiter = ",")
        next(cr)
        for row in cr:
            route1.append(int(row[0]))
            route2.append(int(row[1]))
            
    print "Route 1 length: ", path_length(all_chimneys, route1)
    print "Route 2 length: ", path_length(all_chimneys, route2)