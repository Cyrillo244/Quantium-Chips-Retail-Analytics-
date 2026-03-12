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


### Data Cleaning / Preparation 
Data preparation and transformation were performed in **Jupyter Notebook**:
- preprocessed text data in the **PROD_NAME** column by removing punctuation and correcting wrongly spelt words
- extracted **brand names** from the PROD_NAME to know the **top product brands** by  finding their value counts
- cleaned the PROD_NAME column by word mapping,  whereby the wrong words were replaced with the right ones
- Checked for missing values and duplicates and removed them
- Merged the transaction dataset with the purchase behaviour dataset to make the dataset complete for other analyses like RFM, etc

### Analytics and Modelling 
First of all, the metrics baseline was set up:
- Average sales per transaction
- Average sold quantities per transaction
- Average sales or transactions per month
- Average sales or transactions per store

Metrics deep-dive 
- MoM sales trend
- By store level, distribution, high vs. low performance stores
- By product name level, popular vs. unpopular brands

