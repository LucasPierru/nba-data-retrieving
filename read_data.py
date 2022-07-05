import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamelog, leaguedashteamstats

def transpose_df_to_dict(df):
  return df.T.to_dict().values()

def get_games(start_year=2012, end_year=2022, last_n_games=10):
  df = pd.DataFrame()
  seasons = np.linspace(start_year, end_year-1, num=end_year-start_year)
  for season in seasons:
    games = leaguegamelog.LeagueGameLog(season_type_all_star='Regular Season', season=int(season))
    games_df = games.get_data_frames()[0]
    games_df = games_df.drop(['MIN', 'VIDEO_AVAILABLE'], axis=1)
    games_df['WL'] = games_df['WL'] == 'W'
    games_df = games_df.rename(columns={'WL':'TEAM_WINS'})
    games_df['TEAM_HOME'] = games_df['MATCHUP'].str.contains('vs.', regex=False)
    games_df['TEAM_GAME_NUMBER'] = 1
    games_df['TEAM_WINS'] *= 1
    games_df['TEAM_W_PCT'] = 0
    games_df['TEAM_FGM'] = 0
    games_df['TEAM_FGA'] = 0
    games_df['TEAM_FG_PCT'] = 0
    games_df['TEAM_FG3M'] = 0
    games_df['TEAM_FG3A'] = 0
    games_df['TEAM_FG3_PCT'] = 0
    games_df['TEAM_FTM'] = 0
    games_df['TEAM_FTA'] = 0
    games_df['TEAM_FT_PCT'] = 0
    games_df['TEAM_OREB'] = 0
    games_df['TEAM_DREB'] = 0
    games_df['TEAM_REB'] = 0
    games_df['TEAM_AST'] = 0
    games_df['TEAM_TOV'] = 0
    games_df['TEAM_STL'] = 0
    games_df['TEAM_BLK'] = 0
    games_df['TEAM_PF'] = 0
    games_df['TEAM_PTS'] = 0
    games_df['TEAM_PM'] = 0
    games_df['OPPONENT_NAME'] = np.nan
    games_df['OPPONENT_PTS'] = np.nan
    games_df['OPPONENT_ID'] = np.nan
    games_df['OPP_WINS'] = np.nan
    games_df['OPP_W_PCT'] = np.nan
    games_df['OPP_FGM'] = np.nan
    games_df['OPP_FGA'] = np.nan
    games_df['OPP_FG_PCT'] = np.nan
    games_df['OPP_FG3M'] = np.nan
    games_df['OPP_FG3A'] = np.nan
    games_df['OPP_FG3_PCT'] = np.nan
    games_df['OPP_FTM'] = np.nan
    games_df['OPP_FTA'] = np.nan
    games_df['OPP_FT_PCT'] = np.nan
    games_df['OPP_OREB'] = np.nan
    games_df['OPP_DREB'] = np.nan
    games_df['OPP_REB'] = np.nan
    games_df['OPP_AST'] = np.nan
    games_df['OPP_TOV'] = np.nan
    games_df['OPP_STL'] = np.nan
    games_df['OPP_BLK'] = np.nan
    games_df['OPP_PF'] = np.nan
    games_df['OPP_PTS'] = np.nan
    games_df['OPP_PM'] = np.nan
    
    games_df = games_df.sort_values(by=['TEAM_NAME', 'GAME_DATE'])
    games_df = games_df.reset_index(drop=True)
    
    team_index = 0
    for i in range(1, len(games_df)):
      if (games_df['TEAM_NAME'][i] == games_df['TEAM_NAME'][i-1]):
        games_df.loc[i, 'TEAM_GAME_NUMBER'] = games_df.loc[i-1, 'TEAM_GAME_NUMBER'] + 1

              

        if games_df['TEAM_GAME_NUMBER'][i] <= last_n_games:
          games_df.loc[i, 'TEAM_W_PCT'] = games_df['TEAM_WINS'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_FGM'] = games_df['FGM'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_FGA'] = games_df['FGA'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)          
          games_df.loc[i, 'TEAM_FG3M'] = games_df['FG3M'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_FG3A'] = games_df['FG3A'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_FTM'] = games_df['FTM'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_FTA'] = games_df['FTA'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_OREB'] = games_df['OREB'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_DREB'] = games_df['DREB'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_REB'] = games_df['REB'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_AST'] = games_df['AST'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_TOV'] = games_df['TOV'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_STL'] = games_df['STL'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_BLK'] = games_df['BLK'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_PF'] = games_df['PF'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_PTS'] = games_df['PTS'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
          games_df.loc[i, 'TEAM_PM'] = games_df['PLUS_MINUS'].iloc[team_index:i].sum() / (games_df['TEAM_GAME_NUMBER'][i] - 1)
        else:
          games_df.loc[i, 'TEAM_W_PCT'] = games_df['TEAM_WINS'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FGM'] = games_df['FGM'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FGA'] = games_df['FGA'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FG3M'] = games_df['FG3M'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FG3A'] = games_df['FG3A'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FTM'] = games_df['FTM'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_FTA'] = games_df['FTA'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_OREB'] = games_df['OREB'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_DREB'] = games_df['DREB'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_REB'] = games_df['REB'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_AST'] = games_df['AST'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_TOV'] = games_df['TOV'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_STL'] = games_df['STL'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_BLK'] = games_df['BLK'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_PF'] = games_df['PF'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_PTS'] = games_df['PTS'].iloc[i-last_n_games:i].sum() / last_n_games
          games_df.loc[i, 'TEAM_PM'] = games_df['PLUS_MINUS'].iloc[i-last_n_games:i].sum() / last_n_games
      else:
        games_df.loc[i, 'TEAM_GAME_NUMBER'] = 1
        team_index = i
      
      if (games_df.loc[i, 'TEAM_FGA'] == 0):
          games_df.loc[i, 'TEAM_FG_PCT'] = 0
      else:
        games_df.loc[i, 'TEAM_FG_PCT'] = games_df.loc[i, 'TEAM_FGM'] / games_df.loc[i, 'TEAM_FGA']

      if (games_df.loc[i, 'TEAM_FG3A'] == 0):
        games_df.loc[i, 'TEAM_FG3_PCT'] = 0
      else:
        games_df.loc[i, 'TEAM_FG3_PCT'] = games_df.loc[i, 'TEAM_FG3M'] / games_df.loc[i, 'TEAM_FG3A']

      if (games_df.loc[i, 'TEAM_FTA'] == 0):
        games_df.loc[i, 'TEAM_FT_PCT'] = 0
      else:
        games_df.loc[i, 'TEAM_FT_PCT'] = games_df.loc[i, 'TEAM_FTM'] / games_df.loc[i, 'TEAM_FTA']

    games_df = games_df.sort_values(by=['SEASON_ID', 'GAME_ID', 'TEAM_HOME'])
    games_df = games_df.reset_index(drop=True)

    for i in range(len(games_df)):
      if (games_df.loc[i, 'TEAM_HOME'] == True):
        games_df.loc[i, 'OPPONENT_NAME'] = games_df.loc[i-1, 'TEAM_NAME']
        games_df.loc[i, 'OPPONENT_PTS'] = games_df.loc[i-1, 'TEAM_PTS']
        games_df.loc[i, 'OPPONENT_ID'] = games_df.loc[i-1, 'TEAM_ID']
        games_df.loc[i, 'OPP_WINS'] = games_df.loc[i-1, 'TEAM_WINS']
        games_df.loc[i, 'OPP_FGM'] = games_df.loc[i-1, 'TEAM_FGM']
        games_df.loc[i, 'OPP_FGA'] = games_df.loc[i-1, 'TEAM_FGA']
        games_df.loc[i, 'OPP_FG_PCT'] = games_df.loc[i-1, 'TEAM_FG_PCT']
        games_df.loc[i, 'OPP_FG3M'] = games_df.loc[i-1, 'TEAM_FG3M']
        games_df.loc[i, 'OPP_FG3A'] = games_df.loc[i-1, 'TEAM_FG3A']
        games_df.loc[i, 'OPP_FG3_PCT'] = games_df.loc[i-1, 'TEAM_FG3_PCT']
        games_df.loc[i, 'OPP_FTM'] = games_df.loc[i-1, 'TEAM_FTM']
        games_df.loc[i, 'OPP_FTA'] = games_df.loc[i-1, 'TEAM_FTA']
        games_df.loc[i, 'OPP_FT_PCT'] = games_df.loc[i-1, 'TEAM_FT_PCT']
        games_df.loc[i, 'OPP_OREB'] = games_df.loc[i-1, 'TEAM_OREB']
        games_df.loc[i, 'OPP_DREB'] = games_df.loc[i-1, 'TEAM_DREB']
        games_df.loc[i, 'OPP_REB'] = games_df.loc[i-1, 'TEAM_REB']
        games_df.loc[i, 'OPP_AST'] = games_df.loc[i-1, 'TEAM_AST']
        games_df.loc[i, 'OPP_TOV'] = games_df.loc[i-1, 'TEAM_TOV']
        games_df.loc[i, 'OPP_STL'] = games_df.loc[i-1, 'TEAM_STL']
        games_df.loc[i, 'OPP_BLK'] = games_df.loc[i-1, 'TEAM_BLK']
        games_df.loc[i, 'OPP_PF'] = games_df.loc[i-1, 'TEAM_PF']
        games_df.loc[i, 'OPP_PTS'] = games_df.loc[i-1, 'TEAM_PTS']
        games_df.loc[i, 'OPP_PM'] = games_df.loc[i-1, 'TEAM_PM']
      else:
        games_df.loc[i, 'OPPONENT_NAME'] = games_df.loc[i+1, 'TEAM_NAME']
        games_df.loc[i, 'OPPONENT_PTS'] = games_df.loc[i+1, 'TEAM_PTS']
        games_df.loc[i, 'OPPONENT_ID'] = games_df.loc[i+1, 'TEAM_ID']
        games_df.loc[i, 'OPP_WINS'] = games_df.loc[i+1, 'TEAM_WINS']
        games_df.loc[i, 'OPP_FGM'] = games_df.loc[i+1, 'TEAM_FGM']
        games_df.loc[i, 'OPP_FGA'] = games_df.loc[i+1, 'TEAM_FGA']
        games_df.loc[i, 'OPP_FG_PCT'] = games_df.loc[i+1, 'TEAM_FG_PCT']
        games_df.loc[i, 'OPP_FG3M'] = games_df.loc[i+1, 'TEAM_FG3M']
        games_df.loc[i, 'OPP_FG3A'] = games_df.loc[i+1, 'TEAM_FG3A']
        games_df.loc[i, 'OPP_FG3_PCT'] = games_df.loc[i+1, 'TEAM_FG3_PCT']
        games_df.loc[i, 'OPP_FTM'] = games_df.loc[i+1, 'TEAM_FTM']
        games_df.loc[i, 'OPP_FTA'] = games_df.loc[i+1, 'TEAM_FTA']
        games_df.loc[i, 'OPP_FT_PCT'] = games_df.loc[i+1, 'TEAM_FT_PCT']
        games_df.loc[i, 'OPP_OREB'] = games_df.loc[i+1, 'TEAM_OREB']
        games_df.loc[i, 'OPP_DREB'] = games_df.loc[i+1, 'TEAM_DREB']
        games_df.loc[i, 'OPP_REB'] = games_df.loc[i+1, 'TEAM_REB']
        games_df.loc[i, 'OPP_AST'] = games_df.loc[i+1, 'TEAM_AST']
        games_df.loc[i, 'OPP_TOV'] = games_df.loc[i+1, 'TEAM_TOV']
        games_df.loc[i, 'OPP_STL'] = games_df.loc[i+1, 'TEAM_STL']
        games_df.loc[i, 'OPP_BLK'] = games_df.loc[i+1, 'TEAM_BLK']
        games_df.loc[i, 'OPP_PF'] = games_df.loc[i+1, 'TEAM_PF']
        games_df.loc[i, 'OPP_PTS'] = games_df.loc[i+1, 'TEAM_PTS']
        games_df.loc[i, 'OPP_PM'] = games_df.loc[i+1, 'TEAM_PM']
      
    df = pd.concat([df, games_df])
  
  df = df.drop(columns=['PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS'])

  return df.reset_index(drop=True).sort_values(by=['SEASON_ID', 'TEAM_NAME', 'GAME_DATE'])

def append_team_stats_before_game(df, last_n_games=10):
  df['TEAM_W_PCT'] = np.nan
  df['TEAM_FGM'] = np.nan
  df['TEAM_FGA'] = np.nan
  df['TEAM_FG_PCT'] = np.nan
  df['TEAM_FG3M'] = np.nan
  df['TEAM_FG3A'] = np.nan
  df['TEAM_FG3_PCT'] = np.nan
  df['TEAM_FTM'] = np.nan
  df['TEAM_FTA'] = np.nan
  df['TEAM_FT_PCT'] = np.nan
  df['TEAM_OREB'] = np.nan
  df['TEAM_DREB'] = np.nan
  df['TEAM_REB'] = np.nan
  df['TEAM_AST'] = np.nan
  df['TEAM_TOV'] = np.nan
  df['TEAM_STL'] = np.nan
  df['TEAM_BLK'] = np.nan
  df['TEAM_PF'] = np.nan
  df['TEAM_PTS'] = np.nan
  df['TEAM_PM'] = np.nan

  df['OPP_W_PCT'] = np.nan
  df['OPP_FGM'] = np.nan
  df['OPP_FGA'] = np.nan
  df['OPP_FG_PCT'] = np.nan
  df['OPP_FG3M'] = np.nan
  df['OPP_FG3A'] = np.nan
  df['OPP_FG3_PCT'] = np.nan
  df['OPP_FTM'] = np.nan
  df['OPP_FTA'] = np.nan
  df['OPP_FT_PCT'] = np.nan
  df['OPP_OREB'] = np.nan
  df['OPP_DREB'] = np.nan
  df['OPP_REB'] = np.nan
  df['OPP_AST'] = np.nan
  df['OPP_TOV'] = np.nan
  df['OPP_STL'] = np.nan
  df['OPP_BLK'] = np.nan
  df['OPP_PF'] = np.nan
  df['OPP_PTS'] = np.nan
  df['OPP_PM'] = np.nan

  for i in range(len(df)):
    stats = leaguedashteamstats.LeagueDashTeamStats(
      last_n_games=last_n_games, 
      date_to_nullable=df['GAME_DATE'][i]
    )
    stats_df = stats.get_data_frames()[0]
    print(stats_df)

    df.loc[i, 'TEAM_W_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['W_PCT']
    df.loc[i, 'TEAM_FGM'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FGM']
    df.loc[i, 'TEAM_FGA'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FGA']
    df.loc[i, 'TEAM_FG_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FG_PCT']
    df.loc[i, 'TEAM_FG3M'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FG3M']
    df.loc[i, 'TEAM_FG3A'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FG3A']
    df.loc[i, 'TEAM_FG3_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FG3_PCT']
    df.loc[i, 'TEAM_FTM'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FTM']
    df.loc[i, 'TEAM_FTA'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FTA']
    df.loc[i, 'TEAM_FT_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['FT_PCT']
    df.loc[i, 'TEAM_OREB'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['OREB']
    df.loc[i, 'TEAM_DREB'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['DREB']
    df.loc[i, 'TEAM_REB'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['REB']
    df.loc[i, 'TEAM_AST'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['AST']
    df.loc[i, 'TEAM_TOV'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['TOV']
    df.loc[i, 'TEAM_STL'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['STL']
    df.loc[i, 'TEAM_BLK'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['BLK']
    df.loc[i, 'TEAM_PF'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['PF']
    df.loc[i, 'TEAM_PTS'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['PTS']
    df.loc[i, 'TEAM_PM'] = stats_df[stats_df['TEAM_NAME'] == df['TEAM_NAME'][i]]['PLUS_MINUS']

    df.loc[i, 'OPP_W_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['W_PCT']
    df.loc[i, 'OPP_FGM'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FGM']
    df.loc[i, 'OPP_FGA'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FGA']
    df.loc[i, 'OPP_FG_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FG_PCT']
    df.loc[i, 'OPP_FG3M'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FG3M']
    df.loc[i, 'OPP_FG3A'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FG3A']
    df.loc[i, 'OPP_FG3_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FG3_PCT']
    df.loc[i, 'OPP_FTM'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FTM']
    df.loc[i, 'OPP_FTA'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FTA']
    df.loc[i, 'OPP_FT_PCT'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['FT_PCT']
    df.loc[i, 'OPP_OREB'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['OREB']
    df.loc[i, 'OPP_DREB'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['DREB']
    df.loc[i, 'OPP_REB'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['REB']
    df.loc[i, 'OPP_AST'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['AST']
    df.loc[i, 'OPP_TOV'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['TOV']
    df.loc[i, 'OPP_STL'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['STL']
    df.loc[i, 'OPP_BLK'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['BLK']
    df.loc[i, 'OPP_PF'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['PF']
    df.loc[i, 'OPP_PTS'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['PTS']
    df.loc[i, 'OPP_PM'] = stats_df[stats_df['TEAM_NAME'] == df['OPPONENT_NAME'][i]]['PLUS_MINUS']
  
  return df

games_df = get_games(start_year=2008)
# games_df = append_team_stats_before_game(games_df)
games_df.to_excel('nba_games_2008_2022.xlsx')


