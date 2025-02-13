import pandas as pd
from purchases.models import Purchase

def get_purchase_data(user):
    """Fetch all purchases for a user and return as a DataFrame."""
    purchases = Purchase.objects.filter(user=user).values("name", "category", "price", "date")
    df = pd.DataFrame.from_records(purchases)

    if df.empty:
        return None  # No purchases found

    # ✅ Remove timezone from datetime before converting to periods
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    df["month"] = df["date"].dt.to_period("M").astype(str)  # ✅ Convert Period to string
    df["week"] = df["date"].dt.to_period("W").apply(lambda x: x.start_time.strftime("%Y-%m-%d"))  # ✅ Convert to string
    df["day"] = df["date"].dt.to_period("D").astype(str)  # ✅ Convert Period to string

    return df

def get_grouped_statistics(user):
    """Group purchase data by month, week, day, and category."""
    df = get_purchase_data(user)
    if df is None:
        return None

    stats = {
        "monthly": {str(k): float(v) for k, v in df.groupby("month")["price"].sum().to_dict().items()},
        "weekly": {str(k): float(v) for k, v in df.groupby("week")["price"].sum().to_dict().items()},
        "daily": {str(k): float(v) for k, v in df.groupby("day")["price"].sum().to_dict().items()},
        "category": {str(k): float(v) for k, v in df.groupby("category")["price"].sum().to_dict().items()},
    }
    return stats

def get_most_and_least_bought(user):
    """Finds the most and least bought products for a user."""
    df = get_purchase_data(user)
    if df is None:
        return {"most_bought": "N/A", "least_bought": "N/A"}

    product_counts = df["name"].value_counts()

    most_bought = product_counts.idxmax() if not product_counts.empty else "N/A"
    least_bought = product_counts.idxmin() if len(product_counts) > 1 else "N/A"

    return {"most_bought": most_bought, "least_bought": least_bought}
