from gamefield import GameField
import numpy as np
from copy import deepcopy
import time

ROUND_COUNT = 25000

#Data for graph
roundsCompleted = 0

if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

depth = 30
gameFieldSize = 6

#Balancing a win is 100 less worth than a loss
WINNINGSCOREADDITION = 0
WINNINGSCOREADDITION2 = 0
WINNINGSCOREADDITION3 = 0

#Losing in the next move is weighted 10x higher than in the overnext move
LOSINGSCOREADDITION = 200
LOSINGSCOREADDITION2 = 10
LOSINGSCOREADDITION3 = 1



def getMonteCarloMove(choice, game):
	winCount = np.zeros(gameFieldSize)
	drawCount = np.zeros(gameFieldSize)
	loseCount = np.zeros(gameFieldSize)
	moveProbabiltyScore =  np.zeros(gameFieldSize)

	for p in range(depth-1, -1, -1):
		gamesToPlay = []
		#Play full game based on randomness
		for i1 in range(gameFieldSize):
			gamesToPlay.append(deepcopy(game))
			game_ended = False


			if(gamesToPlay[i1].turn(i1) == False):
				#print("Move " + str(i1) + " not possible")
				winCount[i1] = depth/7
				drawCount[i1] = -100000
				loseCount[i1] = depth/7
			else:
				#Check if it's an imediate win
				if(gamesToPlay[i1].check_winner()):
					winCount[i1] = depth * 1000
				movesPlayed = 0
				while not game_ended:
					gamesToPlay[i1].turn(np.random.randint(0, gameFieldSize))
					if not any(-1 in a for a in gamesToPlay[i1].board):
						drawCount[i1] += 1
						game_ended = True

					if(gamesToPlay[i1].check_winner()):
						if(movesPlayed % 2 == 0):
							loseCount[i1] += 1
						else:
							winCount[i1] += 1
						game_ended = True
					movesPlayed += 1
				#if(movesPlayed > 100):
				#	print(movesPlayed)

	winRateAIW = 0
	winRateAID = 0
	winRateAIL = 0
	for i1 in range(gameFieldSize):
		#print("Field " + str(i1+1) + " w" + str(winCount[i1]) + "/d" + str(drawCount[i1]) + "/l" + str(loseCount[i1]))
		winRateAIW += winCount[i1]
		winRateAID += drawCount[i1]
		winRateAIL += loseCount[i1]
		moveProbabiltyScore[i1] = loseCount[i1] - (drawCount[i1]/5) - winCount[i1]

	#print("Unsorted list")
	#print(moveProbabiltyScore)
	s = np.array(moveProbabiltyScore)
	#print("AI is winning with " + str(int(100/depth*(winRateAIW/7-winRateAIL/7)+50)) + "% confidence.")
	sort_index = np.argsort(s)

	#print(sort_index)
	#print(sort_index[choice])
	return sort_index[choice]


#
def monteCarloAI(localGame):
	loopCheck = -1
	valid_move = False
	#minMaxAI gets called multiple times trough while loop???
	#print("SingleCall")
	for x in range(0, gameFieldSize):
		#print("while false loopCheck =  " + str(loopCheck) + " for loop = " + str(x))
		moveMinMax = getMonteCarloMove(x, deepcopy(localGame))
		#print("MoveMinMax: " + str(moveMinMax))
		valid_move = localGame.turn(moveMinMax)
		print
		#print(valid_move)
		#print(valid_move)
		#print(x)
		#print("minMaxAI move: " + str(moveMinMax) + " | " + str(valid_move))
		if(valid_move):
			#print("minMaxAI move: " + str(moveMinMax))
			return moveMinMax
		#print(str(x) + " " + str(loopCheck))
	#print("Gameboard full game is a draw: " + str(loopCheck))
	#localGame.print_board()
	print("ERROR ------ no picked move return")
	return False # Nach tests zu return -1 anpassen
	#print("return " + str(loopCheck))
	user = 0
	print("ERROR ------ beyond return")
