from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Activation

# Constants

NUM_IMAGES_TRAIN = 5000
NUM_CLASSES = 10
IMAGE_SHAPE = (28, 28)

# Provided Functions

def getNewModel():
    '''
    @returns Get Tensorflow based MNIST classifier
    '''
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(200))
    model.add(Activation("relu"))
    model.add(Dense(200))
    model.add(Activation("relu"))
    model.add(Dense(NUM_CLASSES))
    model.add(Activation("softmax"))

    model.build(input_shape=(NUM_IMAGES_TRAIN, IMAGE_SHAPE[0], IMAGE_SHAPE[1]))
    
    return model

def updateParam(paramList):
    '''
    @param paramList List of parameters of multiple models
    @returns Average of the provided parameters
    '''

    numModels = len(paramList)
    resParam = [layerWeight / numModels for layerWeight in paramList[0]]

    for param in paramList[1:]:
        for i, layerWeight in enumerate(param):
            resParam[i] += layerWeight / numModels

    return resParam

def predict(model, predData):
    '''
    @param model The MNIST classifier
    @param predData Data to predict on - numpy array of images
    it has shape (number of images, height of image, width of image)
    @returns Prediction for each image - it is a numpy array of 
    shape (number of images,)
    '''
    
    return model.predict(predData)

def averageParam(oldParam, newParam):
    '''
    
    '''
    oldMult = float(oldParam[1])
    newMult = float(newParam[1])

    avgWeights = []
    for i in range(len(oldParam[0])):
        oldWeight = oldParam[0][i]
        newWeight = newParam[0][i]
        avgWeights.append(
            (oldMult * oldWeight + newMult * newWeight) / (oldMult + newMult)
        )

    return avgWeights
