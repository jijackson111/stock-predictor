import pandas as pd
from pandasgui import show
import importlib.util
import sys

from retrieve_data import Market

m = Market()
ip = m.calendar('ipos')
print(ip)