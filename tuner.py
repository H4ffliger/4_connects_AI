import pandas as pd
import plotly.express as px
import plotly.express as px
import numpy as np
import argparse
import sys


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='GNeuroNetWK fitness analysis and impact visualization on fitness')
	parser.add_argument('csv_file', type=str, default="output.csv",help="Csv data with headers. Required header fitness_score")
	args = parser.parse_args()


data = pd.read_csv(args.csv_file)
print(data)
data = data.corr()
print(data)
print(data["FITNESS_SCORE"])