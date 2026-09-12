import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("ecommerce_pipeline.log", mode="a"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("EcommercePipeline")

# Silence noisy external library loggers (Matplotlib, PIL, etc.)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

def clean_ecommerce_data(
    input_path: Path | str, output_path: Path | str
) -> pd.DataFrame:
    """Cleans raw e-commerce transaction data, standardizes attributes, handles missing values,

    and exports the finalized dataset.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Safely create target output directory to prevent OSError
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Initiating data ingestion from source: {input_path}")

    try:
        df = pd.read_csv(input_path, encoding="latin1")
    except Exception as e:
        logger.error(f"Failed to load raw dataset from {input_path}: {e}")
        raise

    logger.info(f"Ingested dataset with {len(df)} initial records.")

    # 1. Deduplication & Date Parsing
    df.drop_duplicates(inplace=True)
    df["Transaction_Date"] = pd.to_datetime(
        df["Transaction_Date"], errors="coerce"
    )

    unparseable_dates = df["Transaction_Date"].isna().sum()
    if unparseable_dates > 0:
        logger.warning(
            f"Purging {unparseable_dates} records with invalid dates."
        )
        df.dropna(subset=["Transaction_Date"], inplace=True)

    # 2. Currency Formatting & Sentinel Outlier Neutralization
    df["Revenue"] = df["Revenue"].astype(str).str.replace("$", "", regex=False)
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    df["Revenue"] = df["Revenue"].round(2)

    outliers_detected = (df["Revenue"] == 999999.0).sum()
    if outliers_detected > 0:
        logger.warning(
            f"Isolated {outliers_detected} sentinel outlier values (999999.0) to NaN."
        )
        df["Revenue"] = df["Revenue"].replace(999999.0, np.nan)

    # 3. Categorical Standardization & Grouped Median Imputation
    df["Product_Category"] = df["Product_Category"].fillna("Unknown")
    df["Product_Category"] = df["Product_Category"].replace(
        {"laptop": "Laptop", "MOUZE": "Mouse"}
    )

    category_medians = df.groupby("Product_Category")["Revenue"].transform(
        "median"
    )
    df["Revenue"] = df["Revenue"].fillna(category_medians)

    # 4. Feature Engineering
    df["Year"] = df["Transaction_Date"].dt.year
    df["Month"] = df["Transaction_Date"].dt.month
    df["Day"] = df["Transaction_Date"].dt.day
    df["Day_of_Week"] = df["Transaction_Date"].dt.day_name()

    # 5. Export Processed Artifact
    df.to_csv(output_path, index=False)
    logger.info(f"Data cleaning complete. Clean file saved to: {output_path}")

    return df


def generate_revenue_visualizations(
    df: pd.DataFrame, output_dir: Path | str
) -> None:
    """Generates and exports executive visualization charts."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Generating revenue visualization artifacts...")
    sns.set_theme(style="whitegrid")

    # Chart 1: Revenue by Category
    plt.figure(figsize=(10, 6))
    cat_rev = (
        df.groupby("Product_Category")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    sns.barplot(
        data=cat_rev,
        x="Revenue",
        y="Product_Category",
        palette="Blues_r",
        hue="Product_Category",
        legend=False,
    )
    plt.title(
        "Product Category Revenue Performance",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Total Revenue ($)", fontsize=12)
    plt.ylabel("Product Category", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_dir / "category_revenue.png", dpi=300)
    plt.close()

    # Chart 2: Weekly Revenue Trends
    plt.figure(figsize=(10, 5))
    day_rev = df.groupby("Day_of_Week")["Revenue"].sum().reset_index()
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_rev["Day_of_Week"] = pd.Categorical(
        day_rev["Day_of_Week"], categories=day_order, ordered=True
    )
    day_rev = day_rev.sort_values("Day_of_Week")

    sns.lineplot(
        data=day_rev,
        x="Day_of_Week",
        y="Revenue",
        marker="o",
        color="#2b5c8f",
        linewidth=2.5,
    )
    plt.title(
        "Weekly Revenue Trends (Peak Performance)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Day of Week", fontsize=12)
    plt.ylabel("Total Revenue ($)", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_dir / "weekly_revenue_trends.png", dpi=300)
    plt.close()

    logger.info("Visualizations successfully saved to disk.")


if __name__ == "__main__":
    # Resolve repository root folder dynamically (one level up from /src)
    BASE_DIR = Path(__file__).resolve().parent.parent

    raw_data_path = r"E:\Datasets\messy_ecom_data.csv"
    dbt_seed_path = BASE_DIR / "analytics" / "seeds" / "cleaned_ecom_data.csv"
    reports_directory = BASE_DIR / "reports"

    try:
        cleaned_df = clean_ecommerce_data(raw_data_path, dbt_seed_path)
        generate_revenue_visualizations(cleaned_df, reports_directory)
        logger.info("Pipeline execution finished successfully.")
    except Exception as e:
        logger.critical(f"Pipeline failure: {e}")