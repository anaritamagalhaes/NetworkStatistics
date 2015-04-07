#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
calculate shortestPath length between node pair
Created on 2015年4月7日
@author: zhiqyou@gmail.com
'''

import networkx as nx

def getNodesPairNeedToCompute(filepath):
    edges = []
    f=open(filepath,"r")
    while True:
        line = f.readline()
        if line.strip('\r\n'):
            linearray=line.split('\t')
            node1 = (int)(linearray[0])
            node2 = (int)(linearray[1])
            edges.append((node1,node2))
        else:
            break
    f.close()
    return edges


if __name__=='__main__':
    prePath = '/data/home/zhiqiangyou/'
    G=nx.Graph()
    filename = prePath+'clean_data/sampleMapRelData.txt'
    f=open(filename,"r")
    while True:
        line = f.readline()
        if line.strip('\r\n'):
            linearray=line.split('\t')
            node1 = (int)(linearray[0])
            node2 = (int)(linearray[1])
            G.add_edge(node1,node2)
        else:
            break
    f.close()
    print 'construct graph over'
    edges = getNodesPairNeedToCompute(prePath+'/clean_data/disEdges.txt')
    print 'read userpair over'
    count=0
    dis = []
    
    for m in range(len(edges)):
        edge = edges[m]
        sourcenode = edge[0]
        targetnode = edge[1]
        shortestDis = -1
        try:  
            shortestDis = nx.shortest_path_length(G.to_undirected(),source=sourcenode,target=targetnode) 
        except Exception,ex:
            shortestDis = -1   
        
        rec = str(sourcenode)+"\t"+str(targetnode)+"\t"+str(shortestDis)
        dis.append(rec)
        count = count+1
        print count
        if len(dis)%10==0:
            f = open(prePath+'/clean_data/RandomPairShortestDis.txt', "a")
            for i in range(len(dis)):
                f.write(dis[i]+'\n')
            f.close()
            dis = []
    
    f = open(prePath+'/clean_data/RandomPairShortestDis.txt', "a")
    for i in range(len(dis)):
        f.write(dis[i]+'\n')
    f.close()    
    
    
