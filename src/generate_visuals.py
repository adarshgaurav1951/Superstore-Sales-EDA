"""Visual Generation Suite for Superstore Sales EDA.

Creates 9 high-resolution (300 DPI) publication-quality figures
saved into the `visuals/` directory.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def setup_style():
    """Configure modern aesthetic styling for matplotlib and seaborn."""
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["grid.color"] = "#F1F5F9"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["figure.titlesize"] = 14
    plt.rcParams["figure.titleweight"] = "bold"


def generate_all_visuals(featured_path: str = "data/cleaned/superstore_featured.csv",
                         rfm_path: str = "data/cleaned/customer_rfm.csv",
                         output_dir: str = "visuals"):
    """Generate and save all 9 analytical charts."""
    setup_style()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(featured_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    rfm = pd.read_csv(rfm_path)

    # -------------------------------------------------------------
    # Visual 1: Sales and Profit by Category
    # -------------------------------------------------------------
    print("[1/9] Generating Visual 1: Sales & Profit by Category...")
    cat = df.groupby("Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    cat["Margin%"] = (cat["Profit"] / cat["Sales"]) * 100

    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
    x = np.arange(len(cat))
    width = 0.35

    rects1 = ax1.bar(x - width/2, cat["Sales"] / 1e3, width, label="Gross Sales ($K)", color="#3B82F6")
    rects2 = ax1.bar(x + width/2, cat["Profit"] / 1e3, width, label="Net Profit ($K)", color="#10B981")

    ax1.set_ylabel("Amount in USD ($ Thousands)", fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_title("Gross Sales vs Net Profit by Category", fontsize=13, fontweight="bold", pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat["Category"], fontsize=11, fontweight="bold")
    ax1.legend(frameon=True, facecolor="white", framealpha=0.9)

    # Margin labels above profit bars
    for idx, (p_bar, margin) in enumerate(zip(rects2, cat["Margin%"])):
        ax1.annotate(f"{margin:.1f}% margin",
                     xy=(p_bar.get_x() + p_bar.get_width() / 2, p_bar.get_height()),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=10, fontweight="bold", color="#0F766E")

    plt.tight_layout()
    fig.savefig(out / "01_sales_profit_by_category.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 2: Sub-Category Profitability (Diverging Bar Chart)
    # -------------------------------------------------------------
    print("[2/9] Generating Visual 2: Sub-Category Profitability...")
    sub = df.groupby(["Category", "Sub-Category"]).agg({"Profit": "sum"}).reset_index()
    sub = sub.sort_values(by="Profit", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    colors = ["#EF4444" if p < 0 else "#10B981" if p > 30000 else "#6366F1" for p in sub["Profit"]]

    bars = ax.barh(sub["Sub-Category"], sub["Profit"] / 1e3, color=colors, edgecolor="none", height=0.7)
    ax.axvline(0, color="#475569", linestyle="-", linewidth=1.2)
    ax.set_xlabel("Net Profit ($ Thousands)", fontsize=11, fontweight="bold")
    ax.set_title("Sub-Category Profit Ranking: Severe Loss Leaks in Tables & Bookcases",
                 fontsize=13, fontweight="bold", pad=15)

    for bar, val in zip(bars, sub["Profit"] / 1e3):
        ha = "left" if val >= 0 else "right"
        offset = 0.5 if val >= 0 else -0.5
        ax.annotate(f"${val:+.1f}K",
                    xy=(val + offset, bar.get_y() + bar.get_height() / 2),
                    va="center", ha=ha, fontsize=9, fontweight="bold",
                    color="#1E293B" if val >= 0 else "#DC2626")

    plt.tight_layout()
    fig.savefig(out / "02_subcategory_profitability.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 3: Discount vs Profit Margin (The Tipping Point)
    # -------------------------------------------------------------
    print("[3/9] Generating Visual 3: Discount vs Profit Margin...")
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sns.scatterplot(
        data=df,
        x="Discount",
        y="Profit_Margin",
        hue="Category",
        alpha=0.45,
        palette={"Technology": "#3B82F6", "Office Supplies": "#8B5CF6", "Furniture": "#F97316"},
        ax=ax
    )
    ax.axhline(0, color="#EF4444", linestyle="--", linewidth=1.5, label="Break-Even Threshold (0% Margin)")
    ax.axvline(0.20, color="#B91C1C", linestyle=":", linewidth=1.5, label="Critical Cliff (20% Discount)")

    ax.set_ylim(-3.0, 1.0)
    ax.set_xlabel("Discount Rate Applied (0.0 to 0.8)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Profit Margin Ratio (Profit / Sales)", fontsize=11, fontweight="bold")
    ax.set_title("The Profit Cliff: Discounts Beyond 20% Almost Universally Destroy Margin",
                 fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower left", frameon=True, facecolor="white")

    plt.tight_layout()
    fig.savefig(out / "03_discount_vs_profit_margin.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 4: Loss Rate by Discount Bucket
    # -------------------------------------------------------------
    print("[4/9] Generating Visual 4: Loss-Making Order Rate by Discount Bucket...")
    disc_grp = df.groupby("Discount_Bucket", observed=False).agg(
        Total_Orders=("Row ID", "count"),
        Loss_Orders=("Is_Loss", "sum"),
        Net_Profit=("Profit", "sum")
    ).reset_index()
    disc_grp["Loss_Rate%"] = (disc_grp["Loss_Orders"] / disc_grp["Total_Orders"]) * 100

    fig, ax1 = plt.subplots(figsize=(8.5, 5), dpi=300)
    colors = ["#10B981", "#FBBF24", "#F97316", "#EF4444"]
    bars = ax1.bar(disc_grp["Discount_Bucket"].astype(str), disc_grp["Loss_Rate%"],
                   color=colors, width=0.55, edgecolor="#334155")

    ax1.set_ylabel("Loss-Making Order Rate (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_title("Order Loss-Rate Escalation Across Promotional Discount Buckets",
                  fontsize=13, fontweight="bold", pad=15)
    ax1.set_ylim(0, 115)

    for bar, rate, loss_orders, profit in zip(bars, disc_grp["Loss_Rate%"], disc_grp["Loss_Orders"], disc_grp["Net_Profit"]):
        ax1.annotate(f"{rate:.1f}%\n({loss_orders} orders)\nNet: ${profit/1e3:+.1f}K",
                     xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     xytext=(0, 5), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#0F172A")

    plt.tight_layout()
    fig.savefig(out / "04_loss_rate_by_discount_bucket.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 5: State Profitability Champions vs Drainers
    # -------------------------------------------------------------
    print("[5/9] Generating Visual 5: State Profitability Champions vs Drainers...")
    state_p = df.groupby("State").agg({"Profit": "sum"}).reset_index()
    top10_states = state_p.sort_values(by="Profit", ascending=False).head(10)
    bottom10_states = state_p.sort_values(by="Profit", ascending=True).head(10)
    combined_states = pd.concat([bottom10_states, top10_states]).sort_values(by="Profit")

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    bar_colors = ["#EF4444" if p < 0 else "#10B981" for p in combined_states["Profit"]]
    bars = ax.barh(combined_states["State"], combined_states["Profit"] / 1e3, color=bar_colors, height=0.65)
    ax.axvline(0, color="#475569", linestyle="-", linewidth=1.2)
    ax.set_xlabel("Net Profit ($ Thousands)", fontsize=11, fontweight="bold")
    ax.set_title("Geographic Polarization: Top 10 Champions vs Bottom 10 Loss States",
                 fontsize=13, fontweight="bold", pad=15)

    for bar, val in zip(bars, combined_states["Profit"] / 1e3):
        ha = "left" if val >= 0 else "right"
        offset = 1.0 if val >= 0 else -1.0
        ax.annotate(f"${val:+.1f}K",
                    xy=(val + offset, bar.get_y() + bar.get_height() / 2),
                    va="center", ha=ha, fontsize=8.5, fontweight="bold",
                    color="#1E293B" if val >= 0 else "#DC2626")

    plt.tight_layout()
    fig.savefig(out / "05_state_profitability_top_bottom.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 6: Monthly Sales & Profit Trend (Seasonality)
    # -------------------------------------------------------------
    print("[6/9] Generating Visual 6: Monthly Sales & Profit Trend...")
    monthly = df.set_index("Order Date").resample("ME").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    monthly["Sales_MA3"] = monthly["Sales"].rolling(3).mean()

    fig, ax1 = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax2 = ax1.twinx()

    line1 = ax1.plot(monthly["Order Date"], monthly["Sales"] / 1e3, color="#3B82F6", marker="o",
                     linewidth=2, label="Monthly Sales ($K)")
    line2 = ax1.plot(monthly["Order Date"], monthly["Sales_MA3"] / 1e3, color="#93C5FD", linestyle="--",
                     linewidth=1.5, label="Sales 3-Month Moving Avg ($K)")
    line3 = ax2.plot(monthly["Order Date"], monthly["Profit"] / 1e3, color="#10B981", marker="s",
                     linewidth=2, label="Monthly Profit ($K)")

    ax1.set_ylabel("Gross Sales ($ Thousands)", fontsize=11, fontweight="bold", color="#1D4ED8")
    ax2.set_ylabel("Net Profit ($ Thousands)", fontsize=11, fontweight="bold", color="#047857")
    ax1.set_title("Time Series & Seasonality: Strong Q4 Holiday Spikes across 2014-2017",
                  fontsize=13, fontweight="bold", pad=15)

    # Combine legends
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=True, facecolor="white")

    plt.tight_layout()
    fig.savefig(out / "06_monthly_sales_profit_trend.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 7: Shipping Lead Times by Mode
    # -------------------------------------------------------------
    print("[7/9] Generating Visual 7: Shipping Lead Times by Mode...")
    fig, (ax_box, ax_vol) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300, gridspec_kw={"width_ratios": [1.5, 1]})

    palette_ship = ["#6366F1", "#3B82F6", "#06B6D4", "#10B981"]
    sns.boxplot(data=df, x="Ship Mode", y="Shipping_Days", palette=palette_ship, ax=ax_box, width=0.5)
    ax_box.set_ylabel("Lead Time (Days to Ship)", fontsize=10, fontweight="bold")
    ax_box.set_xlabel("Fulfillment Tier", fontsize=10, fontweight="bold")
    ax_box.set_title("Delivery Lead Time Distribution", fontsize=12, fontweight="bold")

    # Volume pie/bar
    ship_counts = df["Ship Mode"].value_counts()
    ax_vol.pie(ship_counts, labels=ship_counts.index, autopct="%1.1f%%",
               colors=palette_ship, startangle=140,
               wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2))
    ax_vol.set_title("Order Volume Share (%)", fontsize=12, fontweight="bold")

    plt.suptitle("Logistics Performance: Standard Class Leads Volume (59.7%) with 5-Day Mean Dispatch",
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(out / "07_shipping_lead_time_by_mode.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 8: Customer RFM Segmentation Matrix
    # -------------------------------------------------------------
    print("[8/9] Generating Visual 8: Customer RFM Segmentation...")
    rfm_summary = rfm.groupby("RFM_Segment").agg(
        Customer_Count=("Customer ID", "count"),
        Total_Sales=("Monetary_Sales", "sum"),
        Total_Profit=("Monetary_Profit", "sum")
    ).reset_index()
    rfm_summary["Margin%"] = (rfm_summary["Total_Profit"] / rfm_summary["Total_Sales"]) * 100
    rfm_summary = rfm_summary.sort_values(by="Total_Sales", ascending=False)

    fig, ax1 = plt.subplots(figsize=(9.5, 5), dpi=300)
    bars = ax1.bar(rfm_summary["RFM_Segment"], rfm_summary["Total_Sales"] / 1e3, color="#6366F1", width=0.55)
    ax1.set_ylabel("Total Lifetime Sales ($K)", fontsize=11, fontweight="bold", color="#4338CA")
    ax1.set_xticklabels(rfm_summary["RFM_Segment"], rotation=20, ha="right", fontsize=9.5, fontweight="bold")
    ax1.set_title("Customer RFM Value Breakdown: Champions & Loyalists Power 70%+ of Revenue",
                  fontsize=13, fontweight="bold", pad=15)

    for bar, count, margin in zip(bars, rfm_summary["Customer_Count"], rfm_summary["Margin%"]):
        ax1.annotate(f"{count} Custs\n{margin:.1f}% Margin",
                     xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1E293B")

    plt.tight_layout()
    fig.savefig(out / "08_customer_rfm_segments.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Visual 9: Correlation Matrix Heatmap
    # -------------------------------------------------------------
    print("[9/9] Generating Visual 9: Correlation Heatmap...")
    numeric_cols = ["Sales", "Quantity", "Discount", "Profit", "Profit_Margin", "Shipping_Days"]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(7.5, 6), dpi=300)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Feature Correlation Heatmap: Strong Negative Link Between Discount & Margin",
                 fontsize=12, fontweight="bold", pad=15)

    plt.tight_layout()
    fig.savefig(out / "09_correlation_matrix.png")
    plt.close(fig)

    print("Successfully generated all 9 visuals into 'visuals/'!\n")


if __name__ == "__main__":
    generate_all_visuals()
