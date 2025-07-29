from data_narasak.core import data_narasak
import pandas as pd

def main():
    # Create sample CSV data for testing
    sample_data = {
        'age': [25, 30, 22, None, 40, 35, 28],
        'income': [50000, 60000, 45000, 52000, None, 62000, 58000],
        'gender': ['M', 'F', 'F', 'M', 'M', 'F', 'F']
    }

    # Save sample CSV file
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('sample_test.csv', index=False)

    # Initialize data_narasak instance
    dt = data_narasak()

    # Load data
    dt.load_data('sample_test.csv')
    print("Data loaded:\n", dt.df)

    # Fill missing values with mean
    dt.fill_missing(method='mean')
    print("After filling missing values:\n", dt.df)

    # Drop duplicates (none here but just test)
    dt.drop_duplicates()
    print("After dropping duplicates:\n", dt.df)

    # Encode categorical column 'gender'
    dt.encode_categorical(['gender'])
    print("After encoding categorical column 'gender':\n", dt.df)

    # Scale numeric columns 'age' and 'income'
    dt.scale_columns(['age', 'income'])
    print("After scaling columns:\n", dt.df)

    # Show summary stats
    print("Summary statistics:\n", dt.summary())

    # Generate PDF report with plots
    dt.generate_pdf_report(filename='core_test_report.pdf')
    print("PDF report 'core_test_report.pdf' generated.")

if __name__ == "__main__":
    main()
