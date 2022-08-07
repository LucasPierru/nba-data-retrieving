import pandas as pd
from datetime import datetime, timedelta

df = pd.read_excel('nba_games_2021-2022.xlsx')

df = df.drop(columns=['Unnamed: 0'])

print(abs(df['TEAM_WINS'] - 1), df['TEAM_WINS'])

df['TEAM_LOSES'] = abs(df['TEAM_WINS'] - 1)
