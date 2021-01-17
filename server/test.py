import utility
import helper
import pickle
import numpy as np

def load_datasets(path, filenames):

    X = np.load(path + filenames[0])
    Y = np.load(path + filenames[1])

    return (X, Y)

def test(filename):

    fp = open(filename, 'rb')
    data = pickle.load(fp)
    fp.close()
    
    weights = data.get('weights')
    weights = helper.lists_toarray(weights)

    model = utility.getNewModel()
    model.set_weights(weights)

    X, Y = load_datasets(
        "../",
        ["mnist-test-images.npy", "mnist-test-labels.npy"]
    )

    pred = utility.predict(model, X)
    print(np.argmax(pred, axis=1), Y)
    print(sum(np.argmax(pred, axis=1) == Y) / Y.shape[0])

if __name__ == "__main__":
    test('model')
