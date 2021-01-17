# Federated Learning
Federated learning (also known as collaborative learning) is a machine learning technique that trains an algorithm across multiple decentralized edge devices or servers holding local data samples, without exchanging them [1].

It's a Server-Client based application written in Python to demonstrate the federated learning on MNIST dataset classification. The server and the clients
communicate using HTTP (GET / POST) requests. For handling the HTTP requests at the server side, Flask API is used. <b> Flask </b> is a web framework for Python, meaning that it provides functionality for building web applications, including managing HTTP requests and rendering templates [2]. 

Since the federated learning is used for the MNIST dataset classification, the clients train on their private MNIST datasets using tensorflow APIs.

## Run
To run the application, first clone the repository and the download these MNIST training and test datasets from here (<a href="https://drive.google.com/drive/folders/12ri3Qo6XYj8eyaeRPp6rscnsfsZ7JwFi?usp=sharing"> Federated Learning </a>). Put these datasets at the root level. The directory will look similar to this:

<p align="center">
  <img src="https://github.com/iamrakesh28/federated-learning/blob/master/images/fed-learn-dir.png">
  </br>
</p>

The model behind the application trains on `NUM_IMAGES_TRAIN` (currently set to 5,000, defined in `server/utility.py` and `client/utility.py`) samples at a time.
To start the server:
```
cd server
python3 main.py
```

To run a client, from the top directory do the following:
```
cd client
python3 main.py
```
The client will ask for `Client Id` and `Dataset Range`. You can provide any string for the Id as the server doesn't perform authenication on the client for now. </br>
For the datasets, provide two space separated integers between `1` and `12` (inclusive) and first integer should be less than or equal to the second integer. There are `60,000` samples in the MNIST training set and `NUM_IMAGES_TRAIN` is set to `5,000`. If you enter two valid integers `l` and `r`, the client will train on samples from `(l - 1) x 5,000 to r x 5,000` (0-based indexing).

<p align="center">
  <img src="https://github.com/iamrakesh28/federated-learning/blob/master/images/fed-learn-client.png">
  </br>
</p>

## Working Demo on 3 Clients
<p align="center">
  <img src="https://github.com/iamrakesh28/federated-learning/blob/master/images/federated-v1.gif">
  <a href=https://drive.google.com/file/d/12NgnlLGUwOsIooBpNUwluTVKVH2QfhA6/view?usp=sharing> Video </a>
  </br>
</p>

## Working
### Client
In each iteration, the client takes the `NUM_IMAGES_TRAIN` size samples and does the following steps:
* Makes a request from the server to get the updated model weights. It makes `MAX_RETRY` atmost requests to the server. If the server fails (or the server is down) to send the correct data, the client continues to the next step with the previously updated weights. Between each two request, it waits randomly between `0` to `MAX_WAIT` (defined in `client/client.py`) seconds.
* After the client has got the updated weights, it trains on the data and updates the model weights.
* It tries to send the updated weights to the server. Similarly, as in the case of mmaking the request, it makes `MAX_RETRY` atmost requests to the server. If the client fails to send the data, the client continues to the next iteration and since the weights has not been sent, it skips the first step and continues with the training. Between each two request, it waits randomly between `0` to `MAX_WAIT` (defined in `client/client.py`) seconds.

### Server
The server keeps running. For each new request, it spawns a new thread to handle the request. It accepts only GET and POST requests. There are two types of requests:
1. Sending the updated model weights
2. Receiving the trained model weights from the clients

Server does a weighted average of the received model weights from the clients. Clients also send the number of datasets on which their model has been trained in total. The server does the weighted average of their weights and the client weights and updated the weights at the server. If the server's model has been trained on `a` datasets and the client's model on `b` datasets, then weighted average is `(a x server_weights + b x client_weights) / (a + b)`. It's a hypothesis but works well in practice. The server saves the model weights after every `SAVE_MODEL` (defined in `server/server.py`) updates in `model` file.

Also, there could be multiple reader as well as writer threads at the server. In the version 1.0 of the application, it handles single read or write. In current version, it supports multiple readers simultaneously. 

### Testing
To test the model on the training set,
```
cd server && python3 test.py
```

## References
[1] (https://en.wikipedia.org/wiki/Federated_learning) </br>
[2] (https://www.flaskapi.org/)
