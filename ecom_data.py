import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r"E:\Datasets\messy_ecom_data.csv"
df = pd.read_csv(file_path, encoding = "latin1")

# 1. Handling Duplicates
print("---Duplicate Count:---", df.duplicated().sum())
df.drop_duplicates(inplace=True)

# Duplicates after dropping
print("---Duplicate Count after dropping:---", df.duplicated().sum())

# 2. Cleaning Dates
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')

# 3. Cleaning Revenue Column
# Remove dollar sign while it's still text
df['Revenue'] = df['Revenue'].astype(str).str.replace('$', '', regex=True)
# Then convert the clean text to  a folat number 
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

#4. Checking for Nulls
print("---Null Count:---")
print(df.isna().sum())

# 5. Handling Nulls
# Replacing nulls in Product_Category with 'Unknown'
df['Product_Category'] = df['Product_Category'].fillna('Unknown')

# 5.1 Handling misspelled Product_Category values
df['Product_Category'] = df['Product_Category'].replace({'laptop': 'Laptop', 'MOUZE': 'Mouse'})
print(df['Product_Category'].value_counts())  # Check the unique values after replacement

# 5.2 Check the revenue distribution for Mouse category
print('---Revenue Distribution for Mouse Category:---')
print(df[df['Product_Category'] == 'Mouse']['Revenue'].describe()) 

# 5.3 Replace the artificial 999999 placeholder with the true category median
mouse_median = df[df['Product_Category'] == 'Mouse']['Revenue'].median()

# 5.4 Standard, error-free replacement
df.loc[(df['Product_Category'] == 'Mouse') & (df['Revenue'] == 999999.0), 'Revenue'] = mouse_median

# check the revenue distribution for Mouse category after replacement
print('---Revenue Distribution for Mouse Category after replacement:---')
print(df[df['Product_Category'] == 'Mouse']['Revenue'].describe())  

# 5.5 Replacing nulls in Revenue with the median revenue of the respective Product_Category 
df['Revenue'] = df.groupby('Product_Category')['Revenue'].transform(lambda x: x.fillna(x.median()))

# 6. Drop rows with nulls in Transaction_Date
df.dropna(subset=['Transaction_Date'], inplace=True)

# 7. Final Check for Nulls
print("---Null Count after handling:---")
print(df.isna().sum())

# 8. Save the cleaned data to a new CSV file
cleaned_file_path = r"E:\Datasets\cleaned_ecom_data.csv"
df.to_csv(cleaned_file_path, index=False)   

# 9. Breaking down the Transaction_Date into separate columns for Year, Month, and Day
df['Year'] = df['Transaction_Date'].dt.year
df['Month'] = df['Transaction_Date'].dt.month # e.g. January = 1, February = 2, etc.
df['Day'] = df['Transaction_Date'].dt.day # e.g. 1, 2, 3, etc.

# 10 . Summary dataframe of individual customer
print("---Customer Summary:---")
customer_summary = df.groupby('Customer_ID').agg(
    Total_Transactions=('Transaction_Date', 'count'),
    Total_Revenue=('Revenue', 'sum'),
    Average_Revenue=('Revenue', 'mean'),
    First_Transaction_Date=('Transaction_Date', 'min'),
    Last_Transaction_Date=('Transaction_Date', 'max')
).reset_index()


# 11. Which product category has the highest total revenue?
print("---Product Category with Highest Revenue:---")
highest_revenue_category = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
print(highest_revenue_category)

# 12 . Which month has the highest total revenue?
print("---Month with Highest Revenue:---")
highest_revenue_month = df.groupby('Month')['Revenue'].sum().sort_values(ascending=False)   
print(highest_revenue_month)

# 13. Which day of the week has the highest total revenue?
print("---Day of the Week with Highest Revenue:---")
df['Day_of_Week'] = df['Transaction_Date'].dt.day_name()  # e.g. Monday, Tuesday, etc.
print(df.groupby('Day_of_Week')['Revenue'].sum().sort_values(ascending=False))

# 14. Set professional theme for plots 
sns.set_theme(style="whitegrid")    

# ======================================================================
# CHAPTER 1: Total Revenue by Product Category (Horizontal Bar Chart)
# ======================================================================
plt.figure(figsize=(10, 6))

# Group and sort exactly as your terminal output did
cat_rev = df.groupby('Product_Category')['Revenue'].sum().reset_index()
cat_rev = cat_rev.sort_values(by='Revenue', ascending=False)

sns.barplot(
    data=cat_rev, 
    x='Revenue', 
    y='Product_Category', 
    palette='Blues_r', # Sleek blue gradient
    hue='Product_Category',
    legend=False
)

plt.title('Product Category Revenue Performance', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Total Revenue ($)', fontsize=12)
plt.ylabel('Product Category', fontsize=12)
plt.tight_layout()

# Save the plot directly to your project folder for your GitHub readme!
plt.savefig('category_revenue.png', dpi=300)
plt.show()

# =====================================================================
# CHART 2: Day of the Week Sales Volume (Sorted Chronologically)
# =====================================================================
plt.figure(figsize=(10, 5))

day_rev = df.groupby('Day_of_Week')['Revenue'].sum().reset_index()

# Sort days chronologically so the timeline makes visual sense
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_rev['Day_of_Week'] = pd.Categorical(day_rev['Day_of_Week'], categories=day_order, ordered=True)
day_rev = day_rev.sort_values('Day_of_Week')

sns.lineplot(
    data=day_rev, 
    x='Day_of_Week', 
    y='Revenue', 
    marker='o', 
    color='#2b5c8f', 
    linewidth=2.5
)

plt.title('Weekly Revenue Trends (Peak Performance)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.tight_layout()

plt.savefig('weekly_revenue_trends.png', dpi=300)
plt.show()
df.to_csv('cleaned_ecom_data.csv', index=False)