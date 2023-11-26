import numpy as np
from copy import deepcopy



#https://cs231n.github.io/neural-networks-case-study/
def spiral_data(points, classes):
    X = np.zeros((points*classes, 2))
    y = np.zeros(points*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(points*class_number, points*(class_number+1))
        r = np.linspace(0.0, 1, points)  # radius
        t = np.linspace(class_number*4, (class_number+1)*4, points) + np.random.randn(points)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y

class Layer_Dense:
	def __init__(self, n_inputs, n_neurons):
		#Create Weight
		self.weights = 0.1*np.random.randn(n_inputs, n_neurons).astype(np.float16)
		#Create equal amount of biases from the neurons, set all to zero
		self.biases = np.zeros((1, n_neurons))

	def forward(self, inputs):
		#Calculate output of layer amount of output equal to biases / neurons
		self.output = np.dot(inputs, self.weights) + self.biases

#Rectified Linear Unit
class Activation_ReLU:
	def forward(self, inputs):
		#Kleiner als 0 = 0
		self.output = np.where(inputs > 0, inputs, inputs * 0.01)
		#self.output = np.maximum(0, inputs)



class Activation_Softmax:
	def forward(self, inputs):
#Axis = 1 = 2D Matrix, keepdims = dimensionen einhalten [] [] [] => []
#																	[]
#																	[]
		exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
		self.output = probabilities

class NeuralNetwork:
	def __init__(self, aInputs, aOutputs):
		self.fitness = 0
		self.denses = []
		self.denses.append(Layer_Dense(aInputs,32))
		self.activation1 = Activation_ReLU()
		self.denses.append(Layer_Dense(32, 32))
		self.denses.append(Layer_Dense(32, aOutputs))
		self.activation2 = Activation_Softmax()

	def think(self, inputs):
		self.denses[0].forward(inputs)
		self.activation2.forward(self.denses[0].output)
		self.denses[1].forward(self.activation2.output)
		self.activation1.forward(self.denses[1].output)
		self.denses[2].forward(self.activation1.output)
		self.activation2.forward(self.denses[2].output)
		#print(self.denses[4].output)
		#print(self.activation2.output)
		#For higher output and non normalized values on first and last field
		#Reversed for test ToDo: Remove
		self.output = self.activation2.output
	
	def randomize(self, randomizationAmount, randomizationStrengthWeights, randomizationStrengthBiases):
		for index, dense in enumerate(self.denses):
			for index2, weight in enumerate(self.denses[index].weights):
				if(np.random.uniform(0,1) <= randomizationAmount):
					self.denses[index].weights[index2] = self.denses[index].weights[index2] + np.random.uniform(-1,1)*randomizationStrengthWeights
			for index2, biases in enumerate(self.denses[index].biases):
				if(np.random.uniform(0,1) <= randomizationAmount):
					self.denses[index].biases[index2] = self.denses[index].biases[index2] + np.random.uniform(-1,1)*randomizationStrengthBiases

	def copy(self):
		return deepcopy(self)
	def debug_network(self):
		print(self.denses[0].weights)
		print(self.denses[1].weights)
		print(self.denses[2].weights)
		print(self.denses[3].weights)
		print(self.denses[4].weights)


		

testInput = [0.0, 2.0]

'''
nn = NeuralNetwork(2, 2)
nn.think(testInput)
nnCopy = nn.copy()
print(nn.output)
nn.randomize(1, 0.1)
nn.think(testInput)
print(nn.output)
print(nnCopy.output)
'''