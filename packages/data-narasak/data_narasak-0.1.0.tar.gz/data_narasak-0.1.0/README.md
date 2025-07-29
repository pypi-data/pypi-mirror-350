# Data Analysis & Transformation PDF Report Generator

A powerful Python toolkit for performing data transformations on tabular datasets and generating detailed, well-formatted PDF reports. Designed for data analysts, scientists, and engineers, this tool streamlines data preprocessing, exploratory analysis, and documentation by integrating transformation functions, visualizations, and report generation in one package.

---

## 📌 Features

- **Multi-format data loading:** Supports CSV, Excel (`.xlsx`, `.xls`), and JSON files.
- **Flexible data transformations:** Normalization, log transformation, categorical encoding, and more.
- **Comprehensive PDF reports:** Include dataset overview, data types, summary statistics, missing and unique values, correlation matrices, data previews, transformed data insights, and before-after comparisons.
- **Dynamic plot integration:** Optional inclusion of plots like histograms, boxplots, scatterplots, bar charts, and heatmaps.
- **Professional PDF formatting:** Powered by ReportLab with support for pagination, text formatting, and image embedding.
- **Automated cleanup:** Temporary plot images are removed after embedding to keep your workspace tidy.
- **Extensible modular design:** Easy to customize and extend with your own transformations and visualizations.

---

## 🚀 Installation

Install dependencies via pip:

```bash
pip install pandas reportlab matplotlib numpy openpyxl
