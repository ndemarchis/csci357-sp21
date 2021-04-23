import numpy as np
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

class NN:
    def __init__(self, num_in_nodes , num_hid_nodes, num_hid_layers, num_out_nodes, \
        learning_rate = 0.2, max_epoch=10000, max_sse=.01, momentum=0.2, \
        creation_function=None, activation_function=None, random_seed=1):
        '''
        Arguments:
            num_in_nodes -- total # of input nodes for Neural Net
            num_hid_nodes -- total # of hidden nodes for each hidden layer
                    in the Neural Net
            num_hid_layers -- total # of hidden layers for Neural Net
            num_out_nodes -- total # of output nodes for Neural Net
            learning_rate -- learning rate to be used when propagating error
            creation_function -- function that will be used to create the
                    neural network given the input
            activation_function -- list of two functions:
                    1st function will be used by network to determine activation given a weighted summed input
                    2nd function will be the derivative of the 1st function
            random_seed -- used to seed object random attribute.
                    This ensures that we can reproduce results if wanted
        '''
        assert num_in_nodes > 0 and num_hid_layers > 0 and num_hid_nodes and\
            num_out_nodes > 0, "Illegal number of input, hidden, or output layers!"

        self.num_in_nodes = num_in_nodes
        self.num_hid_nodes = num_hid_nodes
        self.num_hid_layers = num_hid_layers
        self.num_out_nodes = num_out_nodes
        self.learning_rate = learning_rate
        self.max_sse = max_sse
        self.max_epoch = max_epoch
        self.momentum = momentum
        self.creation_function = creation_function
        self.activation_function = activation_function
        self.random_seed = np.random.seed(random_seed)

        # self.train_()

    # def set_weights(arr, arry):
    #     pass
    #
    # def set_thetas(arr, arry):
    #     pass

    def classify_input(arr, arr2):
        pass

    def train_net(self, inny, outy, max_sse, max_num_epoch):
        model = Sequential()
        model.add(Dense(self.num_in_nodes, input_dim=len(inny[0]), activation="relu"))
        for i in range(self.num_hid_layers):
            model.add(Dense(self.num_hid_nodes, activation='relu'))
        model.add(Dense(len(outy[0]), activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # fit the keras model on the dataset
        model.fit(inny, outy, epochs=1000, batch_size=10)
        _, accuracy = model.evaluate(inny, outy)
        print('Accuracy: %.2f' % (accuracy*100))


test_agent = NN(2, 2, 1, 1,random_seed=5, max_epoch=1000000, \
                                                        learning_rate=0.2, momentum=0)
test_in = [[1,0],[0,0],[1,1],[0,1]]
test_out = [[1],[0],[0],[1]]
# test_agent.set_weights([[-.37,.26,.1,-.24],[-.01,-.05]])
# test_agent.set_thetas([[0,0],[0,0],[0]])
test_agent.train_net(test_in, test_out, max_sse = test_agent.max_sse, \
                                         max_num_epoch = test_agent.max_epoch)
