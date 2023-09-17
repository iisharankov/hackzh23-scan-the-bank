# Python script for db

import sqlite3
import pandas as pd

from const import *

def is_sensitive(filename, detector = None):

    con = sqlite3.connect(filename)

    table_names = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
    df = pd.read_sql('SELECT * FROM ' + table_names.loc[0][0], con)

    header_sensitive = [col for col in df.columns if col in SENSITIVE_HEADERS]
    df_sensitive = df[header_sensitive]

    entries = ~(df_sensitive.applymap(lambda x: isinstance(x, str) and x.strip() == '')) | (df_sensitive.isnull())
    has_multiple_sensitive = any(entries.sum(axis=1) > 1)

    return has_multiple_sensitive