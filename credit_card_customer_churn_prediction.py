# -*- coding: utf-8 -*-
"""Credit_Card_Customer_Churn_Prediction.ipynb

Original file is located at
    https://colab.research.google.com/drive/1qxZYqOFsH-BcehX4aYicINIeAg4jU0aX

# Step 1: Environment Setup & Data Loading
"""

import pandas as pd
import sqlite3

# Load the dataset verbatim
df = pd.read_csv('/content/BankChurners.csv')
print(df.head())

# Create an in-memory SQL database for analysis
conn = sqlite3.connect(':memory:')
df.to_sql('bank_churners', conn, index=False, if_exists='replace')

"""# Step 2: High-Level Churn Analysis (SQL)
We use SQL to perform the heavy lifting of data aggregation. This query calculates the key behavioral differences between customers who stayed and those who left (churned).
"""

sql_query = """
SELECT
    Attrition_Flag,
    COUNT(*) as Total_Customers,
    ROUND(AVG(Total_Trans_Amt), 2) as Avg_Transaction_Amount,
    ROUND(AVG(Total_Trans_Ct), 2) as Avg_Transaction_Count,
    ROUND(AVG(Avg_Utilization_Ratio), 3) as Avg_Utilization
FROM bank_churners
GROUP BY Attrition_Flag;
"""

churn_analysis_df = pd.read_sql_query(sql_query, conn)
print(churn_analysis_df)

"""# Step 3: Targeted Demographic Segmentation (SQL)
To help Harbor Trust Bank focus its retention efforts, we can identify which demographic groups are highest at risk.
"""

# Identify segments with high churn rates
sql_demographics = """
SELECT
    Income_Category,
    Card_Category,
    COUNT(*) as Total,
    SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) as Churned
FROM bank_churners
GROUP BY Income_Category, Card_Category
ORDER BY Churned DESC
LIMIT 5;
"""
print(pd.read_sql(sql_demographics, conn))
# behavioral_results = pd.read_sql(behavioral_sql, conn)

# --- STEP 4: SQL ANALYSIS (Behavioral Metrics) ---
# We compare engagement levels between existing and churned customers[cite: 1]
behavioral_sql = """
SELECT
    Attrition_Flag,
    COUNT(*) as Total_Customers,
    ROUND(AVG(Total_Trans_Ct), 1) as Avg_Trans_Count,
    ROUND(AVG(Total_Trans_Amt), 2) as Avg_Trans_Amt,
    ROUND(AVG(Avg_Utilization_Ratio), 3) as Avg_Utilization
FROM bank_churners
GROUP BY Attrition_Flag;
"""
behavioral_results = pd.read_sql(behavioral_sql, conn)

# --- STEP 5: PYTHON VISUALIZATION (Engagement Trends) ---
# Creating a density plot to see where transaction counts drop off[cite: 1]
plt.figure(figsize=(10, 5))
sns.kdeplot(data=df, x='Total_Trans_Ct', hue='Attrition_Flag', fill=True, palette='viridis')
plt.title('Engagement Level: Total Transaction Count Distribution')
plt.xlabel('Number of Transactions (Last 12 Months)')
plt.ylabel('Density')
plt.savefig('transaction_distribution.png')

# --- STEP 6: OUTPUT RESULTS ---
print("Analysis Results:\n", behavioral_results)

# Load and prepare data
df = pd.read_csv('BankChurners.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('bank_churners', conn, index=False, if_exists='replace')

# SQL Query for Heatmap data: Churn Rate by Income and Education
# This helps identify the most vulnerable customer segments
sql_heatmap = """
SELECT
    Income_Category,
    Education_Level,
    ROUND(CAST(SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as Churn_Rate
FROM bank_churners
GROUP BY Income_Category, Education_Level
"""
heatmap_data = pd.read_sql(sql_heatmap, conn)

# Pivot data for the heatmap
pivot_table = heatmap_data.pivot(index='Income_Category', columns='Education_Level', values='Churn_Rate')

# Create the visualization
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, cmap='YlOrRd', fmt='.1f', linewidths=.5)
plt.title('Heatmap: Churn Rate (%) by Income and Education Level')
plt.xlabel('Education Level')
plt.ylabel('Income Category')
plt.tight_layout()
plt.savefig('churn_heatmap.png')
plt.show()

# Advanced SQL: Feature Correlation Analysis
# We'll look at Relationship count vs Churn
rel_query = """
SELECT
    Total_Relationship_Count,
    AVG(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1.0 ELSE 0.0 END) * 100 as Churn_Rate
FROM bank_churners
GROUP BY Total_Relationship_Count
ORDER BY Total_Relationship_Count;
"""
rel_df = pd.read_sql(rel_query, conn)

# Advanced Python: Correlation Heatmap
# Select only numeric columns for correlation
numeric_df = df.select_dtypes(include=['number']).drop(columns=['CLIENTNUM'])
plt.figure(figsize=(12, 10))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Matrix')
plt.savefig('correlation_matrix.png')

print("Churn Rate by Total Number of Products Held:")
print(rel_df)