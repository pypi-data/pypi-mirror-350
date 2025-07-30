import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from scipy.stats import kurtosis, skew

def generate_variable_stats(df, col):
    """Generate detailed statistics for a single variable"""
    stats = {}
    s = df[col].dropna()
    
    # Basic counts
    stats['Distinct'] = s.nunique()
    stats['Distinct (%)'] = (s.nunique() / len(s)) * 100
    stats['Missing'] = df[col].isnull().sum()
    stats['Missing (%)'] = (df[col].isnull().mean()) * 100
    
    # Numeric-specific stats
    if pd.api.types.is_numeric_dtype(s):
        stats['Infinite'] = np.isinf(s).sum()
        stats['Infinite (%)'] = (np.isinf(s).mean()) * 100
        stats['Zeros'] = (s == 0).sum()
        stats['Zeros (%)'] = ((s == 0).mean()) * 100
        stats['Negative'] = (s < 0).sum()
        stats['Negative (%)'] = ((s < 0).mean()) * 100
    else:
        stats['Infinite'] = 'N/A'
        stats['Infinite (%)'] = 'N/A'
        stats['Zeros'] = 'N/A'
        stats['Zeros (%)'] = 'N/A'
        stats['Negative'] = 'N/A'
        stats['Negative (%)'] = 'N/A'
    
    # Memory usage
    stats['Memory size'] = df[col].memory_usage(deep=True)
    
    # Create formatted DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
    
    # Round numeric values
    numeric_cols = stats_df.select_dtypes(include=[np.number]).columns
    stats_df[numeric_cols] = stats_df[numeric_cols].round(2)
    
    return stats_df

def generate_quantile_stats(df, col):
    """Generate quantile statistics for a single variable"""
    s = df[col].dropna()
    stats = {}
    
    if pd.api.types.is_numeric_dtype(s):
        quantiles = s.quantile([0, 0.05, 0.25, 0.5, 0.75, 0.95, 1])
        stats['Minimum'] = quantiles[0]
        stats['5th percentile'] = quantiles[0.05]
        stats['Q1'] = quantiles[0.25]
        stats['Median'] = quantiles[0.5]
        stats['Q3'] = quantiles[0.75]
        stats['95th percentile'] = quantiles[0.95]
        stats['Maximum'] = quantiles[1]
        stats['Range'] = quantiles[1] - quantiles[0]
        stats['IQR'] = quantiles[0.75] - quantiles[0.25]
    else:
        stats['Minimum'] = 'N/A'
        stats['5th percentile'] = 'N/A'
        stats['Q1'] = 'N/A'
        stats['Median'] = 'N/A'
        stats['Q3'] = 'N/A'
        stats['95th percentile'] = 'N/A'
        stats['Maximum'] = 'N/A'
        stats['Range'] = 'N/A'
        stats['IQR'] = 'N/A'
    
    quantile_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
    numeric_cols = quantile_df.select_dtypes(include=[np.number]).columns
    quantile_df[numeric_cols] = quantile_df[numeric_cols].round(2)
    
    return quantile_df

def generate_descriptive_stats(df, col):
    """Generate descriptive statistics for a single variable"""
    s = df[col].dropna()
    stats = {}
    
    if pd.api.types.is_numeric_dtype(s):
        stats['Mean'] = s.mean()
        stats['Standard deviation'] = s.std()
        stats['Coefficient of variation (CV)'] = s.std() / s.mean() if s.mean() != 0 else np.nan
        stats['Kurtosis'] = kurtosis(s)
        stats['Median Absolute Deviation (MAD)'] = (s - s.median()).abs().median()
        stats['Skewness'] = skew(s)
        stats['Sum'] = s.sum()
        stats['Variance'] = s.var()
        stats['Monotonicity'] = (s.diff().dropna() >= 0).all() or (s.diff().dropna() <= 0).all()
    else:
        stats['Mean'] = 'N/A'
        stats['Standard deviation'] = 'N/A'
        stats['Coefficient of variation (CV)'] = 'N/A'
        stats['Kurtosis'] = 'N/A'
        stats['Median Absolute Deviation (MAD)'] = 'N/A'
        stats['Skewness'] = 'N/A'
        stats['Sum'] = 'N/A'
        stats['Variance'] = 'N/A'
        stats['Monotonicity'] = 'N/A'
    
    desc_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
    numeric_cols = desc_df.select_dtypes(include=[np.number]).columns
    desc_df[numeric_cols] = desc_df[numeric_cols].round(2)
    
    return desc_df

