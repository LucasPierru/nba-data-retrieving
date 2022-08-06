import pandas as pd

player_df = pd.read_excel('player_data_2021-22.xlsx')

def get_team_best_players(df, game_id, team_id):
  game_df = df[df['GAME_ID'] == game_id]
  team_game_df = game_df[game_df['TEAM_ID'] == team_id]

  print(team_game_df)

get_team_best_players(player_df, 22100082, 1610612737)

# print(player_df)