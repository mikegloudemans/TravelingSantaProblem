'''
Created on Dec 15, 2012

@author: Mike
'''
import csv
import math
import operator
import copy
import time

            
def path_length(chimneys, route):
    total_dist = 0
    for i in range(len(route)-1):
        dist = math.sqrt((chimneys[route[i]][0] - chimneys[route[i+1]][0])**2 + \
                (chimneys[route[i]][1] - chimneys[route[i+1]][1])**2)
        total_dist += dist
    return total_dist
            

if __name__ == '__main__':
    
    grid_dim = 8
    
    start = time.clock()
    
    all_chimneys = {}
    with open("santa_cities.csv") as csvfile:
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
    
    all_paths = [] # A matrix containing all mini-solutions to the problem
    total_path1_length = 0
    total_path2_length = 0
    
    solution1 = []
    solution2 = []
    
    for i in range(grid_dim):
        solution1_row = []
        solution2_row = []
        for j in range(grid_dim):
            sub_chimneys = {}
            for c in all_chimneys.keys():
                if (all_chimneys[c][0] > i*20000/grid_dim and all_chimneys[c][0] <= (i+1)*20000/grid_dim and all_chimneys[c][1] > j*20000/grid_dim and all_chimneys[c][1] <= (j+1)*20000/grid_dim):
                    sub_chimneys[c] = all_chimneys[c]
                    
            print sub_chimneys
        
            dists = {}
            for chim1 in sub_chimneys.keys():
                dists[chim1] = {}
                for chim2 in sub_chimneys.keys():
                    if chim1 == chim2:
                        continue
                    else:
                        d = math.sqrt((sub_chimneys[chim1][0] - sub_chimneys[chim2][0]) ** 2 + (sub_chimneys[chim1][1] - sub_chimneys[chim2][1]) ** 2)
                        dists[chim1][chim2] = d
                        
            print "Initialization elapsed time: ", time.clock() - start, "\n"
                        
            
            chimneys1 = copy.deepcopy(sub_chimneys)
            current_location = chimneys1.keys()[0]
            length = 0
            del chimneys1[current_location]
            full_path1 = [current_location]
            while not (chimneys1.keys() == []):
                routes = sorted(dists[current_location].items(), key = operator.itemgetter(1))
                for route in routes:
                    if route[0] in chimneys1:
                        #print current_location, " -> ", route[0]
                        current_location = route[0]
                        full_path1.append(route[0])
                        length += route[1]
                        del chimneys1[route[0]]
                        break
            
            print "Path 1 elapsed time: ", time.clock() - start        
            print "Path 1:", full_path1
            print "Num vertices path 1: ", len(full_path1)
            print "Length path 1: ", length, "\n"
            
            total_path1_length += length
            solution1_row.append(full_path1)
            
            repeat = True
            num_repeats = 0
            while repeat:
                chimneys2 = copy.deepcopy(sub_chimneys)
                current_location = chimneys2.keys()[1+num_repeats]
                length = 0
                del chimneys2[current_location]
                full_path2 = [current_location]
                last = full_path1.index(current_location)
                repeat = False
                while not (chimneys2.keys() == []):
                    routes = sorted(dists[current_location].items(), key = operator.itemgetter(1))
                    path_found = False
                    for route in routes:
                        #last = full_path1.index(current_location)
                        nextstop = full_path1.index(route[0])
                        if route[0] in chimneys2 and nextstop != last-1 and \
                            nextstop != last+1:
                            #print current_location, " -> ", route[0]
                            current_location = route[0]
                            full_path2.append(route[0])
                            length += route[1]
                            del chimneys2[route[0]]
                            last = nextstop
                            path_found = True
                            break
                    if not path_found:
                        repeat = True
                        num_repeats += 1
                        print "Failed to generate disjoint path. Trying again with different seed.\n"
                        # NOTE: Restarting will mess up the outputted path lengths.
                        break
                    
            print "Path 2: ", full_path2
            print "Num vertices path 2: ", len(full_path2)
            print "Length path 2: ", length, "\n"
            
            total_path2_length += length
            solution2_row.append(full_path2)
            
            print "Elapsed time: ", time.clock() - start, "\n"
        solution1.append(solution1_row)
        solution2.append(solution2_row)
        
    final_route1 = []
    final_route2 = []
    
    for i in range(grid_dim):
        if i % 2 == 0:
            for j in range(grid_dim):
                if not (i == 0 and j == 0):
                    old_num1 = final_route1[len(final_route1)-1]
                    new_num1 = solution1[i][j][0]
                    dist1 = math.sqrt((all_chimneys[old_num1][0] - all_chimneys[new_num1][0])**2 + (all_chimneys[old_num1][1] - all_chimneys[new_num1][1])**2)
                    total_path1_length += dist1           
                    
                    old_num2 = final_route2[len(final_route2)-1]
                    new_num2 = solution2[i][j][0]
                    dist2 = math.sqrt((all_chimneys[old_num2][0] - all_chimneys[new_num2][0])**2 + (all_chimneys[old_num2][1] - all_chimneys[new_num2][1])**2)
                    total_path2_length += dist2
                
                final_route1.extend(solution1[i][j])
                final_route2.extend(solution2[i][j])
        else:
            for j in range(grid_dim - 1,-1,-1):
                if not (i == 0 and j == 0):
                    old_num1 = final_route1[len(final_route1)-1]
                    new_num1 = solution2[i][j][0]
                    dist1 = math.sqrt((all_chimneys[old_num1][0] - all_chimneys[new_num1][0])**2 + (all_chimneys[old_num1][1] - all_chimneys[new_num1][1])**2)
                    total_path1_length += dist1                
                    
                    old_num2 = final_route2[len(final_route2)-1]
                    new_num2 = solution1[i][j][0]
                    dist2 = math.sqrt((all_chimneys[old_num2][0] - all_chimneys[new_num2][0])**2 + (all_chimneys[old_num2][1] - all_chimneys[new_num2][1])**2)
                    total_path2_length += dist2
                
                final_route1.extend(solution2[i][j])
                final_route2.extend(solution1[i][j])
                # NOTE: Output scores do not end up right in this version, because the paths are switched
                # after the computation of scores has already been completed.
    
        # Write CSV file containing results
                
    with open('results.csv', 'wb') as csvfile:
        cw = csv.writer(csvfile, delimiter=',')
        cw.writerow(['path1', 'path2'])
        for i in range(len(final_route1)):
            cw.writerow([final_route1[i],final_route2[i]])                
            
    print "Total path 1 length: ", path_length(all_chimneys, final_route1), "\n"
    print "Total path 2 length: ", path_length(all_chimneys, final_route2), "\n"
    print "Full elapsed time: ", time.clock() - start, "\n"
    
    print "Length of final routes: ", len(final_route1), " ", len(final_route2), "\n"
    

    


        