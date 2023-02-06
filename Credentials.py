import gspread

gc = gspread.service_account()

sh = gc.open("FPL Data")

print(sh.sheet1.get('A1'))

import os
os.getcwd()

