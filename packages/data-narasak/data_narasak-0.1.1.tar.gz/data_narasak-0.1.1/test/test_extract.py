import pandas as pd
from data_narasak.extract import *

print("Testing extract module...")

# Sample CSV
df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
df.to_csv('test.csv', index=False)

loaded_df = load_csv('test.csv')
print("Loaded DataFrame:")
print(loaded_df)
