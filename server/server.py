import utility
import helper
from json import dumps, loads
from threading import Lock

class Server:
    """
    """
    def __init__(self, server_id):
        self.server_id = server_id
        self.model = utility.getNewModel()
        self.datasets = 0
        self.weights = self.model.get_weights()
        self.weight_send = helper.arrays_tolist(self.weights)
        self.lock = Lock

        def __update(self, weights, datasets):
            """
            Updates the weight and dataset count
            It's thread safe
            """
            self.lock.acquire()

            self.weights = utility.update_param(
                (self.weights, self.datasets),
                (weights, datasets)
            )

            self.weight_send = helper.arrays_tolist(self.weights)
            self.datasets += datasets
            self.lock.release()
            
        def __validate_update_data(self, data):

            try:
                datasets = data.get('datasets')
                assert(type(datasets) == int)
                
                updated_weight_list = loads(data.get('weights'))
                updated_weight = utility.list_toarrays(updated_weight_list)
                
                assert(
                    type(self.weight) == type(updated_weight)
                    && len(self.weight) == len(updated_weight)
                )

                for in range(len(self.weight)):
                    assert(
                        type(self.weight[i]) == type(updated_weight[i])
                        && self.weight[i].shape == updated_weight[i].shape
                    )
                    
            except:
                print("Error in validating the data!")
                return

            # everything looks fine, update the data
            self.__update(updated_weight, datasets)

            return

        except:
            print("Error in validating the model weights!")
            
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
        
