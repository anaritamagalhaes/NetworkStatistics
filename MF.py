#!/usr/bin/env python
#-*- coding=utf-8 -*-
import numpy as np

#min: the minmum of users id; max:the maximum of users id; k:the number of latent features
def initial_features(maxOfn,k):
	return np.random.rand(maxOfn,k)


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
		for i in xrange(len(Train)):
			record = Train[i]
			userid = (int)(record[0]-1)
			itemid = (int)(record[1]-1)
			rate = (int)(record[2])
			eui = rate - np.dot(P[userid,:],Q[:,itemid]) #error between real rate and the predicted rate
			#print userid,itemid,rate
			#print P[userid,:]
			#print Q[:,itemid]
			for k in xrange(K):
				P[userid][k] = P[userid][k] + alpha*(2*eui*Q[k][itemid]-beta*P[userid][k])
				Q[k][itemid] = Q[k][itemid] + alpha*(2*eui*P[userid][k]-beta*Q[k][itemid])

		#claculate the sum error ,if the error less than 0.001
		eR = np.dot(P,Q)
		eSum = 0
		for ii in xrange(len(Train)):
			record1 = Train[ii]
			userid1 = record1[0]-1
			itemid1 = record1[1]-1
			rate1 = record1[2]
			eSum = eSum+pow(rate1-eR[userid1][itemid1],2)
			for kk in xrange(K):
				eSum = eSum+beta*0.5*(pow(P[userid1][kk],2)+pow(Q[kk][itemid1],2))
		if eSum < error:
			print 'yes'
			break
	return P,Q


if __name__=='__main__':
	mlensFile_train = 'E:/mf/MF/mlens/u1.base'  #train data of user rating with fields: user id|item id|rating|timestamp
	mlensFile_test = 'E:/mf/MF/mlens/u1.test' #test data:user id|item id|rating|timestamp
	K = 2 #dimension length of latent features
	mlens_train = np.loadtxt(mlensFile_train) #load data into memory
	mlens_test = np.loadtxt(mlensFile_test)
	unique_User_Train = set(mlens_train[:,0])
	unique_Item_Train = set(mlens_train[:,1])

	maxOfUser_Train = (int)(max(unique_User_Train))
	maxOfItem_Train = (int)(max(unique_Item_Train))

	#initial user's latent feature vectors and Item's latent feature vectors
	dict_user_features_Train = initial_features(maxOfUser_Train,K)
	dict_item_features_Train = initial_features(maxOfItem_Train,K)

	#print dict_user_features_Train
	#print dict_item_features_Train

	P,Q = matrix_factorization(mlens_train[:,range(0,3)],dict_user_features_Train,dict_item_features_Train,K)

	print np.dot(P,Q)
