from distutils.command import check
import pandas as pd

player_df = pd.read_excel('player_data_2021-22.xlsx')

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
  team_df['GAME_DATE'] = team_df['GAME_DATE'].astype(str).str[:10]
  team_at_date_df = team_df[team_df['GAME_DATE'] < date]
  team_at_date_df = team_at_date_df.sort_values(by=['GAME_DATE', 'PLAYER_NAME'], ascending=False)
  team_at_date_df = team_at_date_df.drop_duplicates(subset=['PLAYER_NAME'], keep='first')
  team_at_date_df = team_at_date_df[team_at_date_df['PLAYER_MIN'] > 20]
  team_at_date_df = team_at_date_df.sort_values(by=['PLAYER_PER'], ascending=False)
  
  return team_at_date_df[:n_best_players]

def check_best_player_in_game(player_df, game_id, team_id):
  game_df = player_df[player_df['GAME_ID'] == game_id]
  team_df = game_df[game_df['TEAM_ID'] == team_id]

  return team_df

df = get_team_current_players_stats(player_df, 1610612737, '2021-11-24', 3)
print(df)
print(df['GAME_DATE'])

df2 = check_best_player_in_game(player_df, 22100277, 1610612737)
print(df2)

for i in range(len(df)):
  player_name = df['PLAYER_NAME'].iloc[i]
  if (player_name in df2['PLAYER_NAME'].values):
    print(player_name, i + 1)