# StockX Data Extraction Script

This script extracts market sales data from StockX and saves it in a CSV file. It uses the StockX API to fetch product sales information and processes the data for further analysis.

---

## Features
- Retrieves market sales data, including:
  - Sale price
  - Product size
  - Sale date
- Stores data in a CSV file (`output.csv`).
- Ensures headers are properly initialized.
- Handles API requests with necessary headers and cookies.

---

## Requirements
- Python 3.x
- Libraries:
  - `csv`
  - `pandas`
  - `requests`
  - `datetime`

Install dependencies using:
```bash
pip install pandas requests
