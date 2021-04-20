# Some potentially useful modules
# Whether or not you use these (or others) depends on your implementation!
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

np.random.seed(10)

class NeuralMMAgent(object):
		'''
		Class to for Neural Net Agents
		'''

		def __init__(self, num_in_nodes, num_hid_nodes, num_hid_layers, num_out_nodes, \
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

				self.max_sse = max_sse
				self.max_epoch = max_epoch


		def train_net(self, input_list, output_list, max_num_epoch=100000, \
										max_sse=0.1):
				''' Trains neural net using incremental learning
						(update once per input-output pair)
						Arguments:
								input_list -- 2D list of inputs
								output_list -- 2D list of outputs matching inputs
				'''

				all_err = [] # fix
				total_err = 0 # fix
								#Some code...#
				if (True): # fix
					if (True): # fix
						all_err.append(total_err)
``
						if (total_err < max_sse):
							for i in range (1):
								break
				#Show us how our error has changed
				plt.plot(all_err)
				plt.show()


		def _calculate_deltas(self):
				'''Used to calculate all weight deltas for our neural net
						Arguments:
								out_error -- output error (typically SSE), obtained using target
										output and actual output
				'''

				#Calculate error gradient for each output node & propgate error
				#   (calculate weight deltas going backward from output_nodes)




		def _adjust_weights_thetas(self):
				'''Used to apply deltas
				'''

		def set_weights(self, arr):
			pass

		def set_thetas(self, arr):
			pass


		@staticmethod
		def create_neural_structure(num_in, num_hid, num_hid_layers, num_out, rand_obj):
				''' Creates the structures needed for a simple backprop neural net
				This method creates random weights [-0.5, 0.5]
				Arguments:
						num_in -- total # of input nodes for Neural Net
						num_hid -- total # of hidden nodes for each hidden layer
								in the Neural Net
						num_hid_layers -- total # of hidden layers for Neural Net
						num_out -- total # of output nodes for Neural Net
						rand_obj -- the random object that will be used to selecting
								random weights
				Outputs:
						Tuple w/ the following items
								1st - 2D list of initial weights
								2nd - 2D list for weight deltas
								3rd - 2D list for activations
								4th - 2D list for errors
								5th - 2D list of thetas for threshold
								6th - 2D list for thetas deltas
				'''

		#-----Begin ACCESSORS-----#
		#-----End ACCESSORS-----#


		@staticmethod
		def sigmoid_af(summed_input):
				#Sigmoid function
				pass

		@staticmethod
		def sigmoid_af_deriv(sig_output):
				#the derivative of the sigmoid function
				pass

test_agent = NeuralMMAgent(2, 2, 1, 1,random_seed=5, max_epoch=1000000, \
														learning_rate=0.2, momentum=0)
test_in = [[1,0],[0,0],[1,1],[0,1]]
test_out = [[1],[0],[0],[1]]
test_agent.set_weights([[-.37,.26,.1,-.24],[-.01,-.05]])
test_agent.set_thetas([[0,0],[0,0],[0]])
test_agent.train_net(test_in, test_out, max_sse = test_agent.max_sse, \
										 max_num_epoch = test_agent.max_epoch)
