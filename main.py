from threading import Thread
import multiprocessing
from genetics import Genetics
from gamefield import GameField
import numpy as np
import time
import sys

import pyfiglet

#Analyzer
import tracemalloc
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

print("Version 0.01\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to solve compute intense problems\n" +
	"Currently test boilerplate to check functionality\n" + 
	"Beat the randomness function\n\n")

#Game Specific
gameSize = 6*7

#Genetic Algorithm
POP_COUNT = 200
GHOSTAGENTS_POP = POP_COUNT*15
#ROUND_COUNT 0 = 1'000'000
ROUND_COUNT = 5 #250000000
#Individual agents
AGENT_INPUTS = gameSize
#Output needs to be at least 2
AGENT_OUTPUTS = 6 #ToDo:Check if not one to small
#Mutation 0.05 = 5% on 5% of weights
randomizationAmount = 0.05
randomizationStrength = 0.05 	
#Reward is exponential default 1.75
FITNESS_REWARD = 1.75
#Population / Probability = real probability
SNAPSHOT_PROBABILITY = 80
#Games each round for each agent
GAMESPERROUND = 1
GHOSTGAMESPERROUND = 12
PLAYERTOMOVE = 100000
SHOWAFTER = 1000000
SHOWEVERY = 20000

WINFITNESS = 4
DRAWFITNESS = 0.5
LOSEFITNESS = 0.1

EXPORTEVERYXMOVE = 25
#1 = >= Durchschnitt 1.1 = 110% von normaler Qualität
EXPORTQUALITY = 1
EXPORTAFTER = 30
EXPORTAMOUNT = 2


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

