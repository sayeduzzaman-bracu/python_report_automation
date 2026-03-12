from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv
import html
import re


# --------------------------------------------------
# OPTIONAL PDF SUPPORT
# --------------------------------------------------

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def ensure_folder(folder_path: Path) -> None:
    folder_path.mkdir(parents=True, exist_ok=True)


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_float(value) -> float:
    text = clean_text(value).replace(",", "")
    if text == "":
        return 0.0
    return float(text)


def safe_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_").lower()


# --------------------------------------------------
# LOAD CLEANED CSV
# --------------------------------------------------

def load_cleaned_sales_data(csv_file: Path) -> list[dict]:
    if not csv_file.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {csv_file}\n"
            "Run automation.py first."
        )

    rows = []
    with csv_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for raw_row in reader:
            try:
                row = {
                    "order_id": clean_text(raw_row.get("order_id")),
                    "order_date": clean_text(raw_row.get("order_date")),
                    "customer_name": clean_text(raw_row.get("customer_name")),
                    "product": clean_text(raw_row.get("product")),
                    "category": clean_text(raw_row.get("category")),
                    "quantity": parse_float(raw_row.get("quantity")),
                    "unit_price": parse_float(raw_row.get("unit_price")),
                    "city": clean_text(raw_row.get("city")),
                    "revenue": parse_float(raw_row.get("revenue")),
                    "month": clean_text(raw_row.get("month")),
                }
                rows.append(row)
            except ValueError:
                continue

    if not rows:
        raise ValueError("Cleaned CSV exists but contains no valid rows.")

    return rows


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

def generate_summary(rows: list[dict]) -> dict:
    total_orders = len({row["order_id"] for row in rows})
    total_units_sold = sum(row["quantity"] for row in rows)
    total_revenue = sum(row["revenue"] for row in rows)

    revenue_by_order = defaultdict(float)
    revenue_by_product = defaultdict(float)
    revenue_by_category = defaultdict(float)
    revenue_by_city = defaultdict(float)
    revenue_by_month = defaultdict(float)

    for row in rows:
        revenue_by_order[row["order_id"]] += row["revenue"]
        revenue_by_product[row["product"]] += row["revenue"]
        revenue_by_category[row["category"]] += row["revenue"]
        revenue_by_city[row["city"]] += row["revenue"]
        revenue_by_month[row["month"]] += row["revenue"]

    average_order_value = (
        sum(revenue_by_order.values()) / len(revenue_by_order)
        if revenue_by_order else 0.0
    )

    top_products = sorted(
        revenue_by_product.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    top_categories = sorted(
        revenue_by_category.items(),
        key=lambda item: item[1],
        reverse=True
    )

    sales_by_city = sorted(
        revenue_by_city.items(),
        key=lambda item: item[1],
        reverse=True
    )

    monthly_sales = sorted(
        revenue_by_month.items(),
        key=lambda item: item[0]
    )

    return {
        "total_orders": total_orders,
        "total_units_sold": total_units_sold,
        "total_revenue": total_revenue,
        "average_order_value": average_order_value,
        "top_products": top_products,
        "top_categories": top_categories,
        "sales_by_city": sales_by_city,
        "monthly_sales": monthly_sales,
    }


# --------------------------------------------------
# SIMPLE SVG BAR CHART GENERATOR
# --------------------------------------------------

def create_svg_bar_chart(
    title: str,
    items: list[tuple[str, float]],
    output_file: Path,
    width: int = 900,
    bar_height: int = 38,
    left_margin: int = 220,
    right_margin: int = 120,
    top_margin: int = 70,
    bottom_margin: int = 40,
) -> None:
    if not items:
        output_file.write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>", encoding="utf-8")
        return

    max_value = max(value for _, value in items) if items else 1
    chart_width = width - left_margin - right_margin
    height = top_margin + bottom_margin + len(items) * (bar_height + 12)

    svg_lines = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='white'/>",
        f"<text x='{left_margin}' y='35' font-size='24' font-family='Arial' font-weight='bold'>{html.escape(title)}</text>",
    ]

    y = top_margin
    for label, value in items:
        bar_width = 0
        if max_value > 0:
            bar_width = (value / max_value) * chart_width

        safe_label = html.escape(str(label))
        safe_value = html.escape(f"{value:,.2f}")

        svg_lines.append(
            f"<text x='20' y='{y + 24}' font-size='15' font-family='Arial'>{safe_label}</text>"
        )
        svg_lines.append(
            f"<rect x='{left_margin}' y='{y}' width='{bar_width:.2f}' height='{bar_height}' rx='6' ry='6' fill='#4F81BD'/>"
        )
        svg_lines.append(
            f"<text x='{left_margin + bar_width + 10:.2f}' y='{y + 24}' font-size='15' font-family='Arial'>{safe_value}</text>"
        )
        y += bar_height + 12

    svg_lines.append("</svg>")
    output_file.write_text("\n".join(svg_lines), encoding="utf-8")


