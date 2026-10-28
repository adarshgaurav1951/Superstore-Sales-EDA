"""Executive Business Intelligence & Profitability Dashboard.

Superstore Sales Exploratory Data Analysis & Strategic Decision Support App.
Built with Streamlit & Plotly featuring a Premium High-Contrast Executive Dark Theme.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Premium Executive CSS Styling
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

/* Base page & ambient background glow */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #070A13 !important;
    background-image: 
        radial-gradient(circle at 10% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 15%, rgba(168, 85, 247, 0.09) 0%, transparent 40%),
        radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.06) 0%, transparent 45%) !important;
    background-attachment: fixed !important;
    color: #F8FAFC !important;
}

/* Sidebar Styling: Deep Indigo/Slate with glowing border */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0E1A 0%, #0D1322 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.2) !important;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* =========================================================================
   SIDEBAR FILTER TAGS: High-Contrast, Razor-Sharp Legibility
   Deep Navy Background + Crisp White Bold Text + Vivid Purple/Indigo Border
   ========================================================================= */
div[data-baseweb="select"] span[data-baseweb="tag"],
span[data-baseweb="tag"],
.stMultiSelect [data-baseweb="tag"] {
    background: #172033 !important;
    background: linear-gradient(135deg, #1A2238 0%, #151C30 100%) !important;
    border: 1.5px solid #818CF8 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5), 0 0 10px rgba(99, 102, 241, 0.15) !important;
    padding: 4px 10px !important;
    margin: 3px !important;
}

div[data-baseweb="select"] span[data-baseweb="tag"]:hover,
span[data-baseweb="tag"]:hover {
    border-color: #A5B4FC !important;
    background: #1E293B !important;
}

div[data-baseweb="select"] span[data-baseweb="tag"] span,
span[data-baseweb="tag"] span,
.stMultiSelect [data-baseweb="tag"] span {
    color: #FFFFFF !important;
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    -webkit-font-smoothing: antialiased !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.6) !important;
}

div[data-baseweb="select"] span[data-baseweb="tag"] svg,
span[data-baseweb="tag"] svg {
    fill: #A5B4FC !important;
    width: 14px !important;
    height: 14px !important;
    transition: fill 0.15s ease !important;
}

div[data-baseweb="select"] span[data-baseweb="tag"] svg:hover,
span[data-baseweb="tag"] svg:hover {
    fill: #F43F5E !important;
}

/* Tabs: Premium glowing indicators */
div[data-testid="stTabs"] {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin-bottom: 1.5rem !important;
}

div[data-testid="stTabs"] button[role="tab"] {
    color: #94A3B8 !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 12px 20px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTabs"] button[role="tab"]:hover {
    color: #E2E8F0 !important;
}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #38BDF8 !important;
    border-bottom: 2.5px solid #38BDF8 !important;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
}

/* Headers */
h1, h2, h3, h4 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

.gradient-title {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.15rem;
    filter: drop-shadow(0 2px 10px rgba(56, 189, 248, 0.2));
}

.subtitle-text {
    color: #94A3B8 !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    margin-bottom: 1.3rem !important;
}

/* Dataframe & Tables */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    border-radius: 12px !important;
    background-color: #0F172A !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    overflow: hidden !important;
}

/* Info & Benchmark Box */
div[data-testid="stAlert"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-left: 4px solid #818CF8 !important;
    border-radius: 10px !important;
    color: #F1F5F9 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
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
# 3. Premium Eye-Comfort Plotly Styler Helper
# -----------------------------------------------------------------------------
def apply_premium_chart_theme(fig, height=420):
    """Apply rich, high-contrast dark theme to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.75)",
        plot_bgcolor="rgba(11, 15, 25, 0.85)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=11),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", color="#FFFFFF", size=15),
        height=height,
        margin=dict(l=25, r=25, t=55, b=25),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#E2E8F0", size=12)
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#E2E8F0", size=12)
        ),
        legend=dict(
            font=dict(color="#E2E8F0"),
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1
        )
    )
    return fig


# -----------------------------------------------------------------------------
# 4. Sidebar Filtering Engine
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Executive Filters")
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
    st.markdown("### 📌 Executive Guardrail")
    st.info("💡 **Discount Cliff:** Discounts exceeding **20%** produce an alarming **91.6% to 100% loss-making rate**.")


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
# 5. Header & Premium Glowing KPI Cards
# -----------------------------------------------------------------------------
st.markdown('<div class="gradient-title">Superstore Executive Sales & Profit Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Diagnostic Exploratory Data Analysis & Strategic Profitability Platform</div>', unsafe_allow_html=True)

