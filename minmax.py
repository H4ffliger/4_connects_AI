from gamefield_min_max import GameField
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


	game = GameField()
	#Me to play
	#print("Called multible times")
	for i1 in range(gameFieldSize):
		#MetoPlay
		#game.print_board()
		gamesToPlay.append(game)


		gamesToPlay[i1].turn(i1)
		if(gamesToPlay[i1].check_winner()):
			return i1

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
					#Old version
					#moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
					#if(moveProbabiltyScore[moveProbOption] >= LOSINGSCOREADDITION):
					#	moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION			
						
			except:
				print("Invalid move prediction2")

		   #Me to play 2
			for i3 in range(gameFieldSize):
				gamesToPlay2.append(deepcopy(gamesToPlay1[len(gamesToPlay1)-1]))
				depth2Score.append(0)
				try:
					gamesToPlay2[len(gamesToPlay2)-1].turn(i3)
					if(gamesToPlay2[len(gamesToPlay2)-1].check_winner() == 0):
						#print("Winning in 2 on line " + str(i3+1))
						moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
						if(moveProbabiltyScore[moveProbOption] >= WINNINGSCOREADDITION):
							moveProbabiltyScore[moveProbOption] += WINNINGSCOREADDITION		
				except:
					print("Invalid move prediction3")
				
				#Enemy to play 2
				for i4 in range(gameFieldSize):
					gamesToPlay3.append(deepcopy(gamesToPlay2[len(gamesToPlay2)-1]))
					depth3Score.append(0)					
					gamesToPlay3[len(gamesToPlay3)-1].turn(i4)

					if(gamesToPlay3[len(gamesToPlay3)-1].check_winner() == 1):
						#print("Losing in 2 on line " + str(i4+1) + " if enemy sets " + str(i2+1) + ", (me) " + str(i3+1) + " enemy " + str(i4+1))
						moveProbOption = i1
						moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION	
						#Old version
						#moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
						#if(moveProbabiltyScore[moveProbOption] >= LOSINGSCOREADDITION2):
						#	moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION2				
					
					'''
					#Me to play 3
					for i5 in range(gameFieldSize):
						gamesToPlay4.append(deepcopy(gamesToPlay3[len(gamesToPlay3)-1]))
						depth4Score.append(0)
						try:
							gamesToPlay4[len(gamesToPlay4)-1].turn(i5)
							if(gamesToPlay4[len(gamesToPlay4)-1].check_winner() == 0):
								#print("Winning in 3 on line " + str(i5+1))
								moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
								if(moveProbabiltyScore[moveProbOption] >= WINNINGSCOREADDITION2):
									moveProbabiltyScore[moveProbOption] += WINNINGSCOREADDITION2	
						except:
							print("Invalid move prediction5")
						#Enemy to play 3
						for i6 in range(gameFieldSize):
							gamesToPlay5.append(deepcopy(gamesToPlay4[len(gamesToPlay4)-1]))
							depth5Score.append(0)					
							gamesToPlay5[len(gamesToPlay5)-1].turn(i6)

							if(gamesToPlay5[len(gamesToPlay5)-1].check_winner()):
								#print("Losing in 3 on line " + str(i4+1) + " if enemy sets " + str(i2+1) + ", (me) " + str(i3+1) + " enemy " + str(i4+1))
								moveProbOption = i1
								moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION #Not sure if LOSINGADITION3 is better
							'''
		
	#print("Unsorted list")
	#print(moveProbabiltyScore)
	s = np.array(moveProbabiltyScore)
	sort_index = np.argsort(s)
	#print("Loop check: " + str(sort_index[choice]))
	#print(sort_index)
	#print(sort_index[choice])
	#print(moveProbabiltyScore)
	return sort_index[choice]




def minMaxAI(game):
	loopCheck = -1
	valid_move = False
	moveMinMax = -1
	#minMaxAI gets called multiple times trough while loop???
	#print("SingleCall")
	for x in range(0, gameFieldSize):
		loopCheck += 1
		minMaxMove = -2
		#print("while false loopCheck =  " + str(loopCheck) + " for loop = " + str(x))
		moveMinMax = getMinMaxMove(loopCheck, game)
		valid_move = game.turn(moveMinMax)
		#print(valid_move)
		if(valid_move):
			return moveMinMax
		#print(str(x) + " " + str(loopCheck))
	print("Gameboard full game is a draw")

	return False
	#print("return " + str(loopCheck))
	user = 0
	print("ERROR ------ beyond return")