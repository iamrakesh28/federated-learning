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
        self.dataset = 0
        self.weight = self.model.get_weights()

    def __validate_data(self):

        success = False
        try:
            data = loads(self.sender.get_resp_text())
            updated_weight = helper.lists_toarray(data.get('weight'))
            assert(
                type(self.weight) == type(updated_weight)
                and len(self.weight) == len(updated_weight)
            )

            for in range(len(self.weight)):
                assert(
                    type(self.weight[i]) == type(updated_weight[i])
                    and self.weight[i].shape == updated_weight[i].shape
                )

            
            # everything looks fine, update the weight
            self.dataset = data['dataset']
            self.weight = updated_weight
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
            sleep(randint(0, MAX_WAIT))

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
            'id' : client_id,
            'send' : True,
            'dataset' : self.dataset
            'weight' : dumps(self.weight)
        }
        
        while nos_retry < MAX_RETRY:

            print("Trying to send newly updated model weights!")
            success = self.sender.send(data=data, request='post')

            if success and self.__validate_data():
                # Successfully got the weights
                print("Successfully sent the weights")
                return

            print("Failed to send the weights!")

            # Try more if possible but wait for few seconds
            nos_retry += 1
            sleep(randint(0, MAX_WAIT))

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
        self.dataset += train_data[0].shape[0]
        self.weight = self.model.get_weight()
        
        print("Training done and variables updated")
        
        return
        
    def run(self, dataset):
        """
        Runs the client on the list of datasets
        @param dataset list of (X, Y) training data
        """
        for X, Y in dataset:
            print("Training on next dataset")
            self.__request_model()
            self.__train_model(X, Y)
            self.__send_model()

        print("Training done, exiting!")

    
def main():
    
    send_obj = Sender('http://127.0.0.1:5000')
    data = {'id' : 2, 'list' : json.dumps([4, 3, 5])}
    print(send_obj.send(data=data, request='post'))
    obj = json.loads(send_obj.get_resp_text())
    print(obj, type(obj), type(obj['list']))
    """
    t = 1
    while t > 0:
        print(send_obj.send(data=data, request='get'))
        print(send_obj.get_resp_text())
        print(send_obj.get_resp_status())
        t -= 1
    """

    
if __name__ == "__main__":
    main()
