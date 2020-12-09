# TFGNNSnakeFlappy
Neural Network developed in Python with Keras and TFlearn. The NN can be trained via an rest api (developed using Flask microframework). 

Two different games have been implemented (in Javascript) to test the NN server, Flappy Birds and Snake. 

It is interesting to see how the NN server manages to train and then play predicting the movement to be done depending on the state of the game. 

Besides, there is also a web application with documentation about neural networks.

Want to see the results? Check out our video! https://www.youtube.com/watch?v=DDbG2VCwowU


# Run the project with docker:
1)Build the image with the following command:
  
`$ docker build -t flappy .`
  

2)Run the image with the following command:
  
`$ docker run --name flappy -it -d -p 5000:5000 flappy`

3)Visit the following URL in your navigator: http://localhost:5000
