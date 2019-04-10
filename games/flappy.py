from random import randint
import numpy as np
import math

auxiliar=0
inicio=0
prev_score=0
indice=1
anterior=[]

prev_v=0
prev_h=0
v=0
h=0
h2=0
movimientos=0
inicio_game=True

vectors_and_keys = [
                [[0, -1], 0],
                [[0, 1], 1]
                ]  

def generate_action(request):
	global movimientos
	print "MOVIMIENTOS: " + str(movimientos)
	# En el entrenamiento hay 2 tipos de entrenamientos
	# Si los movimientos<700 es un entrenamiento algoritmico intenta no fallar 
	# si >700 i <800 siempre va hacia arriba ya que en el entrenamiento algoritmico no siempre hay ocasiones por arriba del agujero.
	if movimientos<700:
		global indice
		movimientos=movimientos+1
		flappy=request["bird"]
		pipes=request["pipes"]
		a=randint(0,2)
		# Jugamos con la aleatoriedad para hacer que el pajaro falle sino el entrenamiento sería infinito
		if a==1 :	
			try:
				# miramos si el flappy esta pord debajo del punto medio del agujero
				if flappy["y"]>=pipes[indice]["y"]-60:
					return 1,vectors_and_keys[1][0] # devolvemos 1 para saltar
				else:
					return 0,vectors_and_keys[0][0] # devolvemos 0 para dejar caer
	
			except:
				# esto es para el inicio del flappy ya que no hay pipies hacemos una probabilidad 
				# para que el pajaro se mantenga a flote hasta que hay un pipie y reacciona
				global inicio 
				inicio=(inicio+1)%17

				if(inicio!=1):
					return 0,0
				else:
					return 1,1
		else:
			return 0,0
	else:
		# si >800 reseteamos el entreno
		if movimientos>800:
			movimientos=0
		else:
			movimientos=movimientos+1
		# devolvemos siempre 1 para ir hacia arriba
		return 1,vectors_and_keys[1][0]
		

def generate_observation(request):
	flappy=request["bird"]
	pipes=request["pipes"]
	score=request["score"]
	# llamamos la funcion que nos devolvera todos los obs de la situacion
	verticalARRIBA, verticalABAJO,horizontalPRIMERA,horizontalSEGUNDA=get_positions(flappy,pipes,score)
	#print pipes
	#print pipes[0]["y"], pipes[1]["y"], flappy["y"], vertical
	return [verticalARRIBA, verticalABAJO,horizontalPRIMERA,horizontalSEGUNDA] #devolvemos los obs

def get_positions(flappy,pipes,score):
	global indice
	global prev_score
	global auxiliar
	global prev_v
	global prev_h
	global v
	global h

	#print indice, prev_score, auxiliar
	#Miramos si el score anterior es menor para poder actualizarlo
	if prev_score < score:
		if auxiliar>40:
			prev_score=score
			#indice=indice+2
			auxiliar=0
		else:
			auxiliar=auxiliar+1
	try:
		prev_v=v
		prev_h=h
		print "PIPEEEEEEEEEE:" +str(pipes)
		#cojemos los vectores a todos los vertices del agujero por donde tiene que pasar el pajaro respecto el pajaro
		hcerca=pipes[indice]["x"]-flappy["x"]
		v=pipes[indice]["y"]-120-flappy["y"] 
		vcerca=pipes[indice]["y"]-flappy["y"]
		h=pipes[indice]["x"]+60-flappy["x"]

		return v,vcerca,h,hcerca

	except (Exception) as error:
		print (error)
		return 0,0,0,0

def reset():
	global indice
	global prev_score
	global auxiliar
	# reseteamos los valores para poder volver a jugar
	indice=1
	prev_score=0
	auxiliar=0

def wasGoodAction(request):
	global prev_score
	global prev_v
	global v
	global prev_h
	global h
	global indice
	global inicio_game

	flappy=request["bird"]
	score=request["score"]
	pipes=request["pipes"]
	
	#si el score ha mejorado o el pajaro esta dentro el rango del agujero por donde tiene que pasar devolvera true
	if (prev_score<score or (pipes[indice]["y"]>flappy["y"]  and pipes[indice]["y"]-120<flappy["y"])):
		return True
	else:
		if (pipes[indice]["y"]-20<flappy["y"]):
			#si el pajaro esta por debajo del agujero
			return (flappy["y"]<prev_v)
		elif (pipes[indice]["y"]-110>flappy["y"]):
			#si el pajaro esta por arriba del agujero
			return (flappy["y"]>prev_v)
	

