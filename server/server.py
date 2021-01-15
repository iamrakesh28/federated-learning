import utility
import helper
from json import dumps, loads
from pickle import dump
from threading import Lock

class Server:
    """
    """
    def __init__(self, server_id, filename):
        self.server_id = server_id
        self.model = utility.getNewModel()
        self.datasets = 0
        self.weights = self.model.get_weights()
        self.weight_send = helper.arrays_tolist(self.weights)
        self.lock = Lock()
        self.filename = filename

    def __update(self, weights, datasets):
        """
        Updates the weight and dataset count
        It's thread safe
        """
        self.lock.acquire()
        
        self.weights = utility.averageParam(
            (self.weights, self.datasets),
            (weights, datasets)
        )
        
        self.weight_send = helper.arrays_tolist(self.weights)
        self.datasets += datasets
        self.lock.release()

        return
            
    def validate_update_data(self, data):
        
        try:
            datasets = data.get('datasets')
            assert(type(datasets) == int and datasets > 0)

            updated_weight_list = loads(data.get('weights'))
            updated_weight = helper.lists_toarray(updated_weight_list)

            assert(
                type(self.weights) == type(updated_weight)
                and len(self.weights) == len(updated_weight)
            )

            for i in range(len(self.weights)):
                assert(
                    type(self.weights[i]) == type(updated_weight[i])
                    and self.weights[i].shape == updated_weight[i].shape
                )
                    
        except:
            print("Error in validating the data!")
            return
            
        # everything looks fine, update the data
        self.__update(updated_weight, datasets)
        
        return
        
            
    def read_weights(self):
        """
        """
        self.lock.acquire()
        data = {
            'id' : self.server_id,
            'datasets' : self.datasets,
            'weights' : self.weight_send
        }
        self.lock.release()
        
        return data

    def save_model(self):

        self.lock.acquire()
        fp = open(self.filename, 'wb')
        data = {
            'datasets' : self.datasets,
            'weights' : self.weight_send
        }
        pickle.dump(data, fp)
        fp.close()
        self.lock.release()
