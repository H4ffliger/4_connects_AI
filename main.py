from threading import Thread
import multiprocessing
from genetics import Genetics
from gamefield import GameField
import numpy as np
import time
import sys
from concurrent.futures import ThreadPoolExecutor
#For passing arguments
from functools import partial
from montecarlo import monteCarloAI
import pyfiglet
#Analyzer
import tracemalloc
#List add
from operator import add
import random
#game copy min max
from copy import deepcopy
import argparse
import os


import logging
logging.basicConfig(level=logging.INFO)


'''
Performance checks
import linecache
import os
import tracemalloc

def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

tracemalloc.start()
'''

#Introduction
ascii_banner = pyfiglet.figlet_format("GNeuroNetWK")
print(ascii_banner)

print("Version 0.03\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to outperform the minmax algorithm\n" +
	"Currently testing the network\n" + 
	"Beat the game 4 connects with external monte carlo score progress check\n\n")


#Game Specific
gameW = 5
gameH = 4
gameSize = gameW*gameH

#Genetic Algorithm

#ROUND_COUNT 0 = 1'000'000
#ROUND_COUNT = 10000
#Individual agents
AGENT_INPUTS = 4*4+2
#Output needs to be at least 2
AGENT_OUTPUTS = 4 #ToDo:Check if not one to small

#Reward is exponential default 1.75
FITNESS_REWARD = 1 #Temporary disabled
#Population / Probability = real probability
#Games each round for each agent
SHOWAFTER = 10000000
SHOWEVERY = 10000

#How often checks of the AI happen
QUALITY_CHECK_RATE = 5

#1 = >= Durchschnitt 1.1 = 110% von normaler Qualität
EXPORTQUALITY = 1.3
EXPORTAFTER = 2
EXPORTAMOUNT = 10


#Data for graph
roundsCompleted = 0
fitnessOfRound = 0


logging.info("################# Unit Testing #################")
testResult = "0"
testGame = GameField()
testGameOver = False
testChosenMove=2
testInputToPlay = True
while(testResult == "0"):
	validTestMoveMove = False
	#Play in center on x_cord 5, stack to five then move left
	#If testInput wins or draws unit test has failed
	if(testInputToPlay):
		testChosenMove = gameW-1
		while (validTestMoveMove == False and testChosenMove != -2):
			validTestMoveMove = testGame.turn(testChosenMove)
			testChosenMove -=1

		#testGame.turn(validTestMoveMove)
		testInputToPlay = False
	else:
		testChosenMove = monteCarloAI(deepcopy(testGame))
		#Check if move is valid
		validTestMoveMove = testGame.turn(testChosenMove)
		testInputToPlay = True
		#if(validTestMoveMove):


	#Game is a draw
	if(validTestMoveMove == False):
		testResult = "Draw"

	#Check for a winner
	if(testGame.check_winner()):
		if(testInputToPlay):
			testResult = "MonteCarloWon"
		else:
			testResult = "PredefinedMovesWon"


#Debug
if(testResult == "MonteCarloWon"):
	logging.info("UnitTest SUCCESS: MonteCarlAI algorithm works")
else:
	logging.error("UnitTest ERROR: Monte Carlo Algorithm problem, Game status: " + testResult)
	logging.error(testGame.print_board())
logging.info("################# Unit Testing #################")

