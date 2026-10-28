"""Executive Business Intelligence & Profitability Dashboard.

Superstore Sales Exploratory Data Analysis & Strategic Decision Support App.
Built with Streamlit & Plotly.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Superstore Sales & Profit Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Metric Card Containers */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 8px 25px 0 rgba(99, 102, 241, 0.2);
}

div[data-testid="stMetricLabel"] {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
}

div[data-testid="stMetricValue"] {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

/* Headers */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: -0.02em;
}

.gradient-title {
    background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.badge-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-loss {
    background-color: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-profit {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Data Ingestion & Caching
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Load and prepare featured data for high-speed exploration."""
    for cand in [
        Path("data/cleaned/superstore_featured.csv"),
        Path("../data/cleaned/superstore_featured.csv"),
        Path("/home/adarsh/Documents/Superstore Sales EDA/data/cleaned/superstore_featured.csv"),
    ]:
        if cand.exists():
            df = pd.read_csv(cand)
            df["Order Date"] = pd.to_datetime(df["Order Date"])
            df["Ship Date"] = pd.to_datetime(df["Ship Date"])
            return df
    raise FileNotFoundError("Could not find superstore_featured.csv!")


@st.cache_data
def load_rfm():
    """Load customer RFM dataset."""
    for cand in [
        Path("data/cleaned/customer_rfm.csv"),
        Path("../data/cleaned/customer_rfm.csv"),
        Path("/home/adarsh/Documents/Superstore Sales EDA/data/cleaned/customer_rfm.csv"),
    ]:
        if cand.exists():
            return pd.read_csv(cand)
    return None


df_all = load_data()
df_rfm = load_rfm()

# -----------------------------------------------------------------------------
# 3. Sidebar Filtering Engine
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔍 Executive Filters")
    st.caption("Slice and diagnose performance across all dimensions.")

    # Year Multi-select
    all_years = sorted(df_all["Order_Year"].unique())
    selected_years = st.multiselect("Calendar Year", all_years, default=all_years)

    # Region Multi-select
    all_regions = sorted(df_all["Region"].unique())
    selected_regions = st.multiselect("Region", all_regions, default=all_regions)

    # Segment Multi-select
    all_segments = sorted(df_all["Segment"].unique())
    selected_segments = st.multiselect("Customer Segment", all_segments, default=all_segments)

    # Category Multi-select
    all_categories = sorted(df_all["Category"].unique())
    selected_categories = st.multiselect("Product Category", all_categories, default=all_categories)

    # Discount Bucket Filter
    all_buckets = ["0% (None)", "1-20% (Low)", "21-50% (Medium)", "50%+ (High)"]
    selected_buckets = st.multiselect("Discount Bucket", all_buckets, default=all_buckets)

    st.markdown("---")
    st.markdown("### 📌 Quick Benchmark")
    st.info("**Breakeven Ceiling:** Any discount above **20%** triggers severe loss-making transactions.")


# Filter logic
filtered_df = df_all[
    (df_all["Order_Year"].isin(selected_years)) &
    (df_all["Region"].isin(selected_regions)) &
    (df_all["Segment"].isin(selected_segments)) &
    (df_all["Category"].isin(selected_categories)) &
    (df_all["Discount_Bucket"].isin(selected_buckets))
]

if filtered_df.empty:
    st.warning("⚠️ No records match your selected filter criteria. Please broaden your selection.")
    st.stop()


# -----------------------------------------------------------------------------
# 4. Header & Global KPIs
# -----------------------------------------------------------------------------
st.markdown('<div class="gradient-title">Superstore Executive Sales & Profit Intelligence</div>', unsafe_allow_html=True)
st.markdown("#### Diagnostic Exploratory Data Analysis & Strategic Profitability Platform")

