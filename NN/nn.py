from random import randint
import numpy as np
import math
from statistics import mean
from collections import Counter

import tflearn as tf
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from keras.models import Sequential
from keras.layers import Dense
import tensorflow

class NN:
    def __init__(self, initial_games = 10000, test_games = 1000, goal_steps = 2000, lr = 1e-2, lib = ''):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
	self.training_data=[]
	self.lib=lib
	self.session=tensorflow.Session()
	self.graph=tensorflow.get_default_graph()

	# Dependiendo de que html se elige se coje una lib o otra
	if self.lib is 'tfl':
		self.filename = 'NN/snake_tfl_web.tflearn'
        	self.model = self.model_tfl()
	else:		
		self.filename = 'NN/snake_keras_web.h5'
		self.model = self.model_keras()
		with self.graph.as_default():
			with self.session.as_default():
				self.model.load_weights(self.filename)
				print("neural network initialised")

    #llamada POST
    #funciones generales para las 2 libs
    def initial_population_url(self,generate_observation,generateAction,requestJson):
     	observations=generate_observation(requestJson) #snake y food
        action, game_action=generateAction(requestJson)
	return observations,action, game_action
                
    def save_data(self,request,distance,wasGoodAction): #requestJson(obs,action, wasGoodAction,done)
	food_distance=None
	if request["done"]:
		self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), -1])
	else:
		food_distance=distance(request);
		if wasGoodAction(request,food_distance):
			self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), 1])
		else:
			self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), 0])
	#print(self.training_data)
	return food_distance

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)

    def train_rest(self):
        self.model = self.train_model(self.training_data, self.model)

    def train_model(self, training_data, model):
	if self.lib is 'tfl':
        	X = np.array([i[0] for i in training_data]).reshape(-1, 5, 1)   #jugar con numero deparametros 
		y = np.array([i[1] for i in training_data]).reshape(-1, 1)
        	model.fit(X,y, n_epoch = 10, shuffle = True, run_id = self.filename)
		model.save(self.filename)
	else:
		X = np.array([i[0] for i in training_data]).reshape(-1, 5)
		y = np.array([i[1] for i in training_data]).reshape(-1, 1)
		#ERROR: ValueError: Tensor("training/Adam/Const:0", shape=(), dtype=float32) must be from the same graph as Tensor("sub:0", shape=(), dtype=float32).
		#Peta en el fit
		model.fit(X,y,epochs= 3, shuffle = True)
		model.save_weights(self.filename)
        return model

    def predictAction(self,request,generate_observation,get_game_action):
	print(request)      
        prev_observation = generate_observation(request)#food y snake
	predictions=[]
	if self.lib is 'tfl':
        	for action in range(-1,2):
        		predictions.append(self.model.predict(self.add_action_to_observation(prev_observation, action).reshape(-1, 5, 1)))
	else:
  		with self.graph.as_default():
         		with self.session.as_default():   
          			for action in range(-1, 2):
                   			graph=tensorflow.get_default_graph()
                   			with graph.as_default():
                    				prediction=self.model.predict(self.add_action_to_observation(prev_observation, action).reshape(-1, 5)) 
                   				predictions.append(prediction)
        action = np.argmax(np.array(predictions))     
        game_action = get_game_action(request,action-1)
	print(action)
	print(game_action)
        return action,game_action

    #NN con tflearn
    def model_tfl(self):
        network = input_data(shape=[None, 5, 1], name='input')
        network = fully_connected(network, 100, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tf.DNN(network, tensorboard_dir='log')
        return model

    #NN con Keras
    def model_keras(self):
        model = Sequential()
        model.add(Dense(units=5, input_dim=5))
        model.add(Dense(units=25, activation='relu'))
        model.add(Dense(output_dim=1,  activation = 'linear'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

