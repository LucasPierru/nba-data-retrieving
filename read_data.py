import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamelog, leaguedashplayerstats, playergamelogs
from datetime import datetime, timedelta

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
    games_df['TEAM_HOME'] = games_df['MATCHUP'].str.contains('vs.', regex=False)*1
    games_df['TEAM_GAME_NUMBER'] = 1
    games_df['TEAM_WINS'] *= 1
    games_df['TEAM_LOSES'] = abs(games_df['TEAM_WINS'] - 1)
    games_df['TEAM_B2B'] = 0
    games_df['TEAM_WIN_STREAK'] = 0
    games_df['TEAM_LOSE_STREAK'] = 0
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
    games_df['OPP_B2B'] = 0
    games_df['OPP_WIN_STREAK'] = 0
    games_df['OPP_LOSE_STREAK'] = 0
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

      current_date = datetime.strptime(games_df['GAME_DATE'].iloc[i][2:], '%y-%m-%d')
      previous_date = datetime.strptime(games_df['GAME_DATE'].iloc[i-1][2:], '%y-%m-%d')
      next_date = previous_date + timedelta(days=1)
      if(current_date == next_date):
        games_df.loc[i, 'TEAM_B2B'] = 1
      
      if(games_df['TEAM_WINS'].iloc[i-1] == 1):
        games_df.loc[i, 'TEAM_WIN_STREAK'] = games_df.loc[i - 1, 'TEAM_WIN_STREAK'] + games_df.loc[i - 1, 'TEAM_WINS']
      else:
        games_df.loc[i, 'TEAM_WIN_STREAK'] = 0

      if(games_df['TEAM_LOSES'].iloc[i-1] == 1):
        games_df.loc[i, 'TEAM_LOSE_STREAK'] = games_df.loc[i - 1, 'TEAM_LOSE_STREAK'] + games_df.loc[i - 1, 'TEAM_LOSES']
      else:
        games_df.loc[i, 'TEAM_LOSE_STREAK'] = 0


    games_df = games_df.sort_values(by=['SEASON_ID', 'GAME_ID', 'TEAM_HOME'])
    games_df = games_df.reset_index(drop=True)

    for i in range(len(games_df)):
      if (games_df.loc[i, 'TEAM_HOME'] == True):
        games_df.loc[i, 'OPPONENT_NAME'] = games_df.loc[i-1, 'TEAM_NAME']
        games_df.loc[i, 'OPPONENT_PTS'] = games_df.loc[i-1, 'TEAM_PTS']
        games_df.loc[i, 'OPPONENT_ID'] = games_df.loc[i-1, 'TEAM_ID']
        games_df.loc[i, 'OPP_WINS'] = games_df.loc[i-1, 'TEAM_WINS']
        games_df.loc[i, 'OPP_B2B'] = games_df.loc[i-1, 'TEAM_B2B']
        games_df.loc[i, 'OPP_WIN_STREAK'] = games_df.loc[i-1, 'TEAM_WIN_STREAK']
        games_df.loc[i, 'OPP_LOSE_STREAK'] = games_df.loc[i-1, 'TEAM_LOSE_STREAK']
        games_df.loc[i, 'OPP_W_PCT'] = games_df.loc[i-1, 'TEAM_W_PCT']
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
        games_df.loc[i, 'OPP_B2B'] = games_df.loc[i+1, 'TEAM_B2B']
        games_df.loc[i, 'OPP_WIN_STREAK'] = games_df.loc[i+1, 'TEAM_WIN_STREAK']
        games_df.loc[i, 'OPP_LOSE_STREAK'] = games_df.loc[i+1, 'TEAM_LOSE_STREAK']
        games_df.loc[i, 'OPP_W_PCT'] = games_df.loc[i+1, 'TEAM_W_PCT']
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
  
  df = df.drop(columns=['PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS', 'OPPONENT_PTS','OPP_WINS'])

  return df.reset_index(drop=True).sort_values(by=['SEASON_ID', 'TEAM_NAME', 'GAME_DATE'])

def get_year(season_id):
  year_begin = season_id[1:]
  year_end = str(int(season_id[1:]) + 1)[2:]

  return year_begin + '-' + year_end

