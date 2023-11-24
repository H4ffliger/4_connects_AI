from threading import Thread
import multiprocessing
from genetics import Genetics
from gamefield import GameField
import numpy as np
import time
import pyfiglet
import pickle
import sys
from montecarlo import minMaxAI
from copy import deepcopy
import argparse

#List add
from operator import add


#Introduction
ascii_banner = pyfiglet.figlet_format("GNeuroNetWK")
print(ascii_banner)

#Game Specific
gameW = 5
gameH = 4
gameSize = gameW*gameH

#Genetic Algorithm
POP_COUNT = 100
GHOSTAGENTS_POP = 1000
#ROUND_COUNT 0 = 1'000'000
ROUND_COUNT = 25000
#Individual agents
AGENT_INPUTS = 4*4+2
#Output needs to be at least 2
AGENT_OUTPUTS = 4 #ToDo:Check if not one to small
#Games each round for each agent
GAMESPERROUND = 1


#Data for graph
roundsCompleted = 0



if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

#InitializePopulation
genetics = Genetics(1, 1, AGENT_INPUTS, AGENT_OUTPUTS, 1)
genetics2 = Genetics(1, 1, AGENT_INPUTS, AGENT_OUTPUTS, 1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='GNeuroNetWK play against exported neuronal network')
	parser.add_argument('neuronal_nwk', type=str, default="output.csv",help='path to neuronal network without "dumbed_saves"')
	args = parser.parse_args()

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
	for i in range(len(moveProbabiltyScoreAverage)-1, -1, -1):
		moveProbabiltyScoreAverage[i] = (moveProbabiltyScoreAverage[i]*10)**8 / 10
	print(moveProbabiltyScoreAverage)
	return sortedPicks[indexMove]






filehandler = open("dumbed_saves/" + args.neuronal_nwk, 'rb') 
genetics2.agents[0] = deepcopy(pickle.load(filehandler))
genetics2.agents[0].debug_network()

print(len(genetics2.agents))

#Main loop
for b in range(ROUND_COUNT-1, 0, -1):	
	# Initialize the game board
	playedAgainstAI = False
	aiPlayerAgainstHuman = -1
	for k in range(0, GAMESPERROUND):
		#Shuffle
			game = GameField()
			game_over = False
			userToPlay = 1
			firstMoveNoise = np.random.randint(0,gameW)
			firstMovePlayed = False
			for gamesToPlay in range(0, 100):
				debugMoves = 0
				valid_move = False
				for moveCount in range(0, gameW):
					if(firstMovePlayed == False):
						firstMovePlayed = True;
						aiPickOrder = firstMoveNoise
						print(aiPickOrder)

					elif(userToPlay == 0):
						print(game.print_board())
						aiPickOrder = int(input(f"{game.which_turn()}'s Turn - pick a column (0-X): "))-1
						
					else:
						#aiPickOrder = minMaxAI(deepcopy(game))
						aiPickOrder = getAI2Move(0, game.board, moveCount)
					
					print("validMove: " + str(aiPickOrder))
					valid_move = game.turn(aiPickOrder)
					#if(userToPlay == 0):
					#	with open("gameBoard_MinMax_check_"+ str(np.random.randint(0,1000))+".txt", 'wb') as fh:
					#		pickle.dump(game, fh)
					if(valid_move == False):
						if(aiPickOrder == -1 or moveCount >= gameW ):
							print("Game is a draw!")
							game_over = True
							valid_move = True
							break
					else:
						break
				
				if(userToPlay == 0):
					userToPlay = 1
				else:
					userToPlay = 0

				# End the game if there is a winner
				game_overIndex = game.check_winner()
				if(game.check_winner()):
					#X wins the game
					if(userToPlay == 0):
						game.print_board()
						print("AI wins the game!")
						break
					#O winns the game
					else:
						game.print_board()
						print("Human wins the game!")
						break
					game_over = True
					valid_move = True

				# End the game if there is a tie
				if not any(0 in x for x in game.board):
					print("Game is a draw!")
					break

	roundsCompleted += 1

	print("Round: " + str(roundsCompleted))