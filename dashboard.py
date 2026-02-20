import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from sample_data import (
    generate_revenue_data,
    generate_product_sales,
    generate_daily_visitors,
    generate_user_demographics,
    generate_order_status,
    generate_top_products,
)


def render_sidebar(user_info: dict | None = None, logout_fn=None):
    """Render the sidebar with user info, dashboard navigation, and filters."""
    with st.sidebar:
        if user_info:
            st.markdown("### 👤 User Info")
            st.markdown(f"**Username:** {user_info.get('preferred_username', 'N/A')}")
            st.markdown(f"**Email:** {user_info.get('email', 'N/A')}")
            st.markdown(f"**Name:** {user_info.get('name', 'N/A')}")
            st.divider()
            if logout_fn and st.button("🚪 Logout", width="stretch"):
                logout_fn()
                st.rerun()
        else:
            st.markdown("### 👤 Guest Mode")
            st.markdown("Authentication is disabled.")

        st.divider()

        # Dashboard navigation
        st.markdown("### 📊 Dashboards")
        page = st.radio(
            "Select Dashboard",
            options=["💰 Revenue & Sales", "🌐 Traffic & Users", "📦 Orders & Products"],
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown("### 📅 Filters")
        st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
        )

    return page


def render_header(user_info: dict | None = None):
    """Render the common header with KPI metrics."""
    username = user_info.get("preferred_username", "User") if user_info else "Guest"

    st.title("📊 Dashboard Sample")
    st.markdown(f"Welcome back, **{username}**! 👋")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="💰 Total Revenue", value="$892,450", delta="+12.5%")
    with col2:
        st.metric(label="📦 Total Orders", value="2,255", delta="+8.3%")
    with col3:
        st.metric(label="👥 Active Users", value="17,600", delta="+5.1%")
    with col4:
        st.metric(label="⭐ Avg Rating", value="4.7/5", delta="+0.2")

    st.divider()


def render_revenue_sales():
    """Dashboard 1: Monthly Revenue Trend + Sales by Category."""
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Monthly Revenue Trend")
        df_revenue = generate_revenue_data()
        fig_revenue = px.area(
            df_revenue, x="month", y="revenue",
            labels={"month": "Month", "revenue": "Revenue ($)"},
            color_discrete_sequence=["#6366f1"],
        )
        fig_revenue.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_revenue, width="stretch")

    with col_right:
        st.subheader("🏷️ Sales by Category")
        df_products = generate_product_sales()
        fig_products = px.bar(
            df_products, x="sales", y="category", orientation="h",
            color="sales", color_continuous_scale="Viridis",
            labels={"sales": "Units Sold", "category": "Category"},
        )
        fig_products.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
        )
        st.plotly_chart(fig_products, width="stretch")


def render_traffic_users():
    """Dashboard 2: Daily Website Visitors + Users by Region."""
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🌐 Daily Website Visitors")
        df_visitors = generate_daily_visitors()
        fig_visitors = px.line(
            df_visitors, x="date", y="visitors",
            labels={"date": "Date", "visitors": "Visitors"},
            color_discrete_sequence=["#10b981"],
        )
        fig_visitors.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_visitors, width="stretch")

    with col_right:
        st.subheader("🗺️ Users by Region")
        df_demo = generate_user_demographics()
        fig_demo = px.pie(
            df_demo, values="users", names="region",
            color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4,
        )
        fig_demo.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_demo, width="stretch")


def render_orders_products():
    """Dashboard 3: Order Status Breakdown + Top 10 Products."""
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📋 Order Status Breakdown")
        df_orders = generate_order_status()
        colors = ["#10b981", "#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"]
        fig_orders = go.Figure(data=[go.Pie(
            labels=df_orders["status"], values=df_orders["count"],
            marker=dict(colors=colors),
        )])
        fig_orders.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_orders, width="stretch")

    with col_right:
        st.subheader("🏆 Top 10 Products")
        df_top = generate_top_products()
        st.dataframe(
            df_top,
            column_config={
                "product": "Product Name",
                "units_sold": st.column_config.NumberColumn("Units Sold", format="%d"),
                "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.2f"),
            },
            hide_index=True, width="stretch",
        )


def render_dashboard(user_info: dict | None = None, logout_fn=None):
    """Main entry point — render sidebar navigation + selected dashboard."""
    page = render_sidebar(user_info, logout_fn)
    render_header(user_info)

    if page == "💰 Revenue & Sales":
        render_revenue_sales()
    elif page == "🌐 Traffic & Users":
        render_traffic_users()
    elif page == "📦 Orders & Products":
        render_orders_products()

    # --- Footer ---
    st.divider()
    st.caption("📊 Dashboard Sample — Data is randomly generated for demonstration purposes.")
