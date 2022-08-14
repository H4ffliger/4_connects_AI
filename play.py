from threading import Thread
import multiprocessing
from genetics import Genetics
from gamefield import GameField
import numpy as np
import time
import pyfiglet
import pickle
import sys


#Introduction
ascii_banner = pyfiglet.figlet_format("GNeuroNetWK")
print(ascii_banner)

print("Version 0.01\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to solve compute intense problems\n" +
	"Currently test boilerplate to check functionality\n" + 
	"Beat the randomness function\n\n")

#Game Specific
gameSize = 5*5

#Genetic Algorithm
POP_COUNT = 100
GHOSTAGENTS_POP = 1000
#ROUND_COUNT 0 = 1'000'000
ROUND_COUNT = 25000
#Individual agents
AGENT_INPUTS = gameSize
#Output needs to be at least 2
AGENT_OUTPUTS = 5
#Mutation 0.05 = 5% on 5% of weights
randomizationAmount = 1
randomuzationStrength = 0.03
#Reward is exponential default 1.75
FITNESS_REWARD = 1
#Population / Probability = real probability
SNAPSHOT_PROBABILITY = 4
#Games each round for each agent
GAMESPERROUND = 1
SHOWAFTER = 200
SHOWEVERY = 50


EXPORTEVERYXMOVE = 10
#1 = >= Durchschnitt 1.1 = 110% von normaler Qualität
EXPORTQUALITY = 1.2
EXPORTAFTER = 10
EXPORTAMOUNT = 5


#Data for graph
roundsCompleted = 0
fitnessOfRound = 0

#Export


if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

#InitializePopulation
genetics = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)
genetics2 = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)

#Copy random to ghosts
for i in range(0, 10):
	genetics.copyAgenttoGhost(i)
	genetics2.copyAgenttoGhost(i)

#AIPickStuff
bannedOutputs = 0

def getAIMove(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics.thinkParticular(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]


def getAI2Move(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics2.thinkParticular(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]


filehandler = open("dumbed_saves/" + sys.argv[1], 'rb') 
genetics2.agents[0] = pickle.load(filehandler)

#Main loop
for b in range(ROUND_COUNT-1, 0, -1):	
	# Initialize the game board
	playedAgainstAI = False
	aiPlayerAgainstHuman = -1
	for k in range(0, GAMESPERROUND):
		#Shuffle
			game = GameField()
			game_over = False
			userToPlay = 0
			while not game_over:
				debugMoves = 0
				valid_move = False
				bannedOutputs = 0					
				while not valid_move:
					if(userToPlay == 0):
						print(game.print_board())
						aiPickOrder = int(input(f"{game.which_turn()}'s Turn - pick a column (0-X): "))-1
						user_move = aiPickOrder
					else:
						aiPickOrder = getAI2Move(0, game.board, bannedOutputs)
					
					user_move = aiPickOrder
					valid_move = game.turn(aiPickOrder)
					if(valid_move == False):
						bannedOutputs += 1
						if(aiPickOrder == -1 or bannedOutputs >=AGENT_OUTPUTS ):
							print("Game is a draw!")
							game_over = True
							valid_move = True
				
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
					#O winns the game
					else:
						game.print_board()
						print("Human wins the game!")
					game_over = True
					valid_move = True

				# End the game if there is a tie
				if not any(-1 in x for x in game.board):
					print("Game is a draw!")

	roundsCompleted += 1

	print("Round: " + str(roundsCompleted))