def generate_extreme_values_section(df, col):
    """Generate extreme values section with pie charts and tables"""
    if not pd.api.types.is_numeric_dtype(df[col]):
        return ""
    
    # Get top 10 max and min values
    top_max = df[col].value_counts().nlargest(10).reset_index()
    top_max.columns = ['Value', 'Count']
    top_max['Frequency (%)'] = (top_max['Count'] / len(df)) * 100
    top_max = top_max.round(2)
    
    top_min = df[col].value_counts().nsmallest(10).reset_index()
    top_min.columns = ['Value', 'Count']
    top_min['Frequency (%)'] = (top_min['Count'] / len(df)) * 100
    top_min = top_min.round(2)
    
    # Create pie charts
    fig_max = px.pie(top_max, values='Count', names='Value', 
                    title=f'Top 10 Maximum Values: {col}',
                    color_discrete_sequence=px.colors.sequential.Reds_r)
    fig_max.update_layout(plot_bgcolor='white', paper_bgcolor='white', width=350, height=350)
    
    fig_min = px.pie(top_min, values='Count', names='Value', 
                    title=f'Top 10 Minimum Values: {col}',
                    color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_min.update_layout(plot_bgcolor='white', paper_bgcolor='white', width=350, height=350)
    
    # Create HTML section
    extreme_html = f"""
    <div style="margin: 20px 0; page-break-inside: avoid;">
        <h3>Extreme Values Analysis: {col}</h3>
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 350px;">
                {fig_max.to_html(full_html=False, include_plotlyjs='cdn')}
                <div style="margin-top: 10px;">
                    <h4>Top 10 Maximum Values</h4>
                    {top_max.to_html(index=False)}
                </div>
            </div>
            <div style="flex: 1; min-width: 350px;">
                {fig_min.to_html(full_html=False, include_plotlyjs='cdn')}
                <div style="margin-top: 10px;">
                    <h4>Top 10 Minimum Values</h4>
                    {top_min.to_html(index=False)}
                </div>
            </div>
        </div>
    </div>
    """
    return extreme_html

def generate_descriptive_tables(df):
    html_sections = []

    # Extended numeric description
    numeric_df = df.select_dtypes(include='number')
    num_stats = numeric_df.describe(percentiles=[.05, .25, .5, .75, .95]).T
    num_stats['median'] = numeric_df.median()
    num_stats['skew'] = numeric_df.skew()
    num_stats['kurtosis'] = numeric_df.kurtosis()
    num_stats['iqr'] = numeric_df.quantile(0.75) - numeric_df.quantile(0.25)
    num_stats = num_stats.round(2)
    html_sections.append("<h3>🔢 Descriptive Statistics (Numeric)</h3>")
    html_sections.append(num_stats.to_html())

    # Categorical summary
    cat_df = df.select_dtypes(include='object')
    if not cat_df.empty:
        cat_summary = pd.DataFrame({
            "count": cat_df.count(),
            "unique": cat_df.nunique(),
            "top": cat_df.mode().iloc[0],
            "freq": cat_df.apply(lambda x: x.value_counts().iloc[0] if not x.value_counts().empty else None)
        })
        html_sections.append("<h3>🔤 Descriptive Statistics (Categorical)</h3>")
        html_sections.append(cat_summary.to_html())

    return html_sections

def generate_eda_summary(df):
    lines = []
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    lines.append(f"<p><b>Total Rows:</b> {len(df)}</p>")
    lines.append(f"<p><b>Numeric Columns:</b> {len(num_cols)}</p>")
    lines.append(f"<p><b>Categorical Columns:</b> {len(cat_cols)}</p>")
    lines.append(f"<p><b>Total Missing Values:</b> {df.isnull().sum().sum()}</p>")
    lines.append(f"<p><b>Duplicate Rows:</b> {df.duplicated().sum()}</p>")

    missing_percent = df.isnull().mean() * 100
    missing_table = missing_percent[missing_percent > 0].round(1).to_frame(name="Missing (%)")
    if not missing_table.empty:
        lines.append("<h4>Feature-wise Missing %</h4>")
        lines.append(missing_table.to_html())

    corr = df[num_cols].corr()
    high_corr_pairs = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))
        .stack()
        .reset_index()
        .rename(columns={0: "Corr"})
        .query("abs(Corr) > 0.9 and abs(Corr) < 1.0")
    )
    if not high_corr_pairs.empty:
        lines.append("<h4>⚠️ Highly Correlated Features (|r| > 0.9)</h4>")
        lines.append(high_corr_pairs.rename(columns={0: "Correlation"}).to_html(index=False))

    return "".join(lines)

