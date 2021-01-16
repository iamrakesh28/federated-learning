from client import Client
import numpy as np

def load_datasets(path, filenames):

    X = np.load(path + filenames[0])
    Y = np.load(path + filenames[1])

    return (X, Y)

def main():

    client = Client('http://127.0.0.1:5000', 'mustang28')
    X, Y = load_datasets(
        "../",
        ["mnist-train-images.npy", "mnist-train-labels.npy"]
    )
    print(X.shape, Y.shape)
    client.run([(X[:50], Y[:50]), (X[:50], Y[:50])])
    
if __name__ == "__main__":
    main()
