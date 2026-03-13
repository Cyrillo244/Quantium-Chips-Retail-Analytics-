# Quantium-Chips-Retail-Analytics-
A retail data analytics project

### Table of Contents


### Project Overview 
- This project identifies customer segments through purchase behaviour
- Aims to analyse transaction and customer data of chip stores to identify trends and inconsistencies
- Develop metrics and examine sales drivers to gain insights into overall sales performance
- Create visualisations and prepare findings to formulate a clear recommendation for the client's strategy

### Data Sources 
The dataset used for this analysis is the "data.csv" file, containing detailed information about:
- date of each transaction
- different store numbers
- distinct loyalty card number for each customer
- different types of products
- number of transactions purchased by a customer on a particular day
- transaction IDs
- sales per transaction
- units sold per transaction

### Tools
- Excel - Data visualisation (bubble chart)
- Jupyter Notebook - Data exploration,  text preprocessing
- Python Google Colab - Data analysis
- SQL - Google Colab Duckdb
- Power BI
- Microsoft PowerPoint

### Technical Highlights 
**Setting up RFM model**
```sql
# RFM Segmentation (Recency, Frequency, Monetary)
query_rfm = """
WITH customer_rfm AS (
    SELECT
        LYLTY_CARD_NBR,
        MAX(DATE) AS last_purchase,
        COUNT(DISTINCT TXN_ID) AS frequency,
        SUM(TOT_SALES) AS monetary
    FROM df
    GROUP BY LYLTY_CARD_NBR
),
recency_calc AS (
    SELECT
        LYLTY_CARD_NBR,
        date_diff('day', last_purchase, (SELECT MAX(DATE) FROM df)) AS recency,
        frequency,
        monetary
    FROM customer_rfm
)
SELECT
    LYLTY_CARD_NBR,
    recency,
    frequency,
    monetary
FROM recency_calc
ORDER BY monetary DESC
LIMIT 20
"""
df_rfm = duckdb.query(query_rfm).to_df()
df_rfm
```

**Using Pearson Correlation to find control stores for the given trial stores**
```python
#  Correlation function
def calculate_correlation(df, metricCol, storeComparison):
    rows = []
    # months for this trial store (should be complete)
    trial_series = df[df['STORE_NBR'] == storeComparison][['YEARMONTH', metricCol]]
    for s in df['STORE_NBR'].unique():
        if s == storeComparison:
            continue
        control_series = df[df['STORE_NBR'] == s][['YEARMONTH', metricCol]]
        merged = pd.merge(trial_series, control_series, on='YEARMONTH', how='inner', suffixes=('_trial','_control'))
        # require all months present
        if len(merged) == 0:
            continue
        corr = np.nan
        try:
            corr, _ = pearsonr(merged[f"{metricCol}_trial"], merged[f"{metricCol}_control"])
        except Exception:
            corr = np.nan
        rows.append({'Store1': storeComparison, 'Store2': s, 'corr_measure': corr})
    return pd.DataFrame(rows)
```

### Data Visualisation 






### Data Cleaning / Preparation 
Data preparation and transformation were performed in **Jupyter Notebook**:
- preprocessed text data in the **PROD_NAME** column by removing punctuation and correcting wrongly spelt words
- extracted **brand names** from the PROD_NAME to know the **top product brands** by  finding their value counts
- cleaned the PROD_NAME column by word mapping,  whereby the wrong words were replaced with the right ones
- Checked for missing values and duplicates and removed them
- Merged the transaction dataset with the purchase behaviour dataset to make the dataset complete for other analyses like RFM, etc

### Analytics and Modelling 
1. First of all, the metrics baseline was set up:
   - Calculated the average sales per transaction
   - Calculated the average sold quantities per transaction
   - Calculated the average sales or transactions per month
   - Calculated the average sales or transactions per store

2. Metrics deep-dive 
   - calculated the month-on-month (MoM) sales trend
   - Calculated total sales per store and number of transactions per store to analyse the performance of all stores
   - Calculated the total quantities per product and the total sales per product to identify popular and unpopular product  brands

3. Customer analysis 
   - calculated Repeat customers proportion and KPI performance
   - checked customer distribution and performance by 'Lifestage' and 'Premium' level
   - Calculated targeting strategies based on  'Lifestage' or 'Premium'
   - performed customer segmentation based on RFM, recency, frequency, and monetary value

4. A/B testing analysis (Python)
   - selected the control groups to compare with the trial groups
   - Determine comparable groups, based on similar metrics, eg, total sales revenue, total number of customers, and average number of transactions per customer. 
   - used Pearson correlations and magnitude distance
   - Assessed trial group, stores 77, 86 and 88, each store individually based on total sales
   - Statistical testing (T-Test)
   - Summarised findings for each store and provided a recommendation outlining the impact on sales during the trial period. 
   - checked if the driver of sales change is more purchasing customers or more purchases per customer

5. Visualisation and Reporting
    - Power BI was used to create all the charts that were used in the PowerPoint slides 


### Results and Findings
- The highest monthly sale was $156k in 12-2018 according to the MoM trend
- The average sales across the whole period(1 year) was $150k
- The highest MoM % sales was 10.89%
- The average sales per transaction was $7.32 and the average quantity sold per transaction was 1.91 ~ 2 packs of chips 



### Recommendations