def generate_univariate_plots(df):
    figs = []
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        # Generate statistics table for this variable
        stats_df = generate_variable_stats(df, col)
        stats_html = stats_df.to_html()
        
        # Create histogram with adjusted width
        fig = px.histogram(df, x=col, nbins=30, title=f"Histogram of {col}",
                         color_discrete_sequence=['#1f77b4'])
        fig.update_traces(marker_line_color='white', marker_line_width=0.5)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=500,
            height=400
        )
        
        # Combine histogram and stats in one HTML block
        combined_html = f"""
        <div style="display: flex; gap: 20px; margin-bottom: 30px; align-items: flex-start; page-break-inside: avoid;">
            <div style="flex: 1; min-width: 500px;">
                {fig.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div style="flex: 1; min-width: 0; overflow-x: auto;">
                <h4>Variable Statistics for {col}</h4>
                {stats_html}
            </div>
        </div>
        """
        figs.append(combined_html)

        # Generate quantile and descriptive stats
        quantile_df = generate_quantile_stats(df, col)
        desc_df = generate_descriptive_stats(df, col)
        
        # Create boxplot with reduced width
        fig = px.box(df, y=col, title=f"Boxplot of {col}", color_discrete_sequence=['#1f77b4'])
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=350,
            height=400
        )
        
        # Combine boxplot with stats tables
        boxplot_html = f"""
        <div style="display: flex; gap: 20px; margin-bottom: 30px; align-items: flex-start; page-break-inside: avoid;">
            <div style="flex: 0.5; min-width: 350px;">
                {fig.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div style="flex: 1; display: flex; gap: 20px;">
                <div style="flex: 1; min-width: 0; overflow-x: auto;">
                    <h4>Quantile Statistics for {col}</h4>
                    {quantile_df.to_html()}
                </div>
                <div style="flex: 1; min-width: 0; overflow-x: auto;">
                    <h4>Descriptive Statistics for {col}</h4>
                    {desc_df.to_html()}
                </div>
            </div>
        </div>
        """
        figs.append(boxplot_html)
        
        # Add extreme values section
        figs.append(generate_extreme_values_section(df, col))

    return figs

def generate_categorical_plots(df):
    figs = []
    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:
        vc = df[col].value_counts().nlargest(10)
        fig = px.bar(x=vc.index, y=vc.values, labels={'x': col, 'y': 'Count'}, 
                     title=f"Top Categories: {col}", color_discrete_sequence=['#2ca02c'])
        fig.update_layout(
            xaxis_tickangle=45, 
            plot_bgcolor='white', 
            paper_bgcolor='white',
            width=700,
            height=400
        )
        figs.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

        freq_table_html = vc.to_frame().to_html()
        figs.append(f"<div style='page-break-inside: avoid;'><h4>Frequency Table for {col}</h4>{freq_table_html}<br><br></div>")

    return figs

