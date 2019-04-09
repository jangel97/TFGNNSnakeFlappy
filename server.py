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

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tfl')
def tfl():
	global game
	import games.snake as game
    	global nn
	global predict_range
	nn=NN.NN(lib='tfl', game='snake', hidden_neurons=100)
	predict_range=[-1,0,1]

	return render_template('snake_predict.html')

@app.route('/keras')
def keras():
	global game
	import games.snake as game

    	global nn
	global predict_range
	
	nn=NN.NN(lib='keras', game='snake', hidden_neurons=25)
	predict_range=[-1,0,1]
	return render_template('snake_predict.html')

@app.route('/flappy')
def flappy():
	global game
	import games.flappy as game
    	global nn
	global predict_range
	nn=NN.NN(lib='keras', game='flappy', hidden_neurons=200)
	predict_range=[0,1]
	return render_template('flappypredict.html')

# sends the x and y coordinates to the client
@app.route("/getaction", methods = ["POST"])
def getaction():
	send_data = {}
	post_obj = request.json
	global nn
	global game
	obs,action,game_action = nn.initial_population_url(game.generate_observation, game.generate_action, post_obj)
	print obs
        send_data["obs"]=list(obs)
        send_data["action"]=action
        send_data["game_action"]=game_action

	return json.dumps(send_data), 200

@app.route("/saveaction", methods = ["POST"])
def saveaction():
	send_data = {}
	post_obj = request.json
	global nn
	global game
	nn.save_data(post_obj,game.wasGoodAction)
        print "POST_OBJ: "+str(post_obj) 

	return json.dumps(send_data), 200

@app.route("/predict", methods = ["POST"])
def predictAction():
    send_data = {}
    post_obj = request.json #el prev_observation
    global nn
    global predict_range
    global game
    action,game_action=nn.predictAction(post_obj,game.generate_observation,game.get_game_action_predict,predict_range)
    send_data["action"]=action
    send_data["game_action"]=game_action

    return json.dumps(send_data), 200

@app.route("/train", methods = ["POST"])
def train_rest():
    global nn
    nn.train_rest()
    return json.dumps({}), 200

@app.route("/resetflappy", methods = ["POST"])
def resetflappy():
	game.resetflappy()
	return json.dumps({}), 200


if __name__ == "__main__":
    app.run(debug=True, port=str(sys.argv[1]))





