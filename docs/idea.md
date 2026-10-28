# Superstore Sales - EDA: Project Idea

## 1. One-Line Idea
Perform exploratory data analysis on retail sales data by handling missing values, engineering features, and creating business dashboards for actionable insights.

## 2. Problem Statement
A retail business records thousands of orders across products, regions, customers, and shipping modes, but raw sales tables do not show what drives profit, where money is being lost, or which customers and products matter most. This project turns raw order data into clear findings and recommendations that managers can act on.

## 3. Goals
- Clean the data and handle missing values, duplicates, and wrong data types
- Engineer features that explain sales and profit (profit margin, shipping days, discount bucket, time features)
- Identify top and bottom performing products, categories, regions, and customers
- Understand how discounts, shipping mode, and segment affect profit
- Build a business dashboard with KPIs and filters
- Turn findings into specific, actionable recommendations

## 4. Key Business Questions
1. Which categories and sub-categories generate the most profit, and which lose money?
2. How do discounts affect profit and profit margin?
3. Which regions and states underperform?
4. Who are the most valuable customers and segments?
5. What are the monthly, quarterly, and yearly sales trends? Is there seasonality?
6. Does shipping mode affect delivery time or profitability?
7. Which products are frequently sold at a loss?
8. What should the business change to increase profit?

## 5. Target Users
- Business managers, sales and marketing teams, and category owners who need insights
- Students and aspiring data analysts building a portfolio project

## 6. Data
- **Dataset:** Sample - Superstore (Tableau Public or Kaggle), about 9,994 orders and 21 columns
- **Columns:**
  - Order: Order ID, Order Date, Ship Date, Ship Mode
  - Customer: Customer ID, Customer Name, Segment
  - Location: Country, City, State, Postal Code, Region
  - Product: Product ID, Category, Sub-Category, Product Name
  - Numbers: Sales, Quantity, Discount, Profit
- **Notes:** the classic version has few missing values (sometimes only Postal Code). Check for nulls anyway and document the result. Raw data is never modified.

## 7. Approach (Workflow)
1. **Define** business questions and success criteria
2. **Load and inspect** the data (shape, dtypes, nulls, duplicates)
3. **Clean** (missing values, duplicates, date conversion, data types, impossible values)
4. **Feature engineering**
   - Profit margin = Profit / Sales
   - Order year, month, quarter, weekday
   - Shipping days = Ship Date - Order Date
   - Discount bucket (0%, 1-20%, 20-50%, 50%+)
   - Loss-making flag
   - Customer-level RFM (recency, frequency, monetary)
5. **Exploratory analysis**
   - Univariate: distributions of sales, profit, discount, quantity
   - Bivariate: discount vs. profit, category vs. margin, region vs. sales
   - Time series: monthly and yearly trends
   - Correlation heatmap
6. **Dashboard:** KPI tiles, trend lines, category and region breakdowns, top and bottom products, filters
7. **Insights and recommendations:** each finding linked to a business question
8. **Documentation:** notebooks, README, dashboard screenshots

## 8. Tech Stack
| Purpose | Tools |
|---|---|
| Language | Python 3.10+ |
| Data handling | pandas, NumPy |
| Visualization | matplotlib, seaborn, plotly |
| Dashboard | Streamlit |
| Environment | Jupyter Notebook / Google Colab, Antigravity IDE |
| Version control | Git and GitHub |
| Optional | scikit-learn for segmentation |

## 9. Planned Deliverables
- Cleaned and feature-engineered dataset in `data/cleaned/`
- Notebooks: `01_cleaning`, `02_features`, `03_eda`, `04_insights`
- Business dashboard (Streamlit)
- Visualizations saved in `visuals/`
- `README.md` with problem, method, key findings, and screenshots
- Business recommendations report in `reports/`

## 10. Project Structure
```
superstore-sales-eda/
├── data/
│   ├── raw/
│   │   └── Sample - Superstore.csv
│   └── cleaned/
│       ├── superstore_cleaned.csv
│       ├── superstore_featured.csv
│       └── customer_rfm.csv
├── notebooks/
│   ├── 01_cleaning.ipynb
│   ├── 02_features.ipynb
│   ├── 03_eda.ipynb
│   └── 04_insights.ipynb
├── dashboard/
│   └── app.py
├── visuals/
├── docs/
│   ├── idea.md
│   ├── PRD.md
│   ├── DATABASE.md
│   └── AGENTS.md
├── reports/
│   └── business_recommendations.md
├── README.md
└── requirements.txt
```
