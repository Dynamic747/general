from FPL_Data_Puller import FPL_DATA_PULL

import os
import gspread
import pandas as pd
from df2gspread import df2gspread as d2g


manager_data, average_entry_score_df, league_standings, league_ids, chips_count_df, chips_count_by_chip = FPL_DATA_PULL()

os.chdir('C://Users//jai_9//OneDrive//Documents//Python//General Python')
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'jsonFileFromGoogle.json', scope)
gc = gspread.authorize(credentials)

spreadsheet_key = '1GR_XSOY2IaLmAv3ENtGhxVFNUgwnA4QXnCpV7j1ubUQ'

#  League Standings
wks_name = 'League Standings'
d2g.upload(league_standings, spreadsheet_key, wks_name, credentials=credentials, row_names=False)

#  average_entry_score
wks_name = 'Average Entry Score'
d2g.upload(average_entry_score_df, spreadsheet_key, wks_name, credentials=credentials, row_names=False)

#  chips_count_df
wks_name = 'Chips Used'
d2g.upload(chips_count_df, spreadsheet_key, wks_name, credentials=credentials, row_names=False)

#  chips_count_by_chip
wks_name = 'Chips Used By Chip'
d2g.upload(chips_count_by_chip, spreadsheet_key, wks_name, credentials=credentials, row_names=False)

wks_name = 'Full Manager GWs'
d2g.upload(manager_data, spreadsheet_key, wks_name, credentials=credentials, row_names=False)