# Top KPI Metric Cards
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df["Order ID"].nunique()
total_items = len(filtered_df)
loss_orders = filtered_df["Is_Loss"].sum()
loss_rate = (loss_orders / total_items * 100) if total_items > 0 else 0
avg_lead_time = filtered_df["Shipping_Days"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Gross Sales", f"${total_sales:,.0f}", help="Total revenue generated")
kpi2.metric(
    "Net Profit",
    f"${total_profit:,.0f}",
    delta=f"{overall_margin:.1f}% margin",
    delta_color="normal" if total_profit >= 0 else "inverse"
)
kpi3.metric("Profit Margin", f"{overall_margin:.1f}%", help="Net Profit / Gross Sales")
kpi4.metric("Loss-Making Rate", f"{loss_rate:.1f}%", f"{loss_orders:,} items", delta_color="inverse")
kpi5.metric("Avg Fulfillment", f"{avg_lead_time:.1f} Days", f"{total_orders:,} orders")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Tabbed Deep-Dive Navigation
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "📈 Executive Overview",
    "📦 Category & Sub-Category",
    "🎯 Discount & Margin Cliff",
    "🗺️ Regional & State Map",
    "👥 Customer RFM Segments",
    "💡 Strategic Recommendations"
])

# =============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================================
with tabs[0]:
    st.markdown("### 📊 Performance Trajectory & Commercial Momentum")
    col_t1, col_t2 = st.columns([2, 1])

    with col_t1:
        # Monthly Time Series Trend
        monthly = (
            filtered_df.set_index("Order Date")
            .resample("ME")
            .agg({"Sales": "sum", "Profit": "sum"})
            .reset_index()
        )
        monthly["Sales_MA3"] = monthly["Sales"].rolling(3).mean()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Sales"],
            name="Monthly Sales", line=dict(color="#3B82F6", width=2.5),
            mode="lines+markers"
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Sales_MA3"],
            name="Sales 3M Moving Avg", line=dict(color="#93C5FD", width=1.5, dash="dot")
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Profit"],
            name="Net Profit", line=dict(color="#10B981", width=2.5),
            mode="lines+markers", yaxis="y2"
        ))

        fig_trend.update_layout(
            title="Monthly Revenue & Profit Progression (With Dual Axis)",
            template="plotly_dark",
            height=400,
            hovermode="x unified",
            margin=dict(l=20, r=20, t=50, b=20),
            yaxis=dict(title="Gross Sales ($)", showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
            yaxis2=dict(title="Net Profit ($)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t2:
        # Segment Share Donut
        seg_df = filtered_df.groupby("Segment").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        fig_seg = px.pie(
            seg_df, values="Sales", names="Segment",
            title="Revenue Distribution by Segment",
            color="Segment",
            color_discrete_map={"Consumer": "#6366F1", "Corporate": "#3B82F6", "Home Office": "#EC4899"},
            hole=0.55,
            template="plotly_dark"
        )
        fig_seg.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_seg, use_container_width=True)

    # Lower Row: Top & Bottom Products
    st.markdown("### 🏆 SKU Performance Ledger")
    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("**Top 10 Most Profitable Products**")
        top_prod = (
            filtered_df.groupby(["Product Name", "Category", "Sub-Category"])
            .agg(Total_Sales=("Sales", "sum"), Net_Profit=("Profit", "sum"), Units=("Quantity", "sum"))
            .reset_index()
            .sort_values(by="Net_Profit", ascending=False)
            .head(10)
        )
        top_prod["Margin%"] = (top_prod["Net_Profit"] / top_prod["Total_Sales"]) * 100
        st.dataframe(
            top_prod[["Product Name", "Category", "Total_Sales", "Net_Profit", "Margin%"]].style.format({
                "Total_Sales": "${:,.0f}",
                "Net_Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

    with p_col2:
        st.markdown("**Bottom 10 Severe Loss-Making Products**")
        bot_prod = (
            filtered_df.groupby(["Product Name", "Category", "Sub-Category"])
            .agg(Total_Sales=("Sales", "sum"), Net_Profit=("Profit", "sum"), Units=("Quantity", "sum"))
            .reset_index()
            .sort_values(by="Net_Profit", ascending=True)
            .head(10)
        )
        bot_prod["Margin%"] = (bot_prod["Net_Profit"] / bot_prod["Total_Sales"]) * 100
        st.dataframe(
            bot_prod[["Product Name", "Category", "Total_Sales", "Net_Profit", "Margin%"]].style.format({
                "Total_Sales": "${:,.0f}",
                "Net_Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# TAB 2: CATEGORY & SUB-CATEGORY
# =============================================================================
with tabs[1]:
    st.markdown("### 📦 Category Economics & Margin Disparities")

    cat_summary = filtered_df.groupby("Category").agg(
        Gross_Sales=("Sales", "sum"),
        Net_Profit=("Profit", "sum"),
        Order_Count=("Row ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    cat_summary["Profit_Margin%"] = (cat_summary["Net_Profit"] / cat_summary["Gross_Sales"]) * 100

    c1, c2, c3 = st.columns(3)
    for col, (_, row) in zip([c1, c2, c3], cat_summary.iterrows()):
        col.metric(
            f"{row['Category']} Category",
            f"${row['Net_Profit']:,.0f} Profit",
            f"{row['Profit_Margin%']:.1f}% Margin (Sales: ${row['Gross_Sales']:,.0f})",
            delta_color="normal" if row["Net_Profit"] > 25000 else "off"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Sub-category detailed horizontal bar
    sub_summary = filtered_df.groupby(["Category", "Sub-Category"]).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Items=("Row ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index().sort_values(by="Profit", ascending=True)
    sub_summary["Margin%"] = (sub_summary["Profit"] / sub_summary["Sales"]) * 100

    sub_colors = ["#EF4444" if p < 0 else "#10B981" if p > 30000 else "#6366F1" for p in sub_summary["Profit"]]

    fig_sub = go.Figure(go.Bar(
        x=sub_summary["Profit"],
        y=sub_summary["Sub-Category"],
        orientation="h",
        marker=dict(color=sub_colors),
        text=[f"${p/1e3:+.1f}K ({m:.1f}%)" for p, m in zip(sub_summary["Profit"], sub_summary["Margin%"])],
        textposition="auto"
    ))
    fig_sub.update_layout(
        title="Sub-Category Net Profit Ranking (Red: Loss-Makers | Green: Champions)",
        template="plotly_dark",
        height=550,
        xaxis=dict(title="Net Profit ($)"),
        yaxis=dict(title="Sub-Category"),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_sub, use_container_width=True)

    st.info("💡 **Takeaway:** Furniture generates \$742K in sales but almost zero net profit (2.5% margin) due to massive losses in **Tables (-\$17.7K)** and **Bookcases (-\$3.5K)**.")


# =============================================================================
# TAB 3: DISCOUNT & MARGIN CLIFF
# =============================================================================
with tabs[2]:
    st.markdown("### 🎯 Promotional Discount Sensitivity & Margin Destruction")
    st.caption("Investigating the tipping point: Where do promotional discounts shift from sales acceleration to capital destruction?")

    disc_tier = filtered_df.groupby("Discount_Bucket", observed=False).agg(
        Orders=("Row ID", "count"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Loss_Orders=("Is_Loss", "sum")
    ).reset_index()
    disc_tier["Margin%"] = (disc_tier["Profit"] / disc_tier["Sales"]) * 100
    disc_tier["Loss_Rate%"] = (disc_tier["Loss_Orders"] / disc_tier["Orders"]) * 100

    col_d1, col_d2 = st.columns([1, 1])

    with col_d1:
        fig_disc_bar = go.Figure(data=[
            go.Bar(name="Profit Margin (%)", x=disc_tier["Discount_Bucket"].astype(str),
                   y=disc_tier["Margin%"], marker_color="#3B82F6"),
            go.Bar(name="Loss-Making Order Rate (%)", x=disc_tier["Discount_Bucket"].astype(str),
                   y=disc_tier["Loss_Rate%"], marker_color="#EF4444")
        ])
        fig_disc_bar.update_layout(
            barmode="group",
            title="Margin % vs Loss-Rate % Across Discount Buckets",
            template="plotly_dark",
            height=400,
            yaxis=dict(title="Percentage (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_disc_bar, use_container_width=True)

    with col_d2:
        # Scatter of individual transactions
        sample_df = filtered_df.sample(min(2000, len(filtered_df)), random_state=42)
        fig_scat = px.scatter(
            sample_df,
            x="Discount",
            y="Profit_Margin",
            color="Category",
            hover_data=["Sub-Category", "Sales", "Profit"],
            title="Individual Order Discount vs Profit Margin Ratio",
            template="plotly_dark",
            color_discrete_map={"Technology": "#3B82F6", "Office Supplies": "#8B5CF6", "Furniture": "#F97316"}
        )
        fig_scat.add_hline(y=0, line_dash="dash", line_color="#EF4444", annotation_text="Breakeven (0% Margin)")
        fig_scat.add_vline(x=0.20, line_dash="dot", line_color="#F59E0B", annotation_text="20% Discount Cliff")
        fig_scat.update_layout(height=400, yaxis=dict(range=[-2.5, 1.0]))
        st.plotly_chart(fig_scat, use_container_width=True)

    st.error("🚨 **Critical Finding:** Orders with discounts **> 20%** have an astounding **91.6% to 100% loss rate**! Eliminating or capping discounts at 20% would instantly eliminate over **$135,000 in net losses**.")


# =============================================================================
# TAB 4: REGIONAL & STATE MAP
# =============================================================================
with tabs[3]:
    st.markdown("### 🗺️ Geographic Profitability & State-Level Polarization")

    # State aggregation
    state_df = filtered_df.groupby("State").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Row ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    state_df["Margin%"] = (state_df["Profit"] / state_df["Sales"]) * 100

    # US State Code Mapping for Plotly Choropleth
    us_state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
    }
    state_df["Code"] = state_df["State"].map(us_state_to_abbrev)

    col_map, col_stat = st.columns([1.6, 1])

    with col_map:
        fig_map = px.choropleth(
            state_df,
            locations="Code",
            locationmode="USA-states",
            color="Profit",
            scope="usa",
            hover_name="State",
            hover_data={"Code": False, "Sales": ":$,.0f", "Profit": ":$,.0f", "Margin%": ":.1f%"},
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            title="US State Net Profitability Choropleth Map",
            template="plotly_dark"
        )
        fig_map.update_layout(height=450, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_map, use_container_width=True)

    with col_stat:
        st.markdown("**Bottom 5 Loss-Hemorrhaging States**")
        st.dataframe(
            state_df.sort_values(by="Profit", ascending=True).head(5)[["State", "Sales", "Profit", "Margin%"]].style.format({
                "Sales": "${:,.0f}",
                "Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**Top 5 Profit Champion States**")
        st.dataframe(
            state_df.sort_values(by="Profit", ascending=False).head(5)[["State", "Sales", "Profit", "Margin%"]].style.format({
                "Sales": "${:,.0f}",
                "Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# TAB 5: CUSTOMER RFM SEGMENTS
# =============================================================================
with tabs[4]:
    st.markdown("### 👥 Customer RFM (Recency, Frequency, Monetary) Intelligence")
    st.caption("Behavioral customer segmentation based on recency of purchase, repeat order cadence, and lifetime monetary margin.")

    if df_rfm is not None:
        rfm_agg = df_rfm.groupby("RFM_Segment").agg(
            Customer_Count=("Customer ID", "count"),
            Total_Sales=("Monetary_Sales", "sum"),
            Total_Profit=("Monetary_Profit", "sum"),
            Avg_Recency=("Recency_Days", "mean"),
            Avg_Orders=("Frequency", "mean")
        ).reset_index()
        rfm_agg["Margin%"] = (rfm_agg["Total_Profit"] / rfm_agg["Total_Sales"]) * 100
        rfm_agg = rfm_agg.sort_values(by="Total_Sales", ascending=False)

        col_rfm1, col_rfm2 = st.columns([1.2, 1])

        with col_rfm1:
            fig_rfm = px.bar(
                rfm_agg,
                x="RFM_Segment",
                y="Total_Sales",
                color="Margin%",
                color_continuous_scale="Viridis",
                title="Customer Segment Revenue & Margin (%) Contribution",
                template="plotly_dark",
                text=[f"${s/1e3:.0f}K" for s in rfm_agg["Total_Sales"]]
            )
            fig_rfm.update_layout(height=400, xaxis_tickangle=-25)
            st.plotly_chart(fig_rfm, use_container_width=True)

        with col_rfm2:
            st.markdown("**RFM Segment Portfolio Summary**")
            st.dataframe(
                rfm_agg[["RFM_Segment", "Customer_Count", "Total_Sales", "Total_Profit", "Margin%"]].style.format({
                    "Customer_Count": "{:,}",
                    "Total_Sales": "${:,.0f}",
                    "Total_Profit": "${:,.0f}",
                    "Margin%": "{:.1f}%"
                }),
                use_container_width=True,
                hide_index=True
            )

        # High Value Customer Table
        st.markdown("#### 🌟 Top 10 Enterprise Account Champions")
        st.dataframe(
            df_rfm.sort_values(by="Monetary_Profit", ascending=False).head(10)[
                ["Customer Name", "Segment", "RFM_Segment", "Frequency", "Monetary_Sales", "Monetary_Profit", "Profit_Margin"]
            ].style.format({
                "Monetary_Sales": "${:,.0f}",
                "Monetary_Profit": "${:,.0f}",
                "Profit_Margin": "{:.1%}"
            }),
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# TAB 6: STRATEGIC RECOMMENDATIONS & SCENARIO SIMULATOR
# =============================================================================
with tabs[5]:
    st.markdown("### 💡 Executive Action Plan & Financial Scenario Simulator")

    st.markdown("""
    #### 🎯 Answers to Core Business Questions:
    1. **Categories & Sub-Categories:** Technology (\$145.5K) and Office Supplies (\$122.5K) are star performers. Furniture is an acute drag (\$18.5K profit on \$742K sales). **Tables** lose **-$17.7K** and **Bookcases** lose **-$3.5K**.
    2. **Discount Dynamics:** Transactions with discounts between 0-20% maintain healthy margins (12-30%). Discounts above 20% experience an **order loss rate over 91.6%**.
    3. **Underperforming Geography:** Texas (-\$25.7K), Ohio (-\$17.0K), Pennsylvania (-\$15.6K), and Illinois (-\$12.6K) drag company profit down by **over -$78K**.
    4. **Valuable Customers:** Top 20% of customers account for 73% of total profits. "Champions" and "Loyal Customers" generate >70% of enterprise margin.
    5. **Seasonality:** Q4 holiday shopping surge delivers the largest volume (peaking in November and December).
    6. **Logistics:** Standard class accounts for 60% of volume (avg 5.0 days dispatch); First Class maintains the highest margins (13.9%).
    """)

    st.markdown("---")
    st.markdown("### 🎛️ Interactive Profit Sensitivity Simulator")

    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        cap_discount = st.slider("Select Maximum Allowable Discount (%)", min_value=10, max_value=80, value=20, step=5)
        exclude_loss_tables = st.checkbox("Restructure / Discontinue Chronic Loss Tables Sub-Category", value=True)

    # Simulation calculation
    sim_df = df_all.copy()
    if exclude_loss_tables:
        sim_df = sim_df[sim_df["Sub-Category"] != "Tables"]
    sim_df_capped = sim_df[sim_df["Discount"] <= (cap_discount / 100.0)]

    base_p = df_all["Profit"].sum()
    base_s = df_all["Sales"].sum()
    sim_p = sim_df_capped["Profit"].sum()
    sim_s = sim_df_capped["Sales"].sum()
    lift_dollar = sim_p - base_p
    lift_pct = (lift_dollar / base_p) * 100

    with sim_col2:
        st.markdown("#### Projected Financial Impact")
        r1, r2 = st.columns(2)
        r1.metric("Simulated Net Profit", f"${sim_p:,.0f}", f"{lift_dollar:+,.0f} Lift")
        r2.metric("Profit Lift (%)", f"{lift_pct:+.1f}%", f"{(sim_p/sim_s*100):.1f}% Margin")

    st.success(f"""
    **Executive Policy Recommendation:**
    - Capping commercial discounts at **{cap_discount}%** and eliminating loss-making table SKUs will increase total business profit from **${base_p:,.0f}** to **${sim_p:,.0f}** (a **{lift_pct:+.1f}% increase**).
    - Immediately audit regional sales reps in Texas, Ohio, and Illinois who utilize aggressive discounting to meet top-line sales quotas at the expense of profitability.
    """)
