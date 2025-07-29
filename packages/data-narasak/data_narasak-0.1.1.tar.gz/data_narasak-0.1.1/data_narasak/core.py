from . import extract, transform, visualize, report

class data_narasak:
    def __init__(self):
        self.df = None

    def load_data(self, filepath):
        if filepath.endswith('.csv'):
            self.df = extract.load_csv(filepath)
        elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            self.df = extract.load_excel(filepath)
        elif filepath.endswith('.json'):
            self.df = extract.load_json(filepath)
        else:
            raise ValueError('Unsupported file format.')

    def fill_missing(self, method='mean'):
        self.df = transform.fill_missing(self.df, method)

    def drop_duplicates(self):
        self.df = transform.drop_duplicates(self.df)

    def encode_categorical(self, columns):
        self.df = transform.encode_categorical(self.df, columns)

    def scale_columns(self, columns):
        self.df = transform.scale_columns(self.df, columns)

    def summary(self):
        return self.df.describe()

    def generate_pdf_report(self, filename='report.pdf'):
        plot_funcs = []

        # Add some example plots if columns exist
        if 'age' in self.df.columns:
            plot_funcs.append((visualize.plot_histogram_save, [self.df, 'age'], {'title':'Age Distribution Histogram'}))
        if 'income' in self.df.columns:
            plot_funcs.append((visualize.plot_boxplot_save, [self.df, 'income'], {'title':'Income Boxplot'}))
        if 'age' in self.df.columns and 'income' in self.df.columns:
            plot_funcs.append((visualize.plot_scatter_save, [self.df, 'age', 'income'], {'title':'Age vs Income Scatter'}))
            plot_funcs.append((visualize.plot_line_save, [self.df, 'age', 'income'], {'title':'Age vs Income Lineplot'}))
        if 'gender' in self.df.columns:
            plot_funcs.append((visualize.plot_bar_save, [self.df, 'gender'], {'title':'Gender Barplot'}))
        
        plot_funcs.append((visualize.plot_heatmap_save, [self.df], {'title':'Correlation Heatmap'}))

        pdf_report = report.PDFReport(self.df)
        pdf_report.generate_report(filename, plot_funcs)
