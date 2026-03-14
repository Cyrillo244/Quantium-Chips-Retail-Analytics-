#!/usr/bin/env python
# coding: utf-8

# # Analytics Project

# In[1]:


# import important libraries
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import re 
from scipy import stats
from datetime import datetime

# Plot style 
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12,5)


# In[2]:


import os 
fp = str(os.getcwd())
print(fp)


# In[ ]:





# In[ ]:





# In[3]:


# Load dataset into dataframe 
# Read files 
txn_data = pd.read_csv(fp + "\\QVI_transaction_data1.csv")
cust_data = pd.read_csv(fp + "\\QVI_purchase_behaviour1.csv")


# In[4]:


txn_data


# In[ ]:





# In[5]:


cust_data


# In[ ]:





# In[6]:


# Checking length of dataset
len_txn = len(txn_data)
len_txn


# In[7]:


# Checking length of dataset
len_cust = len(cust_data)
len_cust


# In[ ]:





# In[8]:


# Inspect data 
t_inf = txn_data.info()
t_inf


# In[9]:


txn_data.head(10)


# In[ ]:





# In[10]:


c_inf = cust_data.info()


# In[11]:


cust_data.head(10)


# In[ ]:





# In[12]:


# Print the earliest and latest dates in the 'DATE' column 
print("Date range:", txn_data['DATE'].min(), "to", txn_data['DATE'].max())


# In[13]:


# Ensure PROD_NAME exist
if 'PROD_NAME' not in txn_data.columns:
    raise KeyError("PROD_NAME column not found in transactionData. Please check CSV columns.")
    
txn_data['PROD_NAME_LOWER'] = txn_data['PROD_NAME'].astype(str).str.lower()

# Split into words and build frequency
words = txn_data['PROD_NAME_LOWER'].str.replace(r'[^a-z0-9\s]', ' ', regex=True).str.split()
all_words = [w for sub in words.dropna() for w in sub] 
word_freq = pd.Series(all_words).value_counts().reset_index()
word_freq.columns = ['word', 'count']
print("\nTop product words:\n", word_freq.head(40))


# In[ ]:





# In[14]:


# Remove salsa products
txn_data = txn_data[~txn_data['PROD_NAME_LOWER'].str.contains('salsa', na=False)].copy()
print("Rows after removing 'salsa products:", len(txn_data))


# In[ ]:





# In[15]:


# Summary and detect outliers in quantity (PROD_QTY)

#Ensure PROD_QTY column exists
if 'PROD_QTY' not in txn_data.columns:
    raise KeyError("PROD_QTY column not found in txn_data.")

# View summary statistics for quantity
print(txn_data['PROD_QTY'].describe())

# Filter rows where quantity is >= 200
outliers_200 = txn_data[txn_data['PROD_QTY'] >=200].copy()

# Number of such rows 
print("Rows with PROD_QTY >= 200: ", len(outliers_200))

# Preview the outlier rows
display(outliers_200.head(10))


# In[ ]:





# In[16]:


# Define priority columns 
qty_col = 'PROD_QTY'
loyalty_col = 'LYLTY_CARD_NBR'
pp = txn_data[txn_data[loyalty_col] == 226000]
pp


# In[ ]:





# In[17]:


# Define priority columns 
qty_col = 'PROD_QTY'
loyalty_col = 'LYLTY_CARD_NBR'

# Find customers who bought 200 or more chips in a transaction 
customers_to_drop = txn_data.loc[
    txn_data[qty_col] >= 200,
    loyalty_col
].unique() 

print("Customers to drop (high-qty):", customers_to_drop)

# Remove all transactions from these customers 
txn_data = txn_data[
    ~txn_data[loyalty_col].isin(customers_to_drop)
].copy()

print("Rows after dropping those customers:", len(txn_data))


# In[ ]:





# In[18]:


customers_to_drop


# In[19]:


pp = txn_data[txn_data[loyalty_col] == 226000]
pp


# In[ ]:





# In[20]:


txn_data['DATE'].dtype


# In[ ]:





# In[21]:


# Count number of transaction lines per DATE to see if any dates are missing
txn_by_day = txn_data.groupby('DATE').size().reset_index(name='N').sort_values('DATE')

# Ensure DATE is datetime in txn_by_day
txn_by_day['DATE'] = pd.to_datetime(txn_by_day['DATE'])

print("Distinct dates:", len(txn_by_day))

display(txn_by_day.head(10))

# Generate full date range 1 July 2018 -> 30 June 2019
full_range = pd.DataFrame({'DATE': pd.date_range(start='2018-07-01', end='2019-06-30')})

