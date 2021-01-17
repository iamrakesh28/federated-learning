from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy

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

def predict(model, predData):
    '''
    @param model The MNIST classifier
    @param predData Data to predict on - numpy array of images
    it has shape (number of images, height of image, width of image)
    @returns Prediction for each image - it is a numpy array of 
    shape (number of images,)
    '''
    
    return model.predict(predData)

def trainOnData(model, trainData):
    '''
    @param model The MNIST classifier
    @param trainData Data to train the model on - tuple
    (numpy array of images, numpy array of labels), the numpy array of images
    has shape (number of images, height of image, width of image), the numpy
    array of labels has shape (number of images,)
    @returns None
    '''

    model.compile(
        optimizer=Adam(0.001),
        loss=SparseCategoricalCrossentropy(),
        metrics=[SparseCategoricalAccuracy()],
    )

    (X, y) = trainData

    model.fit(
        X,
        y,
        epochs=20
    )