def getGhostMove(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics.thinkParticularGhost(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]

def getGhost2Move(userToPlay, board, indexMove):
	moveProbabiltyScore = genetics2.thinkParticularGhost(userToPlay, board.flatten()).flatten()
	sortedPicks = sorted(range(len(moveProbabiltyScore)), key=lambda k: moveProbabiltyScore[k])
	return sortedPicks[indexMove]


def gameRound();
	#tracemalloc.start()
	#Shuffle
	if(y == 0):
		enemy = np.random.randint(0, len(genetics2.ghostAgents))
	else:
		enemy = np.random.randint(0, len(genetics.ghostAgents))
	for x in range(POP_COUNT-1, 0, -1):
		game = GameField()
		game_over = False
		userToPlay = 0				
		while not game_over:
			debugMoves = 0
			valid_move = False
			bannedOutputs = 0	
			while not valid_move:
				if(y == 0):
					if(userToPlay == 0):
						aiPickOrder = getGhost2Move(enemy, game.board, bannedOutputs)
					else:
						aiPickOrder = getAIMove(x, game.board, bannedOutputs)
				else:
					if(userToPlay == 1):
						aiPickOrder = getGhostMove(enemy, game.board, bannedOutputs)
					else:
						aiPickOrder = getAI2Move(x, game.board, bannedOutputs)
				
				user_move = aiPickOrder
				valid_move = game.turn(aiPickOrder)
				if(valid_move == False and game_over == False):
					bannedOutputs += 1
					if(aiPickOrder == -1 or bannedOutputs >=AGENT_OUTPUTS ):
						if(y == 0):
							genetics2.calculateFitnessParticular(x, DRAWFITNESS)
						else:
							genetics.calculateFitnessParticular(x, DRAWFITNESS)
						game_over = True
						valid_move = True
				if(x > POP_COUNT-2 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
					time.sleep(0.3)
					print(game.print_board())
			
			if(userToPlay == 0):
				userToPlay = 1
			else:
				userToPlay = 0

			# End the game if there is a winner
			game_overIndex = game.check_winner()
			if(game.check_winner() and game_over == False):
				#X wins the game
				#Ghosts
				#y == 0 and usertoplay == 0 genetics2 win
				#y == 0 and usertoplay == 1 genetics2 lose
				#y == 1 and usertoplay == 0 genetics1 win
				#y == 1 and usertoplay == 1 genetics1 lose
				if(userToPlay == 1):
					if(y == 0):
						genetics2.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
					else:
						genetics.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
				#O winns the game
				else:
					if(y == 0):
						genetics2.calculateFitnessParticular(x, WINFITNESS)#Must be 3
					else:
						genetics.calculateFitnessParticular(x, WINFITNESS)#Must be 3
				game_over = True
				valid_move = True


			# End the game if there is a tie
			if not any(-1 in x for x in game.board):
				if(game_over == False):
					if(y == 0):
						genetic2.calculateFitnessParticular(x, DRAWFITNESS)
					else:
						genetics.calculateFitnessParticular(x, DRAWFITNESS)
				game_over = True
				valid_move = True
	#Rewrite because it delets all the ghost agents
	#if(genetics.getFitness() / POP_COUNT >= 42 and y == 0):
		#genetics2.deleteGhostX(enemy)
	#if(genetics2.getFitness() / POP_COUNT >= 43 and y == 1):
		#genetics.deleteGhostX(enemy)
	#Speed analyzing
	#snapshot = tracemalloc.take_snapshot()
	#display_top(snapshot)




#Main loop
for b in range(ROUND_COUNT-1, 0, -1):
	''''
	# Initialize the game board
	playedAgainstAI = False
	aiPlayerAgainstHuman = -1
	for k in range(0, GAMESPERROUND):
		#Shuffle
		for x in range(POP_COUNT-1, 0, -1):
			enemy = x
			game = GameField()
			game_over = False
			userToPlay = 0
			while not game_over:
				debugMoves = 0
				valid_move = False
				bannedOutputs = 0					
				while not valid_move:
					if(userToPlay == 1):
						aiPickOrder = getAIMove(x, game.board, bannedOutputs)
					else:
						aiPickOrder = getAI2Move(x, game.board, bannedOutputs)
					
					user_move = aiPickOrder
					valid_move = game.turn(aiPickOrder)
					if(valid_move == False and game_over == False):
						bannedOutputs += 1
						if(aiPickOrder == -1 or bannedOutputs >=AGENT_OUTPUTS ):
							genetics.calculateFitnessParticular(x, DRAWFITNESS)
							genetics2.calculateFitnessParticular(x, DRAWFITNESS)
							game_over = True
							valid_move = True
					if(x > POP_COUNT-2 and b % SHOWEVERY == 1 and b < ROUND_COUNT - SHOWAFTER):
						time.sleep(0.3)
						print(game.print_board())
				
				if(userToPlay == 0):
					userToPlay = 1
				else:
					userToPlay = 0

				# End the game if there is a winner
				game_overIndex = game.check_winner()
				if(game.check_winner() and game_over == False):
					#X wins the game
					if(userToPlay == 0):
						genetics.calculateFitnessParticular(x, WINFITNESS)#Must be 3
						genetics2.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3
					#O winns the game
					else:
						genetics2.calculateFitnessParticular(x, WINFITNESS)#Must be 3
						genetics.calculateFitnessParticular(x, LOSEFITNESS)#Must be 3

					game_over = True
					valid_move = True


				# End the game if there is a tie
				if not any(-1 in x for x in game.board):
					if(game_over == False):
						genetics.calculateFitnessParticular(x, DRAWFITNESS)
						genetics2.calculateFitnessParticular(x, DRAWFITNESS)
					game_over = True
					valid_move = True

	fitnessOfRound = genetics.getFitness() / POP_COUNT
	fitnessOfRound2 = genetics2.getFitness() / POP_COUNT
'''

	#PlayAgainstGhost
	for y in range(0,2):

		for k in range(GHOSTGAMESPERROUND):
			#ToDO



	fitnessOfRound = genetics.getFitness() / POP_COUNT
	fitnessOfRound2 = genetics2.getFitness() / POP_COUNT


	#Copy agents to ghost agenst (if fitness is greater than 30 then only good trained versions get new enemies)
	for g1 in range(len(genetics.agents)-1, -1, -1):
		if(GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3 <= genetics.agents[g1].fitness and np.random.randint(0,SNAPSHOT_PROBABILITY) == 0 and fitnessOfRound2 > GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3):
			genetics.copyAgenttoGhost(g1)

	for g2 in range(len(genetics2.agents)-1, -1, -1):
		if(GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3 +1 <= genetics2.agents[g2].fitness and np.random.randint(0,SNAPSHOT_PROBABILITY) == 0 and fitnessOfRound > GHOSTGAMESPERROUND + GHOSTGAMESPERROUND/3):
			genetics2.copyAgenttoGhost(g2)


	if(roundsCompleted % EXPORTEVERYXMOVE == 1 and b < ROUND_COUNT - EXPORTAFTER):
		genetics.savetoFile("genetics1-Test-v1-g-"+str(roundsCompleted), EXPORTQUALITY, EXPORTAMOUNT)
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
	genetics.roundClose(randomizationAmount, randomizationStrength)
	genetics2.roundClose(randomizationAmount, randomizationStrength)
	

	roundsCompleted += 1
	file_object = open("dumbed_saves/" + sys.argv[1] + ".txt", 'a')
	file_object.write(str(roundsCompleted)+";"+str(fitnessOfRound)+ ";" + str(fitnessOfRound2)+ ";" +str(len(genetics.ghostAgents))+";"+str(len(genetics2.ghostAgents))+"\n")
	file_object.close()

	print("Round: " + str(roundsCompleted) + "|| Fitness genetics1(2nd to play): " + str(fitnessOfRound) + " || Fitness genetics2: " + str(fitnessOfRound2) +" || Amount of GhostAgents: " + str(len(genetics.ghostAgents)) + " || Amount of GhostAgents2: " + str(len(genetics2.ghostAgents)))