# --------------------------------------------------
# HTML REPORT
# --------------------------------------------------

def build_html_report(summary: dict, output_file: Path) -> None:
    top_products_html = "\n".join(
        f"<li><strong>{html.escape(name)}</strong>: {value:,.2f}</li>"
        for name, value in summary["top_products"]
    )

    category_html = "\n".join(
        f"<li><strong>{html.escape(name)}</strong>: {value:,.2f}</li>"
        for name, value in summary["top_categories"]
    )

    city_html = "\n".join(
        f"<li><strong>{html.escape(name)}</strong>: {value:,.2f}</li>"
        for name, value in summary["sales_by_city"]
    )

    month_html = "\n".join(
        f"<li><strong>{html.escape(name)}</strong>: {value:,.2f}</li>"
        for name, value in summary["monthly_sales"]
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sales Visual Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            color: #222;
            background: #fafafa;
        }}
        .container {{
            max-width: 1100px;
            margin: auto;
            background: white;
            padding: 32px;
            border-radius: 14px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        }}
        h1 {{
            margin-bottom: 10px;
        }}
        h2 {{
            margin-top: 36px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 8px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(2, minmax(220px, 1fr));
            gap: 16px;
            margin: 24px 0 20px 0;
        }}
        .card {{
            background: #f4f7fb;
            padding: 18px;
            border-radius: 12px;
        }}
        .label {{
            font-size: 13px;
            color: #555;
            margin-bottom: 6px;
        }}
        .value {{
            font-size: 24px;
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 10px;
            background: white;
            margin-top: 12px;
        }}
        ul {{
            line-height: 1.8;
        }}
        .footer {{
            margin-top: 40px;
            color: #666;
            font-size: 13px;
        }}
        @media print {{
            body {{
                background: white;
                margin: 0;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
                max-width: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Sales Visual Report</h1>
        <p>Generated from <code>cleaned_sales_data.csv</code></p>

        <div class="metrics">
            <div class="card">
                <div class="label">Total Orders</div>
                <div class="value">{summary['total_orders']}</div>
            </div>
            <div class="card">
                <div class="label">Total Units Sold</div>
                <div class="value">{summary['total_units_sold']:.2f}</div>
            </div>
            <div class="card">
                <div class="label">Total Revenue</div>
                <div class="value">{summary['total_revenue']:,.2f}</div>
            </div>
            <div class="card">
                <div class="label">Average Order Value</div>
                <div class="value">{summary['average_order_value']:,.2f}</div>
            </div>
        </div>

        <h2>Top Products by Revenue</h2>
        <img src="top_products_chart.svg" alt="Top products chart">
        <ul>
            {top_products_html}
        </ul>

        <h2>Category Sales</h2>
        <img src="category_sales_chart.svg" alt="Category sales chart">
        <ul>
            {category_html}
        </ul>

        <h2>City / Location Sales</h2>
        <img src="city_sales_chart.svg" alt="City sales chart">
        <ul>
            {city_html}
        </ul>

        <h2>Monthly Sales</h2>
        <img src="monthly_sales_chart.svg" alt="Monthly sales chart">
        <ul>
            {month_html}
        </ul>

        <div class="footer">
            This report was generated automatically by report_visualizer.py
        </div>
    </div>
</body>
</html>
"""
    output_file.write_text(html_content, encoding="utf-8")


# --------------------------------------------------
# OPTIONAL PDF
# --------------------------------------------------

def create_pdf_report(summary: dict, output_file: Path) -> bool:
    if not REPORTLAB_AVAILABLE:
        return False

    c = canvas.Canvas(str(output_file), pagesize=A4)
    width, height = A4

    y = height - 20 * mm

    def draw_line(text: str, size: int = 11, gap: float = 7):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(20 * mm, y, text[:110])
        y -= gap * mm
        if y < 20 * mm:
            c.showPage()
            y = height - 20 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "Sales PDF Summary")
    y -= 12 * mm

    draw_line(f"Total Orders: {summary['total_orders']}", 12, 6)
    draw_line(f"Total Units Sold: {summary['total_units_sold']:.2f}", 12, 6)
    draw_line(f"Total Revenue: {summary['total_revenue']:,.2f}", 12, 6)
    draw_line(f"Average Order Value: {summary['average_order_value']:,.2f}", 12, 8)

    draw_line("Top Products by Revenue", 14, 6)
    for name, value in summary["top_products"]:
        draw_line(f"- {name}: {value:,.2f}", 11, 5)

    y -= 4 * mm
    draw_line("Category Sales", 14, 6)
    for name, value in summary["top_categories"]:
        draw_line(f"- {name}: {value:,.2f}", 11, 5)

    y -= 4 * mm
    draw_line("City / Location Sales", 14, 6)
    for name, value in summary["sales_by_city"]:
        draw_line(f"- {name}: {value:,.2f}", 11, 5)

    y -= 4 * mm
    draw_line("Monthly Sales", 14, 6)
    for name, value in summary["monthly_sales"]:
        draw_line(f"- {name}: {value:,.2f}", 11, 5)

    c.save()
    return True


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main() -> None:
    project_root = Path(__file__).parent
    output_folder = project_root / "output"

    ensure_folder(output_folder)

    cleaned_csv = output_folder / "cleaned_sales_data.csv"

    top_products_chart = output_folder / "top_products_chart.svg"
    category_sales_chart = output_folder / "category_sales_chart.svg"
    city_sales_chart = output_folder / "city_sales_chart.svg"
    monthly_sales_chart = output_folder / "monthly_sales_chart.svg"
    html_report = output_folder / "sales_visual_report.html"
    pdf_report = output_folder / "sales_visual_report.pdf"

    print("📈 Charts + Visual Report Generator")
    print("-" * 60)

    try:
        rows = load_cleaned_sales_data(cleaned_csv)
        summary = generate_summary(rows)

        create_svg_bar_chart(
            "Top Products by Revenue",
            summary["top_products"],
            top_products_chart
        )

        create_svg_bar_chart(
            "Category Sales",
            summary["top_categories"],
            category_sales_chart
        )

        create_svg_bar_chart(
            "City / Location Sales",
            summary["sales_by_city"],
            city_sales_chart
        )

        create_svg_bar_chart(
            "Monthly Sales",
            summary["monthly_sales"],
            monthly_sales_chart
        )

        build_html_report(summary, html_report)

        print("Charts created:")
        print(f"1. {top_products_chart}")
        print(f"2. {category_sales_chart}")
        print(f"3. {city_sales_chart}")
        print(f"4. {monthly_sales_chart}")
        print("")
        print(f"HTML report created: {html_report}")

        pdf_created = create_pdf_report(summary, pdf_report)
        if pdf_created:
            print(f"PDF report created : {pdf_report}")
        else:
            print("PDF report skipped : reportlab is not installed")

        print("")
        print("✅ Visualization complete.")

    except FileNotFoundError as e:
        print("File error:")
        print(e)

    except ValueError as e:
        print("Data error:")
        print(e)

    except Exception as e:
        print("Unexpected error:")
        print(str(e))


if __name__ == "__main__":
    main()