#For automating hyperparameters
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='GNeuroNetWK for learning the 4 connects game')
	#Hyphen makes argument optional
	parser.add_argument('learning_Name', type=str, default="TESTRUN",help="Name of the GNeuroNetWK learning run")
	parser.add_argument('-randomizationAmount', type=float, default=0.01,help="Amount of mutation which should happen with the genes")
	parser.add_argument('-randomizationStrengthWeights', type=float, default=0.02,help="Value of how strong the Weights should be mutated")
	parser.add_argument('-randomizationStrengthBiases', type=float, default=0.02,help="Value of how strong the Biases should be mutated")
	parser.add_argument('-WINFITNESS', type=float, default=4,help="Reward of win vs current AI")
	parser.add_argument('-DRAWFITNESS', type=float, default=0.6,help="Reward of draw vs current AI")
	parser.add_argument('-LOSEFITNESS', type=float, default=-0.5,help="Reward of lose vs current AI")
	parser.add_argument('-WINFITNESSGHOST', type=float, default=4,help="Reward of win vs old saved AI")
	parser.add_argument('-DRAWFITNESSGHOST', type=float, default=0.2,help="Reward of draw vs old saved AI")
	parser.add_argument('-LOSEFITNESSGHOST', type=float, default=-0.5,help="Reward of lose vs old saved AI")
	parser.add_argument('-GAMESPERROUND', type=int, default=5,help="Games per generation vs a current AI")
	parser.add_argument('-GHOSTGAMESPERROUND', type=int, default=2,help="Games per generation vs old saved AI")
	parser.add_argument('-POP_COUNTER', type=int, default=100,help="Population size of the current AIs")
	parser.add_argument('-GHOSTAGENTS_POP', type=int, default=100,help="Population size of saved old AIs")
	parser.add_argument('-SNAPSHOT_PROBABILITY', type=int, default=20,help="Probability of saving a current AI to the old saved AIs")
	parser.add_argument('-exportRate', type=int, default=50,help="Rate at which generations genetics get exported")
	parser.add_argument('-ROUND_COUNT', type=int, default=2000,help="Amount of rounds to be played")
	#FITNESS_REWARD = 1 #Temporary disabled
	args = parser.parse_args()
	randomizationAmount = args.randomizationAmount
	randomizationStrengthWeights = args.randomizationStrengthWeights
	randomizationStrengthBiases = args.randomizationStrengthBiases
	WINFITNESS = args.WINFITNESS
	DRAWFITNESS = args.DRAWFITNESS
	LOSEFITNESS = args.LOSEFITNESS
	WINFITNESSGHOST = args.WINFITNESSGHOST
	DRAWFITNESSGHOST = args.DRAWFITNESSGHOST
	LOSEFITNESSGHOST = args.LOSEFITNESSGHOST
	GAMESPERROUND = args.GAMESPERROUND
	GHOSTGAMESPERROUND = args.GHOSTGAMESPERROUND
	POP_COUNT = args.POP_COUNTER
	GHOSTAGENTS_POP = args.GHOSTAGENTS_POP
	SNAPSHOT_PROBABILITY = args.SNAPSHOT_PROBABILITY
	EXPORTEVERYXMOVE = args.exportRate
	ROUND_COUNT = args.ROUND_COUNT


#For a more organized hyperparameter tuning
FOLER_STATS = 'dumbed_saves/' + args.learning_Name + '_stats/'
os.makedirs(FOLER_STATS, exist_ok=True)


if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

#InitializePopulation
genetics1 = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)
genetics2 = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)

#Copy random to ghosts
for i in range(0, 1):
	genetics1.copyAgenttoGhost(i)
	genetics2.copyAgenttoGhost(i)

#AIPickStuff
bannedOutputs = 0

def getAIMove(userToPlay, board, indexMove):
	#Append all scores to this list
	moveProbabiltyScoreOverall = []
	for ai_height in range(gameH-4, -1, -1):
		for ai_width in range(gameW-4, -1, -1):
			moveProbabiltyScore = [0] * gameW
			#Create field of inputs for the neural network
			rows = board[ai_height:ai_height+4]
			viewfield = []
			for x in range(0,4):
				viewfield.extend(rows[x][ai_width:ai_width+4])

			moveProbabiltyScoreOffset = [0] * ai_width
			viewfield.insert(0, ai_width)
			viewfield.insert(0, ai_height)
			moveProbabiltyScorePartly = genetics1.thinkParticular(userToPlay, viewfield).flatten()
			moveProbabiltyScoreOffset.extend(moveProbabiltyScorePartly)
			moveProbabiltyScoreFiller = [0] * (gameW - ai_width - 4)
			moveProbabiltyScoreOffset.extend(moveProbabiltyScoreFiller)
			moveProbabiltyScore = list(map(add, moveProbabiltyScore, moveProbabiltyScoreOffset))
			moveProbabiltyScoreOverall.append(moveProbabiltyScore)

	# Average the colums so that the edges of the game don't have lower values
	moveProbabiltyScoreSum = [0] * gameW
	moveProbabiltyScoreSumCount = [0] * gameW
	moveProbabiltyScoreAverage = [0] * gameW
	for i in range(len(moveProbabiltyScoreOverall)-1, -1, -1):
		for s in range(len(moveProbabiltyScoreOverall[i])-1, -1, -1):
			if(moveProbabiltyScoreOverall[i][s] != 0):
				moveProbabiltyScoreSum[s] += moveProbabiltyScoreOverall[i][s]
				moveProbabiltyScoreSumCount[s] += 1
	for i in range(len(moveProbabiltyScoreSum)-1, -1, -1):
		moveProbabiltyScoreAverage[i] = moveProbabiltyScoreSum[i] / moveProbabiltyScoreSumCount[i]

	sortedPicks = sorted(range(len(moveProbabiltyScoreAverage)), key=lambda k: moveProbabiltyScoreAverage[k])
	return sortedPicks[indexMove]

