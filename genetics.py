from neuronalnetwork import NeuralNetwork
import numpy as np
import pickle
#Testing time
import time
import math
#Multithreading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import logging



class Genetics():
	def __init__(self, population, ghostAgentsPop, aInputs, aOutputs, FITNESS_REWARD):
		#self.p=mp.Pool(16)
		self.agents = []
		self.newAgents = []
		self.ghostAgents = []
		self.FITNESS_REWARD = FITNESS_REWARD
		self.population = population
		self.ghostAgentsPop = ghostAgentsPop
		for x in range(self.population):
			self.agents.append(NeuralNetwork(aInputs, aOutputs))
		for x in range(self.population):
			self.agents[x].randomize(1, 0.05, 0.1)




	def thinkParticular(self, index, inputs):
		#print(inputs)
		self.agents[index].think(inputs)
		return self.agents[index].output

	def thinkParticularGhost(self, index, inputs):
		self.ghostAgents[index].think(inputs)
		return self.ghostAgents[index].output

	def think(self, inputs):
		for i in range(len(self.agents)-1, -1, -1):
			self.agents[i].think(inputs)

	def shuffle(self):
		np.random.shuffle(self.agents)


	def calculateFitnessParticular(self, index,input):
		self.agents[index].fitness += input

	def calculateFitness(self, randomNumber):
		for i in range(len(self.agents)-1, -1, -1):
			if(randomNumber >= 0.5 and self.agents[i].output[0][0] >= 0.5 or randomNumber <= 0.5 and self.agents[i].output[0][0] <= 0.5):
				self.agents[i].fitness += 1.0


	def copyAgents(self, i):
		for y in range(0, int(self.agents[i].fitness/2)):
			self.newAgents.append(self.agents[i].copy())

	def deleteGhostX(self, i):
		if(len(self.ghostAgents)>10):
			self.ghostAgents.pop(i)


	def copyAgenttoGhost(self, i):
		if(len(self.ghostAgents) >= self.ghostAgentsPop):
			self.ghostAgents.pop(np.random.randint(0, self.ghostAgentsPop))
		self.ghostAgents.append(self.agents[i].copy())


	def getFitness(self):
		totalFitness = 0
		for i in range(len(self.agents)-1, -1, -1):
			totalFitness += self.agents[i].fitness
		return totalFitness

	def resetFitness(self):
		for i in range(len(self.agents)-1, -1, -1):
			self.agents[i].fitness = 0


	def savetoFile(self, fileName, quality, amountOfSaves):

		sortedAgents = sorted(self.agents, key=lambda k: k.fitness)

		for i in range(amountOfSaves):
				with open("dumbed_saves/" + fileName + "-" + str(i) + "-q-"+ str(sortedAgents[len(sortedAgents)-i-1].fitness).replace(".", "_")  + ".txt", 'wb') as fh:
					pickle.dump(sortedAgents[len(sortedAgents)-i-1], fh)



	def roundClose(self, randomizationAmount, randomuzationStrengthWeights, randomuzationStrengthBiases):
		#start_time = time.time()
		totalFitness = 0
		self.newAgents = []
		totalRightGuesses = 0
		#In precentage
		x = []

		for i in range(len(self.agents)-1, -1, -1):
			totalFitness += self.agents[i].fitness
			totalRightGuesses += self.agents[i].fitness
		for i in range(len(self.agents)-1, -1, -1):
			#Fitness calculation
			#devide by 5 to get smaller fitness
			#Agents with fitness 10/5 = 2 **2 = 4 20 / 5 = 4 **2 = 16
			#self.agents[i].fitness = self.agents[i].fitness + 100
			self.agents[i].fitness = self.agents[i].fitness/(totalFitness/300)
			self.agents[i].fitness = math.pow(self.agents[i].fitness,self.FITNESS_REWARD)
			#Just in case every agent has a score of 0
			#self.agents[i].fitness += 1

			#self.p.map(self.newAgents.append(self.agents[i].copy()), range(0, int(self.agents[i].fitness)))
			#self.p.close()
			#self.p.join()
			#Multithread not able to do lists
			#with ThreadPoolExecutor() as executor:
			#	executor.map(self.newAgents.append(self.agents[i].copy()), range(0, int(self.agents[i].fitness)))
			for y in range(0, int(self.agents[i].fitness)):
				self.newAgents.append(self.agents[i].copy())
		#print("totalFitness: " + str(totalFitness))
		logging.debug("newAgents list size: " + str(len(self.newAgents)))

		#print("Checkittttt")
		#print(len(self.newAgents))
		#np.random.randint(0,0)
		self.agents = []
		#executor = concurrent.futures.ThreadPoolExecutor() # Or ProcessPoolExecutor
		#executor.map(self.agents.append(self.newAgents[np.random.randint(0, len(self.newAgents)-1)].copy()), range(0, 10))
		#time.sleep(2)
		for x in range(self.population):
			#print(len(self.agents))
			self.agents.append(self.newAgents[np.random.randint(0, len(self.newAgents)-1)].copy())
			self.agents[x].fitness = 0
			#Mutate
			self.agents[x].randomize(randomizationAmount, randomuzationStrengthWeights, randomuzationStrengthBiases)

		#Remember print is bevore randomization takes place
		#print("--- %s seconds ---" % (time.time() - start_time))
		return totalRightGuesses