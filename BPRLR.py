#!/usr/bin/env python
#-*- coding=utf-8 -*-
import numpy as np
import operator
import math
from numpy import *
from copy import copy, deepcopy

'''
BPR logistic rank algorithm 
'''
datapath = 'E:/MF/lr/'
featureFileName = 'userFeatures.txt'
userFeatureFile = ''.join([datapath,featureFileName])

#min: the minmum of users id; max:the maximum of users id; k:the number of latent features
def initial_features(k):
	return ones((k,1))

def load_user_features():
	userWeightMat = loadtxt(userFeatureFile)
	return userWeightMat

def clac_edge_weight(featuresOfUser1,featuresOfUser2):
	divide = []
	for i in xrange(len(featuresOfUser1)):
		divide.append(math.exp(featuresOfUser1[i])/math.exp(featuresOfUser2[i]))
	return mat(divide)

def der_exp(x):
	return math.exp(-x)/(1+math.exp(-x))

def clac_AUC(test_list,remian_list):
	Auc = 0;
	n1 = 0
	n2 = 0
	n = len(test_list)*len(remain_list)
	for i in xrange(len(test_list)):
		rate = test_list[i]
		for j in xrange(len(remain_list)):
			if rate > remain_list[j]:
				n1=n1+1
			elif rate == remain_list[j]:
				n2=n2+1
	Auc = (n1+0.5*n2)/n
	return Auc

'''
INPUT:
	Train: userid | perfer userid | less perfer userid
	P: an initial matrix of features N X K for (Users)
	Q: tranpose of matrix of features K X N for (Users)
	K: init_weights to be learned , set all = 1 at first
	steps: the maximum number of steps to perform the optimisation
	alpha: the learning rate
	beta: the regularization parameter
'''
def logistic_rank(Train,TrainCan,P,init_weights,steps=5000,alpha=0.0002,beta=0.02,error=1e-15):
	#lenOfTrainCan = len(TrainCan)
	for step in xrange(steps):
		#if i%100000==0 and i!=0:
		print step
		flag=0
		#origin_weights = deepcopy(init_weights)
		for i in xrange(len(Train)):
			origin_weights = deepcopy(init_weights)
			record = Train[i]
			userid = (int)(record[0]-1)
			itemid1 = (int)(record[1]-1)
			record2 = random.choice(TrainCan)
			#print 'xxx',record2
			itemid2 = (int)(record2-1)
			preferX = P[itemid1,:]
			print preferX
			lessPreferX = mat(P[itemid2,:])
			tran_preferX = preferX.T
			tran_lessPreferX = lessPreferX.T
			Xuij = np.dot(preferX,init_weights) - np.dot(lessPreferX,init_weights) #error between real rate and the predicted rate
			init_weights = init_weights+alpha*(der_exp(Xuij)*(tran_preferX-tran_lessPreferX)+beta*init_weights)

			#claculate the sum error of weights ,if the error less than 0.001,than break
			eSum = 0
			for ii in xrange(len(init_weights)):
				eSum = eSum+pow(init_weights[ii]-origin_weights[ii],2)
			#print 'eSum',eSum
			if eSum < error:
				flag=1
				print 'yes'
				break
		if flag==1:
			break
	return init_weights


if __name__=='__main__':
	mlensFile_train = 'E:/MF/lr/dataset/0/bprLr.base'  #train data of user perfer userid: user id|item id1|item id2(user id)
	mlensFileCan_train = 'E:/MF/lr/dataset/0/bprLrCan.base'
	mlensFile_test = 'E:/MF/lr/dataset/0/bprLr.test' #test data:user id|item id(user id)
	mlensFile_remain = 'E:/MF/lr/dataset/0/bprLr.remain'
	mlens_train = np.loadtxt(mlensFile_train) #load data into memory
	mlensCan_train = np.loadtxt(mlensFileCan_train)
	mlens_test = np.loadtxt(mlensFile_test)
	mlens_remain = np.loadtxt(mlensFile_remain)

	userWeights = load_user_features() #get all users' features
	m,n = shape(userWeights)   # get the length of features vector
	initial_weights = initial_features(n) #initial the weights of features , at the beginning, set all weights equal 1

	weights = logistic_rank(mlens_train,mlensCan_train,userWeights,initial_weights,100) # learn to rank

	#sort the rates of test set and remain
	test_list = []
	for record in mlens_test:
		userid = (int)(record[0]-1)
		itemid = (int)(record[1]-1)
		#key = str(userid+1)+"\t"+str(itemid+1)
		preferX = clac_edge_weight(userWeights[itemid,:],userWeights[userid,:])
		val=np.dot(preferX,weights)
		test_list.append(val)

	remain_list = []
	for record1 in mlens_remain:
		userid1 = (int)(record1[0]-1)
		itemid1 = (int)(record1[1]-1)
		#key1 = str(userid1+1)+'-'+str(itemid1+1)
		preferX1 = clac_edge_weight(userWeights[itemid1,:],userWeights[userid1,:])
		val1=np.dot(preferX1,weights)
		remain_list.append(val1)

	#sorted_ratesToBeSorted = sorted(ratesToBeSorted.iteritems(), key=operator.itemgetter(1), reverse=True)
	Auc = clac_AUC(test_list,remain_list)
	print Auc