# Metrics calculation
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df["Order ID"].nunique()
total_items = len(filtered_df)
loss_orders = filtered_df["Is_Loss"].sum()
loss_rate = (loss_orders / total_items * 100) if total_items > 0 else 0
avg_lead_time = filtered_df["Shipping_Days"].mean()


def render_premium_kpi_card(title, value, subtitle, icon, accent_color, badge_text="", is_positive=True):
    """Render a modern, luminous executive KPI card."""
    badge_bg = f"{accent_color}22" if is_positive else "rgba(244, 63, 94, 0.22)"
    badge_color = accent_color if is_positive else "#FB7185"
    badge_border = f"{accent_color}55" if is_positive else "rgba(244, 63, 94, 0.5)"
    
    badge_html = f"""
    <span style="display:inline-block; padding: 3px 9px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; letter-spacing: 0.02em;">
        {badge_text}
    </span>
    """ if badge_text else ""

    html = f"""
    <div style="
        background: linear-gradient(145deg, #131B2E 0%, #0D1424 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 3.5px solid {accent_color};
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45), 0 0 15px {accent_color}12;
        margin-bottom: 15px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="color: #94A3B8; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em;">{title}</span>
            <span style="font-size: 1.15rem; padding: 4px 8px; border-radius: 8px; background: {accent_color}18; color: {accent_color};">{icon}</span>
        </div>
        <div style="font-size: 1.95rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 6px;">
            {value}
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; color: #94A3B8;">
            <span>{subtitle}</span>
            {badge_html}
        </div>
    </div>
    """
    return html


col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

with col_k1:
    st.markdown(
        render_premium_kpi_card(
            title="Gross Revenue",
            value=f"${total_sales:,.0f}",
            subtitle=f"{total_orders:,} Orders Placed",
            icon="💎",
            accent_color="#38BDF8",
            badge_text="Volume Leader",
            is_positive=True
        ),
        unsafe_allow_html=True
    )

with col_k2:
    st.markdown(
        render_premium_kpi_card(
            title="Net Profit",
            value=f"${total_profit:,.0f}",
            subtitle="Bottom-Line Cash",
            icon="📈",
            accent_color="#10B981" if total_profit >= 0 else "#F43F5E",
            badge_text=f"{overall_margin:+.1f}% Margin",
            is_positive=total_profit >= 0
        ),
        unsafe_allow_html=True
    )

with col_k3:
    margin_ok = overall_margin >= 12.0
    st.markdown(
        render_premium_kpi_card(
            title="Profit Margin",
            value=f"{overall_margin:.1f}%",
            subtitle="Net / Gross Ratio",
            icon="⚡",
            accent_color="#A855F7",
            badge_text="Target ≥ 12%" if margin_ok else "Below Benchmark",
            is_positive=margin_ok
        ),
        unsafe_allow_html=True
    )

with col_k4:
    st.markdown(
        render_premium_kpi_card(
            title="Loss Order Rate",
            value=f"{loss_rate:.1f}%",
            subtitle=f"{loss_orders:,} of {total_items:,} Items",
            icon="⚠️",
            accent_color="#F43F5E",
            badge_text="Attention Required",
            is_positive=False
        ),
        unsafe_allow_html=True
    )

with col_k5:
    st.markdown(
        render_premium_kpi_card(
            title="Avg Fulfillment",
            value=f"{avg_lead_time:.1f} Days",
            subtitle="Order to Dispatch",
            icon="🚚",
            accent_color="#F59E0B",
            badge_text="4 Delivery Tiers",
            is_positive=True
        ),
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. Tabbed Deep-Dive Navigation
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
    st.markdown("#### 📊 Performance Trajectory & Commercial Momentum")
    col_t1, col_t2 = st.columns([2, 1])

    with col_t1:
        # Monthly Time Series Trend with Area Gradients
        monthly = (
            filtered_df.set_index("Order Date")
            .resample("ME")
            .agg({"Sales": "sum", "Profit": "sum"})
            .reset_index()
        )
        monthly["Sales_MA3"] = monthly["Sales"].rolling(3).mean()

        fig_trend = go.Figure()
        # Sales area
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Sales"],
            name="Monthly Sales ($)", line=dict(color="#38BDF8", width=3),
            fill="tozeroy", fillcolor="rgba(56, 189, 248, 0.08)",
            mode="lines+markers",
            marker=dict(size=6, color="#38BDF8", line=dict(color="#FFFFFF", width=1.5))
        ))
        # 3-Month Moving Average
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Sales_MA3"],
            name="Sales 3M Moving Avg", line=dict(color="#FBBF24", width=2, dash="dash")
        ))
        # Net Profit area
        fig_trend.add_trace(go.Scatter(
            x=monthly["Order Date"], y=monthly["Profit"],
            name="Net Profit ($)", line=dict(color="#10B981", width=3),
            fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.08)",
            mode="lines+markers",
            marker=dict(size=6, color="#10B981", line=dict(color="#FFFFFF", width=1.5)),
            yaxis="y2"
        ))

        fig_trend = apply_premium_chart_theme(fig_trend, height=430)
        fig_trend.update_layout(
            title="<b>Monthly Revenue & Profit Progression</b> (Dual-Axis with Area Fill)",
            hovermode="x unified",
            yaxis=dict(
                title=dict(text="Gross Sales ($)", font=dict(color="#38BDF8", size=12)),
                gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")
            ),
            yaxis2=dict(
                title=dict(text="Net Profit ($)", font=dict(color="#10B981", size=12)),
                overlaying="y", side="right", showgrid=False,
                tickfont=dict(color="#10B981")
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, width="stretch")

    with col_t2:
        # Segment Share Donut with Center Callout
        seg_df = filtered_df.groupby("Segment").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        fig_seg = px.pie(
            seg_df, values="Sales", names="Segment",
            title="<b>Revenue Distribution by Segment</b>",
            color="Segment",
            color_discrete_map={
                "Consumer": "#6366F1",    # Vivid Indigo
                "Corporate": "#06B6D4",   # Electric Cyan
                "Home Office": "#EC4899"  # Radiant Magenta
            },
            hole=0.62
        )
        fig_seg.update_traces(
            textinfo="percent+label",
            textposition="outside",
            marker=dict(line=dict(color="#0B0F19", width=2.5))
        )
        fig_seg = apply_premium_chart_theme(fig_seg, height=430)
        fig_seg.update_layout(
            annotations=[dict(
                text=f"<b>${total_sales/1e6:.2f}M</b><br><span style='font-size:11px;color:#94A3B8'>Total Sales</span>",
                x=0.5, y=0.5, font_size=17, showarrow=False, font_color="#FFFFFF"
            )],
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_seg, width="stretch")

    # Lower Row: Top & Bottom Products
    st.markdown("#### 🏆 SKU Performance Ledger")
    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("**🌟 Top 10 Most Profitable Products**")
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
            width="stretch",
            hide_index=True
        )

    with p_col2:
        st.markdown("**⚠️ Bottom 10 Severe Loss-Making Products**")
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
            width="stretch",
            hide_index=True
        )


# =============================================================================
# TAB 2: CATEGORY & SUB-CATEGORY
# =============================================================================
with tabs[1]:
    st.markdown("#### 📦 Category Economics & Margin Disparities")

    cat_summary = filtered_df.groupby("Category").agg(
        Gross_Sales=("Sales", "sum"),
        Net_Profit=("Profit", "sum"),
        Order_Count=("Row ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    cat_summary["Profit_Margin%"] = (cat_summary["Net_Profit"] / cat_summary["Gross_Sales"]) * 100

    c1, c2, c3 = st.columns(3)
    cat_colors = {"Technology": "#38BDF8", "Office Supplies": "#A855F7", "Furniture": "#F97316"}
    cat_icons = {"Technology": "💻", "Office Supplies": "📎", "Furniture": "🛋️"}

    for col, (_, row) in zip([c1, c2, c3], cat_summary.iterrows()):
        c_name = row["Category"]
        with col:
            st.markdown(
                render_premium_kpi_card(
                    title=f"{c_name} Category",
                    value=f"${row['Net_Profit']:,.0f}",
                    subtitle=f"Sales: ${row['Gross_Sales']:,.0f}",
                    icon=cat_icons.get(c_name, "📦"),
                    accent_color=cat_colors.get(c_name, "#818CF8"),
                    badge_text=f"{row['Profit_Margin%']:.1f}% Margin",
                    is_positive=row["Net_Profit"] > 0
                ),
                unsafe_allow_html=True
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

    sub_colors = ["#F43F5E" if p < 0 else "#10B981" if p > 30000 else "#6366F1" for p in sub_summary["Profit"]]

    fig_sub = go.Figure(go.Bar(
        x=sub_summary["Profit"],
        y=sub_summary["Sub-Category"],
        orientation="h",
        marker=dict(color=sub_colors, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        text=[f"${p/1e3:+.1f}K ({m:.1f}%)" for p, m in zip(sub_summary["Profit"], sub_summary["Margin%"])],
        textposition="auto",
        textfont=dict(color="#FFFFFF", size=10, family="Plus Jakarta Sans, sans-serif")
    ))
    fig_sub = apply_premium_chart_theme(fig_sub, height=560)
    fig_sub.update_layout(
        title="<b>Sub-Category Net Profit Ranking</b> (Vivid Crimson: Loss | Emerald: Champions)",
        xaxis=dict(title="Net Profit ($)"),
        yaxis=dict(title="Sub-Category")
    )
    st.plotly_chart(fig_sub, width="stretch")

    st.info("💡 **Takeaway:** Furniture generates $742K in sales but almost zero net profit (2.5% margin) due to massive losses in **Tables (-$17.7K)** and **Bookcases (-$3.5K)**.")


# =============================================================================
# TAB 3: DISCOUNT & MARGIN CLIFF
# =============================================================================
with tabs[2]:
    st.markdown("#### 🎯 Promotional Discount Sensitivity & Margin Destruction")
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
                   y=disc_tier["Margin%"], marker_color="#38BDF8"),
            go.Bar(name="Loss-Making Order Rate (%)", x=disc_tier["Discount_Bucket"].astype(str),
                   y=disc_tier["Loss_Rate%"], marker_color="#F43F5E")
        ])
        fig_disc_bar = apply_premium_chart_theme(fig_disc_bar, height=410)
        fig_disc_bar.update_layout(
            barmode="group",
            title="<b>Margin % vs Loss-Rate % Across Discount Buckets</b>",
            yaxis=dict(title="Percentage (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_disc_bar, width="stretch")

    with col_d2:
        # Scatter of individual transactions
        sample_df = filtered_df.sample(min(2000, len(filtered_df)), random_state=42)
        fig_scat = px.scatter(
            sample_df,
            x="Discount",
            y="Profit_Margin",
            color="Category",
            hover_data=["Sub-Category", "Sales", "Profit"],
            title="<b>Order Discount vs Profit Margin Ratio</b>",
            color_discrete_map={"Technology": "#38BDF8", "Office Supplies": "#A855F7", "Furniture": "#F97316"}
        )
        fig_scat.add_hline(y=0, line_dash="dash", line_color="#F43F5E", annotation_text="Breakeven (0% Margin)", annotation_font_color="#F43F5E")
        fig_scat.add_vline(x=0.20, line_dash="dot", line_color="#FBBF24", annotation_text="20% Discount Cliff", annotation_font_color="#FBBF24")
        fig_scat = apply_premium_chart_theme(fig_scat, height=410)
        fig_scat.update_layout(yaxis=dict(range=[-2.5, 1.0]))
        st.plotly_chart(fig_scat, width="stretch")

    st.error("🚨 **Critical Finding:** Orders with discounts **> 20%** have an astounding **91.6% to 100% loss rate**! Eliminating or capping discounts at 20% would instantly eliminate over **$135,000 in net losses**.")


# =============================================================================
# TAB 4: REGIONAL & STATE MAP
# =============================================================================
with tabs[3]:
    st.markdown("#### 🗺️ Geographic Profitability & State-Level Polarization")

    # State aggregation
    state_df = filtered_df.groupby("State").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Row ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    state_df["Margin%"] = (state_df["Profit"] / state_df["Sales"]) * 100

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
            color_continuous_scale=["#EF4444", "#334155", "#10B981"],
            color_continuous_midpoint=0,
            title="<b>US State Net Profitability Choropleth Map</b>"
        )
        fig_map = apply_premium_chart_theme(fig_map, height=460)
        fig_map.update_geos(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="#0B0F19",
            landcolor="#1E293B",
            subunitcolor="rgba(255,255,255,0.12)"
        )
        st.plotly_chart(fig_map, width="stretch")

    with col_stat:
        st.markdown("**⚠️ Bottom 5 Loss-Hemorrhaging States**")
        st.dataframe(
            state_df.sort_values(by="Profit", ascending=True).head(5)[["State", "Sales", "Profit", "Margin%"]].style.format({
                "Sales": "${:,.0f}",
                "Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            width="stretch",
            hide_index=True
        )

        st.markdown("**🌟 Top 5 Profit Champion States**")
        st.dataframe(
            state_df.sort_values(by="Profit", ascending=False).head(5)[["State", "Sales", "Profit", "Margin%"]].style.format({
                "Sales": "${:,.0f}",
                "Profit": "${:,.0f}",
                "Margin%": "{:.1f}%"
            }),
            width="stretch",
            hide_index=True
        )


# =============================================================================
# TAB 5: CUSTOMER RFM SEGMENTS
# =============================================================================
with tabs[4]:
    st.markdown("#### 👥 Customer RFM (Recency, Frequency, Monetary) Intelligence")
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
                title="<b>Customer Segment Revenue & Margin (%) Contribution</b>",
                text=[f"${s/1e3:.0f}K" for s in rfm_agg["Total_Sales"]]
            )
            fig_rfm = apply_premium_chart_theme(fig_rfm, height=410)
            fig_rfm.update_layout(xaxis_tickangle=-25)
            st.plotly_chart(fig_rfm, width="stretch")

        with col_rfm2:
            st.markdown("**RFM Segment Portfolio Summary**")
            st.dataframe(
                rfm_agg[["RFM_Segment", "Customer_Count", "Total_Sales", "Total_Profit", "Margin%"]].style.format({
                    "Customer_Count": "{:,}",
                    "Total_Sales": "${:,.0f}",
                    "Total_Profit": "${:,.0f}",
                    "Margin%": "{:.1f}%"
                }),
                width="stretch",
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
            width="stretch",
            hide_index=True
        )


# =============================================================================
# TAB 6: STRATEGIC RECOMMENDATIONS & SCENARIO SIMULATOR
# =============================================================================
with tabs[5]:
    st.markdown("#### 💡 Executive Action Plan & Financial Scenario Simulator")

    st.markdown(r"""
    ##### 🎯 Answers to Core Business Questions:
    1. **Categories & Sub-Categories:** Technology ($145.5K) and Office Supplies ($122.5K) are star performers. Furniture is an acute drag ($18.5K profit on $742K sales). **Tables** lose **-$17.7K** and **Bookcases** lose **-$3.5K**.
    2. **Discount Dynamics:** Transactions with discounts between 0-20% maintain healthy margins (12-30%). Discounts above 20% experience an **order loss rate over 91.6%**.
    3. **Underperforming Geography:** Texas (-$25.7K), Ohio (-$17.0K), Pennsylvania (-$15.6K), and Illinois (-$12.6K) drag company profit down by **over -$78K**.
    4. **Valuable Customers:** Top 20% of customers account for 73% of total profits. "Champions" and "Loyal Customers" generate >70% of enterprise margin.
    5. **Seasonality:** Q4 holiday shopping surge delivers the largest volume (peaking in November and December).
    6. **Logistics:** Standard class accounts for 60% of volume (avg 5.0 days dispatch); First Class maintains the highest margins (13.9%).
    """)

    st.markdown("---")
    st.markdown("#### 🎛️ Interactive Profit Sensitivity Simulator")

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
        st.markdown("##### Projected Financial Impact")
        r1, r2 = st.columns(2)
        r1.metric("Simulated Net Profit", f"${sim_p:,.0f}", f"{lift_dollar:+,.0f} Lift")
        r2.metric("Profit Lift (%)", f"{lift_pct:+.1f}%", f"{(sim_p/sim_s*100):.1f}% Margin")

    st.success(f"""
    **Executive Policy Recommendation:**
    - Capping commercial discounts at **{cap_discount}%** and eliminating loss-making table SKUs will increase total business profit from **${base_p:,.0f}** to **${sim_p:,.0f}** (a **{lift_pct:+.1f}% increase**).
    - Immediately audit regional sales reps in Texas, Ohio, and Illinois who utilize aggressive discounting to meet top-line sales quotas at the expense of profitability.
    """)
