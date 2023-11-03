#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: E-Commerce Public Dataset 

# Nama: Tobias Mikha Sulistiyo
# Email: tobias_mikha33
# Id Dicoding: tobias_mikha

# # Menentukan Pertanyaan Bisnis

# 1. Bagaimana demografi Customer?
# 2. Produk Manakah yang paling laris terjual?

# # Menyiapkan Library yang Dibutuhkan

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# # Data Wrangling

# ## Gathering Data 

# In[2]:


data='products_dataset.csv'
data2='customers_dataset.csv'
data3='order_items_dataset.csv'
data4='product_category_name_translation.csv'
data5='orders_dataset.csv'


# In[3]:


products_df=pd.read_csv(data)
customers_df=pd.read_csv(data2)
order_item_df=pd.read_csv(data3)
translate_df=pd.read_csv(data4)
orders_df=pd.read_csv(data5)


# ## Assesing Data

# In[4]:


products_df.info()


# In[5]:


products_df.duplicated().sum()


# In[6]:


translate_df.info()


# In[7]:


customers_df.info()


# In[8]:


customers_df.duplicated().sum()


# In[9]:


order_item_df.info()


# In[10]:


order_item_df.duplicated().sum()


# In[11]:


orders_df.info()


# In[12]:


orders_df.duplicated().sum()


# karena informasi dari tiap file berbeda, maka perlu dilakukan grouping berdasarkan id tiap order maupun customer. Dalam data ini, saya berpatokan pada order_items.csv untuk pembelian

# ## Data Wrangling

# ## Proses penggabungan/group by customer_id pada data customers dan orders

# In[13]:


join_df=customers_df.set_index('customer_id').join(orders_df.set_index('customer_id'), how='outer')
join_df=join_df[['order_id', 'customer_city', 'customer_state', 'order_status']]


# In[14]:


join_df.info()


# ## Proses penggabungan/group by order_id pada dataframe join_df dengan dataframe order_item_df

# In[15]:


join2_df=join_df.set_index('order_id').join(order_item_df.set_index('order_id'), how='right')
join=join2_df[['product_id','customer_city','customer_state','price', 'order_status']]


# In[16]:


join2_df.info()


# In[17]:


join.head(-5)


# ## Proses penggabungan/group by product_id pada dataframe join dengan dataframe product_df

# In[18]:


join2=join.set_index('product_id').join(products_df.set_index('product_id'),how='right')
join3_df=join2[['customer_city', 'customer_state', 'price', 'order_status', 'product_category_name']]


# In[19]:


join3_df.info()


# terlihat bahwa product category name memiliki missing value sehingga perlu dilakukan data manipulation (imputation) supaya jumlah data sama

# In[20]:


join3_df.product_category_name.fillna('Na',inplace=True)


# In[21]:


join3_df.info()


# Jumlah data sudah sama, yang berarti proses data manipulation telah berhasil

# ## Proses penggabungan/group by product_category_name pada dataframe join3_df dengan dataframe translate_df

# pada proses ini, kemudian dibuat dataframe baru bernama final_df yang berisikan customer_city, customer_state, price, order_status, dan product_category_name_english

# final_df merupakan dataframe yang diolah

# In[22]:


final_df=join3_df.set_index('product_category_name').join(translate_df.set_index('product_category_name'), how='left')


# In[23]:


final_df.info()


# Dari final tabel yang akan digunakan, category name in english terdapat missing value, sehingga dilakukan data manipulation (imputation)

# In[24]:


final_df.product_category_name_english.fillna('NA',inplace=True)


# In[25]:


final_df.info()


# Jumlah setiap data sudah sama, sehingga tidak ada missing value. Data telah siap dilakukan Analisis

# # Visualization & Explanatory Analysis

# ## Bagaimana Demografi Pelanggan?

# In[26]:


jumlah_cust=final_df.groupby(['customer_state','customer_city'])['order_status'].count().reset_index()
print(jumlah_cust)


# In[27]:


jumlah=jumlah_cust.sort_values(by='order_status', ascending=False)
print(jumlah)


# In[28]:


# Mencari 3 customer_state terbanyak
top_3_states = jumlah_cust.groupby('customer_state')['order_status'].sum().nlargest(3).index

