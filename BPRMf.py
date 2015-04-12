#!/usr/bin/env python
#-*- coding=utf-8 -*-
import numpy as np
import operator
import math

'''
BPR matrix factorization algorithm 
'''
#min: the minmum of users id; max:the maximum of users id; k:the number of latent features
def initial_features(maxOfn,k):
	return np.random.rand(maxOfn,k)

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
	Train:a training matrix to be factorization,dimension N X M 
	P: an initial matrix of dimension N X K for (Users)
	Q: an initial matrix of dimension M X K for (Items)
	K: the number of latent features
	steps: the maximum number of steps to perform the optimisation
	alpha: the learning rate
	beta: the regularization parameter
'''
def matrix_factorization(Train,P,Q,K,steps=5000,alpha=0.0002,beta=0.02,error=0.001):
	Q = Q.T
	for step in xrange(steps):
		rateBefore = np.dot(P,Q)
		for i in xrange(len(Train)):
			record = Train[i]
			userid = (int)(record[0]-1)
			itemid1 = (int)(record[1]-1)
			itemid2 = (int)(record[2]-1)
			Xuij = np.dot(P[userid,:],Q[:,itemid1]) - np.dot(P[userid,:],Q[:,itemid2]) #error between real rate and the predicted rate
			#print userid,itemid,rate
			#print P[userid,:]
			#print Q[:,itemid]
			for k in xrange(K):
				P[userid][k] = P[userid][k] + alpha*(der_exp(Xuij)*(Q[k][itemid1]-Q[k][itemid2])+beta*P[userid][k])
				Q[k][itemid1] = Q[k][itemid1] + alpha*(der_exp(Xuij)*P[userid][k]+beta*Q[k][itemid1])
				Q[k][itemid2] = Q[k][itemid2] + alpha*(der_exp(Xuij)*(-P[userid][k])+beta*Q[k][itemid2])

		#claculate the sum error ,if the error less than 0.001
		eR = np.dot(P,Q)
		eSum = 0
		HaveDealBefore = set([])
		for ii in xrange(len(Train)):
			record1 = Train[ii]
			userid1 = (int)(record[0]-1)
			itemid1 = (int)(record[1]-1)
			itemid2 = (int)(record[2]-1)
			key1 = str(userid1)+'-'+str(itemid1)
			key2 = str(userid1)+'-'+str(itemid2)
			if key1 in HaveDealBefore:
				pass
			else:
				eSum = eSum+pow(rateBefore[userid1][itemid1]-eR[userid1][itemid1],2)
				for kk in xrange(K):
					eSum = eSum+beta*0.5*(pow(P[userid1][kk],2)+pow(Q[kk][itemid1],2))
				HaveDealBefore.add(key1)

			if key2 in HaveDealBefore:
				pass
			else:
				eSum = eSum+pow(rateBefore[userid1][itemid2]-eR[userid1][itemid2],2)
				for kk in xrange(K):
					eSum = eSum+beta*0.5*(pow(P[userid1][kk],2)+pow(Q[kk][itemid2],2))
				HaveDealBefore.add(key2)
			
		if eSum < error:
			print 'yes'
			break
	return P,Q


if __name__=='__main__':
	mlensFile_train = 'E:/MF/mlens/bpr.base'  #train data of user rating with fields: user id|item id|rating|timestamp
	mlensFile_test = 'E:/MF/mlens/bpr.test' #test data:user id|item id|rating|timestamp
	mlensFile_remain = 'E:/MF/mlens/bpr.remain'
	K = 20 #dimension length of latent features
	mlens_train = np.loadtxt(mlensFile_train) #load data into memory
	mlens_test = np.loadtxt(mlensFile_test)
	mlens_remain = np.loadtxt(mlensFile_remain)

	unique_User_Train = set(mlens_train[:,0])
	unique_Item1_Train = set(mlens_train[:,1])
	unique_Item2_Train = set(mlens_train[:,2])
	new_unique_Item_Train = unique_Item1_Train.union(unique_Item2_Train)

	maxOfUser_Train = (int)(max(unique_User_Train))
	maxOfItem_Train = (int)(max(new_unique_Item_Train))

	#initial user's latent feature vectors and Item's latent feature vectors
	dict_user_features_Train = initial_features(maxOfUser_Train,K)
	dict_item_features_Train = initial_features(maxOfItem_Train,K)

	#print dict_user_features_Train
	#print dict_item_features_Train

	P,Q = matrix_factorization(mlens_train,dict_user_features_Train,dict_item_features_Train,K,5000)
	Prerate = np.dot(P,Q) 
	print Prerate

	#sort the rates of test set and remain
	test_list = []
	for record in mlens_test:
		userid = (int)(record[0]-1)
		itemid = (int)(record[1]-1)
		key = str(userid+1)+"\t"+str(itemid+1)
		test_list.append(Prerate[userid][itemid])

	remain_list = []
	for record1 in mlens_remain:
		userid1 = (int)(record1[0]-1)
		itemid1 = (int)(record1[1]-1)
		key1 = str(userid1+1)+'-'+str(itemid1+1)
		remain_list.append(Prerate[userid1][itemid1])

	#sorted_ratesToBeSorted = sorted(ratesToBeSorted.iteritems(), key=operator.itemgetter(1), reverse=True)
	Auc = clac_AUC(test_list,remain_list)
	print Auc


