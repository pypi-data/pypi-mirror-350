import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import warnings

def _save_plot_temp(fig):
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig.savefig(tmp.name, bbox_inches='tight')
    plt.close(fig)
    return tmp.name

def plot_histogram_save(df, column, title=None):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if df[column].dropna().empty:
        raise ValueError(f"No valid data in column '{column}' for histogram.")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(df[column].dropna(), kde=True, ax=ax)
    ax.set_title(title or f'Histogram of {column}')
    return _save_plot_temp(fig)

def plot_boxplot_save(df, column, title=None):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if df[column].dropna().empty:
        raise ValueError(f"No valid data in column '{column}' for boxplot.")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(x=df[column].dropna(), ax=ax)
    ax.set_title(title or f'Boxplot of {column}')
    return _save_plot_temp(fig)

def plot_scatter_save(df, x_col, y_col, title=None):
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Columns '{x_col}' and/or '{y_col}' not found in DataFrame.")
    if df[[x_col, y_col]].dropna().empty:
        raise ValueError(f"No valid data in columns '{x_col}' and '{y_col}' for scatter plot.")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    ax.set_title(title or f'Scatter plot: {x_col} vs {y_col}')
    return _save_plot_temp(fig)

def plot_line_save(df, x_col, y_col, title=None):
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Columns '{x_col}' and/or '{y_col}' not found in DataFrame.")
    if df[[x_col, y_col]].dropna().empty:
        raise ValueError(f"No valid data in columns '{x_col}' and '{y_col}' for line plot.")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
    ax.set_title(title or f'Line plot: {x_col} vs {y_col}')
    return _save_plot_temp(fig)

def plot_bar_save(df, x_col, y_col=None, title=None):
    if x_col not in df.columns:
        raise ValueError(f"Column '{x_col}' not found in DataFrame.")
    if y_col and y_col not in df.columns:
        raise ValueError(f"Column '{y_col}' not found in DataFrame.")
    if y_col:
        if df[[x_col, y_col]].dropna().empty:
            raise ValueError(f"No valid data in columns '{x_col}' and '{y_col}' for bar plot.")
    else:
        if df[x_col].dropna().empty:
            raise ValueError(f"No valid data in column '{x_col}' for bar plot.")
    fig, ax = plt.subplots(figsize=(8,5))
    if y_col:
        sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        ax.set_title(title or f'Bar plot: {x_col} vs {y_col}')
    else:
        sns.countplot(data=df, x=x_col, ax=ax)
        ax.set_title(title or f'Bar plot: {x_col}')
    return _save_plot_temp(fig)

def plot_heatmap_save(df, title=None):
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        raise ValueError("DataFrame has no numeric columns for correlation heatmap.")
    corr = numeric_df.corr()
    if corr.empty:
        raise ValueError("Correlation matrix is empty; cannot plot heatmap.")
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title(title or 'Correlation Heatmap')
    return _save_plot_temp(fig)
