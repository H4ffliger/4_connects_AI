# Folder descriptions
> /Saves - Data to be saved manually
> /dumbed_saves -	Data gets saved and processed automatically in this folder
					For every run, there will be generated a 2 new folders, the \_stats
					folder for the csv statistics and the main folder which contains the 
					exported neural network of different generations.
> main.py - Main program for learing the 4 connects game
> play.py - Test a exported neuronal network from the dumbed_saves folder
> tuner.py - Analyzes the csv export for hyperparameter correlation between the different hyperparameters
> visualizer.py - 	Run after as soon as the first csv export \_visualizer.csv are available in the \_stats folder
					and then enter /dumbed_saves/visualizer/index.html to get a "realtime" view of the different runs

Hello everybody, thanks for the help and replies. I want to ask about two other questions which bother me since weeks. 
Here is some information to understand my problem better:
Currently I'm working on an 4 connects neural network. I don't use any RL libraries and tried to build up everything from scratch. But with the current methods I'm trying to solve the problem I run into some limitations. My project does only use the output of the neural network to evaluate the positions of the game field. It does not use any Tree Searches or something like that.

I know there are better ways to get around this problem by performing a position evaluation based on a value function return of each possible turn to take. But my goal is to let the network decide without looking into the future to choose the best move.

I run into the following 2 big problems:
1) I don't know how many number of rounds need to be played per generation. The main problem is the amount of games against the old versions of themselves. By default, each generation will play 20 games against itself and 7 games against a random version of the past. This is done to avoid a “strategy collapse“. However, every X generations there is one more old past agents to be played against and therefore at a certain generation there are just too many past agents to play against. So, the network can not play regularly against the past versions of them self and so it collapses at some point. Consequently, I experience a “strategy collapse“ after a certain period of time. If the number of games per generation is increased the training will take longer, so there is a computational performance problem. If I decrease the frequency of the agents being copied to the past archive, I may loose strategies which where developed in between those rounds. 
2) There is much randomness in the game to get persistent results. I train the first and the second generations against themselves, therefore they learn to play against each other. But this way I can't see if they make any progress, that's why I implemented a minmax algorithm to test them every five rounds and log the progress to a linear trendline. The problem is they don't learn the same phases with the same speed and certain runs might not learn some things at all. The output against the minmax AI varies a lot between the different runs and I can't compare them very good to each other. I get different results with the same hyperparameters over many runs. How can I tell it's just because of the randomness or if the result is because of the bad hyperparameters. So if I try different hyperparameters it can just be luck some of them work out better.