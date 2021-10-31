import numpy as np
from numpy import inf
import random
import re
import ast
import datetime
np.seterr(divide='ignore', invalid='ignore')
import os
import csv

def RouletteWheelSelection(P):
    C=np.cumsum(P)
##    j=np.where(random.random()<=C)[0][0]
    j=np.argmax(P)
    return j
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
        
def createModel(places):
    model={}
    model["w"] = ast.literal_eval(re.search("w=\[\[(\d|\,|\]|\[)+\,", places).group().replace("w=","")[:-1])
    model["d"] = ast.literal_eval(re.search("d=\[\[(\d|\,|\]|\[)+\,", places).group().replace("d=","")[:-1])
    model["m"] = int(re.search("m=\d+", places).group().replace("m=",""))
#     model["m"]=25
#     model["d"]=[[0,2,24,26,30,2,24,25,35,22,22,9,25,52,63,50,3,24,22,29,23,5,25,37,12],
# [2,0,22,20,35,22,4,5,29,22,35,44,25,60,22,35,24,22,29,30,5,5,7,19,22],
# [24,22,0,23,20,9,24,22,35,22,29,22,24,25,39,24,22,33,50,6,52,30,21,37,12],
# [26,20,23,0,29,5,24,36,39,25,34,3,20,20,35,22,6,52,63,22,20,35,36,39,17],
# [30,35,20,29,0,24,25,35,22,9,22,25,33,22,25,3,24,23,22,26,34,62,37,22,9],
# [2,22,9,5,24,0,35,22,25,24,29,33,6,50,82,25,22,33,24,29,23,26,12,25,14],
# [24,4,24,24,25,35,0,35,22,44,3,50,60,38,40,22,23,29,24,33,6,80,37,12,44],
# [25,5,22,36,35,22,35,0,24,22,25,29,36,40,3,50,22,35,32,23,5,24,3,15,12],
# [35,29,35,39,22,25,22,24,0,25,3,24,22,80,32,25,52,22,24,25,39,22,16,22,14],
# [22,22,22,25,9,24,44,22,25,0,40,29,32,60,25,28,33,8,9,22,24,25,15,12,40],
# [22,35,29,34,22,29,3,25,3,40,0,30,22,22,29,30,26,35,24,20,29,22,17,5,40],
# [9,44,22,3,25,33,50,29,24,29,30,0,22,33,64,92,25,25,29,30,20,50,50,29,14],
# [25,25,24,20,33,6,60,36,22,32,22,22,0,25,33,24,29,22,33,24,29,32,60,36,22],
# [52,60,25,20,22,50,38,40,80,60,22,33,25,0,29,35,50,44,32,24,23,28,38,40,80],
# [63,22,39,35,25,82,40,3,32,25,29,64,33,29,0,22,22,50,25,62,24,22,40,3,31],
# [50,35,24,22,3,25,22,50,25,28,30,92,24,35,22,0,29,23,50,24,29,25,12,50,27],
# [3,24,22,6,24,22,23,22,52,33,26,25,29,50,22,29,0,24,39,50,22,50,13,22,52],
# [24,22,33,52,23,33,29,35,22,8,35,25,22,44,50,23,24,0,29,32,24,25,19,37,12],
# [22,29,50,63,22,24,24,32,24,9,24,29,33,32,25,50,39,29,0,29,26,35,24,31,14],
# [29,30,6,22,26,29,33,23,25,22,20,30,24,24,62,24,50,32,29,0,28,24,33,23,27],
# [23,5,52,20,34,23,6,5,39,24,29,20,29,23,24,29,22,24,26,28,0,35,6,7,39],
# [5,5,30,35,62,26,80,24,22,25,22,50,32,28,22,25,50,25,35,24,35,0,80,14,12],
# [25,7,21,36,37,12,37,3,16,15,17,50,60,38,40,12,13,19,24,33,6,80,0,10,15],
# [37,19,37,39,22,25,12,15,22,12,5,29,36,40,3,50,22,37,31,23,7,14,10,0,25],
# [12,22,12,17,9,14,44,12,14,40,40,14,22,80,31,27,52,12,14,27,39,12,15,25,0]]