def getAI2Move(userToPlay, board, indexMove):
	#Append all scores to this list
	moveProbabiltyScoreOverall = []
	for ai_height in range(gameH-4, -1, -1):
		for ai_width in range(gameW-4, -1, -1):
			moveProbabiltyScore = [0] * gameW
			#Create field of inputs for the neural network
			rows = board[ai_height:ai_height+4]
			viewfield = []
			for x in range(0,4):
				viewfield.extend(rows[x][ai_width:ai_width+4])

			moveProbabiltyScoreOffset = [0] * ai_width

			viewfield.insert(0, ai_width)
			viewfield.insert(0, ai_height)
			moveProbabiltyScorePartly = genetics2.thinkParticular(userToPlay, viewfield).flatten()
			moveProbabiltyScoreOffset.extend(moveProbabiltyScorePartly)
			moveProbabiltyScoreFiller = [0] * (gameW - ai_width - 4)
			moveProbabiltyScoreOffset.extend(moveProbabiltyScoreFiller)
			moveProbabiltyScore = list(map(add, moveProbabiltyScore, moveProbabiltyScoreOffset))
			moveProbabiltyScoreOverall.append(moveProbabiltyScore)
	# Average the colums so that the edges of the game don't have lower values
	moveProbabiltyScoreSum = [0] * gameW
	moveProbabiltyScoreSumCount = [0] * gameW
	moveProbabiltyScoreAverage = [0] * gameW
	for i in range(len(moveProbabiltyScoreOverall)-1, -1, -1):
		for s in range(len(moveProbabiltyScoreOverall[i])-1, -1, -1):
			if(moveProbabiltyScoreOverall[i][s] != 0):
				moveProbabiltyScoreSum[s] += moveProbabiltyScoreOverall[i][s]
				moveProbabiltyScoreSumCount[s] += 1
	for i in range(len(moveProbabiltyScoreSum)-1, -1, -1):
		moveProbabiltyScoreAverage[i] = moveProbabiltyScoreSum[i] / moveProbabiltyScoreSumCount[i]

	sortedPicks = sorted(range(len(moveProbabiltyScoreAverage)), key=lambda k: moveProbabiltyScoreAverage[k])
	return sortedPicks[indexMove]

def getGhostMove(userToPlay, board, indexMove):
	#Append all scores to this list
	moveProbabiltyScoreOverall = []
	for ai_height in range(gameH-4, -1, -1):
		for ai_width in range(gameW-4, -1, -1):
			moveProbabiltyScore = [0] * gameW
			#Create field of inputs for the neural network
			rows = board[ai_height:ai_height+4]
			viewfield = []
			for x in range(0,4):
				viewfield.extend(rows[x][ai_width:ai_width+4])

			moveProbabiltyScoreOffset = [0] * ai_width
			viewfield.insert(0, ai_width)
			viewfield.insert(0, ai_height)
			moveProbabiltyScorePartly = genetics1.thinkParticularGhost(userToPlay, viewfield).flatten()
			moveProbabiltyScoreOffset.extend(moveProbabiltyScorePartly)
			moveProbabiltyScoreFiller = [0] * (gameW - ai_width - 4)
			moveProbabiltyScoreOffset.extend(moveProbabiltyScoreFiller)
			moveProbabiltyScore = list(map(add, moveProbabiltyScore, moveProbabiltyScoreOffset))
			moveProbabiltyScoreOverall.append(moveProbabiltyScore)
	# Average the colums so that the edges of the game don't have lower values
	moveProbabiltyScoreSum = [0] * gameW
	moveProbabiltyScoreSumCount = [0] * gameW
	moveProbabiltyScoreAverage = [0] * gameW
	for i in range(len(moveProbabiltyScoreOverall)-1, -1, -1):
		for s in range(len(moveProbabiltyScoreOverall[i])-1, -1, -1):
			if(moveProbabiltyScoreOverall[i][s] != 0):
				moveProbabiltyScoreSum[s] += moveProbabiltyScoreOverall[i][s]
				moveProbabiltyScoreSumCount[s] += 1
	for i in range(len(moveProbabiltyScoreSum)-1, -1, -1):
		moveProbabiltyScoreAverage[i] = moveProbabiltyScoreSum[i] / moveProbabiltyScoreSumCount[i]

	sortedPicks = sorted(range(len(moveProbabiltyScoreAverage)), key=lambda k: moveProbabiltyScoreAverage[k])
	return sortedPicks[indexMove]

