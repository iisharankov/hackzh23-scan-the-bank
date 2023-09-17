# Python script for xlsx

import pandas as pd
import re
from modules import csv

from const import *

def is_sensitive(filename, detector = None): 
    df = pd.read_excel(filename, nrows = 20)
    return csv.check_is_sensitive(df, filename)