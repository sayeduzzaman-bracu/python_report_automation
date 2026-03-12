# Python Report Automation

A Python automation tool that processes raw sales datasets, cleans the
data, generates summary reports, and creates visual business reports
automatically.

The project demonstrates how Python can automate a typical business
reporting workflow by converting raw transaction data into structured
insights and visual reports.

The dataset used in this repository is a publicly available developer
demo dataset.

------------------------------------------------------------------------

## Features

-   Supports multiple input formats
    -   CSV\
    -   TSV\
    -   TXT\
    -   JSON\
    -   XLSX (optional with `openpyxl`)\
-   Automatic column name detection\
-   Cleans and standardizes sales-style datasets\
-   Removes invalid or duplicate records\
-   Generates cleaned CSV output\
-   Generates text summary report\
-   Generates Markdown summary report\
-   Generates SVG charts\
-   Generates HTML visual report\
-   Optional PDF export support

------------------------------------------------------------------------

## Workflow

    Raw Data (input/)
            │
            ▼
    automation.py
    Data Cleaning + Summary Generation
            │
            ▼
    Cleaned Data + Reports (output/)
            │
            ▼
    report_visualizer.py
    Charts + Visual Report

------------------------------------------------------------------------

## Project Structure

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

------------------------------------------------------------------------

## How It Works

### 1. automation.py

This script:

-   scans the `input/` folder
-   detects supported input files
-   maps flexible column names automatically
-   cleans and standardizes the dataset
-   removes invalid or duplicate rows

Outputs generated:

-   `cleaned_sales_data.csv`
-   `sales_summary_report.txt`
-   `sales_summary_report.md`

------------------------------------------------------------------------

### 2. report_visualizer.py

This script reads the cleaned dataset and generates visual outputs.

It:

-   calculates summary metrics
-   generates business charts
-   produces visual reports

Outputs generated:

-   SVG charts
-   HTML visual report
-   optional PDF report

------------------------------------------------------------------------

## Supported Input Types

Base version supports:

-   `.csv`
-   `.tsv`
-   `.txt`
-   `.json`

Optional support:

-   `.xlsx` with `openpyxl`

Invalid or unsupported files return clear error messages instead of
crashing.

------------------------------------------------------------------------

## How to Run

### Step 1 --- Run the automation script

``` bash
python automation.py
```

This generates:

-   cleaned dataset
-   text summary report
-   markdown summary report

------------------------------------------------------------------------

### Step 2 --- Generate charts and visual report

``` bash
python report_visualizer.py
```

This generates:

-   charts
-   HTML visual report
-   optional PDF report

------------------------------------------------------------------------

## Output Files

After running both scripts, the `output/` folder will contain:

-   `cleaned_sales_data.csv`
-   `sales_summary_report.txt`
-   `sales_summary_report.md`
-   `top_products_chart.svg`
-   `category_sales_chart.svg`
-   `city_sales_chart.svg`
-   `monthly_sales_chart.svg`
-   `sales_visual_report.html`

------------------------------------------------------------------------

## Example Use Case

Businesses often export raw sales data from internal systems.\
This project demonstrates how Python automation can transform those raw
files into:

-   cleaned datasets
-   summary reports
-   visual dashboards

automatically.

------------------------------------------------------------------------

## Skills Demonstrated

-   Python scripting
-   data cleaning automation
-   flexible file parsing
-   business reporting automation
-   automated visualization
-   error-safe workflow design

---

## Related Project

If you want to generate automation tools like this instantly, you can use my AI automation assistant:

**.pyLee — Python Automation Engineer Assistant**

This AI agent helps generate practical Python automation scripts for tasks such as:

- data cleaning
- reporting automation
- web scraping
- workflow automation

It is designed to help developers and businesses quickly build automation tools without writing everything from scratch.

🔗 Project link:  
https://github.com/sayeduzzaman-bracu/pyLee-python-automation-assistant

------------------------------------------------------------------------
## Author

**Sayed Uz Zaman**\
Python Automation & AI Agent Developer