def getGhost2Move(userToPlay, board, indexMove):
	#Append all scores to this list
	moveProbabiltyScoreOverall = []
	for ai_height in range(gameH-4, -1, -1):
		for ai_width in range(gameW-4, -1, -1):
			moveProbabiltyScore = [0] * gameW
			#Create field of inputs for the neural network
			rows = board[ai_height:ai_height+4]
			viewfield = []
			for x in range(0,4):
				viewfield.extend(rows[x][ai_width:ai_width+4])

			moveProbabiltyScoreOffset = [0] * ai_width
			viewfield.insert(0, ai_width)
			viewfield.insert(0, ai_height)
			moveProbabiltyScorePartly = genetics2.thinkParticularGhost(userToPlay, viewfield).flatten()
			moveProbabiltyScoreOffset.extend(moveProbabiltyScorePartly)
			moveProbabiltyScoreFiller = [0] * (gameW - ai_width - 4)
			moveProbabiltyScoreOffset.extend(moveProbabiltyScoreFiller)
			moveProbabiltyScore = list(map(add, moveProbabiltyScore, moveProbabiltyScoreOffset))
			moveProbabiltyScoreOverall.append(moveProbabiltyScore)
	# Average the colums so that the edges of the game don't have lower values
	moveProbabiltyScoreSum = [0] * gameW
	moveProbabiltyScoreSumCount = [0] * gameW
	moveProbabiltyScoreAverage = [0] * gameW
	for i in range(len(moveProbabiltyScoreOverall)-1, -1, -1):
		for s in range(len(moveProbabiltyScoreOverall[i])-1, -1, -1):
			if(moveProbabiltyScoreOverall[i][s] != 0):
				moveProbabiltyScoreSum[s] += moveProbabiltyScoreOverall[i][s]
				moveProbabiltyScoreSumCount[s] += 1
	for i in range(len(moveProbabiltyScoreSum)-1, -1, -1):
		moveProbabiltyScoreAverage[i] = moveProbabiltyScoreSum[i] / moveProbabiltyScoreSumCount[i]

	sortedPicks = sorted(range(len(moveProbabiltyScoreAverage)), key=lambda k: moveProbabiltyScoreAverage[k])
	return sortedPicks[indexMove]


