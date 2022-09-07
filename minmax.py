from gamefield import GameField
import numpy as np
from copy import deepcopy
import time

ROUND_COUNT = 25000

#Data for graph
roundsCompleted = 0

if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

depth = 1
gameFieldSize = 5

#Balancing a win is 100 less worth than a loss
WINNINGSCOREADDITION = 0
WINNINGSCOREADDITION2 = 0
WINNINGSCOREADDITION3 = 0

#Losing in the next move is weighted 10x higher than in the overnext move
LOSINGSCOREADDITION = 200
LOSINGSCOREADDITION2 = 10
LOSINGSCOREADDITION3 = 1



def getMinMaxMove(choice, game):
	gamesToPlay = []
	gamesToPlay1 = []
	gamesToPlay2 = []
	gamesToPlay3 = []
	gamesToPlay4 = []
	gamesToPlay5 = []
	bestPick = np.random.randint(3, 4)
	bestPickLossesScore = 100000
	#Me to play
	depth1Score = []
	depth2Score = []
	depth3Score = []
	depth4Score = []
	depth5Score = []

	moveProbabiltyScore = [2] * gameFieldSize


	#Me to play
	#print("Called multible times")
	for i1 in range(gameFieldSize):
		#MetoPlay
		gamesToPlay.append(game)
		try:
			gamesToPlay[i1].turn(i1)
			if(gamesToPlay[i1].check_winner()):
				return i1
		except:
			print("Invalid move prediction1")
		#Enemy to play 1
		for i2 in range(gameFieldSize):
			#print(str(i)+ " : "+ str(y))
			gamesToPlay1.append(deepcopy(gamesToPlay[len(gamesToPlay)-1]))
			depth1Score.append(0)
			try:
				gamesToPlay1[len(gamesToPlay1)-1].turn(i2)
				#gamesToPlay1[len(gamesToPlay1)-1].print_board()
				#print(str(gamesToPlay1[len(gamesToPlay1)-1].check_winner()))
				if(gamesToPlay1[len(gamesToPlay1)-1].check_winner() == 1):
					#print("Losing in 1 on line " + str(i2+1) + " if i set " + str(i1+1))
					moveProbOption = i1
					moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION			
			except:
				print("Invalid move prediction2")
	#print("Unsorted list")
	#print(moveProbabiltyScore)
	s = np.array(moveProbabiltyScore)
	sort_index = np.argsort(s)
	#print(sort_index)
	#print(sort_index[choice])
	return sort_index[choice]

def minMaxAI(localGame):
	loopCheck = -1
	valid_move = False
	#minMaxAI gets called multiple times trough while loop???
	#print("SingleCall")
	for x in range(0, gameFieldSize):
		#print("while false loopCheck =  " + str(loopCheck) + " for loop = " + str(x))
		moveMinMax = getMinMaxMove(x, deepcopy(localGame))
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