# Membuat bar chart untuk setiap customer_state
for state in top_3_states:
    state_data = jumlah_cust[jumlah_cust['customer_state'] == state]
    top_3_cities_in_state = state_data.nlargest(3, 'order_status')

    plt.figure(figsize=(12, 6))
    plt.bar(top_3_cities_in_state['customer_city'], top_3_cities_in_state['order_status'])
    plt.title(f'3 Customer City Terbanyak di {state}')
    plt.xlabel('Customer City')
    plt.ylabel('Jumlah')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# In[29]:


st.write("""
# Dashboard Data Customer Demografi dan Penjualan Produk
Berikut ini merupakan dashboard data 3 customer state terbanyak dengan perincian 3 kota terbanyak tiap customer state
""")


# In[30]:


import matplotlib.pyplot as plt

#mencari 3 customer state terbanyak
top_3_states = jumlah_cust.groupby('customer_state')['order_status'].sum().nlargest(3).index

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

#menampilkan bar chart pada setiap customer state
for i, state in enumerate(top_3_states):
    state_data = jumlah_cust[jumlah_cust['customer_state'] == state]
    top_3_cities_in_state = state_data.nlargest(3, 'order_status')
    
    axes[i].bar(top_3_cities_in_state['customer_city'], top_3_cities_in_state['order_status'])
    axes[i].set_title(f'3 Customer City Terbanyak di {state}')
    axes[i].set_xlabel('Customer City')
    axes[i].set_ylabel('Jumlah')
    axes[i].tick_params(axis='x', rotation=45, labelrotation=45)  

#Plot ke jupyter
plt.tight_layout()
plt.show()

#Plot ke streamlit
st.pyplot(plt)


# ## Produk Manakah yang Paling Laris Terjual?

# In[31]:


jumlah_produk=final_df.groupby('product_category_name_english')['order_status'].count().reset_index()
print(jumlah_produk)


# In[32]:


jumlah_produk=jumlah_produk.sort_values(by='order_status', ascending=False)
print(jumlah_produk)


# In[33]:


st.write("""
Berikut ini merupakan dashboard Penjualan produk paling laris dan paling rugi
""")


# In[34]:


laku = jumlah_produk.head(5)
rugi = jumlah_produk.tail(5)


fig, axes = plt.subplots(1, 2, figsize=(12, 6))


axes[0].bar(laku['product_category_name_english'], laku['order_status'], color='#72BCD4')
axes[0].set_title('Produk Paling Laku')
axes[0].set_xlabel('Produk')
axes[0].set_ylabel('Jumlah')

axes[1].bar(rugi['product_category_name_english'], rugi['order_status'], color='#D3D3D3')
axes[1].set_title('Produk Paling Rugi')
axes[1].set_xlabel('Produk')
axes[1].set_ylabel('Jumlah')

axes[0].tick_params(axis='x', rotation=45)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

st.pyplot(fig)


# # Conclusion

# 1. Jumlah customer state tertinggi ada di SP, RJ, MG. Pada tiap customer state terdapat 3 customer city terbanyak yaitu di SP terdapat Sao Paulo, Campinas, dan Guarulhos. Di RJ terdapat 3 customer city terbanyak yaitu di Rio De Jainero, Niteroi, dan Nova Iguacu. Di MG terdapat 3 customer city terbanyak yaitu Belo Horizonte, Contagem, dan Juiz de Fora.
# 
#     Untuk kesimpulan customer demography, Dapat meningkatkan penjualan/ memfokuskan penjualan di 3 customer state terbanyak. Penjualan dapat difokuskan di Cusomer city yang memiliki customer sedikit 
# 
# 

# 
# 2. Produk dengan penjualan terbanyak pada kategori bed_bath_table, health_beauty, sports_leisure, furniture_decor, computers_accessories. Sedangkan produk yang tidak laku adalah arts_and_craftmanship, cds_dvds_musicals, la_cuisine, fashion_childrens_clothes, security_and_services.
# 
#     Kesimpulan Untuk produk, dapat memfokuskan/memperbanyak produk dengan nilai penjualan terbanyak dan dapat mengurangi jumlah produk dengan penjualan sedikit
