from random import randint
import numpy as np
import math
from statistics import mean
from collections import Counter

#import tflearn as tf
#from tflearn.layers.core import input_data, fully_connected
#from tflearn.layers.estimator import regression
from keras.models import Sequential
from keras.layers import Dense
import tensorflow
import logging 
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class NN:
    def __init__(self, initial_games = 10000, test_games = 1000, goal_steps = 2000, lr = 1e-2, lib = '',game = '', hidden_neurons=1):
	# Inicializamos las variables necesarias para la NN
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
	self.training_data=[]
	self.lib=lib
	self.game=game
	self.hidden_neurons=hidden_neurons
	self.session=tensorflow.Session()
	self.graph=tensorflow.get_default_graph()

	# Dependiendo de que html se elige se coje una lib o otra
	if self.lib is 'tfl':
		#Se prepara el fichero que hay el train, se crea el modelo de la NN y se carga el entrenamiento
		self.filename = 'NN/'+self.game+'_tfl_web.tflearn'
        	self.model = self.model_tfl()
		self.model.load(self.filename)
	else:	
		#Se prepara el fichero que hay el train, se crea el modelo de la NN y se carga el entrenamiento	
		self.filename = 'NN/'+self.game+'_keras_web.h5'
		self.model = self.model_keras()
		with self.graph.as_default(): # preparamos la sesion para la carga de keras
			with self.session.as_default():
				self.model.load_weights(self.filename)
				print("neural network initialised")

    #llamada POST
    #funciones generales para las 2 libs
    def initial_population_url(self,generate_observation,generateAction,requestJson):
     	observations=generate_observation(requestJson) # llamamos la funcion encargada de generar los obs 
        action, game_action=generateAction(requestJson) # llamamos la funcion encargada de generar la accion
	return observations,action, game_action
                
    def save_data(self,request,wasGoodAction): #requestJson(obs,action, wasGoodAction,done)
	food_distance=None
	# Si el done es ture la accion es mala y se guardan los obs y accion con un -1 
	if request["done"]:
		self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), -1])
	else:
		# Llamamos al wasGoodAction, que se pasa por parametro, para poder calificar si es una accion neutra o buena
		if wasGoodAction(request):
			self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), 1])
		else:
			self.training_data.append([self.add_action_to_observation(request["obs"], request["action"]), 0])
	#print(self.training_data)
	return food_distance

    def add_action_to_observation(self, observation, action):
	# Juntamos los obs en actions para poderlos tratar mejor en el predict
        return np.append([action], observation)

    def train_rest(self):
	# Llamamos la funcion encargada de entrenar el model de NN
        self.model = self.train_model(self.training_data, self.model) 

    def train_model(self, training_data, model):
	print len(training_data[0][0])
	# Entrenamos la red neuronal dependiendo la libreria elegida
	if self.lib is 'tfl':
        	X = np.array([i[0] for i in training_data]).reshape(-1, 5, 1)   #x= obs+action
		y = np.array([i[1] for i in training_data]).reshape(-1, 1)	#y= calidad de la accion [-1,0,1]
        	model.fit(X,y, n_epoch = 10, shuffle = True, run_id = self.filename) # entrenamos la red neuronal tfl
		model.save(self.filename)					# guardamos la red neuronal entrenada en un fichero
	else:
		X = np.array([i[0] for i in training_data]).reshape(-1, 5)	#x= obs+action
		y = np.array([i[1] for i in training_data]).reshape(-1, 1)	#y= calidad de la accion [-1,0,1]
		#ERROR: ValueError: Tensor("training/Adam/Const:0", shape=(), dtype=float32) must be from the same graph as Tensor("sub:0", shape=(), dtype=float32).
		#Peta en el fit
		model.fit(X,y,epochs= 3, shuffle = True)	# entrenamos la red neuronal keras
		model.save_weights(self.filename)		# guardamos la red neuronal entrenada en un fichero
        return model

    def predictAction(self,request,generate_observation,get_game_action,prange):
	root.debug('Flappy info: '+str(request))      
        prev_observation = generate_observation(request)	# miramos que obs tiene la situacion en que estamos
	predictions=[]
	# Dependiendo de que libreria 
	if self.lib is 'tfl':
        	for action in prange:
			# Llenamos el array con los possibles predicts para las possibles acciones que hay en el prange (prange=predict_range del server.py)
        		predictions.append(self.model.predict(self.add_action_to_observation(prev_observation, action).reshape(-1, 5, 1)))
	else:
  		with self.graph.as_default():
         		with self.session.as_default():   
          			for action in prange:
                   			graph=tensorflow.get_default_graph()
                   			with graph.as_default():
						# Llenamos el array con los possibles predicts para las possibles acciones que hay en el prange (prange=predict_range del server.py)
                    				prediction=self.model.predict(self.add_action_to_observation(prev_observation, action).reshape(-1, 5)) 
                   				predictions.append(prediction)
	# Cojemos la prediccion mas alta (que es la mejor)
        action = np.argmax(np.array(predictions))     
        game_action = get_game_action(request,action-1)

	root.debug("Accion: "+str(action))

        return action,game_action

    #NN con tflearn
    def model_tfl(self):
	# Montamos la estructura de la NN
        network = input_data(shape=[None, 5, 1], name='input')
        network = fully_connected(network, self.hidden_neurons, activation='relu')
        network = fully_connected(network, 1, activation='linear')
	#Especificamos  que tipo de NN es (clasificatoria)
        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tf.DNN(network, tensorboard_dir='log')
	
        return model

    #NN con Keras
    def model_keras(self):
	#Especificamos  que tipo de NN es (clasificatoria)
        model = Sequential()
	# Montamos la estructura de la NN
        model.add(Dense(units=5, input_dim=5))
        model.add(Dense(units=self.hidden_neurons, activation='relu'))
        model.add(Dense(output_dim=1,  activation = 'linear'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

