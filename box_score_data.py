from nba_api.stats.endpoints import playergamelogs

season = '2021-22'

games = playergamelogs.PlayerGameLogs(season_nullable=season);

games_df = games.get_data_frames()[0]
games_df = games_df.sort_values(by=['TEAM_NAME', 'PLAYER_NAME', 'GAME_DATE'])
games_df = games_df.reset_index(drop=True)

games_df['PLAYER_GAME_NUMBER'] = 1

for i in range(1, len(games_df)):
  if(i == 1):
    print(games_df['PLAYER_NAME'][i], games_df['PLAYER_NAME'][i-1])
  if (games_df['PLAYER_NAME'][i] == games_df['PLAYER_NAME'][i-1]):
    games_df.loc[i, 'PLAYER_GAME_NUMBER'] = games_df.loc[i-1, 'PLAYER_GAME_NUMBER'] + 1

print(games_df)

games_df.to_excel(f'player_data_{season}.xlsx')
