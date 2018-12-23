# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:43:06 2018

@author: james
"""
import glob
import numpy as np
import os
import copy

PATH = os.path.join(os.path.dirname(__file__), 'hw3dataset')
print(PATH)
fn = glob.glob(os.path.join(PATH, "*.txt"))


rows6g = [6,5,4,7,469,1228]
#assign input here
graphnum = 4
C = 0.8 #decay


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


    
adj = create_adj(rows6g[graphnum])
dpsim_last = create_adj(rows6g[graphnum])
dpsim = create_adj(rows6g[graphnum])


    
#select graph from graph 1 to 6
with open(fn[graphnum], 'r') as fp:
    for lines in fp:
        tmpstr = [x.strip() for x in lines.split(',')]
        #initialize with 1
        adj[int(tmpstr[0])-1][int(tmpstr[1])-1] = 1

def transpose_mat(mat):
    newmat = create_adj(len(mat))
    for i in range(len(mat)):
        for j in range(i, len(mat)):
            newmat[i][j] = mat[j][i]
            newmat[j][i] = mat[i][j]
    return newmat




        
#SIMRANK
count = 0
transmat = transpose_mat(adj) #get ingoing links

#initialize s0
for i in range(len(adj)):
    for j in range(i, len(adj)):
        if i==j:
            dpsim_last[i][j] = 1
        else:
            dpsim_last[i][j] = 0
            dpsim_last[j][i] = 0

error_last = []
errorjudge = []

maxiter = 100
while(count<maxiter):
    count = count + 1
    print("Iteration: ", count)
    for i in range(len(adj)):
        for j in range(i, len(adj)):
            if i==j:
                dpsim[i][j] = 1
            else:
                ingoinga = list(transmat[i])
                idxa = np.where(np.asarray(ingoinga) > 0)
                idxa = idxa[0].tolist()
                ingoingb = list(transmat[j])
                idxb = np.where(np.asarray(ingoingb) > 0)
                idxb = idxb[0].tolist()
                if len(idxa) == 0 or len(idxb) == 0:
                    dpsim[i][j] = 0
                else:
                    calc = 0
                    for ii in idxa:
                        ii = int(ii)
                        for jj in idxb:
                            jj = int(jj)
                            calc = calc + dpsim_last[ii][jj]                    
                    dpsim[i][j] = C*calc/(len(idxa)*len(idxb))
                #print(i+1, j+1, "Simrank: ", dpsim[i][j])
                if count==1:
                    error_last.append(0)
                    errorjudge.append(dpsim[i][j])
                else:
                    errorjudge.append(dpsim[i][j])
    
    diff = np.subtract(errorjudge, error_last)
    erroreps = sum(x*x for x in diff)**(1/2)
    if erroreps < 0.000001:
        break
    dpsim_last = copy.deepcopy(dpsim)
    error_last = copy.deepcopy(errorjudge)
    errorjudge = []

print("Done, Total Iteration: ", count)    
#recursive failed, modified with dynamic programming above
#corpse below, preserving usage
#def recurs_calc(a, b):
#    if a==b:
#        return 1
#    ingoinga = list(transmat[a])
#    idxa = np.where(np.asarray(ingoinga) > 0)
#    idxa = idxa[0].tolist()
#    ingoingb = list(transmat[b])
#    idxb = np.where(np.asarray(ingoingb) > 0)
#    idxb = idxb[0].tolist()
#    if len(idxa) == 0 or len(idxb) == 0:
#        return 0
#    calc = 0
#    for i in idxa:
#        i = int(i)
#        for j in idxb:
#            j = int(j)
#            calc = calc + recurs_calc(i,j)
#    
#    return C*calc/(len(idxa)*len(idxb))
#
#
#
#
#for i in range(len(adj)):
#    for j in range(i, len(adj)):
#        simrank = recurs_calc(i, j)
#        print(i, j, "Simrank: ", simrank)



#%%
import csv
outputcsv = []
ccccc = 0
with open('simrank.csv', 'w', newline='') as csvfile:
    for i in range(len(adj)):
        for j in range(i+1, len(adj)):
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([i+1,j+1,errorjudge[ccccc]])
            ccccc = ccccc + 1



    
    
    