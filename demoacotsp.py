import numpy as np
from numpy import inf

import random
import datetime
import re
import ast
import datetime
np.seterr(divide='ignore', invalid='ignore')
import os
import csv



def calculate_nextnode(visited,startnode,pheromone,visibility,n,alpha,beta):
    prob=.1*np.zeros(n)
    prob_up=.1*np.zeros(n)
    temp_pheromone=pheromone[startnode]
    temp_visibility=visibility[startnode]
    temp_sum=0.0
    
    for j in range(n):
        if(j not in visited):
            prob_up[j]=(temp_pheromone[j]**alpha)* (temp_visibility[j] ** beta)
            temp_sum+=(temp_pheromone[j]**alpha)* (temp_visibility[j] ** beta)
    for j in range(n):
        if(j not in visited):
            prob[j]=prob_up[j]/temp_sum
              
    next_city=np.argmax(prob)
    return next_city

def parth_travesing(m,n,pheromone,visibility,best_tour,best_cost,first_ant,last_ant,all_path,tourcost,alpha,beta,d):
    for i in range(first_ant,(last_ant+1)):
        visited=[]
        path=[]
        visited.append(i)
        current_city=i
       
        tour_cost=0.0
        for j in range(n):
            next_city=calculate_nextnode(visited,current_city,pheromone,visibility,n,alpha,beta)
            visited.append(next_city)
            tour_cost+=d[current_city,next_city]
            path.append((current_city,next_city))
            current_city=next_city
        path.append((next_city,i))
        visited.append(i)
        tourcost.append(tour_cost)
        all_path.append(path)
        if(best_cost>tour_cost):
            best_cost=tour_cost
            best_tour=visited
    return all_path,tourcost,best_cost,best_tour


def start_data(ant_no,file):
#given values for the problems
    
    start =  datetime.datetime.now()
    # intialization part
    with open(file, 'r') as filehandle:
        places = filehandle.read()
    places= places.replace("\n","],[")
    places =  "[["+re.sub("\s+"," ",places).replace(" ",",").replace("[,","[")+"]]"
    places = ast.literal_eval(places.replace("[[,","[["))
    d=np.array(places)
