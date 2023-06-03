import pandas as pd
from pandasgui import show
import importlib.util
import sys

from retrieve_data import Stock

s = Stock('AAPL.US')
eod = s.eod()

print(eod)