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
from minmax import minMaxAI
import pyfiglet
#Analyzer
import tracemalloc

import logging
logging.basicConfig(level=logging.DEBUG)
'''
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

print("Version 0.02\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to solve compute intense problems\n" +
	"Currently test boilerplate to check functionality\n" + 
	"Beat the game 4 connects with external minmax score progress check\n\n")

#Game Specific
gameSize = 6*7

#Genetic Algorithm
POP_COUNT = 400
GHOSTAGENTS_POP = POP_COUNT*15
#ROUND_COUNT 0 = 1'000'000
ROUND_COUNT = 250000000
#Individual agents
AGENT_INPUTS = gameSize
#Output needs to be at least 2
AGENT_OUTPUTS = 6 #ToDo:Check if not one to small
#Mutation 0.05 = 5% on 5% of weights
randomizationAmount = 0.01
randomuzationStrengthWeights = 0.02
randomuzationStrengthBiases = 0.05
#Reward is exponential default 1.75
FITNESS_REWARD = 1.5
#Population / Probability = real probability
SNAPSHOT_PROBABILITY = POP_COUNT/0.8
#Games each round for each agent
GAMESPERROUND = 20
GHOSTGAMESPERROUND = 10
SHOWAFTER = 100000000
SHOWEVERY = 1000

#AI vs AI
WINFITNESS = 4
DRAWFITNESS = 0.5
LOSEFITNESS = -0.2 # experiment with -0.5

#AI vs Ghost (Ghost doesnt get fitness thats why AI gets only half of it)
WINFITNESSGHOST = 8
DRAWFITNESSGHOST = 1
LOSEFITNESSGHOST = 0.2


EXPORTEVERYXMOVE = 25
#1 = >= Durchschnitt 1.1 = 110% von normaler Qualität
EXPORTQUALITY = 1
EXPORTAFTER = 2
EXPORTAMOUNT = 2


#Data for graph
roundsCompleted = 0
fitnessOfRound = 0

#Export


if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

#InitializePopulation
genetics1 = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)
genetics2 = Genetics(POP_COUNT, GHOSTAGENTS_POP, AGENT_INPUTS, AGENT_OUTPUTS, FITNESS_REWARD)

#Copy random to ghosts
for i in range(0, 10):
	genetics1.copyAgenttoGhost(i)
	genetics2.copyAgenttoGhost(i)

#AIPickStuff
bannedOutputs = 0

def getAIMove(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics1.thinkParticular(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]


def getAI2Move(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics2.thinkParticular(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]

def getGhostMove(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics1.thinkParticularGhost(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]

def getGhost2Move(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics2.thinkParticularGhost(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]

def getStack2Move(userToPlay, board, indexMove):
	return minMaxAI(board)


def gameRoundGhost(y: int, idx: int):

	#All fight the same enemy
	if(y == 0):
		enemy = np.random.randint(0, len(genetics1.ghostAgents))
	else:
		enemy = np.random.randint(0, len(genetics2.ghostAgents))

	for x in range(POP_COUNT-1, 0, -1):


		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 moves
		firstMoveNoise = np.random.randint(2,5)
		firstMovePlayed = False


		while not game_over:
			debugMoves = 0
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True;
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
					if(chosen_move == -1 or bannedOutputs >= AGENT_OUTPUTS):
						if(y == 0):
							genetics2.calculateFitnessParticular(x, DRAWFITNESSGHOST)
						else:
							genetics1.calculateFitnessParticular(x, DRAWFITNESSGHOST)
						game_over = True
						valid_move = True

				if(x > POP_COUNT-2 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
					time.sleep(0.3)
					print(game.print_board())
			



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
			if not any(-1 in x for x in game.board):
				if(game_over == False):
					if(y == 0):
						genetics2.calculateFitnessParticular(x, DRAWFITNESSGHOST)
					else:
						genetics1.calculateFitnessParticular(x, DRAWFITNESSGHOST)
				game_over = True
				valid_move = True


def gameRoundAI(y: int, idx: int):

	for x in range(POP_COUNT-1, 0, -1):

		#All fight random enemies
		if(y == 0):
			enemy = np.random.randint(0, POP_COUNT)
		else:
			enemy = np.random.randint(0, POP_COUNT)


		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 moves
		firstMoveNoise = np.random.randint(2,5)
		firstMovePlayed = False


		while not game_over:
			debugMoves = 0
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True;
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
					if(chosen_move == -1 or bannedOutputs >= AGENT_OUTPUTS):
						if(y == 0):
							genetics2.calculateFitnessParticular(x, DRAWFITNESS)
							genetics1.calculateFitnessParticular(enemy, DRAWFITNESS)
						else:
							genetics1.calculateFitnessParticular(x, DRAWFITNESS)
							genetics2.calculateFitnessParticular(enemy, DRAWFITNESS)
						game_over = True
						valid_move = True

				if(x > POP_COUNT-1 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
					#time.sleep(0.2)
					print(game.print_board())
			



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
						genetics2.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
						genetics1.calculateFitnessParticular(enemy, WINFITNESS)
					else:
						genetics2.calculateFitnessParticular(x, WINFITNESS)#Must be 3
						genetics1.calculateFitnessParticular(enemy, LOSEFITNESS)
				#1 winns the game
				else:
					if(userToPlay == 0):
						genetics1.calculateFitnessParticular(x, WINFITNESS)#Must be 3
						genetics2.calculateFitnessParticular(enemy, LOSEFITNESS)
					else:
						genetics1.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
						genetics2.calculateFitnessParticular(enemy, WINFITNESS)
				game_over = True
				valid_move = True

			if(userToPlay == 0):
				userToPlay = 1
			else:
				userToPlay = 0


			# End the game if there is a tie
			if not any(-1 in x for x in game.board):
				if(game_over == False):
					if(y == 0):
						genetics2.calculateFitnessParticular(x, DRAWFITNESS)
						genetics1.calculateFitnessParticular(enemy, DRAWFITNESS)
					else:
						genetics1.calculateFitnessParticular(x, DRAWFITNESS)
						genetics2.calculateFitnessParticular(enemy, DRAWFITNESS)
				game_over = True
				valid_move = True


# Change to do => don't train on this data (don't cloe the round /generations)

def checkAIQuality(y: int, idx: int):
	qual_check_wins = 0;
	qual_check_draws = 0;
	qual_check_losses = 0;
	logging.debug("Starting quality check on generation " + str(y+1))
	#Performance wise only 20% of the population gets testet
	for x in range(int(POP_COUNT/10)-1, 0, -1):
		game = GameField()
		game_over = False
		userToPlay = 0
		#First move throws off the AI for the first x 100 moves
		firstMoveNoise = np.random.randint(2,5)
		firstMovePlayed = False

		print("Checking agent " + str(x))
		while not game_over:
			valid_move = False
			bannedOutputs = 0

			while not valid_move:
				#y == 0 > AI gets second move
				if(firstMovePlayed == False):
					firstMovePlayed = True;
					chosen_move = firstMoveNoise
				elif(y == 0):
					#userToPay 0 = Ghost gets first move
					if(userToPlay == 0):
						chosen_move = minMaxAI(game.board)
						#chosen_move = getGhostMove(enemy, game.board, bannedOutputs)
					else:
						chosen_move = getAI2Move(x, game.board, bannedOutputs)
				else:
					if(userToPlay == 0):
						chosen_move = getAIMove(x, game.board, bannedOutputs)
					else:
						#chosen_move = getGhost2Move(enemy, game.board, bannedOutputs)
						chosen_move = minMaxAI(game.board)

				valid_move = game.turn(chosen_move)
				if(valid_move == False and game_over == False):
					bannedOutputs += 1
					if(chosen_move == -1 or bannedOutputs >= AGENT_OUTPUTS):
						if(y == 0):
							qual_check_draws += 1
						else:
							qual_check_draws += 1
						game_over = True
						valid_move = True
				if(x > POP_COUNT-2 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
					time.sleep(0.3)
					print(game.print_board())
			



			# End the game if there is a winner CHECK IS REVERSED
			if(game.check_winner() and game_over == False):
				#X wins the game
				#Ghosts
				# y == 0 then gen2
				# y == 1 then gen1
				#y == 0 and usertoplay == 0 AI win
				#y == 0 and usertoplay == 1 AI lose
				#y == 1 and usertoplay == 0 AI lose
				#y == 1 and usertoplay == 1 AI win
				if(y == 0):
					if(userToPlay == 0):
						qual_check_losses += 1
					else:
						qual_check_wins += 1
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
			if not any(-1 in x for x in game.board):
				if(game_over == False):
					if(y == 0):
						qual_check_draws += 1
					else:
						qual_check_draws += 1
				game_over = True
				valid_move = True
	file_object = open("dumbed_saves/" + sys.argv[1] + "_GEN_"+str(y+1) +"_min_max_progress.csv", 'a')
	file_object.write(str(roundsCompleted)+";" +str(qual_check_wins)+";"+str(qual_check_draws)+";"+str(qual_check_losses)+"\n")
	file_object.close()
	print("Generation " + str(y+1) + " wins: " + str(qual_check_wins) + " draws: " + str(qual_check_draws) + " losses: " + str(qual_check_losses))





#Main loop
for b in range(ROUND_COUNT-1, 0, -1):
	#PlayAgainstGhost
	for y in range(0,2):
		#Testing
		#Doble amount of fitness due to double reward 
		#for x in range(0, GAMESPERROUND):
		#	gameRoundAI(y,1)

		with ThreadPoolExecutor() as executor:
			worker = partial(gameRoundAI, y)
			executor.map(worker, range(0, GAMESPERROUND))

		



		#Debug Testing gameRound(y,1)
		#for x in range(0, GHOSTGAMESPERROUND):
		#	gameRoundGhost(y,1)

		with ThreadPoolExecutor() as executor:
			worker = partial(gameRoundGhost, y)
			executor.map(worker, range(0, GHOSTGAMESPERROUND))

		#Play against external minmax algorithm
		checkAIQuality(y,1)



	fitnessOfRound1 = genetics1.getFitness() / POP_COUNT
	fitnessOfRound2 = genetics2.getFitness() / POP_COUNT


	#Copy agents to ghost agenst (if fitness is greater than 30 then only good trained versions get new enemies)

	#New approach (and fitnessOfRound2 > GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3)
	for g1 in range(len(genetics1.agents)-1, -1, -1):
		if(GHOSTGAMESPERROUND*2 + GAMESPERROUND*3 <= genetics1.agents[g1].fitness and np.random.randint(0,SNAPSHOT_PROBABILITY) == 0):
			genetics1.copyAgenttoGhost(g1)

	#New approach (and fitnessOfRound > GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3)
	for g2 in range(len(genetics2.agents)-1, -1, -1):
		if(GHOSTGAMESPERROUND*2 + GAMESPERROUND*3 <= genetics2.agents[g2].fitness and np.random.randint(0,SNAPSHOT_PROBABILITY) == 0):
			genetics2.copyAgenttoGhost(g2)


	if(roundsCompleted % EXPORTEVERYXMOVE == 1 and b < ROUND_COUNT - EXPORTAFTER):
		genetics1.savetoFile("genetics1-Test-v1-g-"+str(roundsCompleted), EXPORTQUALITY, EXPORTAMOUNT)
		genetics2.savetoFile("genetics2-Test-v1-g-"+str(roundsCompleted), EXPORTQUALITY, EXPORTAMOUNT)
	#7
	'''if(fitnessOfRound >= (WINFITNESS*GAMESPERROUND/2 + WINFITNESS * GHOSTGAMESPERROUND/2)):
		genetics2.roundClose(randomizationAmount, randomizationStrength)
		genetics.resetFitness()
		#4
	elif(fitnessOfRound < WINFITNESS*GAMESPERROUND/2 + WINFITNESS * GHOSTGAMESPERROUND/2):
		genetic.roundClose(randomizationAmount, randomizationStrength)
		genetics2.resetFitness()
	else:'''
	genetics1.roundClose(randomizationAmount, randomuzationStrengthWeights, randomuzationStrengthBiases, GAMESPERROUND + GHOSTGAMESPERROUND + POP_COUNT/40)
	genetics2.roundClose(randomizationAmount, randomuzationStrengthWeights, randomuzationStrengthBiases, GAMESPERROUND + GHOSTGAMESPERROUND + POP_COUNT/40)



	roundsCompleted += 1
	file_object = open("dumbed_saves/" + sys.argv[1] + ".csv", 'a')
	file_object.write(str(roundsCompleted)+";"+str(fitnessOfRound1)+ ";" + str(fitnessOfRound2)+ ";" +str(len(genetics1.ghostAgents))+";"+str(len(genetics2.ghostAgents))+"\n")
	file_object.close()

	print("Round: " + str(roundsCompleted) + "|| Fitness genetics1(2nd to play): " + str(fitnessOfRound1) + " || Fitness genetics2: " + str(fitnessOfRound2) +" || Amount of GhostAgents: " + str(len(genetics1.ghostAgents)) + " || Amount of GhostAgents2: " + str(len(genetics2.ghostAgents)))