#     d = np.array([[0,39,22,59,54,33,57,32,89,73,29,46,16,83,120,45,24,32,36,25,38,16,43,21,50,57,46,72,121,73],
# [39,0,20,20,81,8,49,64,63,84,10,61,25,49,81,81,58,16,72,60,78,24,69,18,75,88,68,44,83,52],
# [22,20,0,39,74,18,60,44,71,73,11,46,6,61,99,61,37,10,51,40,59,5,62,7,57,78,51,51,100,56],
# [59,20,39,0,93,27,51,81,48,80,30,69,45,32,61,97,75,31,89,78,97,44,83,38,84,100,77,31,63,42],
# [54,81,74,93,0,73,43,56,104,76,76,77,69,111,72,46,56,84,49,53,33,69,12,69,64,7,69,122,73,114],
# [33,8,18,27,73,0,45,61,71,88,8,63,22,57,87,77,54,18,68,56,71,20,61,13,75,80,68,52,90,60],
# [57,49,60,51,43,45,0,85,88,115,52,103,60,75,64,85,79,63,83,78,70,58,38,52,103,49,102,81,69,92],
# [32,64,44,81,56,61,85,0,74,43,55,23,40,81,97,17,8,50,8,7,23,41,53,48,19,53,17,70,92,63],
# [89,63,71,48,104,71,88,74,0,38,69,51,75,16,35,75,77,61,77,80,90,76,116,76,58,98,57,19,33,16],
# [73,84,73,80,76,88,115,43,38,0,81,28,72,53,55,38,49,70,42,50,53,75,83,80,24,69,27,49,51,39],
# [29,10,11,30,76,8,52,55,69,81,0,55,16,57,91,71,48,11,62,50,68,14,64,9,67,81,61,49,93,56],
# [46,61,46,69,77,63,103,23,51,28,55,0,44,59,81,32,26,46,29,29,45,47,76,53,15,73,9,49,77,40],
# [16,25,6,45,69,22,60,40,75,72,16,44,0,67,105,56,33,16,46,35,53,2,57,9,54,72,48,57,106,60],
# [83,49,61,32,111,57,75,81,16,53,57,59,67,0,39,88,82,51,87,85,103,67,113,65,70,109,67,12,39,19],
# [120,81,99,61,72,87,64,97,35,55,91,81,105,39,0,84,104,90,93,104,90,104,82,99,79,70,82,50,4,51],
# [45,81,61,97,46,77,85,17,75,38,71,32,56,88,84,0,23,67,9,21,15,57,48,64,19,41,23,80,81,70],
# [24,58,37,75,56,54,79,8,77,49,48,26,33,82,104,23,0,44,14,3,25,34,51,41,25,54,23,70,100,65],
# [32,16,10,32,84,18,63,50,61,70,11,46,16,51,90,67,44,0,58,47,67,16,72,15,59,88,52,42,90,47],
# [36,72,51,89,49,68,83,8,77,42,62,29,46,87,93,9,14,58,0,12,16,48,48,55,19,45,21,77,89,69],
# [25,60,40,78,53,56,78,7,80,50,50,29,35,85,104,21,3,47,12,0,22,36,48,43,26,51,24,73,100,68],
# [38,78,59,97,33,71,70,23,90,53,68,45,53,103,90,15,25,67,16,22,0,54,33,59,33,31,37,93,88,84],
# [16,24,5,44,69,20,58,41,76,75,14,47,2,67,104,57,34,16,48,36,54,0,57,7,56,72,50,57,105,61],
# [43,69,62,83,12,61,38,53,116,83,64,76,57,113,82,48,51,72,48,48,33,57,0,57,66,18,69,113,84,115],
# [21,18,7,38,69,13,52,48,76,80,9,53,9,65,99,64,41,15,55,43,59,7,57,0,63,74,57,57,101,61],
# [50,75,57,84,64,75,103,19,58,24,67,15,54,70,79,19,25,59,19,26,33,56,66,63,0,59,7,61,74,52],
# [57,88,78,100,7,80,49,53,98,69,81,73,72,109,70,41,54,88,45,51,31,72,18,74,59,0,64,117,71,107],
# [46,68,51,77,69,68,102,17,57,27,61,9,48,67,82,23,23,52,21,24,37,50,69,57,7,64,0,57,77,48],
# [72,44,51,31,122,52,81,70,19,49,49,49,57,12,50,80,70,42,77,73,93,57,113,57,61,117,57,0,49,11],
# [121,83,100,63,73,90,69,92,33,51,93,77,106,39,4,81,100,90,89,100,88,105,84,101,74,71,77,49,0,48],
# [73,52,56,42,114,60,92,63,16,39,56,40,60,19,51,70,65,47,69,68,84,61,115,61,52,107,48,11,48,0]])


    iteration = 10
    n_ants = ant_no
    n_citys = len(d) 

    m = n_ants
    n = n_citys
    e = .5         #evaporation rate
    alpha = 1     #pheromone factor
    beta = 1       #visibility factor

    while(m>n):
        m=m//2
    ALOT = 1e6
    d[d == 0.0 ] = ALOT
    visibility = 1/d
    pheromone = 0.1*np.ones((n,n))
    bestcostiter=[]
    best_cost=np.inf
    best_tour=None
    cities= [x for x in range(n)]
    start_city_chunks=[]
    for i in range(0,len(cities),m):
        start_city_chunks.append(cities[i:(i+m)])
    for ite in range(iteration):
        all_path=[]
        tourcost=[]
        
        rute = np.ones((m,n+1))
        for start_city_chunk in start_city_chunks:
            for i in range(len(start_city_chunk)):
                for j in range((n+1)):
                    if(j==0 or j==(n)):
                        rute[i,j]=i
                    else:
                        rute[i,j]=1
        for start_city_chunk in start_city_chunks:
            all_path,tourcost,best_cost,best_tour=parth_travesing(m,n,pheromone,visibility,best_tour,best_cost,start_city_chunk[0],start_city_chunk[-1],all_path,tourcost,alpha,beta,d)

        pheromone= e * pheromone
        for i in range(n):
            for j in range(n):
                if(i<=j):
                    dt=0.0
                    for k  in range(len(all_path)):
                        if((i,j) in all_path[k] or (j,i) in all_path[k]):
                            dt+=1/tourcost[k]
                    pheromone[i,j]+=dt
                    pheromone[j,i]+=dt
        bestcostiter.append(best_cost)  
    end =  datetime.datetime.now()
    duration=end-start
    mincost = min(bestcostiter)
    
    return(n,m,mincost,best_tour, duration)

f = open('resultrtsp.csv', 'w')
path = "tspdataset"
os.chdir(path)

writer = csv.writer(f)
writer.writerow(["Filename", "Iteration","No. of Cities","Ant No","No.Of Actual Ant","best tour","Cost","Execution Time"])
for file in os.listdir():
    print("----------------------------------------")
    print("file name",file) 
    print("----------------------------------------")
    antno=[10,20,30,40]
    times=[]
    bestcostiters=[]
    bests_tours=[]
    for x in antno:
        city,aano,cost,tour,duration=start_data(x,file)
        bestcostiters.append(cost)
        bests_tours.append(tour)
        times.append(str(duration))
        print(file,10,city,x,aano,tour,cost,str(duration))
        writer.writerow([file,10,city,x,aano,tour,cost,str(duration)])
    print("ant no",antno)
    print("time duration",times)
    print("bestcostiters",bestcostiters)
    print("bestcostiters",bestcostiters)
    print("besttour",bests_tours)
f.close()