def gameRoundGhost(y: int, idx: int):

	#All fight the same enemy
	if(y == 0):
		enemy = np.random.randint(0, len(genetics1.ghostAgents))
	else:
		enemy = np.random.randint(0, len(genetics2.ghostAgents))

	for x in range(POP_COUNT-1, -1, -1):


		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 generations
		firstMoveNoise = np.random.randint(0,gameW)
		firstMovePlayed = False


		while not game_over:
			debugMoves = 0
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True
					chosen_move = firstMoveNoise
				elif(y == 0):
					#userToPay 0 = Ghost gets first move
					if(userToPlay == 0):
						chosen_move = getGhostMove(enemy, game.board, bannedOutputs)
					else:
						chosen_move = getAI2Move(x, game.board, bannedOutputs)
				else:
					if(userToPlay == 0):
						chosen_move = getAIMove(x, game.board, bannedOutputs)

					else:
						chosen_move = getGhost2Move(enemy, game.board, bannedOutputs)



				valid_move = game.turn(chosen_move)
				if(valid_move == False and game_over == False):
					bannedOutputs += 1
					if(chosen_move == -1 or bannedOutputs >= gameW):
						if(y == 0):
							genetics2.calculateFitnessParticular(x, DRAWFITNESSGHOST)
						else:
							genetics1.calculateFitnessParticular(x, DRAWFITNESSGHOST)
						game_over = True
						valid_move = True

				#if(x > POP_COUNT-2 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
				#	time.sleep(0.3)
				#	print(game.print_board())
			



			# End the game if there is a winner CHECK IS REVERSED
			if(game.check_winner() and game_over == False):
				#X wins the game
				#Ghosts
				#y == 0 and usertoplay == 0 AI win
				#y == 0 and usertoplay == 1 AI lose
				#y == 1 and usertoplay == 0 AI lose
				#y == 1 and usertoplay == 1 AI win
				if(y == 0):
					if(userToPlay == 0):
						genetics2.calculateFitnessParticular(x, LOSEFITNESSGHOST)#Must be 3
					else:
						genetics2.calculateFitnessParticular(x, WINFITNESSGHOST)#Must be 3
				#1 winns the game
				else:
					if(userToPlay == 0):
						genetics1.calculateFitnessParticular(x, WINFITNESSGHOST)#Must be 3
					else:
						genetics1.calculateFitnessParticular(x, LOSEFITNESSGHOST)#Must be 3
				game_over = True
				valid_move = True

			if(userToPlay == 0):
				userToPlay = 1
			else:
				userToPlay = 0


			# End the game if there is a tie
			if not any(0 in z for z in game.board):
				if(game_over == False):
					if(y == 0):
						genetics2.calculateFitnessParticular(x, DRAWFITNESSGHOST)
					else:
						genetics1.calculateFitnessParticular(x, DRAWFITNESSGHOST)
				game_over = True
				valid_move = True


def gameRoundAI(y: int, idx: int):

	#All fight the same enemy
	if(y == 0):
		enemy = np.random.randint(0, POP_COUNT)
	else:
		enemy = np.random.randint(0, POP_COUNT)

	for x in range(POP_COUNT-1, -1, -1):

		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 generations
		firstMoveNoise = np.random.randint(0,gameW)
		firstMovePlayed = False


		while not game_over:
			debugMoves = 0
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True
					chosen_move = firstMoveNoise
				elif(y == 0):
					#userToPay 0 = Ghost gets first move
					if(userToPlay == 0):
						chosen_move = getAIMove(enemy, game.board, bannedOutputs)
					else:
						chosen_move = getAI2Move(x, game.board, bannedOutputs)

				else:
					if(userToPlay == 0):
						chosen_move = getAIMove(x, game.board, bannedOutputs)

					else:
						chosen_move = getAI2Move(enemy, game.board, bannedOutputs)


				valid_move = game.turn(chosen_move)
				if(valid_move == False and game_over == False):
					bannedOutputs += 1
					if(chosen_move == -1 or bannedOutputs >= gameW):
						if(y == 0):
							genetics2.calculateFitnessParticular(x, DRAWFITNESS)
						else:
							genetics1.calculateFitnessParticular(x, DRAWFITNESS)
						game_over = True
						valid_move = True

				#if(x > POP_COUNT-1 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
					#time.sleep(0.2)
					#print(game.print_board())
			



			# End the game if there is a winner CHECK IS REVERSED
			if(game.check_winner() and game_over == False):
				#X wins the game
				#Ghosts
				#y == 0 and usertoplay == 0 AI win
				#y == 0 and usertoplay == 1 AI lose
				#y == 1 and usertoplay == 0 AI lose
				#y == 1 and usertoplay == 1 AI win
				#genetics2 training
				if(y == 0):
					if(userToPlay == 0):
						genetics2.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
					else:
						genetics2.calculateFitnessParticular(x, WINFITNESS)#Must be 3
				#1 genetics1 training
				else:
					if(userToPlay == 0):
						genetics1.calculateFitnessParticular(x, WINFITNESS)#Must be 3
					else:
						genetics1.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
				game_over = True
				valid_move = True

			if(userToPlay == 0):
				userToPlay = 1
			else:
				userToPlay = 0


			# End the game if there is a tie
			if not any(0 in z for z in game.board):
				if(game_over == False):
					if(y == 0):
						genetics2.calculateFitnessParticular(x, DRAWFITNESS)
					else:
						genetics1.calculateFitnessParticular(x, DRAWFITNESS)
				game_over = True
				valid_move = True


