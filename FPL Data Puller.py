
def data_puller():

    import pandas as pd
    import numpy as np
    import json
    import requests
    import gspread
    import df2gspread as d2g
    from pandas.io.json import json_normalize
    from pprint import pprint
    
    # Define a function to get info from the FPL API and save to the specified file_path
    # It might be a good idea to navigate to the link in a browser to get an idea of what the data looks like

    # base url for all FPL API endpoints
    base_url = 'https://fantasy.premierleague.com/api/'

    # get data from bootstrap-static endpoint
    r = requests.get(base_url+'bootstrap-static/').json()

    # DATAFRAMES CREATED
    # average_entry_score_df 
    # league_standings
    # manager_details
    # league_ids
    # chips_count_df
    # chips_count_by_chip 
    # manager_data

    # pull average entry score
    average_entry_score_df = pd.DataFrame(pd.json_normalize(r['events']).average_entry_score).reset_index()
    average_entry_score_df = average_entry_score_df.rename(columns={'index':'gameweek', 'average_entry_score' : 'average_entry_score'})

    # pull overall league standings
    r = requests.get(base_url+'leagues-classic/511267/standings').json()
    league_standings=pd.DataFrame(pd.json_normalize(r['standings']).results[0])
    league_standings = league_standings[['player_name', 'entry_name', 'rank', 'total']]

    # manager details
    manager_details = pd.DataFrame(pd.json_normalize(r['standings']).results[0])
    manager_details = manager_details[['entry', 'entry_name', 'player_name']]
    manager_details.rename(columns={'entry': 'team_id', 'entry_name':'team_name', 'player_name':'player_name'}, inplace=True)

    # Define past gameweek data getter
    def past_data_getter(id: int):
        base_url = 'https://fantasy.premierleague.com/api/'
        r = requests.get(base_url+'entry/{}/history/'.format(id)).json()
        df = pd.json_normalize(r['current'])
        df['id_cell']='{}'.format(id)
        return df

    # get each persons league ids
    r = requests.get(base_url+'leagues-classic/511267/standings').json()
    league_ids=pd.DataFrame(pd.json_normalize(r['standings']).results[0])['entry']

    # get past gameweek manager data
    data_frame_list = []

    for i in league_ids:
        df = past_data_getter(i)
        data_frame_list.append(df)
    past_manager_data = pd.concat(data_frame_list , axis = 0)

    # CHIPS USED FUNCTION
    def chips_used_getter(id: int):
        base_url = 'https://fantasy.premierleague.com/api/'
        r = requests.get(base_url+'entry/{}/history/'.format(id)).json()
        df = pd.json_normalize(r['chips'])
        df['id_cell']='{}'.format(id)
        return df

    # get chips used for each manager
    empty_df = []
    for i in league_ids:
            df = chips_used_getter(i)
            empty_df.append(df)
    merged_data_2 = pd.concat(empty_df, axis = 0)

    # reformat chips used
    merged_data_2['id_cell']=merged_data_2['id_cell'].astype('int')
    chips_used_df = pd.merge(merged_data_2, manager_details, how = 'left', left_on = 'id_cell', right_on = 'team_id')
    chips_used_df[['player_name', 'name']]

    conditions = [chips_used_df['name']=='wildcard', chips_used_df['name']=='bboost', chips_used_df['name']=='3xc', chips_used_df['name']=='freehit']

    values = ['wildcard', 'bench boost', 'triple captain', 'freehit']

    chips_used_df['chips']=np.select(conditions, values)

    # create chips count df
    chips_count_df = chips_used_df[['player_name', 'name']].groupby(by='player_name').count()

    # create chips used by chip
    chips_count_by_chip = chips_used_df[['player_name', 'chips', 'name']].groupby(by=['player_name', 'chips']).count()
    chips_count_by_chip

    # Join manager details onto past_manager gameweek data
    past_manager_data['id_cell']=past_manager_data['id_cell'].astype('int')
    manager_data = pd.merge(past_manager_data, manager_details, left_on= 'id_cell', right_on= 'team_id', how = 'left') 

