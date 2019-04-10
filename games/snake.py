from random import randint
import numpy as np
import math

vectors_and_keys = [
                [[-1, 0], 0],
                [[0, 1], 1],
                [[1, 0], 2],
                [[0, -1], 3]
                ]  

def generate_action(request):
	snake=request["snake"]
	#Las coordenadas [X,Y] que estaban en un diccionario las ponemos en una lista
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
	action = randint(0,2) - 1 #generamos una accion aleatoria
	return action, get_game_action(snake, action) #devolvemos la accion aleatoria y el vector de la accion

def get_game_action(snake, action):
	global vectors_and_keys
	snake_direction = get_snake_direction_vector(snake) # cojemos la direccion de la serpiente
	# si accion es 0 new_direction = snake_direction 
	# si es -1 se girara al izquierda el vector
	# si es 1 se girara al derecha el vector
	new_direction = snake_direction
	if action == -1:
	    new_direction = turn_vector_to_the_left(snake_direction)
	elif action == 1:
	    new_direction = turn_vector_to_the_right(snake_direction)
	#recorremos el array vectors_and_keys para ver que direccion coincide con la nueva seleccionada y creamos el game_action
	for pair in vectors_and_keys:
	    if pair[0] == new_direction.tolist():
	        game_action = pair[1]
	return game_action #devolvemos game_action

def get_game_action_predict(request, action):
	print 'REQUEST: ' + str(request) + '\n'
	print 'ACTION Q VIENE: ' + str(action)
	snake=request["snake"]
	#Las coordenadas [X,Y] que estaban en un diccionario las ponemos en una lista
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
	global vectors_and_keys
	snake_direction = get_snake_direction_vector(snake)
	new_direction = snake_direction
	if action == -1:
	    new_direction = turn_vector_to_the_left(snake_direction)
	elif action == 1:
	    new_direction = turn_vector_to_the_right(snake_direction)
	for pair in vectors_and_keys:
	    if pair[0] == new_direction.tolist():
	        game_action = pair[1]
	return game_action

def generate_observation(request):
	snake=request["snake"]
	# Las coordenadas [X,Y] que estaban en un diccionario las ponemos en una lista
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
	food=request["food"]
	# miramos que direccion tiene la serpiente y que direccion tiene respecto la comida
	snake_direction = get_snake_direction_vector(snake)
	food_direction = get_food_direction_vector(snake, food)
	# miramos si la serpiente esta bloqueada hacia alguna de las possibles direcciones
	barrier_left = is_direction_blocked(snake, turn_vector_to_the_left(snake_direction)) # le pasamos la serpiente y un giro a la izquierda para ver si chocamos hacia la izquierda
	barrier_front = is_direction_blocked(snake, snake_direction)				# le pasamos la serpiente y su direccion para ver si chocamos hacia adelante
	barrier_right = is_direction_blocked(snake, turn_vector_to_the_right(snake_direction)) # le pasamos la serpiente y un giro a la derecha para ver si chocamos hacia la derecha
	# miramos que angulo tiene la serpiente sobre la comida
	angle = get_angle(snake_direction, food_direction)

	return np.array([int(barrier_left), int(barrier_front), int(barrier_right), angle])

def get_snake_direction_vector(snake):
	return np.array(snake[0]) - np.array(snake[1]) #devuelve la direccion de la serpiente

def turn_vector_to_the_left(vector):
        return np.array([-vector[1], vector[0]]) # devuelve un vector con la X invertida

def turn_vector_to_the_right(vector):
        return np.array([vector[1], -vector[0]]) # devuelve un vector con la Y invertida

def get_food_direction_vector(snake, food):
        return np.array(food) - np.array(snake[0]) #devuelve el vector de la serpiente a la comida

def get_food_distance(request):
	snake=request["snake"]
	food=request["food"]
	snake=map(lambda d : [d["x"],d["y"]] ,snake) #Las coordenadas [X,Y] que estaban en un diccionario las ponemos en una lista
        return np.linalg.norm(get_food_direction_vector(snake, food)) # devuelve la distancia de la serpiente a la comida

def wasGoodAction(request):
	#evaluamos el tipo de accion si es neutra o buena
	# si el score ha augmentado es buena o si la distancia a la comida disminuye es buena sino es neutro
	return (request["score"]>request["score_prev"] or get_food_distance(request) < request[u'prev_distance'])

def normalize_vector(vector):
        return vector / np.linalg.norm(vector) # normalizamos el vector

def is_direction_blocked(snake, direction):
        point = np.array(snake[0]) + np.array(direction)
	# devuelve si la serpiente se ha chocado con ella o contra una paret
        return point.tolist() in snake[:-1] or point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21

def get_angle(a, b):
        a = normalize_vector(a)
        b = normalize_vector(b)
	# calculamos que angulo tiene a sobre b (la cabeza de la serpiente sobre la comda)
        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi
