# Macro Economic Indicators Normalization Logic
import pandas as pd

def normalize_inflation(cpi_series):
    return cpi_series.pct_change()
