# Import modules
from datetime import date
import requests
import pandas as pd
from io import StringIO
from pandasgui import show

# Global variables
PATH = 'https://eodhistoricaldata.com/api/'
TOKEN = '62fd0c7c17f9b6.32258657'
today = str(date.today())
year_d1 = today[:5] + '01-01'

# Dataframe class
class DataFrame:  
    def __init__(self, data):
        self.data = data
        
    def csv(self):
        csvString = StringIO(self.data)
        df = pd.read_csv(csvString, sep=",", header=None)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.set_index(df.columns[0])
        return df
    
    def dict_list(self):
        df = pd.DataFrame.from_dict(self.data) 
        df = df.set_index(df.columns[0])
        return df 
    
    def create_df(self, fmt):
        p = self.__getattribute__(fmt)
        return p()
    
    def show_gui(dataframe):
        show(dataframe)
    
# Stock class
class Stock:
    def __init__(self, ticker, from_date=year_d1, to_date=today, fmt='csv'):
        self.ticker = ticker
        self.fdate = from_date
        self.tdate = to_date
        self.fmt = fmt
        
    def get_data(self, url):
        data = requests.get(url).text
        d = DataFrame(data)
        df = d.create_df(self.fmt)
        return df
        
    def eod(self, period='w', order='d'):
        code = 'eod'
        url = '{}{}/{}?from={}&to={}&period={}&order={}&api_token={}'.format(PATH, code, self.ticker, self.fdate, self.tdate, period, order, TOKEN)
        df = self.get_data(url)
        return df
    
    def realtime(self):
        code = 'real-time'
        url = '{}{}/{}?self.fmt={}&api_token={}'.format(PATH, code, self.ticker, self.fmt, TOKEN)
        df = self.get_data(url)
        return df
    
    def dividends(self):
        code = 'div'
        url = '{}{}/{}?from={}&to={}&api_token={}'.format(PATH, code, self.ticker, self.fdate, self.tdate, TOKEN)
        df = self.get_data(url)
        return df
    
    def splits(self):
        code = 'splits'
        url = '{}{}/{}?from={}&to={}&api_token={}'.format(PATH, code, self.ticker, self.fdate, self.tdate, TOKEN)
        df = self.get_data(url)
        return df
    
    def technical(self, func, period='w', order='d'):
        code = 'technical'
        url = '{}{}/{}?order={}&fmt={}&from={}&to={}&function={}&period={}&&api_token={}'.format(PATH, code, self.ticker, order, self.fmt, self.fdate, self.tdate, func, period, TOKEN)
        df = self.get_data(url)
        return df
    
    def intraday(self, interval=5):
        code = 'intraday'
        inv = '{}m'.format(interval)
        url = '{}{}/{}?api_token={}&interval={}'.format(PATH, code, self.ticker, TOKEN, inv)
        df = self.get_data(url)
        return df
        
    def fundamentals(self, filt=None):
        code = 'fundamentals'
        url = '{}{}/{}?api_token={}'.format(PATH, code, self.ticker, TOKEN)
        if filt != None:
            add = '&filter={}'.format(filt)
            url = url + add
        df = self.get_data(url)
        return df       
    
    def sentiments(self, form='financial'):
        if form == 'financial':
            code = 'sentiments'
        elif form == 'tweets':
            code = 'tweets-sentiments'
        else:
            return 'Invalid parameter'
        tick = str.lower(self.ticker[:self.ticker.find('.')])
        url = '{}{}?s={}&from={}&to={}&api_token={}'.format(PATH, code, tick, self.fdate, self.tdate, TOKEN)
        df = self.get_data(url)
        return df       
    
# Market class
class Market:
    def __init__(self, from_date=year_d1, to_date=today, fmt='csv'):
        self.fdate = from_date
        self.tdate = to_date
        self.fmt = fmt
        
    def eod_bulk(self, country):
        code = 'eod-bulk-last-day'
        url = '{}{}/{}?api_token={}&fmt={}'.format(PATH, code, country, TOKEN, self.fmt)
        data = requests.get(url).text
        d = DataFrame(data)
        df = d.create_df('csv')
        return df
        
    def calendar(self, category, ticker=None):
        code = 'calendar'
        categories = ['earnings', 'trends', 'ipos', 'splits']
        if category not in categories:
            return 'Invalid category'
        url = '{}{}/{}?api_token={}&fmt=json'.format(PATH, code, category, TOKEN)
        if ticker != None:
            url += '&symbols={}'.format(ticker)
        url = url + '&from={}&to={}'.format(self.fdate, self.tdate)
        null = 'null'
        data = eval(requests.get(url).text)
        data_cropped = data.get(category)
        d = DataFrame(data_cropped)
        df = d.create_df('dict_list')
        return df
    
    def econ_events(self, country=None):
        code = 'economic-events'
        url = '{}{}?api_token={}&from={}&to={}'.format(PATH, code, TOKEN, self.fdate, self.tdate)
        if country != None:
            url += '&country={}'.format(country)
        null = 'null'
        data = eval(requests.get(url).text)
        d = DataFrame(data)
        df = d.create_df('dict_list')
        return df
            
    def insider(self, ticker=None, limit=100):
        code = 'insider-transactions'
        url = '{}{}?api_token={}&limit={}&from={}&to={}'.format(PATH, code, TOKEN, limit, self.fdate, self.tdate)
        if ticker != None:
            url += '&code={}'.format(ticker)
        null = 'null'
        data = eval(requests.get(url).text)
        d = DataFrame(data)
        df = d.create_df('dict_list')
        return df
            
    def news(self, limit=50, s=None, t=None):
        if s == None and t == None:
            return 'Add either s or t'
        code = 'news'
        url = '{}{}?api_token={}&limit={}&from={}&to={}'.format(PATH, code, TOKEN, limit, self.fdate, self.tdate)
        if s != None:
            url += '&s={}'.format(s)
        elif t != None:
            url += '&t=()'.format(t)
        null = 'null'
        data = eval(requests.get(url).text)
        d = DataFrame(data)
        df = d.create_df('dict_list')
        return df
            
    def macro_indicators(self, country, indicator=None):
        code = 'macro-indicator'
        url = '{}{}/{}?api_token={}&fmt={}'.format(PATH, code, country, TOKEN, self.fmt)
        if indicator != None:
            url += '&indicator={}'.format(indicator)
        data = requests.get(url).text
        d = DataFrame(data)
        df = d.create_df('csv')
        return df

    
# List class
class List:
    def exchanges():
        url = 'https://eodhistoricaldata.com/api/exchanges-list/?api_token={}'.append(TOKEN)
        
    def tickers(exchange):
        url = 'https://eodhistoricaldata.com/api/exchange-symbol-list/{}?api_token={}'.format(exchange, TOKEN)
    
    