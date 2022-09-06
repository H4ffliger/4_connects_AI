import pandas as pd
import plotly.express as px
from pathlib import Path
import time
import argparse
import os

import logging
logging.basicConfig(level=logging.DEBUG)

#Visualization_module
FOLER_HTML = 'dumbed_saves/visualizer/'
os.makedirs(FOLER_HTML, exist_ok=True)
FOLER_IMG = 'dumbed_saves/visualizer/images/'
os.makedirs(FOLER_IMG, exist_ok=True)

file_css = open(FOLER_HTML +"mystyles.css", 'w')
file_css.write('body {background-color: #515151;font-family: "Lucida Console", "Courier New", monospace;}h2{text-align: center;}div{background-color: #404040;margin: 0px;}img{	width: 23%;	padding-right: 0.5%;	padding-left: 0.5%;}')
file_css.close()

#csvFileList = []
def find_files(root, extensions):
    for ext in extensions:
        yield from Path(root).glob(f'**/*.{ext}')


def vizualizer():
	global initialized
	if(initialized == False):
		logging.info("Writing index.html file")
		file_object = open(FOLER_HTML +"index.html", 'w')
		file_object.write('<link rel="stylesheet" type="text/css" href="mystyles.css" media="screen" />\n')
		file_object.write('<meta http-equiv="refresh" content="10" />\n')
		file_object.write('<h2>GNeuroNetWK visualizer</h2>\n')

	logging.info("Updating graphs")
	for csvs in find_files('dumbed_saves', ['csv']):
		csvs_sting = str(csvs)
		csvs_name = csvs_sting.split("\\")
		logging.debug("Analyzing: " + csvs_sting)
		if(csvs_sting.__contains__("_relative.csv")):
			if(initialized == False):
				file_object.write('<div class="w3-container">')
				file_object.write('<h3>' + csvs_name[1] +'</h3>')
				file_object.write('<img src="images/' + csvs_name[1] + '00.png" alt="Statistics">')
				file_object.write('<img src="images/' + csvs_name[1] + '01.png" alt="Statistics">')
				file_object.write('<img src="images/' + csvs_name[1] + '02.png" alt="Statistics">')
				file_object.write('<img src="images/' + csvs_name[1] + '03.png" alt="Statistics">')
				file_object.write('</div>\n')
			df = pd.read_csv(csvs_sting)
			df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Fitness_Genetics1', 'Fitness_Genetics2'])
			fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="rolling", trendline_options=dict(window=5), title="Relative fitness")
			fig.data = [t for t in fig.data if t.mode == "lines"]
			fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
			fig.write_image(FOLER_IMG + csvs_name[1] + "00.png",engine='orca')
		if(csvs_sting.__contains__("GEN_1_min_max_progress.csv")):
			df = pd.read_csv(csvs_sting)
			df_long=pd.melt(df, id_vars='Round_Number', value_vars=['wins', 'draws', 'losses'])
			fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="rolling", trendline_options=dict(window=5), title="Player 1")
			fig.data = [t for t in fig.data if t.mode == "lines"]
			fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
			fig.write_image(FOLER_IMG + csvs_name[1] + "01.png",engine='orca')
		if(csvs_sting.__contains__("GEN_2_min_max_progress.csv")):
			df = pd.read_csv(csvs_sting)
			df_long=pd.melt(df, id_vars='Round_Number', value_vars=['wins', 'draws', 'losses'])
			fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="rolling", trendline_options=dict(window=5), title="Player 2")
			fig.data = [t for t in fig.data if t.mode == "lines"]
			fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
			fig.write_image(FOLER_IMG + csvs_name[1] + "02.png",engine='orca')
		if(csvs_sting.__contains__("visualizer.csv")):
			df = pd.read_csv(csvs_sting)
			df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Absolute_Fitness'])
			fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="rolling", trendline_options=dict(window=5), title="Overall fitness")
			#fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=args.trendline_dict))
			fig.data = [t for t in fig.data if t.mode == "lines"]
			fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
			fig.write_image(FOLER_IMG + csvs_name[1] + "03.png",engine='orca')

	if(initialized == False):
		file_object.close()
		initialized = True

	logging.info("Images created waiting: " + str(args.refreshtime))
	time.sleep(args.refreshtime)
	vizualizer()

			
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='GNeuroNetWK web visualizer\n Open /dumbed_saves/visualizer/index.html')
	parser.add_argument('-refreshtime', type=int, default=7,help="Refresh time of graphs in seconds. May vary depending on amout of graphs to generate")
	parser.add_argument('-trendline_dict', type=int, default=0.015,help="Trendline trigger/smooting (default 0.015)")
	args = parser.parse_args()


initialized = False
vizualizer()




'''
tailLenght =  int(ROUND_COUNT/10) # Dynamic last 10 % of the learning will be meassured
		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_1_min_max_progress.csv")
		gen_01_win_sum = df.tail(tailLenght)['wins'].sum()/tailLenght
		gen_01_draw_sum = df.tail(tailLenght)['draws'].sum()/tailLenght
		gen_01_loss_sum = df.tail(tailLenght)['losses'].sum()/tailLenght

		df = pd.read_csv(FOLER_STATS + args.learning_Name + "_GEN_2_min_max_progress.csv")
		gen_02_win_sum = df.tail(tailLenght)['wins'].sum()/tailLenght
		gen_02_draw_sum = df.tail(tailLenght)['draws'].sum()/tailLenght
		gen_02_loss_sum = df.tail(tailLenght)['losses'].sum()/tailLenght

		hyperparameter_fitness = gen_01_win_sum + gen_02_win_sum + gen_01_draw_sum/6 + gen_02_draw_sum/6 - gen_01_loss_sum - gen_02_loss_sum
'''




'''
df = pd.read_csv('dumbed_saves/testCSV.csv')
df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Fitness_Genetics1', 'Fitness_Genetics2'])
#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
fig.data = [t for t in fig.data if t.mode == "lines"]
fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
#fig.show()
fig.write_image("test.png", engine='orca')
'''