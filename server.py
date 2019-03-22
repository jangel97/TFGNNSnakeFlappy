import games.snake as snk
import NN.nn as NN
import NN.nnf as NNF
from flask import Flask
from flask import render_template
from flask import json
from flask import request

#SE INICIA EL SERVER
app = Flask(__name__, template_folder='templates')
nn=None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tfl')
def tfl():
    	global nn
	nn=NN.NN(lib='tfl')
        nn.model.load(nn.filename)
	return render_template('snake_predict.html')

@app.route('/keras')
def keras():
    	global nn
	nn=NN.NN(lib='keras')
	return render_template('snake_predict.html')

@app.route('/flappy')
def flappy():
    	#global nn
	#nn=NN.NN(lib='keras')
	return render_template('flappy.html')

# sends the x and y coordinates to the client
@app.route("/getaction", methods = ["POST"])
def getaction():
	send_data = {}
	post_obj = request.json
	print post_obj
	global nn
	obs,action,game_action = nn.initial_population_url(snk.generate_observation_snake, snk.generate_action, post_obj)

        send_data["observations"]=list(obs)
        send_data["action"]=action
        send_data["game_action"]=game_action

	return json.dumps(send_data), 200

@app.route("/saveaction", methods = ["POST"])
def saveaction():
	send_data = {}
	post_obj = request.json
	
	global nn
	distance= nn.save_data(post_obj,snk.get_food_distance,snk.wasGoodActionSnake)
        print post_obj 
        send_data["distance"]=distance

	return json.dumps(send_data), 200

@app.route("/predict", methods = ["POST"])
def predictAction():
    send_data = {}
    post_obj = request.json #el prev_observation
    global nn
  
    action,game_action=nn.predictAction(post_obj,snk.generate_observation_snake,snk.get_game_action_predict)
    send_data["action"]=action
    send_data["game_action"]=game_action
    return json.dumps(send_data), 200

@app.route("/train", methods = ["POST"])
def train_rest():
    send_data = {}
    post_obj = request.json #el prev_observation
    global nn
    nn.train_rest()
    return json.dumps(send_data), 200


if __name__ == "__main__":
    app.run(debug=True)





