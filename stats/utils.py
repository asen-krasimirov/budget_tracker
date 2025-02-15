import pandas as pd
from purchases.models import Purchase

import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from stats.utils import get_grouped_statistics
from accounts.models import UserProfile

import matplotlib
matplotlib.use("Agg")

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

def generate_graph_image(data, title, xlabel, ylabel, currency_symbol):
    """Creates a Matplotlib graph and returns it as a base64-encoded image."""
    if not data:
        return None

    df = pd.DataFrame(data.items(), columns=[xlabel, ylabel])
    plt.figure(figsize=(7, 4))
    plt.bar(df[xlabel], df[ylabel], color="blue", alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel(f"{ylabel} ({currency_symbol})")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def send_statistics_email(user):
    """Generates and sends an email with the user's spending statistics and graphs."""

    # Fetch user statistics
    stats = get_grouped_statistics(user)
    profile = UserProfile.objects.get(user=user)
    currency_symbol = profile.get_currency_display().split()[-1]  # Get currency symbol

    # Generate Graphs
    monthly_graph = generate_graph_image(stats["monthly"], "Monthly Spending", "Month", "Total Spent", currency_symbol)
    weekly_graph = generate_graph_image(stats["weekly"], "Weekly Spending", "Week", "Total Spent", currency_symbol)
    daily_graph = generate_graph_image(stats["daily"], "Daily Spending", "Day", "Total Spent", currency_symbol)
    category_graph = generate_graph_image(stats["category"], "Spending by Category", "Category", "Total Spent", currency_symbol)

    # Prepare email content
    email_content = render_to_string("stats/email_stats.html", {
        "user": user,
        "currency_symbol": currency_symbol,
        "monthly_graph": monthly_graph,
        "weekly_graph": weekly_graph,
        "daily_graph": daily_graph,
        "category_graph": category_graph,
    })

    # Create and send email
    email = EmailMessage(
        subject=f"{user.username}, Your Monthly Budget Report 📊",
        body=email_content,
        from_email="no-reply@yourapp.com",
        to=[user.email],
    )
    email.content_subtype = "html"  # Ensure HTML email rendering
    email.send()
