from numpy import array, float32

def arrays_tolist(array_list):
    """
    Convert the list of numpy arrays to list of lists
    
    @param array_list list of numpy arrays 
    """

    new_list = []
    for i in range(len(array_list)):
        new_list.append(array_list[i].tolist())

    return new_list


def lists_toarray(lists):
    """
    Convert the list of lists to list of numpy arrays
    Datatype is float32 as this is datatype in the tensorflow Sequential model
    
    @param lists list of lists 
    """

    new_list = []
    for i in range(len(lists)):
        new_list.append(array(lists[i], dtype=float32))

    return new_list