def get_team_current_players_stats(player_df, team_id, date, n_best_players=3):
  """
  Function that allows you to get the best nba players
  of a team at a certain date with the player dataframe
  you can also select a certain amount of players

  Parameters:
  - player_df: Players dataframe
  - team_id: id of the team of which you want the best players
  - date: the date at which you want the data
  - n_best_players: the numbers of players you want

  Return:
  - A dataframe of the best players of selected team
  """
  # game_df = df[df['GAME_ID'] == game_id]
  team_df = player_df[player_df['TEAM_ID'] == team_id]
  team_at_date_df = team_df[team_df['GAME_DATE'].astype(str).str[:10] <= date]
  team_at_date_df = team_at_date_df.sort_values(by=['GAME_DATE', 'PLAYER_NAME'], ascending=False)
  team_at_date_df = team_at_date_df.drop_duplicates(subset=['PLAYER_NAME'], keep='first')
  team_at_date_df = team_at_date_df[team_at_date_df['PLAYER_MIN'] > 20]
  team_at_date_df = team_at_date_df.sort_values(by=['PLAYER_PER'], ascending=False)
  
  return team_at_date_df[:n_best_players]

def check_best_player_in_game(player_df, game_id, team_id):
  game_df = player_df[player_df['GAME_ID'] == game_id]
  team_df = game_df[game_df['TEAM_ID'] == team_id]

  return team_df

def get_player_stats(df):
  season = 0
  df['TEAM PLAYER 1'] = False
  df['TEAM PLAYER 2'] = False
  df['TEAM PLAYER 3'] = False

  df['TEAM PLAYER NAME 1'] = ''
  df['TEAM PLAYER NAME 2'] = ''
  df['TEAM PLAYER NAME 3'] = ''

  df = df.reset_index(drop=True)

  for i in range(len(df)):
    print(f'{i} out of {len(df)}')
    if(season != get_year(df['SEASON_ID'].iloc[i])):
      season = get_year(df['SEASON_ID'].iloc[i])
      players = playergamelogs.PlayerGameLogs(season_nullable=season)
      players_df = players.get_data_frames()[0]
      players_df = create_player_data(players_df, 15)
    team_id = df['TEAM_ID'].iloc[i]
    game_date = df['GAME_DATE'].iloc[i]
    game_id = df['GAME_ID'].iloc[i]
    team_players_df = get_team_current_players_stats(players_df, team_id, game_date, 3)
    team_game_players_df = check_best_player_in_game(players_df, game_id, team_id)

    for j in range(len(team_players_df)):
      player_name = team_players_df['PLAYER_NAME'].iloc[j]
      df.loc[i, f'TEAM PLAYER NAME {j + 1}'] = player_name
      if (player_name in team_game_players_df['PLAYER_NAME'].values):
        df.loc[i, f'TEAM PLAYER {j + 1}'] = True
  return df

def create_player_data(games_df, last_n_games):
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
      player_index = i

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

  games_df['PLAYER_PER'] = (games_df['PLAYER_FGM'] * 85.91 + games_df['PLAYER_STL'] * 53.897 + games_df['PLAYER_FG3M'] * 51.757 +  games_df['PLAYER_FTM'] * 46.845 + games_df['PLAYER_BLK'] * 39.19 + games_df['PLAYER_OREB'] * 39.19 + games_df['PLAYER_AST'] * 34.677 + games_df['PLAYER_DREB'] * 14.707 - games_df['PLAYER_PF'] * 17.174 - (games_df['PLAYER_FTA'] - games_df['PLAYER_FTM']) * 20.091 - (games_df['PLAYER_FGA'] - games_df['PLAYER_FGM']) * 39.19 - games_df['PLAYER_TOV'] * 53.897 ) / games_df['PLAYER_MIN'] 

  games_df['PLAYER_PER'] = games_df['PLAYER_PER'].fillna(0)

  return games_df

start_year = '2008'
end_year = '2022'

years = start_year + '-' + end_year

print('getting games')
games_df = get_games(start_year=int(start_year))
print('adding player stats')
player_df = get_player_stats(df=games_df)
player_df.to_excel(f'nba_games_{years}.xlsx')