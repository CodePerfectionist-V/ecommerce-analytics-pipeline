## E-Commerce Data Engineering & Analytics Pipeline
An enterprise-grade, modular Python and dbt ETL pipeline designed to ingest, clean, transform, and visualize raw e-commerce transaction data. Built with production standards including structured logging, robust error handling, dynamic pathing, and analytics-ready dbt seed integration.

## 🏗️ Architecture & Project Layout

# Plaintext

ecommerce-data-pipeline/
├── analytics/                  # dbt analytics transformation layer
│   ├── models/                 # Analytical data models
│   ├── seeds/                  # Cleaned data target for dbt ingestion
│   │   └── cleaned_ecom_data.csv
│   └── dev.duckdb              # Embedded analytical database
├── reports/                    # Auto-generated visualization artifacts
│   ├── category_revenue.png
│   └── weekly_revenue_trends.png
├── src/                        # Modular Python source modules
│   └── ecom_data.py            # Primary ETL execution script
├── .gitignore                  # Production Git ignore rules
└── README.md                   # Technical documentation

## 🛠️ Tech Stack & Key Tools
Language: Python 3.10+

Data Manipulation: Pandas, NumPy

Visualization: Seaborn, Matplotlib

Transformation & Warehousing: dbt (data build tool), DuckDB

Logging & Pathing: Native logging framework, pathlib

## ⚡ Data Pipeline Features
Robust Ingestion & Error Handling: Uses pathlib for cross-platform file execution and standard logging handlers for operational visibility.

Schema & Date Standardizing: Coerces string transactions into ISO standard datetime formats, purging unparseable records.

Outlier Mitigation: Isolates sentinel noise values (999999.0) to NaN to maintain mathematical integrity across analytical models.

Grouped Median Imputation: Fills missing revenue records dynamically using categorical median values based on standard product classifications.

Feature Engineering: Derives Year, Month, Day, and Day_of_Week columns for trend analyses.

Automated Visual Reporting: Exports crisp high-resolution plots directly to /reports without blocking pipeline execution.
