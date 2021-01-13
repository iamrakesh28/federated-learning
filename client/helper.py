import json

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
    return json.dumps(data)

"""
Used for testing...
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

if __name__ == "__main__":
    test()
"""
