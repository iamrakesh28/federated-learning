from utility import NUM_IMAGES_TRAIN
from client import Client
import numpy as np

def load_datasets(path, filenames):

    X = np.load(path + filenames[0])
    Y = np.load(path + filenames[1])

    return (X, Y)

def main():

    client_id = input("Client Id : ")
    line = input("Dataset Range : ").split(' ')
    L, R = (None, None)

    try:
        L = int(line[0])
        R = int(line[1])
        assert(L >= 1 and L <= R and R <= 12)
    except:
        print("Invalid dataset range! (1 <= L <= R <= 12)")
        return
        
    client = Client('http://127.0.0.1:5000', client_id)
    X, Y = load_datasets(
        "../",
        ["mnist-train-images.npy", "mnist-train-labels.npy"]
    )

    datasets = []
    for i in range(L - 1, R):
        start = i * NUM_IMAGES_TRAIN
        end = start + NUM_IMAGES_TRAIN
        datasets.append((X[start:end], Y[start:end]))
        
    client.run(datasets)
    
if __name__ == "__main__":
    main()
