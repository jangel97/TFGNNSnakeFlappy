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
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
	action = randint(0,2) - 1
	return action, get_game_action(snake, action)

def get_game_action(snake, action):
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

def get_game_action_predict(request, action):
	print 'REQUEST: ' + str(request) + '\n'
	print 'ACTION Q VIENE: ' + str(action)
	snake=request["snake"]
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
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
	food=request["food"]
	snake_direction = get_snake_direction_vector(snake)
	food_direction = get_food_direction_vector(snake, food)
	barrier_left = is_direction_blocked(snake, turn_vector_to_the_left(snake_direction))
	barrier_front = is_direction_blocked(snake, snake_direction)
	barrier_right = is_direction_blocked(snake, turn_vector_to_the_right(snake_direction))
	angle = get_angle(snake_direction, food_direction)

	return np.array([int(barrier_left), int(barrier_front), int(barrier_right), angle])

def get_snake_direction_vector(snake):
	return np.array(snake[0]) - np.array(snake[1])

def turn_vector_to_the_left(vector):
        return np.array([-vector[1], vector[0]])

def turn_vector_to_the_right(vector):
        return np.array([vector[1], -vector[0]])

def get_food_direction_vector(snake, food):
        return np.array(food) - np.array(snake[0])

def get_food_distance(request):
	snake=request["snake"]
	food=request["food"]
	snake=map(lambda d : [d["x"],d["y"]] ,snake)
        return np.linalg.norm(get_food_direction_vector(snake, food))

def wasGoodActionSnake(request):
	return (request["score"]>request["score_prev"] or get_food_distance(request) < request[u'prev_distance'])

def normalize_vector(vector):
        return vector / np.linalg.norm(vector)

def is_direction_blocked(snake, direction):
        point = np.array(snake[0]) + np.array(direction)
        return point.tolist() in snake[:-1] or point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21

def get_angle(a, b):
        a = normalize_vector(a)
        b = normalize_vector(b)
        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi
