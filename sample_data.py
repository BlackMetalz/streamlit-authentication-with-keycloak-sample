import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


@st.cache_data
def generate_revenue_data():
    """Monthly revenue data for the last 12 months."""
    np.random.seed(42)
    months = pd.date_range(end=datetime.now(), periods=12, freq="ME")
    revenue = np.random.uniform(50_000, 150_000, size=12).cumsum() / 12
    revenue = revenue + np.linspace(30_000, 80_000, 12)
    return pd.DataFrame({"month": months, "revenue": np.round(revenue, 2)})


@st.cache_data
def generate_product_sales():
    """Product category sales data."""
    categories = [
        "Electronics", "Clothing", "Food & Beverage",
        "Home & Garden", "Sports", "Books", "Toys"
    ]
    np.random.seed(123)
    sales = np.random.randint(1000, 10000, size=len(categories))
    return pd.DataFrame({"category": categories, "sales": sales})


@st.cache_data
def generate_daily_visitors():
    """Daily website visitors for the last 30 days."""
    np.random.seed(99)
    days = pd.date_range(end=datetime.now(), periods=30, freq="D")
    visitors = []
    for d in days:
        base = 5000 if d.weekday() < 5 else 3000
        visitors.append(base + np.random.randint(-800, 1500))
    return pd.DataFrame({"date": days, "visitors": visitors})


@st.cache_data
def generate_user_demographics():
    """User demographics by region."""
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa"]
    users = [4500, 3800, 6200, 1900, 1200]
    return pd.DataFrame({"region": regions, "users": users})


@st.cache_data
def generate_order_status():
    """Order status breakdown."""
    statuses = ["Delivered", "Processing", "Shipped", "Cancelled", "Returned"]
    counts = [1250, 340, 520, 85, 60]
    return pd.DataFrame({"status": statuses, "count": counts})


@st.cache_data
def generate_top_products():
    """Top 10 selling products."""
    np.random.seed(55)
    products = [
        "Wireless Headphones", "Smart Watch", "USB-C Hub", "Mechanical Keyboard",
        "Portable Charger", "Webcam HD", "Mouse Pad XL", "LED Desk Lamp",
        "Bluetooth Speaker", "Phone Stand"
    ]
    units_sold = sorted(np.random.randint(200, 2000, size=10), reverse=True)
    revenue = [u * np.random.uniform(15, 80) for u in units_sold]
    return pd.DataFrame({
        "product": products,
        "units_sold": units_sold,
        "revenue": np.round(revenue, 2),
    })
