from random import randint
import numpy as np
import math
'''
vectors_and_keys = [
                [[0, -1], 0],
                [[0, 1], 1],
                [[1, 0], 2],
                [[0, -1], 3]
                ]  

canvas:
	heigth=358
	width=320
'''
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

'''
TAREAS: 
- VARIAR POSICION INICIAL DEL PAJARO AL PRINCIPIO DE LA PARTIDA
- AnADIR MAS OBSERVATIONS
- DEBUG Y VALIDACION DEL ENTRENO
- VARIAR EL ENTRENO AUN MAS
- QUITAR PUNTO MEDIO Y PONER LAS 4 ESQUINAS DEL AGUJERO QUE DELIMITAN EL AGUJERO de DISTANCIA

'''
def generate_action(request):
	global movimientos
	print "MOVIMIENTOS: " + str(movimientos)
	if movimientos<700:
		global indice
		movimientos=movimientos+1
		flappy=request["bird"]
		pipes=request["pipes"]
		a=randint(0,2)	#JUGAR CON ALEATORIEDAD PODRIA SER INTERESANTE PARA EL TEMA DEL ENTRENO
		if a==1 :	
			try:
				#print flappy["y"], pipes[1]["y"]-60
				if flappy["y"]>=pipes[indice]["y"]-60:
					return 1,vectors_and_keys[1][0]
				else:
					return 0,vectors_and_keys[0][0]
	
			except:
				global inicio 
				inicio=(inicio+1)%17

				if(inicio!=1):
					return 0,0
				else:
					return 1,1
		else:
			return 0,0
			
		
	else:
		if movimientos>800:
			movimientos=0
		else:
			movimientos=movimientos+1
		print "EMPIEZO ENTRENO ARRIBA"

		return 1,vectors_and_keys[1][0]
		

def generate_observation(request):
	flappy=request["bird"]
	pipes=request["pipes"]
	score=request["score"]
	
	verticalARRIBA, verticalABAJO,horizontalPRIMERA,horizontalSEGUNDA=get_positions(flappy,pipes,score)
	#print pipes
	#print pipes[0]["y"], pipes[1]["y"], flappy["y"], vertical
	return [verticalARRIBA, verticalABAJO,horizontalPRIMERA,horizontalSEGUNDA]

def get_positions(flappy,pipes,score):
	global indice
	global prev_score
	global auxiliar
	global prev_v
	global prev_h
	global v
	global h

	#print indice, prev_score, auxiliar
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
		hcerca=pipes[indice]["x"]-flappy["x"]
		v=pipes[indice]["y"]-120-flappy["y"] #pipes[0]=top pipes[1]=bot (considerar el punto medio ancho del hole=120 sumar 60 para punto medio)
		vcerca=pipes[indice]["y"]-flappy["y"]
		h=pipes[indice]["x"]+60-flappy["x"] #50 antes

		return v,vcerca,h,hcerca

	except (Exception) as error:	#PETA JUSTO AL PASAR POR UN PIPE
		print (error)
		return 0,0,0,0

def resetflappy():
	global indice
	global prev_score
	global auxiliar

	indice=1
	prev_score=0
	auxiliar=0

def get_flappy_direction_vector(flappy):
	global anterior
	if anterior is []:
		anterior=flappy
                #print "ANTERIOOOOOR: " + anterior
		return [0,0]	#!!!!
	else:
		direction = np.array(flappy) - np.array(anterior)	#vector direccion del flappy
		anterior=flappy
		return direction


def get_game_action_predict(request, action):
	#print 'REQUEST: ' + str(request) + '\n'
	#print 'ACTION Q VIENE: ' + str(action)
	if (action==1):
		return [0,1]
	else:
		return [0,-1]

def wasGoodActionFlappy(request):
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
	'''
	if (pipes[indice]["y"]<flappy["y"]):	#si el pajaro esta por debajo del agujero
			#return (flappy["y"]<prev_v or prev_score<score )
			return (flappy["y"]<prev_v)
		elif (pipes[indice]["y"]-120>flappy["y"]):
			#return (flappy["y"]>prev_v or prev_score<score)
			return (flappy["y"]>prev_v)
	'''
	#PROPUESTA JOSE	
		
	if (prev_score<score or (pipes[indice]["y"]>flappy["y"]  and pipes[indice]["y"]-120<flappy["y"])):	#TENER EN CUENTA HORIZONTAL
		#return (not(request["done"]) or prev_score<score) 	 #NO ALEJARSE DEL PUNTO MEDIO
		return True
	else:
		if (pipes[indice]["y"]-20<flappy["y"]):	#si el pajaro esta por debajo del agujero
			#return (flappy["y"]<prev_v or prev_score<score )
			return (flappy["y"]<prev_v)
		elif (pipes[indice]["y"]-110>flappy["y"]):
			#return (flappy["y"]>prev_v or prev_score<score)
			return (flappy["y"]>prev_v)
	

