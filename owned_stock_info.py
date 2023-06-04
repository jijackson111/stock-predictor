import os
from retrieve_data import Stock, DataFrame

# Get list of owed stocks
curr_dir = os.getcwd()
file = '{}/usr/stocks_owned.txt'.format(curr_dir)
f = open(file, 'r')
file_contents = f.read()
file_contents = file_contents.split('\n')
owned_stocks = [ln for ln in file_contents]

# Get stock info
for stock in owned_stocks:
    s = Stock(stock)
    df = s.eod()
    df = df.drop(['High', 'Low', 'Adjusted_close'], axis=1)
    DataFrame.show_gui(df)
    
