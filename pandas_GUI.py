# Load packages
import pandas as pd
from pandasgui import show

# Datasets
df = pd.DataFrame(([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
show(df)

# Download all the sample datasets
from pandasgui.datasets import pokemon, titanic, all_datasets

# Show all the datasets
show(**all_datasets)