txn_by_day_full = full_range.merge(txn_by_day, on='DATE', how='left').fillna({'N':0})

print('Full range rows:', len(txn_by_day_full))


# In[ ]:





# In[22]:


display(txn_by_day.head(30))


# In[23]:


display(txn_by_day.tail(30))


# In[ ]:





# In[24]:


print(txn_by_day_full)


# In[ ]:





# In[25]:


zero_txn_days = txn_by_day_full[
    txn_by_day_full['N'] == 0
]

len(zero_txn_days)


# In[ ]:





# In[26]:


print(txn_by_day_full.head(30))


# In[27]:


print(txn_by_day_full.tail(30))


# In[ ]:





# In[28]:


# Plot a line chart: transactions per day, with monthly x-axis ticks. 
plt.figure(figsize=(14,4))
plt.plot(txn_by_day_full['DATE'], txn_by_day_full['N'], linewidth=1)
plt.title('Transactions over time')
plt.xlabel('Day')
plt.ylabel('Number of transactions')
plt.xticks(pd.date_range(start='2018-07-01', end='2019-06-30', freq='1M'), rotation=90)
plt.tight_layout()
plt.show()


# In[ ]:





# In[29]:


# Analysing Zero sales days in December
mask_dec = (txn_by_day_full['DATE'] >= '2018-12-01') & (txn_by_day_full['DATE'] <= '2018-12-31')
plt.figure(figsize=(12,3))
plt.plot(txn_by_day_full.loc[mask_dec, 'DATE'], txn_by_day_full.loc[mask_dec, 'N'], marker='o')
plt.title('Transactions in December 2018')
plt.xticks(rotation=90)
plt.ylabel('Number of transactions')
plt.tight_layout()
plt.show()


# In[ ]:





# In[30]:


# We use regex to find the first number in the product name and interpret it as grams.

def digit_extxn(s):
    if pd.isna(s):
        return np.nan
    m = re.search(r'(\d+)', str(s))
    return int(m.group(1)) if m else np.nan

txn_data['PACK_SIZE'] = txn_data['PROD_NAME'].apply(digit_extxn)
display(txn_data['PACK_SIZE'].value_counts(dropna=False).sort_index().head(30))   


# In[ ]:





# In[31]:


# Plot frequency of PACK_SIZE values (bars)
plt.figure(figsize=(10,4))
txn_data['PACK_SIZE'].dropna().astype(int).value_counts().sort_index().plot(kind='bar')
plt.title('Number of Transactions by Pack size')
plt.xlabel('Pack size (g)')
plt.ylabel('Transaction count')
plt.tight_layout()
plt.show()


# In[ ]:





# In[32]:


#  extract brand by splitting product name and taking first token.
txn_data['BRAND'] = txn_data['PROD_NAME_LOWER'].str.split().str[0]

# Trim punctuation possibly attached
txn_data['BRAND'] = txn_data['BRAND'].str.replace(r'[^a-z0-9]', '', regex=True)

print("Top brands \n", txn_data['BRAND'].value_counts(30))


# In[ ]:





# In[33]:


# Clean brand names (merge variants)

brand_mapping = {
    'red':'rrd',
    'rrd':'rrd',
    'smith':'smiths',
    'smiths':'smiths',
    'dorito':'doritos',
    'doritos':'doritos',
    'infzns':'infuzions',
    'infuzions':'infuzions',
    'snbts':'sunbites',
    'sunbites':'sunbites'
}

# Apply mapping to 'BRAND' column 
txn_data['BRAND_CLEAN'] = txn_data['BRAND'].replace(brand_mapping)

txn_data['BRAND_CLEAN'] = txn_data['BRAND_CLEAN'].fillna(txn_data['BRAND'])

print("Top brands: \n", txn_data['BRAND_CLEAN'].value_counts().head(30))


# In[ ]:





# In[34]:


# Merge the two datasets or dataframes txn_data and cust_data
merged_data = pd.merge(txn_data, cust_data, on='LYLTY_CARD_NBR', how='left')


# In[35]:


merged_data


# In[ ]:





# In[ ]:





# In[38]:


# Check for unmatched transactions (nulls in joined customer columns)
missing_customers = merged_data[['LIFESTAGE','PREMIUM_CUSTOMER']].isnull().all(axis=1).sum()

print("transactions without matched customer info:", missing_customers)


# In[ ]:





# In[39]:


# Save merged dataset (optional)
merged_data.to_csv('data.csv', index=False)


# In[40]:


import os 
os.getcwd()


# In[ ]:





# In[41]:


merged_data


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




