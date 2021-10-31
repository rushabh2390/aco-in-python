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