def generate_missing_value_plot(df):
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if null_counts.empty:
        return ["<p>No missing values in dataset.</p>"]

    fig = px.bar(x=null_counts.index, y=null_counts.values,
                 labels={"x": "Column", "y": "Missing Count"},
                 title="Missing Value Count per Column",
                 color_discrete_sequence=['#d62728'])
    fig.update_layout(
        xaxis_tickangle=45, 
        plot_bgcolor='white', 
        paper_bgcolor='white',
        width=700,
        height=400
    )
    return [fig.to_html(full_html=False, include_plotlyjs='cdn')]

def generate_bivariate_plots(df):
    figs = []
    numeric_cols = df.select_dtypes(include='number').columns
    corr = df[numeric_cols].corr().round(2)

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis'
    ))
    heatmap.update_layout(
        title="Correlation Heatmap", 
        plot_bgcolor='white', 
        paper_bgcolor='white',
        width=700,
        height=600
    )
    figs.append(heatmap.to_html(full_html=False, include_plotlyjs='cdn'))

    correlated_pairs = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))
        .stack()
        .reset_index()
        .rename(columns={"level_0": "Var1", "level_1": "Var2", 0: "Corr"})
    )
    top_pairs = correlated_pairs[correlated_pairs["Corr"].abs() > 0.7].sort_values(by="Corr", ascending=False)
    seen = set()
    for _, row in top_pairs.iterrows():
        pair = tuple(sorted((row["Var1"], row["Var2"])))
        if pair in seen:
            continue
        seen.add(pair)
        fig = px.scatter(df, x=row["Var1"], y=row["Var2"], trendline="ols",
                         title=f"Scatter: {row['Var1']} vs {row['Var2']} (Corr={row['Corr']:.2f})",
                         color_discrete_sequence=['#9467bd'])
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            width=700,
            height=500
        )
        figs.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    return figs

