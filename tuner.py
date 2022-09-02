import pandas as pd
import plotly.express as px
import plotly.express as px
import numpy as np
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='GNeuroNetWK fitness analysis and impact visualization on fitness')
	parser.add_argument('csv_file', type=str, default="output.csv",help="Csv data with headers. Required header fitness_score")
	args = parser.parse_args()



#print(np.corrcoef(var1, var2)[1][0])


#print(df.tail['wins'])

data = pd.read_csv(args.csv_file)
#print(data)
#data = data.corr()
print(data['FITNESS_SCORE'])

'''
df = pd.read_csv(csv_file)
df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Fitness_Genetics1', 'Fitness_Genetics2'])
#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
fig.data = [t for t in fig.data if t.mode == "lines"]
fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
#fig.show()
fig.write_image("test.png", engine='orca')'''