# Credit_Card_Customer_Churn_prediction

Harbor Trust BankThis project analyzes the factors leading to customer attrition at Harbor Trust Bank. By leveraging SQL for data manipulation and Python for advanced visualization and analysis, we have identified key behavioral "red flags" and high-risk demographic segments to help the bank improve retention strategies.

## 📊 Project Overview
The primary goal is to minimize revenue loss by identifying customers likely to leave credit card services. The analysis focuses on demographic traits and transaction behavior to understand why customers opt out.  

Key Performance Indicators (KPIs)

Based on the analysis of BankChurners.csv:  

Churn Rate: ~16.1% of the total customer base.  
Transaction Threshold: Churned customers typically stop engaging once their annual transaction count drops below 50.  
Product Stickiness: Customers with 3 or more bank products show a significantly higher retention rate than those with only 1 or 2.  

## 🛠️ Technical Implementation

The project is contained within credit_card_customer_churn_prediction.py and follows a structured data science workflow:  
1. Data ProcessingPython: Loads raw CSV data and performs initial cleaning.  SQL (SQLite3): An in-memory database is used to perform high-speed aggregations and complex joins on customer data.
2. Behavioral SQL AnalysisWe use SQL to isolate the financial differences between existing and churned customers:  SQLSELECT Attrition_Flag, 
       AVG(Total_Trans_Ct) as Avg_Trans, 
       AVG(Avg_Utilization_Ratio) as Avg_Usage
FROM bank_churners
GROUP BY Attrition_Flag;

## 🔍 Visual Insights

Our analysis produced several key visualizations to assist bank management:  
Heatmaps: Correlating Income and Education Level to identify "at-risk" segments like Doctorate holders in the <$40K bracket.  
Distribution Plots: Highlighting the "Engagement Gap" where churned customers peak at low transaction volumes.  
Correlation Matrix: Showing the strong relationship between transaction count and total amount.  

## 💡 Strategic Recommendations

Re-activation Campaigns: Target customers whose transaction counts drop month-over-month before they reach the "churn zone" of 40-50 transactions.  
Cross-Selling Incentives: Offer benefits for opening a third or fourth product, as this drastically reduces the probability of leaving.  
Utilization Boost: Encourage card usage for daily small-ticket items to increase the utilization ratio, which is currently low (16%) among churners.  

## 🚀 Getting StartedTo replicate this analysis, ensure you have the BankChurners.csv file in your directory and run:
python credit_card_customer_churn_prediction.py
