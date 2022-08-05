from nba_api.stats.endpoints import boxscoreusagev2

games = boxscoreusagev2.BoxScoreUsageV2(game_id='0020800004');

games_df = games.get_data_frames()[0]

print(games_df[games_df['PLAYER_NAME'] == 'Maurice Evans'], games_df[games_df['PLAYER_NAME'] == 'Trae Young'])

if(not games_df[games_df['PLAYER_NAME'] == 'Maurice Evans'].empty): 
  print('Maurice')

if(not games_df[games_df['PLAYER_NAME'] == 'Trae Young'].empty):
  print('Trae')