from json import loads, dumps
from numpy import array, float32

def arrays_tolist(array_list):
    """
    Convert the list of numpy arrays to list of lists
    It converts the arrays in place
    
    @param array_list list of numpy arrays 
    """

    for i in range(len(array_list)):
        array_list[i] = array_list[i].tolist()

    return

def json_encoder(data):
    """
    Convert the data into string using json encoding
    
    @data python standard data structure
    @return json encoded string
    """
    return dumps(data)


def lists_toarray(lists):
    """
    Convert the list of lists to list of numpy arrays
    Datatype is float32 as this is datatype in the tensorflow Sequential model
    It converts the lists in place
    
    @param lists list of lists 
    """

    for i in range(len(lists)):
        lists[i] = array(lists[i], float32)

    return

def json_decoder(data):
    """
    Decodes back the json data to python data structure
    
    @data json encoded string
    @return python standard data structure
    """
    return loads(data)


"""
# Used for testing...
def test():
    import numpy
    
    a = numpy.arange(4).reshape(2, 2)
    b = numpy.arange(4, 8).reshape(2, 2)

    lst = [a, b]
    print(lst)
    arrays_tolist(lst)
    print(lst)
    json_str = json_encoder(lst)
    print(json_str, type(json_str))

    lists_toarray(lst)
    print(lst)
    decoded_str = json_decoder(json_str)
    print(decoded_str, type(decoded_str))


if __name__ == "__main__":
    test()

"""
