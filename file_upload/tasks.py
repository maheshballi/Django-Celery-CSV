import os
import pandas as pd
import logging
from celery import shared_task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@shared_task
def process_csv(file_path):
    """
    Celery task to process the uploaded CSV file and perform calculations.
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        # Load the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        if df.empty:
            return {"error": "CSV file is empty."}

        # Identify numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        # Perform calculations with conversion to Python native types
        calculations = {
            col: {
                "sum": float(df[col].sum()),  
                "average": float(df[col].mean()),  
                "count": int(df[col].count())  
            }
            for col in numeric_cols
        }

        # Additional Metrics (Convert to Python native types)
        total_revenue = float(df["Sales"].sum()) if "Sales" in df.columns else 0.0
        avg_discount = float(df["Discount"].mean()) if "Discount" in df.columns else 0.0

        # Handle possible NaN values safely
        best_selling_product = (
            df.groupby("Product Name")["Quantity"].sum().idxmax()
            if {"Product Name", "Quantity"}.issubset(df.columns) and df["Quantity"].notna().any()
            else None
        )

        most_profitable_product = (
            df.groupby("Product Name")["Profit"].sum().idxmax()
            if {"Product Name", "Profit"}.issubset(df.columns) and df["Profit"].notna().any()
            else None
        )

        max_discount_product = (
            df.loc[df["Discount"].idxmax(), "Product Name"]
            if {"Product Name", "Discount"}.issubset(df.columns) and df["Discount"].notna().any()
            else None
        )

        # Log completion
        logger.info(f"CSV processing completed for file: {file_path}")

        return {
            "calculations": calculations,
            "total_revenue": total_revenue,
            "avg_discount": avg_discount,
            "best_selling_product": best_selling_product,
            "most_profitable_product": most_profitable_product,
            "max_discount_product": max_discount_product
        }

    except Exception as e:
        logger.error(f"Error processing CSV file {file_path}: {e}", exc_info=True)
        return {"error": str(e)}
