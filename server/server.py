import utility
import helper
import pickle
from json import dumps, loads
from threading import Lock, Condition

SAVE_MODEL = 2

class Server:
    """
    """
    def __init__(self, server_id, filename, logger):
        self.server_id = server_id
        self.model = utility.getNewModel()
        self.datasets = 0
        self.weights = self.model.get_weights()
        self.weight_send = helper.arrays_tolist(self.weights)
        self.lock = Lock()
        self.filename = filename
        self.save = SAVE_MODEL
        self.logger = logger
        self.readers = 0
        self.read_write = Condition(self.lock)

    def __update(self, weights, datasets):
        """
        Updates the weight and dataset count
        It's thread safe
        """
        # acquire write lock
        self.read_write.acquire()

        while self.readers > 0:
            self.read_write.wait()

        self.weights = utility.averageParam(
            (self.weights, self.datasets),
            (weights, datasets)
        )
        
        self.weight_send = helper.arrays_tolist(self.weights)
        self.datasets += datasets

        if self.save == 0:
            self.__save_model()
            self.save = SAVE_MODEL
        else:
            self.save -= 1

        # release write lock
        self.read_write.release()

        return
            
    def validate_update_data(self, data):

        try:
            datasets = int(data.get('datasets'))
            assert(datasets > 0)
            
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
            self.logger.error("Error in validating the data!")
            return

        # everything looks fine, update the data
        self.__update(updated_weight, datasets)
        self.logger.info("Successfully updated the model")
        
        return
        
            
    def read_weights(self):
        """
        """
        # acquire read lock
        self.read_write.acquire()
        self.readers += 1
        self.read_write.release()

        data = {
            'id' : self.server_id,
            'datasets' : self.datasets,
            'weights' : self.weight_send
        }

        # release read lock
        self.read_write.acquire()
        self.readers -= 1

        if self.readers == 0:
            self.read_write.notify_all()
        self.read_write.release()
                
        return data

    def __save_model(self):

        fp = open(self.filename, 'wb')
        data = {
            'datasets' : self.datasets,
            'weights' : self.weight_send
        }
        pickle.dump(data, fp)
        fp.close()

        self.logger.info("Successfully saved the model")
