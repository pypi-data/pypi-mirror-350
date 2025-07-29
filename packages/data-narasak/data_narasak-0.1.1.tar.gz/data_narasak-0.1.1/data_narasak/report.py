from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class PDFReport:
    def __init__(self, df):
        self.df = df

    def generate_report(self, filename='report.pdf', plot_funcs=None):
        width, height = letter
        margin = 40
        y = height - margin
        line_height = 12

        c = canvas.Canvas(filename, pagesize=letter)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y, "Data Analysis Report")
        y -= 40

        # Helper to add multiline text with page breaks
        def add_text_block(text, font="Helvetica", font_size=9):
            nonlocal y
            c.setFont(font, font_size)
            for line in text.split('\n'):
                if y < margin + 50:
                    c.showPage()
                    y = height - margin
                    c.setFont(font, font_size)
                c.drawString(margin, y, line)
                y -= line_height

        # 1. Dataset Overview
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "1. Dataset Overview")
        y -= 20
        add_text_block(f"The dataset contains {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        y -= 10

        # 2. Data Types
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "2. Data Types")
        y -= 20
        add_text_block("Data types of each column:")
        add_text_block(self.df.dtypes.astype(str).to_string())
        y -= 10

        # 3. Summary Statistics
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "3. Summary Statistics")
        y -= 20
        add_text_block("Descriptive statistics for numeric columns:")
        add_text_block(self.df.describe().round(2).astype(str).to_string())
        y -= 10

        # 4. Unique Values Count
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "4. Unique Values Count")
        y -= 20
        add_text_block("Count of unique values per column:")
        add_text_block(self.df.nunique().to_string())
        y -= 10

        # 5. Missing Values Count
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "5. Missing Values Count")
        y -= 20
        add_text_block("Number of missing values per column:")
        add_text_block(self.df.isnull().sum().to_string())
        y -= 10

        # 6. Correlation Matrix (show top 5 cols only to save space)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "6. Correlation Matrix (Top 5 columns)")
        y -= 20
        corr = self.df.select_dtypes(include=['number']).corr().round(2)
        # Get first 5 rows and cols only for brevity
        corr_snippet = corr.iloc[:5, :5].to_string()
        add_text_block("Pearson correlation coefficients:")
        add_text_block(corr_snippet)
        y -= 10

        # 7. Data Sample Preview (First 5 rows)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "7. Sample Data (First 5 Rows)")
        y -= 20
        add_text_block("Preview of first five rows of the dataset:")
        add_text_block(self.df.head().to_string())
        y -= 10

        # 8. Plots (if any)
        if plot_funcs:
            for plot_func, args, kwargs in plot_funcs:
                img_path = plot_func(*args, **kwargs)

                c.showPage()
                y = height - margin

                c.setFont("Helvetica-Bold", 14)
                title = kwargs.get('title', 'Plot')
                c.drawString(margin, y, title)
                y -= 30

                img = ImageReader(img_path)
                img_width, img_height = img.getSize()

                max_width = width - 2 * margin
                scale = max_width / img_width
                img_width = int(img_width * scale)
                img_height = int(img_height * scale)

                c.drawImage(img, margin, y - img_height, width=img_width, height=img_height)

                y -= img_height + 20

                if os.path.exists(img_path):
                    os.remove(img_path)

        c.save()
