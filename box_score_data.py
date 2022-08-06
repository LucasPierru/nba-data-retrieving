from nba_api.stats.endpoints import playergamelogs

season = '2020-21'
last_n_games = 15

games = playergamelogs.PlayerGameLogs(season_nullable=season);

games_df = games.get_data_frames()[0]
games_df = games_df.sort_values(by=['TEAM_NAME', 'PLAYER_NAME', 'GAME_DATE'])
games_df = games_df.reset_index(drop=True)

games_df['PLAYER_GAME_NUMBER'] = 1
games_df['WL'] = games_df['WL'] == 'W'
games_df = games_df.rename(columns={'WL':'PLAYER_WINS'})
games_df['PLAYER_WINS'] *= 1

games_df = games_df.drop(columns=['NBA_FANTASY_PTS', 'WNBA_FANTASY_PTS'])
games_df = games_df.drop(games_df.filter(regex='RANK').columns, axis=1)

games_df['PLAYER_W_PCT'] = 0
games_df['PLAYER_FGM'] = 0
games_df['PLAYER_FGA'] = 0
games_df['PLAYER_FG_PCT'] = 0
games_df['PLAYER_FG3M'] = 0
games_df['PLAYER_FG3A'] = 0
games_df['PLAYER_FG3_PCT'] = 0
games_df['PLAYER_FTM'] = 0
games_df['PLAYER_FTA'] = 0
games_df['PLAYER_FT_PCT'] = 0
games_df['PLAYER_OREB'] = 0
games_df['PLAYER_DREB'] = 0
games_df['PLAYER_REB'] = 0
games_df['PLAYER_AST'] = 0
games_df['PLAYER_TOV'] = 0
games_df['PLAYER_STL'] = 0
games_df['PLAYER_BLK'] = 0
games_df['PLAYER_PF'] = 0
games_df['PLAYER_PTS'] = 0
games_df['PLAYER_PM'] = 0
games_df['PLAYER_MIN'] = 0
games_df['PLAYER_PER'] = 0

player_index = 0

for i in range(1, len(games_df)):
  if (games_df['PLAYER_NAME'][i] == games_df['PLAYER_NAME'][i-1]):
    games_df.loc[i, 'PLAYER_GAME_NUMBER'] = games_df.loc[i-1, 'PLAYER_GAME_NUMBER'] + 1

    if games_df['PLAYER_GAME_NUMBER'][i] <= last_n_games:
      games_df.loc[i, 'PLAYER_W_PCT'] = games_df['PLAYER_WINS'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_FGM'] = games_df['FGM'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_FGA'] = games_df['FGA'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)          
      games_df.loc[i, 'PLAYER_FG3M'] = games_df['FG3M'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_FG3A'] = games_df['FG3A'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_FTM'] = games_df['FTM'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_FTA'] = games_df['FTA'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_OREB'] = games_df['OREB'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_DREB'] = games_df['DREB'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_REB'] = games_df['REB'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_AST'] = games_df['AST'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_TOV'] = games_df['TOV'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_STL'] = games_df['STL'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_BLK'] = games_df['BLK'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_PF'] = games_df['PF'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_PTS'] = games_df['PTS'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_PM'] = games_df['PLUS_MINUS'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
      games_df.loc[i, 'PLAYER_MIN'] = games_df['MIN'].iloc[player_index:i].sum() / (games_df['PLAYER_GAME_NUMBER'][i] - 1)
    else:
      games_df.loc[i, 'PLAYER_W_PCT'] = games_df['PLAYER_WINS'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FGM'] = games_df['FGM'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FGA'] = games_df['FGA'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FG3M'] = games_df['FG3M'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FG3A'] = games_df['FG3A'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FTM'] = games_df['FTM'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_FTA'] = games_df['FTA'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_OREB'] = games_df['OREB'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_DREB'] = games_df['DREB'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_REB'] = games_df['REB'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_AST'] = games_df['AST'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_TOV'] = games_df['TOV'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_STL'] = games_df['STL'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_BLK'] = games_df['BLK'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_PF'] = games_df['PF'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_PTS'] = games_df['PTS'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_PM'] = games_df['PLUS_MINUS'].iloc[i-last_n_games:i].sum() / last_n_games
      games_df.loc[i, 'PLAYER_MIN'] = games_df['MIN'].iloc[i-last_n_games:i].sum() / last_n_games
  else:
    games_df.loc[i, 'PLAYER_GAME_NUMBER'] = 1
    team_index = i

  if (games_df.loc[i, 'PLAYER_FGA'] == 0):
          games_df.loc[i, 'PLAYER_FG_PCT'] = 0
  else:
    games_df.loc[i, 'PLAYER_FG_PCT'] = games_df.loc[i, 'PLAYER_FGM'] / games_df.loc[i, 'PLAYER_FGA']

  if (games_df.loc[i, 'PLAYER_FG3A'] == 0):
    games_df.loc[i, 'PLAYER_FG3_PCT'] = 0
  else:
    games_df.loc[i, 'PLAYER_FG3_PCT'] = games_df.loc[i, 'PLAYER_FG3M'] / games_df.loc[i, 'PLAYER_FG3A']

  if (games_df.loc[i, 'PLAYER_FTA'] == 0):
    games_df.loc[i, 'PLAYER_FT_PCT'] = 0
  else:
    games_df.loc[i, 'PLAYER_FT_PCT'] = games_df.loc[i, 'PLAYER_FTM'] / games_df.loc[i, 'PLAYER_FTA']

games_df['PLAYER_PER'] = (games_df['PLAYER_FGM'] * 85.91 +  games_df['PLAYER_STL'] * 53.897 +  games_df['PLAYER_FG3M'] * 51.757 +  games_df['PLAYER_FTM'] * 46.845 +  games_df['PLAYER_BLK'] * 39.19 + games_df['PLAYER_OREB'] * 39.19 +  games_df['PLAYER_AST'] * 34.677 +  games_df['PLAYER_DREB'] * 14.707 -  games_df['PLAYER_PF'] * 17.174 -  (games_df['PLAYER_FTA'] -  games_df['PLAYER_FTM']) * 20.091 - (games_df['PLAYER_FGA'] -  games_df['PLAYER_FGM']) * 39.19 - games_df['PLAYER_TOV'] * 53.897 ) /  games_df['PLAYER_MIN'] 

games_df['PLAYER_PER'] = games_df['PLAYER_PER'].fillna(0)

print(games_df)

games_df.to_excel(f'player_data_{season}.xlsx')
