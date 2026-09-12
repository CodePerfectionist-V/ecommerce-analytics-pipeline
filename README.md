```markdown
![Analytics Pipeline CI](https://github.com/CodePerfectionist-V/ecommerce-analytics-pipeline/actions/workflows/ci.yml/badge.svg?branch=main)

# E-Commerce Data Engineering & Analytics Pipeline

An enterprise-grade, modular Python and dbt ETL pipeline designed to ingest, clean, transform, and visualize raw e-commerce transaction data. Built with production standards including structured logging, robust error handling, dynamic pathing, and analytics-ready dbt seed integration.

## 🏗️ Architecture & Project Layout

### System Architecture & Pipeline Flow

```text
 [ Raw Sources ]          [ Python ETL ]                [ Analytical Warehouse ]
+----------------+       +-------------------+          +-----------------------+
|  Synthetic     | ----> | src/ecom_data.py  | -------> | DuckDB (dev.duckdb)   |
|  JSON/CSV Seeds|       | Ingestion Engine  |          | Raw Storage Layer     |
+----------------+       +-------------------+          +-----------------------+
                                                                   |
                                                                   v
                                                        [ dbt Core Pipeline ]
                                                        +-----------------------+
                                                        | Staging (Silver)      |
                                                        | Marts (Gold)          |
                                                        +-----------------------+
                                                                   |
                                                                   v
                                                        [ Automated Quality ]
                                                        +-----------------------+
                                                        | GitHub Actions CI     |
                                                        | dbt test Assertions   |
                                                        +-----------------------+

```

### Data Lineage (Medallion Pattern)

* **Bronze (Raw Ingestion):** Unmodified transactional data landing directly into DuckDB target tables: `raw_customers`, `raw_orders`, `raw_payments`.
* **Silver (Staging Layer):** Standardized, type-casted, and sanitized intermediate models defined via modular `stg_*.sql` views:
* `stg_customers`: Cleaned customer profile attributes and status flags.
* `stg_orders`: Type-casted timestamps, order status codes, and normalized monetary values.
* `stg_payments`: Structured payment methods and transaction totals.


* **Gold (Marts Layer):** Production-ready dimensional models structured into analytical star schemas:
* `dim_customers`: Dimensional table calculating lifetime value (LTV), order frequency, and retention cohorts.
* `fct_orders`: Fact table consolidating order metrics, customer keys, and payment validation states.



### Data Quality Assertions & Testing Matrix
```
| Layer | Target Model | Key Assertions (`dbt test`) | Business Rule Enforced |
| --- | --- | --- | --- |
| Silver | `stg_customers` | `unique`, `not_null` (`customer_id`) | Primary key integrity |
| Silver | `stg_orders` | `accepted_values` (`status`) | Valid status domain (`completed`, `shipped`, `pending`) |
| Gold | `fct_orders` | `relationships` (`customer_id` -> `dim_customers`) | Referential integrity between facts & dimensions |
| Gold | `dim_customers` | `expression_is_true` (`lifetime_value >= 0`) | Non-negative financial metrics |
```
### Repository Directory Structure

```text
ecommerce-data-pipeline/
├── analytics/                     # dbt analytics transformation layer
│   ├── models/                    # Analytical data models (staging & marts)
│   └── seeds/                     # Cleaned dataset target for dbt ingestion
│       └── cleaned_ecom_data.csv
├── reports/                       # Auto-generated visualization artifacts
│   ├── category_revenue.png
│   └── weekly_revenue_trends.png
├── src/                           # Modular Python source modules
│   └── ecom_data.py               # Primary ETL execution script
├── .gitignore                     # Production Git ignore rules
├── LICENSE                        # MIT License
├── README.md                      # Project documentation
└── requirements.txt               # Environment dependencies

```

## 🛠️ Tech Stack & Key Tools

* **Language:** Python 3.12
* **Data Manipulation:** Pandas, NumPy
* **Visualization:** Seaborn, Matplotlib
* **Transformation & Warehousing:** dbt Core (`dbt-duckdb`), DuckDB
* **Logging & Pathing:** Native `logging` framework, `pathlib`
* **Orchestration & CI/CD:** GitHub Actions

## ⚡ Data Pipeline Features

* **Robust Ingestion & Error Handling:** Uses `pathlib` for cross-platform file execution and standard logging handlers for operational visibility.
* **Schema & Date Standardization:** Coerces string transactions into ISO standard datetime formats, purging unparseable records.
* **Outlier Mitigation:** Isolates sentinel noise values (`999999.0`) to `NaN` to maintain mathematical integrity across analytical models.
* **Grouped Median Imputation:** Fills missing revenue records dynamically using categorical median values based on standard product classifications.
* **Feature Engineering:** Derives `Year`, `Month`, `Day`, and `Day_of_Week` columns for downstream trend analyses.
* **Automated Visual Reporting:** Exports high-resolution plots directly to `/reports` without blocking pipeline execution.


