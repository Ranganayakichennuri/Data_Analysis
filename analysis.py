
import pandas as pd
import matplotlib.pyplot as plt

# File paths
products_file = '/mnt/data/PRODUCTS_TAKEHOME.csv'
transactions_file = '/mnt/data/TRANSACTION_TAKEHOME.csv'
users_file = '/mnt/data/USER_TAKEHOME.csv'

# Load datasets
products_df = pd.read_csv(products_file)
transactions_df = pd.read_csv(transactions_file)
users_df = pd.read_csv(users_file)

# 1. Products Dataset Analysis
products_analysis = {
    "missing_values": products_df.isnull().sum(),
    "unique_values": products_df.nunique(),
    "top_categories": products_df['CATEGORY_1'].value_counts()
}

# 2. Transactions Dataset Analysis
transactions_df['PURCHASE_DATE'] = pd.to_datetime(transactions_df['PURCHASE_DATE'], errors='coerce', format='%y/%m/%d')
transactions_df['SCAN_DATE'] = pd.to_datetime(transactions_df['SCAN_DATE'], errors='coerce')
transactions_analysis = {
    "missing_values": transactions_df.isnull().sum(),
    "unique_values": transactions_df.nunique(),
    "store_distribution": transactions_df['STORE_NAME'].value_counts(),
    "quantity_summary": transactions_df['FINAL_QUANTITY'].describe()
}

# 3. Users Dataset Analysis
users_df['BIRTH_DATE'] = pd.to_datetime(users_df['BIRTH_DATE'], errors='coerce')
users_df['CREATED_DATE'] = pd.to_datetime(users_df['CREATED_DATE'], errors='coerce')
users_analysis = {
    "missing_values": users_df.isnull().sum(),
    "unique_values": users_df.nunique(),
    "state_distribution": users_df['STATE'].value_counts(),
    "language_distribution": users_df['LANGUAGE'].value_counts(),
    "gender_distribution": users_df['GENDER'].value_counts()
}

# Combine Missing Data Summary
missing_data_products = (products_df.isnull().sum() / len(products_df) * 100).round(2).to_frame(name='Missing Percentage')
missing_data_transactions = (transactions_df.isnull().sum() / len(transactions_df) * 100).round(2).to_frame(name='Missing Percentage')
missing_data_users = (users_df.isnull().sum() / len(users_df) * 100).round(2).to_frame(name='Missing Percentage')
missing_data_products.index = [f"Products - {col}" for col in missing_data_products.index]
missing_data_transactions.index = [f"Transactions - {col}" for col in missing_data_transactions.index]
missing_data_users.index = [f"Users - {col}" for col in missing_data_users.index]
missing_data_summary = pd.concat([missing_data_products, missing_data_transactions, missing_data_users])

# Plot Missing Data
fig, axes = plt.subplots(3, 1, figsize=(10, 18), sharex=True)
fig.suptitle("Missing Data Percentage by Field", fontsize=16)

# Products dataset
axes[0].bar(missing_data_products.index, missing_data_products['Missing Percentage'], color='teal')
axes[0].set_title("Products Dataset")
axes[0].set_ylabel("Missing Percentage (%)")
axes[0].tick_params(axis='x', rotation=45)

# Transactions dataset
axes[1].bar(missing_data_transactions.index, missing_data_transactions['Missing Percentage'], color='orange')
axes[1].set_title("Transactions Dataset")
axes[1].set_ylabel("Missing Percentage (%)")
axes[1].tick_params(axis='x', rotation=45)

# Users dataset
axes[2].bar(missing_data_users.index, missing_data_users['Missing Percentage'], color='purple')
axes[2].set_title("Users Dataset")
axes[2].set_ylabel("Missing Percentage (%)")
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Additional Analysis

# 1. Bar chart: Age distribution of users
users_df['BIRTH_DATE'] = pd.to_datetime(users_df['BIRTH_DATE'], errors='coerce')
current_year = pd.Timestamp.now().year
users_df['AGE'] = current_year - users_df['BIRTH_DATE'].dt.year

plt.figure(figsize=(12, 6))
plt.hist(users_df['AGE'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title('Age Distribution of Users')
plt.xlabel('Age')
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 2. Bar chart: Gender distribution of users
plt.figure(figsize=(8, 5))
users_df['GENDER'].value_counts().plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Gender Distribution of Users')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 3. Bar chart: Top 10 brands
top_brands = products_df['BRAND'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_brands.plot(kind='bar', color='mediumseagreen', edgecolor='black')
plt.title('Top 10 Brands')
plt.xlabel('Brand')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 4. Bar chart: Top 10 manufacturers
top_manufacturers = products_df['MANUFACTURER'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_manufacturers.plot(kind='bar', color='royalblue', edgecolor='black')
plt.title('Top 10 Manufacturers')
plt.xlabel('Manufacturer')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 5. Detect duplicate transactions
duplicates = transactions_df[transactions_df.duplicated()]

# Save duplicate transactions to a CSV file
duplicates.to_csv('/mnt/data/duplicate_transactions.csv', index=False)

