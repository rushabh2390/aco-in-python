import numpy as np
from numpy import inf
import math
import random
import datetime
import csv
def Eta(tabu,allow,colnum):
    contradiction = np.zeros(len(allow))
    m=0
    for i in allow:
        row=math.floor((i-1)/colnum)+1
        col=((i-1)%colnum)+1
        leftslash = row + col - 2;
        rightslash = colnum - 1 + col - row;
        taburow = ((tabu-1)//colnum)+1;
        tabucol = ((tabu-1)%colnum)+1;
        tabuleftslash = taburow + tabucol - 2;
        taburightslash = colnum - 1 + tabucol - taburow;
        if row in taburow:
            colcontra=1
        else:
            colcontra=0
        if col in tabucol:
            rowcontra=1
        else:
            rowcontra=0
        slashcontra=0
        if leftslash in tabuleftslash:
            slashcontra+=1
        if rightslash in taburightslash:
            slashcontra+=1
        contradiction[m] = colcontra + rowcontra + slashcontra
        m=m+1;
    
    return contradiction

def start_op(antno,boardno):
    start_time =  datetime.datetime.now()
    n=boardno
    N=int(math.sqrt(n))
    m=antno
    alpha=1.5
    beta=1.5
    rho=0.4
    Q=1
    tau = np.ones((n,n))
    table=np.zeros((m,N))
    ite=0
    iter_max=100
    route_best=np.zeros((iter_max,N))
    Collision_best = np.zeros ((iter_max,1))
    Collision_ave = np.zeros ((iter_max,1)); 
    while(ite<iter_max):
        start = np.zeros((m,1))
        for i in range(m):
            temp=np.random.permutation(n)
            start[i]=temp[0]
        table[:,0]=start[:,0]
        board_ind=[]
        for i in range(n):
            board_ind.append(i)
        Contradiction = np.zeros((m,1))
        for i in range(m):
            for j in range(1,N):
                tabu=table[i,0:j]
                allow_ind=[]
                allow=board_ind[:]
                for position in tabu:
                    if position in allow:
                        allow.remove(int(position))
                P=allow[:]
                for k in range(0,len(allow)):
                   P[k]=tau[int(tabu[-1]),allow[k]]**alpha
                contra=Eta(tabu,allow,N)
                P = P * (1.0/ (contra + 0.1))**beta
                P=P/sum(P)
                Pc=np.cumsum(P)
                target_index = np.where(Pc>=random.random())[0]
                target = allow [target_index[0]]
                Contradiction[i]=Contradiction[i]+contra[target_index[0]]
                table[i,j]=target
                
                

        if ite==0:
            min_contradiction=min(Contradiction)
            min_index=np.where(Contradiction==min_contradiction)[0][0]
            Collision_best[ite]=min_contradiction
            
            Collision_ave[ite]=np.mean(Contradiction)
            route_best[ite,:]=table[min_index,:]
        else:
            min_Contradiction = min(Contradiction)
            min_index=np.where(Contradiction==min(Contradiction))[0][0]
            Collision_best[ite] = min(Collision_best[ite-1],min_Contradiction)
            Collision_ave [ite] = np.mean(Contradiction)
            if Collision_best[ite] == min_Contradiction:
                route_best[ite,:] = table [min_index,:]
            else:
                route_best [ite,:] = route_best [(ite-1),:]            

        Delta_Tau = np.zeros ((n, n))
        for i in range(0,m):
            for j in range(1,(N-1)):
                Delta_Tau[int(table[i,j]),int(table [i,j+1])] = Delta_Tau [int(table [i, j]), int(table [i, j+1])] + Q/(Contradiction [i]+0.1);
                
        tau = (1-rho) * tau + Delta_Tau
        ite+=1
        table=np.zeros((m,N),dtype = 'float')
    conflict=min(Contradiction)
    min_index=np.where(Contradiction==min(Contradiction))[0][0]
    end_time =  datetime.datetime.now()
    duration=end_time-start_time
    return route_best[min_index,:],str(duration),conflict

antno=[10,20,30,40]
checkerboardno=[25,36,49,64,81,100]
f = open('resultmqueen.csv', 'w')
writer = csv.writer(f)
writer.writerow(["No Of Queen", "Iteration","No.Of Ant","Positions","Minority Conflict","Execution Time"])
for bsize in checkerboardno:
    for ants in antno:
        print("+++++++++++++++++++++++++++++++++++")
        x,y,z=start_op(ants,bsize)
        writer.writerow([math.sqrt(bsize),100,ants,x,z,y])        
        print(bsize,ants,x,y,z)
    print("=====================================")
f.close()
