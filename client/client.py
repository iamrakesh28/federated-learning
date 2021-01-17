import utility
import helper
from random import randint
from sender import Sender
from json import loads, dumps
from time import sleep

MAX_RETRY = 2
MAX_WAIT = 2

class Client:
    """
    """
    def __init__(self, addr, client_id):
        self.sender = Sender(addr)
        self.model = utility.getNewModel()
        self.client_id = client_id
        self.datasets = 0
        self.weights = self.model.get_weights()
        self.sent = True

    def __validate_data(self):

        success = False
        try:
            data = loads(self.sender.get_resp_text())

            datasets = data.get('datasets')
            assert(type(datasets) == int and datasets >= 0)

            updated_weight = helper.lists_toarray(data.get('weights'))
            assert(
                type(self.weights) == type(updated_weight)
                and len(self.weights) == len(updated_weight)
            )

            for i in range(len(self.weights)):
                assert(
                    type(self.weights[i]) == type(updated_weight[i])
                    and self.weights[i].shape == updated_weight[i].shape
                )

            
            # everything looks fine, update the weight
            self.datasets = datasets
            self.weights = updated_weight
            self.model.set_weights(updated_weight)

            success = True

        except:
            print("Error in validating the model weights!")

        return success
            
    def __request_model(self):
        """
        Gets the updated weights from the server
        It tries MAX_RETRY times till it succesfully gets
        """
        
        nos_retry = 0
        data = {
            'id' : self.client_id,
            'send' : False
        }
        
        while nos_retry < MAX_RETRY:

            print("Trying to get the server model weights!")
            success = self.sender.send(data=data, request='post')

            if success and self.__validate_data():
                # Successfully got the weights
                print("Successfully got the weights")
                return

            print("Failed to get the weights!")

            # Try more if possible but wait for few seconds
            nos_retry += 1

            if nos_retry < MAX_RETRY:
                sleep_time = randint(0, MAX_WAIT)
                print("Trying again in", sleep_time, "s")
                sleep(sleep_time)

        # Couldn't get the updated model from the server
        # Continue with the previous version model
        return

    def __send_model(self):
        """
        Sends the updated weights to the server
        It tries MAX_RETRY times till it succesfully sends
        """

        nos_retry = 0
        data = {
            'id' : self.client_id,
            'send' : True,
            'datasets' : self.datasets,
            'weights' : dumps(helper.arrays_tolist(self.weights))
        }

        self.sent = False
        while nos_retry < MAX_RETRY:

            print("Trying to send newly updated model weights!")
            success = self.sender.send(data=data, request='post')

            if success:
                # Successfully got the weights
                self.sent = True
                print("Successfully sent the weights")
                return

            print("Failed to send the weights!")

            # Try more if possible but wait for few seconds
            nos_retry += 1
            
            if nos_retry < MAX_RETRY:
                sleep_time = randint(0, MAX_WAIT)
                print("Trying again in", sleep_time, "s")
                sleep(sleep_time)

        # Couldn't send the updated model weights to the server
        # Continue with the previous version model
        return

    def __train_model(self, train_data):
        """
        Trains on the train_data and 
        updates the dataset count and weight 
        @param train_data training dataset
        """
        print("Training on the dataset")
        
        utility.trainOnData(self.model, train_data)
        self.datasets += train_data[0].shape[0]
        self.weights = self.model.get_weights()
        
        print("Training done and variables updated")
        
        return
        
    def run(self, dataset):
        """
        Runs the client on the list of datasets
        @param dataset list of (X, Y) training data
        """

        for X, Y in dataset:
            print("Training on next dataset")
            if self.sent:
                self.__request_model()
            self.__train_model((X, Y))
            self.__send_model()

        print("Training done, exiting!")
