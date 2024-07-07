# Folder descriptions
- /Saves - Data to be saved manually
- /dumbed_saves -	Data gets saved and processed automatically in this folder
					For every run, there will be generated a 2 new folders, the \_stats
					folder for the csv statistics and the main folder which contains the 
					exported neural network of different generations.
- main.py - Main program for learing the 4 connects game
- play.py - Test a exported neuronal network from the dumbed_saves folder
- tuner.py - Analyzes the csv export for hyperparameter correlation between the different hyperparameters
- visualizer.py - 	Run after as soon as the first csv export \_visualizer.csv are available in the \_stats folder
					and then enter /dumbed_saves/visualizer/index.html to get a "realtime" view of the different runs
