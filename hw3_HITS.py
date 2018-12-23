# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:43:06 2018

@author: james
"""
import glob
import numpy as np
import os
PATH = os.path.join(os.path.dirname('__file__'), 'hw3dataset')
print(PATH)
fn = glob.glob(os.path.join(PATH, "*.txt"))

rows6g = [6,5,4,7,469,1228, 1000]



#assign input here
graphnum = 4
d = 0.15 #dampling factor
project1 = False
bidir = False



graphnum = graphnum-1

#create adjacency matrix
def create_adj(row):
    newlist = []
    for i in range(row):
        tmp = []
        for j in range(row):
            tmp.append(0)
        newlist.append(tmp)
    return newlist


def transpose_mat(mat):
    newmat = create_adj(len(mat))
    for i in range(len(mat)):
        for j in range(i, len(mat)):
            newmat[i][j] = mat[j][i]
            newmat[j][i] = mat[i][j]
    return newmat


if project1 == True:
    rfile = np.loadtxt("data3.data")
    n_rfile = rfile.shape[0]
    n_trans = 1000
#t_len = 30
    n_item = 1000


#data preprocessing
    start =1
    trans_list = []
    trans_tmp = []
    for i in range(n_rfile):
        if(start == rfile[i,0]):
            trans_tmp.append(rfile[i,2])
        else:
            if trans_tmp:
                trans_list.append(tuple(trans_tmp))
                trans_tmp = []
                start = start+1
                trans_tmp.append(rfile[i,2])
    trans_list.append(tuple(trans_tmp))
    print(len(trans_list))
    #build adj
    adj = create_adj(len(trans_list))
    for loop in range(len(trans_list)):
        for var1 in trans_list[loop]:
            for var2 in trans_list[loop]:
                if var1 == var2:
                    continue
                else:
                    if bidir == False:
                        if int(var1) > int(var2):
                            continue
                        adj[int(var1)][int(var2)] = 1
                    else:
                        adj[int(var1)][int(var2)] = 1

else:
    adj = create_adj(rows6g[graphnum])
#select graph from graph 1 to 6
    with open(fn[graphnum], 'r') as fp:
        for lines in fp:
            tmpstr = [x.strip() for x in lines.split(',')]
        #initialize with 1
            adj[int(tmpstr[0])-1][int(tmpstr[1])-1] = 1

auth = []
hub = []
auth_last = []
hub_last = []
pr = []
pr_last = []
for i in range(rows6g[graphnum]):
    #initialize with 1
    auth.append(1)
    hub.append(1)
    auth_last.append(1)
    hub_last.append(1)
    pr.append(1)
    pr_last.append(1)
    

        
#HITS GO (base root set??? Don`t know to implement or not)
count = 0
transmat = transpose_mat(adj) #get ingoing links

while(count < 10000):
    count = count + 1
    calc = 0
    norm = 0
    #update authority
    for nodes in range(rows6g[graphnum]):
        ingoing = list(transmat[nodes])
        idx = np.where(np.asarray(ingoing) > 0)
        idx = idx[0].tolist()
        for i in idx:
            calc = calc + hub[int(i)]
        auth[nodes] = calc
        calc = 0
    
    #update hub
    for nodes in range(rows6g[graphnum]):
        ingoing = list(adj[nodes])
        idx = np.where(np.asarray(ingoing) > 0)
        idx = idx[0].tolist()
        for i in idx:
            calc = calc + auth_last[int(i)]
        hub[nodes] = calc
        calc = 0    
    #norm = sum(x*x for x in auth)**(1/2)
    norm = sum(x for x in auth)
    auth = [x/norm for x in auth]
    #norm = sum(x*x for x in hub)**(1/2)
    norm = sum(x for x in hub)
    hub = [x/norm for x in hub]
    
    #check stop condition
    print(auth[0], hub[0])
    diffa = np.subtract(auth, auth_last)
    diffh = np.subtract(hub, hub_last)
    erroreps = sum(x*x for x in diffa)**(1/2) + sum(x*x for x in diffh)**(1/2)
    if erroreps < 0.0000001:
        break
    auth_last = auth.copy()
    hub_last = hub.copy()

print("Graph: ", graphnum+1)        
print("Iterations stopped: ", count)
print("HITS Complete")

    
#PAGERANK GO

count = 0
while(count<10000):
    count = count + 1
    calc = 0
    newpr = []
    for nodes in range(rows6g[graphnum]):
        ingoing = list(transmat[nodes])
        idx = np.where(np.asarray(ingoing) > 0)
        idx = idx[0].tolist()
        for i in idx:
            i = int(i)
            tmpcountpc = np.array(adj[i])
            calc = calc + pr[i]/(tmpcountpc > 0).sum()
        calc = 1*d/rows6g[graphnum] + (1-d)*calc
        newpr.append(calc)
        calc = 0
    pr = newpr.copy()
    norm = sum(x for x in pr)
    pr = [x/norm for x in pr]
    newpr = []
    print(pr[0])
    #check stop condition
    diffpr = np.subtract(pr, pr_last)
    erroreps = sum(x*x for x in diffpr)**(1/2) + sum(x*x for x in diffpr)**(1/2)
    if erroreps < 0.0000001:
        break
    pr_last = pr.copy()
    
    
print("Pagerank iterations stopped: ", count)
print("Done")


import csv
outputcsv = []
with open('hits_pr_g.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Node", "auth", "hub", "pr"])
    for i in range(len(adj)):
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([i+1, auth[i], hub[i], pr[i]])


    
    
    