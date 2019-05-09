import NN.nn as NN
import sys
from flask import Flask
from flask import render_template
from flask import json
from flask import request

#SE INICIA EL SERVER
app = Flask(__name__, template_folder='templates')
nn=None
predict_range=[]

###################################
#######Functiones Navegacion#######
###################################

@app.route('/')
def index():
	return render_template('index.html') #Se renderiza index.html y se envia el template al navegador

@app.route('/resumen')
def resumen():
	return render_template('sobre.html') 

@app.route('/teoria')
def teoria():
	return render_template('teoria.html') #Se renderiza teoria.html y se envia el template al navegador

@app.route('/framework')
def framework():
	return render_template('framework.html') #Se renderiza framework.html y se envia el template al navegador

@app.route('/libTfl')
def libTfl():
	return render_template('libTfl.html') #Se renderiza libTfl.html y se envia el template al navegador

@app.route('/libKeras')
def libKeras():
	return render_template('libKeras.html') #Se renderiza libKeras.html y se envia el template al navegador

@app.route('/comparativaLibs')
def comparativaLibs():
	return render_template('comparativaLibs.html') #Se renderiza comparativaLibs.html y se envia el template al navegador

@app.route('/tfl')
def tfl():
	# creamos una variable global y le cargamos el fichero de juego de snake tiene que importar en ella 
	global game
	import games.snake as game
	
	# importamos las variables globales que contienen la red neuronal y el array de possibles predicciones para el snake
    	global nn
	global predict_range
	
	# Creamos la instancia de la NN describiendo la libreria a usar, el juego y cuantas neuronas tendra la hidden layer
	nn=NN.NN(lib='tfl', game='snake', hidden_neurons=100)
	predict_range=[-1,0,1] #inicializamos el array de predicciones

	return render_template('gamesHTML/snake_predict.html') #Se renderiza snake_predict.html y se envia el template al navegador

@app.route('/keras')
def keras():
	# creamos una variable global y le cargamos el fichero de juego de snake tiene que importar en ella 
	global game
	import games.snake as game
	
	# importamos las variables globales que contienen la red neuronal y el array de possibles predicciones para el snake
    	global nn
	global predict_range
	
	# Creamos la instancia de la NN describiendo la libreria a usar, el juego y cuantas neuronas tendra la hidden layer
	nn=NN.NN(lib='keras', game='snake', hidden_neurons=25)
	predict_range=[-1,0,1] #inicializamos el array de predicciones

	return render_template('gamesHTML/snake_predict.html') #Se renderiza snake_predict.html y se envia el template al navegador

@app.route('/flappy')
def flappy():
	# creamos una variable global y le cargamos el fichero de juego de flappy tiene que importar en ella 
	global game
	import games.flappy as game
	
	# importamos las variables globales que contienen la red neuronal y el array de possibles predicciones para el flappy
    	global nn
	global predict_range
	
	# Creamos la instancia de la NN describiendo la libreria a usar, el juego y cuantas neuronas tendra la hidden layer
	nn=NN.NN(lib='keras', game='flappy', hidden_neurons=200)
	predict_range=[0,1] #inicializamos el array de predicciones

	return render_template('gamesHTML/flappypredict.html') #Se renderiza flappypredict.html y se envia el template al navegador

###################################
###Functiones de la Red Neuronal###
###################################

@app.route("/getaction", methods = ["POST"])
def getaction():
	# importamos las variables globales que contienen la red neuronal y el fichero de juego que se usa
	global nn
	global game

	# preparamos el diccionario para responder la request y cojemos el json con datos para sacar los obs
	send_data = {}
	post_obj = request.json
	
	# Llamamos la funcion de la NN para aconseguir los obs y la accion
	obs,action,game_action = nn.initial_population_url(game.generate_observation, game.generate_action, post_obj)

	print obs

	# preparamos el send_data para enviarlo
        send_data["obs"]=list(obs)
        send_data["action"]=action
        send_data["game_action"]=game_action

	#enviamos el send_data
	return json.dumps(send_data), 200

@app.route("/saveaction", methods = ["POST"])
def saveaction():
	# importamos las variables globales que contienen la red neuronal y el fichero de juego que se usa
	global nn
	global game
	
	# preparamos el diccionario para responder la request y cojemos el json con datos para sacar los obs
	send_data = {}
	post_obj = request.json
	
	# Llamamos la funcion de la NN para guardar los obs i actions para su posterior entrenamiento
	nn.save_data(post_obj,game.wasGoodAction)
        print "POST_OBJ: "+str(post_obj) 

	#enviamos el send_data
	return json.dumps(send_data), 200

@app.route("/predict", methods = ["POST"])
def predictAction():
    # importamos las variables globales que contienen la red neuronal, el fichero de juego que se usa y el array inicializado anteriormente para las predicciones
    global nn
    global predict_range
    global game

    # preparamos el diccionario para responder la request y cojemos el json con datos para sacar los obs
    send_data = {}
    post_obj = request.json #el prev_observation
    
    # llamamos a la NN para que haga una prediccion segun los obs que se le pasa por la reuqest
    action,game_action=nn.predictAction(post_obj,game.generate_observation,game.get_game_action_predict,predict_range)
    
    # preparamos el send_data para enviarlo
    send_data["action"]=action
    send_data["game_action"]=game_action

    #enviamos el send_data
    return json.dumps(send_data), 200

@app.route("/train", methods = ["POST"])
def train_rest():
    # importamos las variables globales que contienen la red neuronal
    global nn
    
    # Llamamos la funcion NN para entrenar la red neuronal
    nn.train_rest()

    return json.dumps({}), 200

@app.route("/reset", methods = ["POST"])
def reset():
	# reseteamos la informacion de la NN
	game.reset()

	return json.dumps({}), 200


if __name__ == "__main__":
    app.run(debug=True, port=str(sys.argv[1]))





