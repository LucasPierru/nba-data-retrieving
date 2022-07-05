import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashteamstats, teamdashboardbylastngames


gamedata = leaguedashteamstats.LeagueDashTeamStats(
  last_n_games=10, 
  season='2019-20', 
  date_to_nullable='2020-02-01',
  season_type_all_star='Regular Season'
)

df = gamedata.get_data_frames()[0]
print(df)
print(df[df['TEAM_NAME'] == 'Atlanta Hawks']['W_PCT'])