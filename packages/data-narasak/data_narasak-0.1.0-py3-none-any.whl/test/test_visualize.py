import pandas as pd
from data_narasak.visualize import *

# Sample DataFrame
df = pd.DataFrame({
    'age': [23, 45, 31, 35, 22, 34, 42],
    'salary': [50000, 60000, 55000, 58000, 52000, 61000, 57000],
    'department': ['HR', 'IT', 'HR', 'IT', 'Marketing', 'Marketing', 'HR']
})

print("Testing plot_histogram_save:")
path = plot_histogram_save(df, 'age')
print(f"Histogram saved to: {path}")

print("\nTesting plot_boxplot_save:")
path = plot_boxplot_save(df, 'salary')
print(f"Boxplot saved to: {path}")

print("\nTesting plot_scatter_save:")
path = plot_scatter_save(df, 'age', 'salary')
print(f"Scatter plot saved to: {path}")

print("\nTesting plot_line_save:")
path = plot_line_save(df, 'age', 'salary')
print(f"Line plot saved to: {path}")

print("\nTesting plot_bar_save (with y_col):")
path = plot_bar_save(df, 'department', 'salary')
print(f"Bar plot (with y_col) saved to: {path}")

print("\nTesting plot_bar_save (without y_col):")
path = plot_bar_save(df, 'department')
print(f"Bar plot (count) saved to: {path}")

print("\nTesting plot_heatmap_save:")
path = plot_heatmap_save(df)
print(f"Heatmap saved to: {path}")
