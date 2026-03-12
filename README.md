# Python Report Automation

A Python automation project that reads raw business sales data, cleans it, generates summary reports, and creates visual report outputs automatically.

This project was tested on a real publicly available developer demo dataset.

## Features

- Supports multiple common input formats
  - CSV
  - TSV
  - TXT
  - JSON
  - XLSX (optional if `openpyxl` is installed)
- Detects flexible column names automatically
- Cleans and standardizes sales-style tabular data
- Removes invalid and duplicate rows
- Generates cleaned CSV export
- Generates text summary report
- Generates Markdown summary report
- Generates SVG charts
- Generates HTML visual report
- Optional PDF summary if `reportlab` is installed

## Project Structure

```text
python-report-automation/
│
├── input/
│   └── retail_sales_data - Sheet1.csv
│
├── output/
│   ├── cleaned_sales_data.csv
│   ├── sales_summary_report.txt
│   ├── sales_summary_report.md
│   ├── top_products_chart.svg
│   ├── category_sales_chart.svg
│   ├── city_sales_chart.svg
│   ├── monthly_sales_chart.svg
│   └── sales_visual_report.html
│
├── automation.py
├── report_visualizer.py
├── requirements.txt
├── README.md
└── .gitignore