def checkAIQuality(y: int, idx: int):
	qual_check_wins = 0
	qual_check_draws = 0
	qual_check_losses = 0
	#logging.debug("Starting quality check on generation " + str(y+1))
	#Performance wise only 50% of the population gets testet
	for x in range(int(POP_COUNT/2)-1, -1, -1):
		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 generations
		firstMoveNoise = np.random.randint(0,gameW)
		firstMovePlayed = False

		#print("Checking agent " + str(x))
		while not game_over:
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True
					chosen_move = firstMoveNoise
				elif(y == 0):
					#userToPay 0 = Ghost gets first move
					if(userToPlay == 0):
						chosen_move = monteCarloAI(deepcopy(game))
						#chosen_move = getGhostMove(enemy, game.board, bannedOutputs)
					else:
						chosen_move = getAI2Move(x, game.board, bannedOutputs)
				else:
					if(userToPlay == 0):
						chosen_move = getAIMove(x, game.board, bannedOutputs)
					else:
						#chosen_move = getGhost2Move(enemy, game.board, bannedOutputs)
						chosen_move = monteCarloAI(deepcopy(game))

				valid_move = game.turn(chosen_move)
					
				if(valid_move == False and game_over == False):
					
					bannedOutputs += 1
					if(chosen_move == -1 or bannedOutputs >= gameW):
						if(y == 0):
							qual_check_draws += 1
						else:
							qual_check_draws += 1
						game_over = True
						valid_move = True
						return
				#if(x < 5 and y == 0):
				#	time.sleep(0.3)
				#	print(game.print_board())
			



			# End the game if there is a winner CHECK IS REVERSED
			if(game.check_winner() and game_over == False):
				#X wins the game
				#Ghosts
				# y == 0 then gen2
				# y == 1 then gen1
				#y == 0 and usertoplay == 1 AI win montecarlo loss
				#y == 0 and usertoplay == 0 AI lose
				#y == 1 and usertoplay == 1 AI lose
				#y == 1 and usertoplay == 0 AI win
				if(y == 0):
					if(userToPlay == 0):
						qual_check_losses += 1
						#print("AI loses to montecarlo")
					else:
						qual_check_wins += 1
						#print("AI wins to montecarlo")
					#time.sleep(2)

				#1 winns the game
				else:
					if(userToPlay == 0):
						qual_check_wins += 1
					else:
						qual_check_losses += 1
				game_over = True
				valid_move = True

			if(userToPlay == 0):
				userToPlay = 1
			else:
				userToPlay = 0


			# End the game if there is a tie
			if not any(0 in z for z in game.board):
				if(game_over == False):
					if(y == 0):
						qual_check_draws += 1
					else:
						qual_check_draws += 1
				game_over = True
				valid_move = True
	file_object = open(FOLER_STATS + args.learning_Name + "_GEN_"+str(2-y) +"_min_max_progress.csv", 'a')
	file_object.write(str(roundsCompleted)+"," +str(qual_check_wins)+","+str(qual_check_draws)+","+str(qual_check_losses)+"\n")
	file_object.close()
	print("Generation" + str(2-y) + ": wins: " + str(qual_check_wins) + " draws: " + str(qual_check_draws) + " losses: " + str(qual_check_losses))	
	return qual_check_wins + (qual_check_draws/6)


