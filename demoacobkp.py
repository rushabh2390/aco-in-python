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

def RouletteWheelSelection(P):
    C=np.cumsum(P)
    j=np.where(random.random()<=C)[0][0]
    return j        
def createModel(places):
    model={}
    model["v"] = ast.literal_eval(re.search("v=\[.+\]w", places).group().replace("v=","")[:-1])
    model["w"] = ast.literal_eval(re.search("w=\[.+\]W", places).group().replace("w=","")[:-1])
    model["W"] = int(re.search("W=\d+", places).group().replace("W=",""))
    model["n"]=len(model["v"])
    return model
    

def myCost(x,model):
    v=model["v"]
    cost=np.sum(np.dot(v,x[0,:]))
    return cost


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
    # intialization part
    with open(file, 'r') as filehandle:
        places = filehandle.read()
    
    places= places.replace("\n","").replace("]]","]],")
    model=createModel(places)
    nVar=model["n"]
    MaxIt = 10
    nAnt = ant_no
    Q=1
    tau0=0.1
    alpha=1
    beta=0.02
    rho=0.1
    N=1
    eta=np.zeros((2,nVar))
    for i in range(len(model["v"])):
        eta[0,i]=model["w"][i]/model["v"][i]
        eta[1,i]=model["v"][i]/model["w"][i]
    tau=tau0*np.ones((2,nVar))
    while(nAnt>nVar):
        nAnt=nAnt//2
    print("nAnt",nAnt)
    BestCost=np.zeros((MaxIt,1))
    BestTour=np.zeros((MaxIt,nVar))
    empty_ant={}
    empty_ant["Tour"]=[]
    empty_ant["x"]=[]
    empty_ant["Sol"]=[]
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
                value=0.0
                weight=0.0
                ant[k,0]["Tour"]=np.zeros((1,nVar))
                ant[k,0]["Tour"][0,k]=1
                weight += model["w"][k]
                limit=(tau[:,k]**alpha)*(eta[:,k]**beta)
                limit=limit/np.sum(limit)
                for l in range(nVar):

                    if l!=k:
                        P=(tau[:,l]**alpha)*(eta[:,l]**beta)
                        P=P/np.sum(P)
                        if (P[1]>limit[1]) and (weight+model["w"][l]) < model["W"]:
                            weight += model["w"][l]
                            ant[k,0]["Tour"][0,l]=1
                        else:
                            ant[k,0]["Tour"][0,l]=0
                ant[k,0]["x"]=np.dot(N,ant[k,0]["Tour"])
                ant[k,0]["x"]=ant[k,0]["Tour"]

                ant[k,0]["Cost"]=myCost(ant[k,0]["x"],model)
                if float(BestSol["Cost"])==inf and weight<model["W"]:
                     BestSol["Tour"]=ant[k,0]["Tour"]
                     BestSol["Cost"]=float(ant[k,0]["Cost"])
                elif float(ant[k,0]["Cost"]) > float(BestSol["Cost"])and weight<model["W"]:
                    BestSol["Tour"]=ant[k,0]["Tour"]
                    BestSol["Cost"]=float(ant[k,0]["Cost"])
            for k in range(len(start_loc_chunk)):
                tour=ant[k,0]["Tour"]
                for l in range(nVar):
                    tau[int(tour[0,l]),l]=tau[int(tour[0,l]),l]+Q/ant[k,0]["Cost"]
        tau=(1-rho)*tau
        BestCost[ite]=BestSol["Cost"]
        BestTour[ite]=BestSol["Tour"]
        weight=np.sum(np.dot(model["w"],BestSol["Tour"][0,:]))
    end =  datetime.datetime.now()
    duration=end-start
    return(BestSol["Tour"],BestSol["Cost"],duration,nAnt,nVar)

f = open('resultbkp.csv', 'w')
path = "bkpdataset"
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
        writer.writerow([file,sizeof,10,x,ano,tour,cost,str(time)])  
    print("ant no",antno)
    print("time duration",times)
    print("bestcostiters",bestcostiters)
    print("best Tour",best_tours)
f.close()