#     model["w"]=[[0,8,5,14,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [8,0,0,0,0,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [5,0,0,0,0,0,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [14,0,0,0,0,0,0,2,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [12,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,23,0,0,0,0,0,0,0,0,8,13,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,2,0,0,0,0,0,0,0,0,29,35,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,4,0,0,0,0,0,0,0,0,0,12,15,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,0,7,9,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,0,10,3,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,20,35,5,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,26,31],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,0,0,0,0,0]]
    model["n"]=len(model["w"][0])
    return model
    

def myCost(p,model):
    n=model["n"]
    w=model["w"]
    d=model["d"]
    z=0
    for i in range((n-1)):
        for j in range((i+1),n):
            z=z+w[i][j]*d[p[i]][p[j]]
    return z
    


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

def start_data(ant_no,file):
#given values for the problems

    start =  datetime.datetime.now()
    with open(file, 'r') as filehandle:
        places = filehandle.read()
    
    places= places.replace("\n","").replace("]]","]],")
    model=createModel(places)
    nVar=model["n"]
    MaxIt = 10
    nAnt = ant_no
    Q=1
    tau0=10
    alpha=0.3
    rho=0.1
    while(nAnt>nVar):
        nAnt=nAnt//2
    print("nAnt",nAnt)
    tau=tau0*np.ones((model["m"],nVar))
    BestCost=np.zeros((MaxIt,1))
    BestTour=np.zeros((MaxIt,nVar))
    empty_ant={}
    empty_ant["Tour"]=[]
    empty_ant["Cost"]=[]
    locs= [x for x in range(nVar)]
    ant=np.tile(empty_ant,(nAnt,1))
    BestSol={}
    BestSol["Tour"]=[]
    BestSol["Cost"]=inf
    start_loc_chunks=[]
    for i in range(0,nVar,nAnt):
        start_loc_chunks.append(locs[i:(i+nAnt)])
    for ite in range(MaxIt):
        for start_loc_chunk in start_loc_chunks:
            for k in range(len(start_loc_chunk)):
                ant[k,0]["Tour"]=[]
                ant[k,0]["Tour"].append(start_loc_chunk[k])
                for l in range((nVar-1)):
                    P=tau[:,l]**alpha
                    for i in ant[k,0]["Tour"]:
                        P[i]=0
                    P=P/sum(P)
                    j=RouletteWheelSelection(P)
                    ant[k,0]["Tour"].append(j)
                    
                ant[k,0]["Cost"]=myCost(ant[k,0]["Tour"],model)
               
                
                if float(ant[k,0]["Cost"]) < float(BestSol["Cost"]):
                    BestSol["Tour"]=ant[k,0]["Tour"]
                    BestSol["Cost"]=float(ant[k,0]["Cost"])
            
            for k in range(len(start_loc_chunk)):
                tour=ant[k,0]["Tour"]
                for l in range(nVar):
                    tau[tour[l],l]=tau[tour[l],l]+Q/ant[k,0]["Cost"]
        
        tau=(1-rho)*tau
        BestCost[ite]=BestSol["Cost"];
        BestTour[ite]=BestSol["Tour"]
        
    end =  datetime.datetime.now()
    duration=end-start
    return(BestSol["Tour"],BestSol["Cost"],duration,nAnt,nVar)


f = open('resultqap.csv', 'w')
path = "qapdataset"
os.chdir(path)

writer = csv.writer(f)
writer.writerow(["Filename", "SizeOf","Iteration","Ant No","No.Of Actual Ant","Permutation","Cost","Execution Time"])
for file in os.listdir():
    print("----------------------------------------")
    print("file name",file) 
    print("----------------------------------------")
    antno=[10,20,30,40]
    times=[]
    bestcostiters=[]
    best_tours=[]
    for x in antno:
        tour,cost,time,ano,sizeof=start_data(x,file)
        best_tours.append(tour)
        bestcostiters.append(cost)
        times.append(str(time))
        writer.writerow([file,sizeof,10,x,ano,tour,cost,times])  
    print("ant no",antno)
    print("time duration",times)
    print("bestcostiters",bestcostiters)
    print("best Tour",best_tours)
f.close()
    # read_text_file(file)