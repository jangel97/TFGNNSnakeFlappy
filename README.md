# TFGNNSnakeFlappy
Neural Network developed in Python with Keras and TFlearn. The NN can be trained via an api rest (develop ed in Flask). 
Two different games have been implemented (in Javascript) to test the NN server. Snake and Flappy Bird.
If you want to see the result, check out this video: https://www.youtube.com/watch?v=DDbG2VCwowU


# Run the project with docker:
1)Build the image with the following command:
  $ docker build -t flappy .
  

2)Run the image with the following command:
  $ docker run --name flappy -it -d -p 5000:5000 flappy

3)Visit the following URL in your navigator: http://localhost:5000
