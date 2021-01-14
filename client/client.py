#import utility
from random import randint
from sender import Sender
from json import loads, dumps
from time import sleep


class Client:
    """
    """
    def __init__(self, addr):
        self.sender = Sender(addr)
        self.model = utility.getNewModel()
        self.RETRY = 5
        self.MAX_WAIT = 5
        self._id = 'iamrakesh28'
        self.dataset = 0
        self.weight = self.model.get_weights()

    def __validate_data(self):

        success = False
        try:
            data = loads(self.sender.get_resp_text())
            updated_weight = data.get('weight')
            assert(
                type(self.weight) == type(updated_weight)
                && len(self.weight) == len(updated_weight)
            )

            for in range(len(self.weight)):
                assert(
                    type(self.weight[i]) == type(updated_weight[i])
                    && self.weight[i].shape == updated_weight[i].shape
                )

            
            # everything looks fine, update the weight
            self.dataset = data['dataset']
            self.weight = updated_weight
            success = True

        except:
            print("Error in validating the model weights!")

        return success
            
    def __request_model(self):

        nos_retry = 0
        data = {'id' : self_id, 'send' : False}
        
        while nos_retry < RETRY:

            print("Trying to get the server model weights!")
            success = self.sender.send(data=data, request='post')

            if success and self.__validate_data():
                # Successfully got the weights
                print("Successfully got the weights")
                return

            print("Failed to get the weights!")

            # Try more if possible but wait for few seconds
            nos_retry += 1
            sleep(randint(0, self.MAX_WAIT))

        # Couldn't get the updated model from the server
        # Continue with the previous version model
        return

    def __send_model(self):

    
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
