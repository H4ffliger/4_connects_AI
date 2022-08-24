import pandas as pd
import plotly.express as px
import sys


filehandler = open("dumbed_saves/" + sys.argv[1], 'rb') 

df = pd.read_csv(filehandler)

fig = px.line(df, title='Neural NetWK Stats')
fig.show()