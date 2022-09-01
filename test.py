import pandas as pd
import plotly.express as px


df = pd.read_csv('dumbed_saves/testCSV.csv')
df_long=pd.melt(df, id_vars='Round_Number', value_vars=['Fitness_Genetics1', 'Fitness_Genetics2'])
#fig = px.line(df_long, x = 'Round_Number', y = 'value',color='variable', title='TITLE')
fig = px.scatter(df_long, x="Round_Number", y="value",color='variable', trendline="lowess", trendline_options=dict(frac=0.015))
fig.data = [t for t in fig.data if t.mode == "lines"]
fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
#fig.show()
fig.write_image("test.png", engine='orca')