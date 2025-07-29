import pandas as pd
from data_narasak.transform import fill_missing, drop_duplicates, encode_categorical, scale_columns

# Sample DataFrame
data = {
    'age': [25, None, 35, 25],
    'gender': ['Male', 'Female', 'Female', 'Male'],
    'salary': [50000, 60000, None, 50000]
}
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# 1. Test fill_missing
df_filled = fill_missing(df, method='mean')
print("\nAfter fill_missing (mean):")
print(df_filled)

# 2. Test drop_duplicates
df_deduped = drop_duplicates(df_filled)
print("\nAfter drop_duplicates:")
print(df_deduped)

# 3. Test encode_categorical
df_encoded = encode_categorical(df_deduped, columns=['gender'])
print("\nAfter encode_categorical (gender):")
print(df_encoded)

# 4. Test scale_columns
df_scaled = scale_columns(df_encoded, columns=['age', 'salary'])
print("\nAfter scale_columns (age, salary):")
print(df_scaled)