#Main loop
for b in range(ROUND_COUNT-1, -1, -1):
	hyperParameterScore = 0

	#PlayAgainstGhost
	for y in range(0,2):
		for x in range(0, GAMESPERROUND):
			gameRoundAI(y,1)



		



		#Debug Testing gameRound(y,1)
		for x in range(0, GHOSTGAMESPERROUND):
			gameRoundGhost(y,1)



		#Play against external montecarlo algorithm
		#Major performance issues with this _RATE == 1):
		if(roundsCompleted % QUALITY_CHECK_RATE == 1):
			hyperParameterScore += checkAIQuality(y,1)
			if(y == 1):
				hyperParameterScore = hyperParameterScore / 2
				file_object = open(FOLER_STATS + args.learning_Name + "_visualizer.csv", 'a')
				file_object.write(str(roundsCompleted)+ "," + str(hyperParameterScore) + "\n")
				file_object.close()
				#Saving graph for hyperparamer



	fitnessOfRound1 = genetics1.getFitness() / POP_COUNT
	fitnessOfRound2 = genetics2.getFitness() / POP_COUNT


	#Copy agents to ghost agenst (if fitness is greater than 30 then only good trained versions get new enemies)
	#New approach (and fitnessOfRound2 > GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3)
	bestAgentIndex = 0
	bestAgentScore = 0
	#Copy best agent to history
	if(b % SNAPSHOT_PROBABILITY == 0):
		for g1 in range(len(genetics1.agents)-1, -1, -1):
			if(genetics1.agents[g1].fitness > bestAgentScore):
				bestAgentScore = genetics1.agents[g1].fitness
				bestAgentIndex = g1
		genetics1.copyAgenttoGhost(bestAgentIndex)

	bestAgentIndex = 0
	bestAgentScore = 0
	#Copy best agent to history
	if(b % SNAPSHOT_PROBABILITY == 0):
		for g2 in range(len(genetics2.agents)-1, -1, -1):
			if(genetics1.agents[g2].fitness > bestAgentScore):
				bestAgentScore = genetics2.agents[g2].fitness
				bestAgentIndex = g2
		genetics2.copyAgenttoGhost(bestAgentIndex)

	if(roundsCompleted % EXPORTEVERYXMOVE == 1 and b < ROUND_COUNT - EXPORTAFTER):
		genetics1.savetoFile("genetics1-Test-v1-g-"+str(roundsCompleted), EXPORTQUALITY, EXPORTAMOUNT, args.learning_Name)
		genetics2.savetoFile("genetics2-Test-v1-g-"+str(roundsCompleted), EXPORTQUALITY, EXPORTAMOUNT, args.learning_Name)
	#7
	genetics1.roundClose(randomizationAmount, randomizationStrengthWeights, randomizationStrengthBiases)
	genetics2.roundClose(randomizationAmount, randomizationStrengthWeights, randomizationStrengthBiases)

	if(roundsCompleted == 0):
		file_object = open(FOLER_STATS + args.learning_Name + "_relative.csv", 'a')
		file_object.write("Round_Number,Fitness_Genetics1,Fitness_Genetics2,Amount_GhostAgents1,Amount_GhostAgents2\n")
		file_object.close()
		file_object = open(FOLER_STATS + args.learning_Name + "_visualizer.csv", 'a')
		file_object.write("Round_Number,Absolute_Fitness\n")
		file_object.close()
		file_object = open(FOLER_STATS + args.learning_Name + "_GEN_1_min_max_progress.csv", 'a')
		file_object.write("Round_Number,wins,draws,losses\n")
		file_object.close()
		file_object = open(FOLER_STATS+ args.learning_Name + "_GEN_2_min_max_progress.csv", 'a')
		file_object.write("Round_Number,wins,draws,losses\n")
		file_object.close()

	file_object = open(FOLER_STATS + args.learning_Name + "_relative.csv", 'a')
	file_object.write(str(roundsCompleted)+","+str(fitnessOfRound1)+ "," + str(fitnessOfRound2)+ "," +str(len(genetics1.ghostAgents))+";"+str(len(genetics2.ghostAgents))+"\n")
	file_object.close()
	roundsCompleted += 1

	if(b == 0):
		file_object = open(FOLER_STATS + args.learning_Name + ".txt", 'a')
		file_object.write("GAMESPERROUND: " + str(GAMESPERROUND) + "\n"
			+ "GHOSTGAMESPERROUND: " + str(GHOSTGAMESPERROUND) + "\n"
			+ "randomizationAmount: " + str(randomizationAmount) + "\n"
			+ "randomizationStrengthWeights: " + str(randomizationStrengthWeights) + "\n"
			+ "randomizationStrengthBiases: " + str(randomizationStrengthBiases) + "\n"
			+ "SNAPSHOT_PROBABILITY: " + str(SNAPSHOT_PROBABILITY) + "\n"
			+ "GHOSTAGENTS_POP: " + str(GHOSTAGENTS_POP))
		#ToDo: Add the other parameters
		file_object.close()

		#Create graphs
		import pandas as pd
		import plotly.express as px

		#Relative view
		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_relative.csv")
		df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Fitness_Genetics1', 'Fitness_Genetics2'])
		#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
		fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
		fig.data = [t for t in fig.data if t.mode == "lines"]
		fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
		#fig.show()
		fig.write_image(FOLER_STATS + args.learning_Name +".png",engine='orca')

		#Gen1 absolute
		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_1_min_max_progress.csv")
		df_long=pd.melt(df, id_vars='Round_Number', value_vars=['wins', 'draws', 'losses'])
		#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
		fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
		fig.data = [t for t in fig.data if t.mode == "lines"]
		fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
		#fig.show()
		fig.write_image(FOLER_STATS + args.learning_Name +"_GEN_1.png",engine='orca')
		#Gen2 absolute
		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_2_min_max_progress.csv")
		df_long=pd.melt(df, id_vars='Round_Number', value_vars=['wins', 'draws', 'losses'])
		#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
		fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
		fig.data = [t for t in fig.data if t.mode == "lines"]
		fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
		#fig.show()
		fig.write_image(FOLER_STATS + args.learning_Name +"_GEN_2.png",engine='orca')


		tailLenght =  int(ROUND_COUNT/10) # Dynamic last 10 % of the learning will be meassured
		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_1_min_max_progress.csv")
		gen_01_win_sum = df.tail(tailLenght)['wins'].sum()/tailLenght
		gen_01_draw_sum = df.tail(tailLenght)['draws'].sum()/tailLenght
		gen_01_loss_sum = df.tail(tailLenght)['losses'].sum()/tailLenght

		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_2_min_max_progress.csv")
		gen_02_win_sum = df.tail(tailLenght)['wins'].sum()/tailLenght
		gen_02_draw_sum = df.tail(tailLenght)['draws'].sum()/tailLenght
		gen_02_loss_sum = df.tail(tailLenght)['losses'].sum()/tailLenght

		hyperparameter_fitness = gen_01_win_sum + gen_02_win_sum + gen_01_draw_sum/6 + gen_02_draw_sum/6

		#Reinforcement hyperparameter Correlation analyzer
		if not (os.path.exists("dumbed_saves/reinforcement_hyperparameter_correlation.csv")):
			file_object = open("dumbed_saves/reinforcement_hyperparameter_correlation.csv", 'a')
			file_object.write("GAMESPERROUND,GHOSTGAMESPERROUND,randomizationAmount,randomizationStrengthWeights,"+
				"randomizationStrengthBiases,SNAPSHOT_PROBABILITY,GHOSTAGENTS_POP,ROUND_COUNT,WINFITNESS,DRAWFITNESS,"+
				"LOSEFITNESS,WINFITNESSGHOST,DRAWFITNESSGHOST,LOSEFITNESSGHOST,FITNESS_SCORE\n")
			file_object.close()

		file_object = open("dumbed_saves/reinforcement_hyperparameter_correlation.csv", 'a')
		file_object.write(
			str(GAMESPERROUND) + "," +
			str(GHOSTGAMESPERROUND) + "," +
			str(randomizationAmount) + "," +
			str(randomizationStrengthWeights) + "," +
			str(randomizationStrengthBiases) + "," +
			str(SNAPSHOT_PROBABILITY) + "," +
			str(GHOSTAGENTS_POP)  + "," +
			str(ROUND_COUNT) + "," +
			str(WINFITNESS) + "," +
			str(DRAWFITNESS) + "," +
			str(LOSEFITNESS) + "," +
			str(WINFITNESSGHOST) + "," +
			str(DRAWFITNESSGHOST) + "," +
			str(LOSEFITNESSGHOST) + "," +
			str(hyperparameter_fitness) + "\n")
		file_object.close()


	print("Round: " + str(roundsCompleted) + "|| Fitness genetics1(1st to play): " + str(fitnessOfRound1) + " || Fitness genetics2: " + str(fitnessOfRound2) +" || Amount of GhostAgents: " + str(len(genetics1.ghostAgents)) + " || Amount of GhostAgents2: " + str(len(genetics2.ghostAgents)))