#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
calculate clustering coefficient
Created on 2015年4月7日
@author: zhiqyou@gmail.com
'''
import networkx as nx

def getNodesNeedToCompute(filepath):
    nodes = []
    f=open(filepath,"r")
    while True:
        line = f.readline()
        if line.strip('\r\n'):
            node = (int)(line)
            nodes.append(node)
        else:
            break
    f.close()
    return nodes

if __name__ == '__main__':
    prePath = 'E:/'
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
    nodes = getNodesNeedToCompute(prePath+'/clean_data/CluNodes.txt')
    print 'read users over'
    count=0
    coe = []
    for m in range(len(nodes)):
        node = nodes[m]
        clusterCoe = -1
        try:  
            clusterCoe = nx.clustering(G.to_undirected(),node)
        except Exception,ex:
            clusterCoe = -1   
        
        coe.append(str(clusterCoe))
        count = count+1
        print count
        if len(coe)%2==0:
            f = open(prePath+'/clean_data/RandomNodeClusterCoe.txt', "a")
            for i in range(len(coe)):
                f.write(coe[i]+'\n')
            f.close()
            coe = []
    f = open(prePath+'/clean_data/RandomNodeClusterCoe.txt', "a")
    for i in range(len(coe)):
        f.write(coe[i]+'\n')
    f.close()
