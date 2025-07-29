import pandas as pd
from data_narasak.report import PDFReport
from data_narasak.visualize import plot_histogram_save, plot_boxplot_save

# Sample DataFrame for testing
df = pd.DataFrame({
    'new': [23, 45, 31, None, 22, 34, 42],
    'salary': [50000, 60000, 55000, 58000, None, 61000, 57000],
    'department': ['HR', 'IT', 'HR', 'IT', 'Marketing', 'Marketing', 'HR']
})

# Initialize PDFReport
report = PDFReport(df)

# Define plots to include in report as tuples: (plot_function, args, kwargs)
plots_to_include = [
    (plot_histogram_save, (df, 'new'), {'title': 'New Distribution'}),
    (plot_boxplot_save, (df, 'salary'), {'title': 'Salary Boxplot'}),
]

# Generate PDF report
report.generate_report(filename='test_report.pdf', plot_funcs=plots_to_include)

print("Report 'test_report.pdf' generated successfully.")
