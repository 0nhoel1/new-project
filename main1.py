import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#########

# Membaca Data
all_df = pd.read_csv('all_data1.csv')

# Pastikan kolom tanggal dalam format datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Judul Dashboard
st.title("Dashboard E-Commerce")

# Filter Berdasarkan Tanggal
st.sidebar.header("Filter Data Berdasarkan Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", value=all_df['order_purchase_timestamp'].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", value=all_df['order_purchase_timestamp'].max().date())

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = all_df[
    (all_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (all_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

# Filter Berdasarkan Pelanggan
st.sidebar.header("Filter Data")
customer_id = st.sidebar.selectbox("Pilih Customer ID", all_df['customer_id'].unique())
customer_data = all_df[all_df['customer_id'] == customer_id]

# Tampilkan Statistik Umum Setelah Filter
st.header("Statistik Umum (Berdasarkan Tanggal yang Difilter)")

total_sales = filtered_data['price'].sum()  # Total Penjualan
total_orders = filtered_data['order_id'].nunique()  # Total Pesanan
total_customers = filtered_data['customer_id'].nunique()  # Total Pelanggan
avg_rating = filtered_data['review_score'].mean()  # Rata-Rata Rating

st.metric("Total Penjualan", f"Rp{total_sales:,.2f}")
st.metric("Jumlah Pesanan", total_orders)
st.metric("Jumlah Pelanggan", total_customers)
st.metric("Rata-Rata Rating", f"{avg_rating:.2f}")

# Penjualan Berdasarkan Kategori Produk
st.header("Penjualan Berdasarkan Kategori Produk (Filtered)")
sales_by_category = filtered_data.groupby("product_category_name_english")['price'].sum().sort_values(ascending=False)
st.bar_chart(sales_by_category)

# Jumlah Pesanan Berdasarkan Status
st.header("Jumlah Pesanan Berdasarkan Status (Filtered)")
orders_by_status = filtered_data['order_status'].value_counts()
fig, ax = plt.subplots()
ax.pie(orders_by_status, labels=orders_by_status.index, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Tren Penjualan Bulanan
st.header("Tren Penjualan Bulanan (Filtered)")
filtered_data['month_year'] = filtered_data['order_purchase_timestamp'].dt.to_period("M")
monthly_sales = filtered_data.groupby("month_year")['price'].sum()
st.line_chart(monthly_sales)