def create_report_html(summary_html, desc_html, eda_html, plots_html, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Analysis Report</title>
            <meta charset="utf-8">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                @page {{
                    size: A4;
                    margin: 1cm;
                }}
                body {{
                    font-family: Arial; 
                    padding: 20px; 
                    max-width: 1000px; 
                    margin: auto;
                    font-size: 12px;
                }}
                h1 {{ font-size: 18px; color: #2c3e50; }}
                h2 {{ font-size: 16px; color: #2c3e50; }}
                h3 {{ font-size: 14px; color: #2c3e50; }}
                h4 {{ font-size: 12px; color: #2c3e50; }}
                .plot-container {{
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                }}
                .button-bar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: white;
                    padding: 10px 20px;
                    border-bottom: 1px solid #ccc;
                    z-index: 999;
                    display: flex;
                    justify-content: start;
                    gap: 10px;
                }}
                .button-bar button {{
                    padding: 8px 15px;
                    font-size: 12px;
                    border: none;
                    border-radius: 5px;
                    background-color: #3498db;
                    color: white;
                    cursor: pointer;
                }}
                .content-wrapper {{
                    margin-top: 60px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 15px;
                    font-size: 11px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 6px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .stats-container {{
                    display: flex;
                    gap: 15px;
                    margin-bottom: 20px;
                    align-items: flex-start;
                    page-break-inside: avoid;
                }}
                .plot-wrapper {{
                    flex: 1;
                    min-width: 0;
                }}
                .stats-wrapper {{
                    flex: 1;
                    min-width: 0;
                    overflow-x: auto;
                }}
                .extreme-values-container {{
                    display: flex;
                    gap: 15px;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                    page-break-inside: avoid;
                }}
                .extreme-values-box {{
                    flex: 1;
                    min-width: 350px;
                }}
                @media print {{
                    .button-bar {{
                        display: none;
                    }}
                    body {{
                        padding: 0;
                    }}
                }}
            </style>
        </head>
        <body>
        <div class="button-bar">
            <button onclick="window.print()">🖨 Export PDF</button>
            <button onclick="displayAll()">👁 Display All</button>
        </div>

        <div class="content-wrapper">
            <h1>📊 Data Profiling Report</h1>


            <h1>&nbsp;</h1>
            <div class="plot-block" id="block-summary" style="margin-bottom: 30px;">
                <div class="plot-controls">
                    <input type="checkbox" id="checkbox-summary" class="plot-checkbox" checked onchange="toggleBlock('block-summary', this)">
                    <label for="checkbox-summary">Include Summary Statistics Table</label>
                </div>
                <div id="summary-content">
                    <h2>Summary Statistics</h2>
                    {summary_html}
                </div>
            </div>


            <h1>&nbsp;</h1>
            <div class="plot-block" id="block-desc" style="margin-bottom: 30px;">
                <div class="plot-controls">
                    <input type="checkbox" id="checkbox-desc" class="plot-checkbox" checked onchange="toggleBlock('block-desc', this)">
                    <label for="checkbox-desc">Include Descriptive Statistics Section</label>
                </div>
                <div id="desc-section">
                    <h2>Descriptive Statistics</h2>
                    <div id="desc-content">
                        {''.join(desc_html)}
                    </div>
                </div>
            </div>

            <h1>&nbsp;</h1>
            <div class="plot-block" id="block-eda" style="margin-bottom: 30px;">
                <div class="plot-controls">
                    <input type="checkbox" id="checkbox-eda" class="plot-checkbox" checked onchange="toggleBlock('block-eda', this)">
                    <label for="checkbox-eda">Include EDA Summary</label>
                </div>
                <div id="eda-content">
                    <h2>Exploratory Data Analysis</h2>
                    {eda_html}
                </div>
            </div>
        

            <hr style="margin: 20px 0;">




            <!-- All other plots -->
            {"".join(
                f'''
                <div class="plot-block" id="block-{i}">
                    <div class="plot-controls">
                        <input type="checkbox" id="checkbox-{i}" class="plot-checkbox" checked onchange="toggleBlock('block-{i}', this)">
                        <label for="checkbox-{i}">Include this section</label>
                    </div>
                    <div class="plot">{plot}</div>
                </div>
                ''' for i, plot in enumerate(plots_html)
            )}
        </div>



<script>
function toggleBlock(blockId, checkbox) {{
    const block = document.getElementById(blockId);
    if (!block) return;

    if (checkbox.checked) {{
        block.style.display = 'block';
    }} else {{
        block.style.display = 'none';
    }}
}}

function displayAll() {{
    document.querySelectorAll('.plot-block').forEach(el => {{
        el.style.display = 'block';
    }});
    document.querySelectorAll('.plot-checkbox').forEach(cb => cb.checked = true);
}}
</script>
        </body>
        </html>
        """)

def generate_report_from_excel(excel_path, output_html="report.html", output_pdf="report.pdf"):
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"❌ Failed to read Excel file: {e}")
        return

    numeric_cols = df.select_dtypes(include='number').columns
    summary_stats = df[numeric_cols].describe(percentiles=[.05, .25, .5, .75, .95]).transpose().round(2)
    summary_html = summary_stats.to_html(classes="summary", border=0)
    eda_html = generate_eda_summary(df)
    desc_html = generate_descriptive_tables(df)
    plots = []
    plots += generate_missing_value_plot(df)
    plots += generate_univariate_plots(df)
    plots += generate_categorical_plots(df)
    plots += generate_bivariate_plots(df)

    create_report_html(summary_html, desc_html, eda_html, plots, output_html)
    print(f"✅ Report saved to {output_html}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate full manual data report")
    parser.add_argument("excel_path", help="Path to Excel file")
    parser.add_argument("--out_html", default="report.html", help="HTML output path")
    parser.add_argument("--out_pdf", default="report.pdf", help="PDF output path")
    args = parser.parse_args()

    generate_report_from_excel(args.excel_path, args.out_html, args.out_pdf)
