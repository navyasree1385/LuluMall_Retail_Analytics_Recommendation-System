# 🛍️ Lulu Mall Retail Analytics & Recommendation System

An end-to-end retail analytics project combining **Python, Excel, MySQL/SQL, Power BI, Machine Learning, and Streamlit** to analyze retail transactions and provide product recommendations.

## 🚀 Live Demo

**[Open the Live Recommendation System](https://lulmall-retailanalytics-recommendationsystem.streamlit.app/)**

The deployed application supports:
- Product-based recommendations
- Personalized customer recommendations
- Product search
- Customer profile and purchase history
- Recommendation scores
- Maximum-budget filtering

## 📂 GitHub Repository

**[View the GitHub Repository](https://github.com/navyasree1385/LuluMall_Retail_Analytics_Recommendation-System)**

---

## 📌 Project Overview

```text
Retail Sales Dataset
        ↓
Python Data Cleaning & EDA
        ↓
MySQL Database
        ↓
SQL Sales & Customer Analysis
        ↓
Power BI Dashboard
        ↓
Recommendation System
        ↓
Streamlit Web Application
        ↓
Streamlit Community Cloud
```

The project demonstrates how a retail dataset can support both **business intelligence** and **customer-facing recommendations**.

## 🎯 Objectives

- Clean and prepare retail transaction data
- Perform exploratory analysis using Python
- Analyze sales and customer behavior using SQL
- Build interactive Power BI dashboards
- Develop product and customer recommendations
- Build a Streamlit web application
- Deploy the application online

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Data cleaning, EDA, customer analysis and recommendations |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Cosine similarity |
| MySQL | Database storage and analytics |
| SQL | Sales, customer and advanced analysis |
| Power BI | Interactive dashboards and KPIs |
| Streamlit | Recommendation web application |
| Excel | Source dataset |
| Git/GitHub | Version control |
| Streamlit Community Cloud | Deployment |

## 📊 Dataset

Main dataset:

```text
02_python/Lulu_Mall_Sales_Dataset.xlsx
```

Important fields include:

- Customer_ID
- Order_ID
- Order_Date
- Product_Name
- Product_Category
- Quantity
- Unit_Price
- Revenue
- Store_ID
- Store_Name
- City
- State
- Region
- Payment_Mode
- Customer_Gender
- Month
- Quarter
- Year

## 🐍 Python Analysis

```text
02_python/
├── 01_Data_Cleaning.ipynb
├── 02_Exploratory_Data_Analysis.ipynb
├── 03_Customer_Analysis.ipynb
├── 05_Recommendation_System.ipynb
└── recommendation_app.py
```

The notebooks cover data cleaning, exploratory analysis, customer analysis and recommendation-system development.

## 🗄️ SQL / MySQL

```text
03_SQL/
├── 01_Create_Database.sql
├── 02_Create_Tables.sql
├── 03_load_data.sql
├── 04_Data_Validation.sql
├── 05_Sales_Analysis.sql
├── 06_Customer_Analysis.sql
└── 07_Advanced_Analytics.sql
```

The SQL layer covers database creation, table creation, loading, validation, sales analysis, customer analysis and advanced analytics.

## 📈 Power BI

Power BI file:

```text
04_PowerBI/Lulu_Mall_Retail_Analytics.pbix
```

Dashboard pages:

1. **Executive Overview**
2. **Sales Performance**
3. **Customer Analytics**
4. **Product & Store Analytics**

> The `.pbix` file is intended for Power BI Desktop. The Power BI component is separate from the deployed Streamlit application and may require the MySQL/data environment used during development.

## 🤖 Recommendation System

### Product-Based Recommendations

A customer-product interaction matrix is created using purchase quantity. Product similarity is then calculated using **cosine similarity**.

```text
Customer × Product Matrix
          ↓
Product Similarity
          ↓
Top Similar Products
```

### Personalized Customer Recommendations

Customer recommendations combine:

- Customer similarity
- Product popularity
- Customer category preferences

Previously purchased products are excluded from the recommendation results.

## 🌐 Streamlit Application

Main application:

```text
02_python/recommendation_app.py
```

Features:

- 🛍️ Product-based recommendations
- 👤 Personalized customer recommendations
- 🔎 Product search
- 🧾 Purchase history
- 📊 Customer profile metrics
- ⭐ Recommendation scores
- 💰 Maximum budget filter
- Interactive product cards

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/navyasree1385/LuluMall_Retail_Analytics_Recommendation-System.git
cd LuluMall_Retail_Analytics_Recommendation-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:

```text
streamlit
pandas
numpy
scikit-learn
openpyxl
```

### 3. Verify the dataset

Make sure this file exists:

```text
02_python/Lulu_Mall_Sales_Dataset.xlsx
```

### 4. Run Streamlit

Run this command from the **project root**:

```bash
streamlit run 02_python/recommendation_app.py
```

Then open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## ☁️ Deployment

The recommendation application is deployed using **Streamlit Community Cloud**.

```text
Repository:
navyasree1385/LuluMall_Retail_Analytics_Recommendation-System

Branch:
main

Entrypoint:
02_python/recommendation_app.py
```

The repository contains `requirements.txt` so the cloud environment can install the required Python packages.


## 🔄 Updating the Deployed App

After making code changes:

```bash
git add .
git commit -m "Update recommendation system"
git push origin main
```

The deployed Streamlit application uses the GitHub repository as its source, so pushed changes are picked up by Community Cloud.

## ⚠️ Important Instructions

1. **Keep the dataset in `02_python/`** because the application loads it relative to `recommendation_app.py`.
2. **Run Streamlit from the project root** using:
   ```bash
   streamlit run 02_python/recommendation_app.py
   ```
3. If a new Python package is added, update `requirements.txt` and push the change.
4. Never commit passwords, API keys, database credentials, `.env` files or private tokens.
5. The Streamlit app uses the Excel dataset for recommendations; Power BI is a separate analytics component.

## 📁 Complete Project Structure

```text
LuluMall_Retail_Analytics_Recommendation-System/
│
├── 02_python/
│   ├── output/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   ├── 03_Customer_Analysis.ipynb
│   ├── 05_Recommendation_System.ipynb
│   ├── recommendation_app.py
│   └── Lulu_Mall_Sales_Dataset.xlsx
│
├── 03_SQL/
│   ├── 01_Create_Database.sql
│   ├── 02_Create_Tables.sql
│   ├── 03_load_data.sql
│   ├── 04_Data_Validation.sql
│   ├── 05_Sales_Analysis.sql
│   ├── 06_Customer_Analysis.sql
│   └── 07_Advanced_Analytics.sql
│
├── 04_PowerBI/
│   └── Lulu_Mall_Retail_Analytics.pbix
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 💼 Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis
- Retail Sales Analytics
- Customer Analytics
- SQL and MySQL
- Python
- Pandas and NumPy
- Scikit-learn
- Cosine Similarity
- Collaborative Filtering
- Hybrid Recommendation Ranking
- Power BI
- Dashboard Development
- Streamlit
- Git/GitHub
- Cloud Deployment

## 🎓 Interview Explanation

> I developed an end-to-end retail analytics solution using a Lulu Mall sales dataset. I cleaned and analyzed the data using Python, stored and validated it using MySQL, performed sales and customer analysis using SQL, and created interactive Power BI dashboards. I then developed a recommendation system using customer-product purchase patterns and cosine similarity, enhanced the customer recommendations with popularity and category preferences, built a Streamlit interface, and deployed the application using Streamlit Community Cloud.

## 🔗 Project Links

- **Live Demo:** https://lulmall-retailanalytics-recommendationsystem.streamlit.app/
- **GitHub:** https://github.com/navyasree1385/LuluMall_Retail_Analytics_Recommendation-System

## 📌 Project Status

**Completed and Deployed 🚀**

