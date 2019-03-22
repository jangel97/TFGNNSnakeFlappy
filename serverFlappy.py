import games.flappy as snk
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
	#nn=NNF.NN(lib='tfl')
        #nn.model.load(nn.filename)
	return render_template('snake_predict.html')

@app.route('/keras')
def keras():
    	global nn
	#nn=NN.NN(lib='keras')
	return render_template('snake_predict.html')

@app.route('/flappy')
def flappy():
    	global nn
	nn=NNF.NN(lib='keras')
	return render_template('loko.html')

# sends the x and y coordinates to the client
@app.route("/getaction", methods = ["POST"])
def getaction():
	send_data = {}
	post_obj = request.json
	#print post_obj
	global nn
	obs,action,game_action = nn.initial_population_url(snk.generate_observation, snk.generate_action, post_obj)
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
	distance= nn.save_data(post_obj,None,snk.wasGoodActionFlappy)
        print "POST_OBJ: "+str(post_obj) 
        send_data["distance"]=distance	#este DISTANCE era del snake AHORA YA NO HAY, GENERICO?

	return json.dumps(send_data), 200

@app.route("/predict", methods = ["POST"])
def predictAction():
    send_data = {}
    post_obj = request.json #el prev_observation
    global nn
  
    action,game_action=nn.predictAction(post_obj,snk.generate_observation,snk.get_game_action_predict)
    print "\nOBSERVATIONS PREDICT: " + str(post_obj) + "\n"
    send_data["action"]=action
    send_data["game_action"]=game_action
    print "PREDIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIICT"
    return json.dumps(send_data), 200

@app.route("/train", methods = ["POST"])
def train_rest():
    send_data = {}
    print "TRAAAAAAAAAAAAAAAAAAIN"
    post_obj = request.json #el prev_observation
    global nn
    nn.train_rest()
    return json.dumps(send_data), 200

@app.route("/resetflappy", methods = ["POST"])
def resetflappy():
	send_data = {}
	post_obj = request.json
	#print post_obj
	snk.resetflappy()

	return json.dumps(send_data), 200


if __name__ == "__main__":
    app.run(debug=True)





