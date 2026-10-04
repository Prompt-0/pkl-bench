import pandas as pd
df = pd.read_parquet('data/matches/matches.parquet')
teams = pd.read_csv('data/metadata/teams.csv')
venues = pd.read_csv('data/metadata/venues.csv')

df_merged = df.merge(venues[['venue_id', 'city']], on='venue_id', how='left')
df_merged = df_merged.merge(teams[['team_id', 'home_city']], left_on='team1_id', right_on='team_id', how='left', suffixes=('', '_team1'))
df_merged = df_merged.merge(teams[['team_id', 'home_city']], left_on='team2_id', right_on='team_id', how='left', suffixes=('_team1', '_team2'))

# Check how often team1 is home, team2 is home
team1_home = (df_merged['city'] == df_merged['home_city_team1']).sum()
team2_home = (df_merged['city'] == df_merged['home_city_team2']).sum()
neutral = (~(df_merged['city'] == df_merged['home_city_team1'])) & (~(df_merged['city'] == df_merged['home_city_team2']))
neutral_count = neutral.sum()
print(f"Team 1 home: {team1_home}, Team 2 home: {team2_home}, Neutral: {neutral_count}")
