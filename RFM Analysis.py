#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel("/Users/uguryigit/Desktop/RFM_Data.xlsx")  

len(df["Customer_id"].unique())

df["Bought"].value_counts()

df["Amount"].describe()

# count    635.000000
# mean      20.192898
# std       12.030023
# min        0.140000
# 25%        9.565000 1.quartile
# 50%       20.160000 (medyan)
# 75%       28.800000 3.quartile
# max       48.890000

plt.hist(df['Date'],bins=10,)
plt.grid(alpha=0.75)
plt.xlabel("Tarih")
plt.ylabel("İşlem Adet")
plt.show()


# In[18]:


sonTarih = dt.datetime(2012,5,4)
df['Gun_farki'] = sonTarih - df['Date']
df['Gun_farki'].astype('timedelta64[D]')
df['Gun_farki'] = df['Gun_farki'] / np.timedelta64(1, 'D')
df.head()

plt.hist(df['Gun_farki'])
plt.grid(alpha=0.75)
plt.xlabel("Gun Farki")
plt.ylabel("Islem Adet")
plt.show()


# In[ ]:


rfmTable = df.groupby('Customer_id').agg(
    {'Gun_farkı': lambda x:x.min(), # Recency
     'Customer_id': lambda x: len(x), # Frequency
     'Amount': lambda x: x.sum()}) # Monetary Value

rfmTable.rename(columns=
                {'Gun_farkı': 'recency',
                 'Customer_id': 'frequency',
                 'Amount': 'monetary_value'}, 
                inplace=True)
rfmTable.head()


# In[ ]:


quart = rfmTable.quantile(q=[0.25,0.50,0.75])
quart


# In[ ]:


quart = quart.to_dict()
print(quart)
{
  'recency': 
      {
      0.25: 2131.0, 
      0.5: 3032.0, 
      0.75: 4170.0
      },
 'frequency': 
     {
     0.25: 4.0, 
     0.5: 5.0, 
     0.75: 6.0
     },
 'monetary_value': 
     {
     0.25: 79.61, 
     0.5: 104.04, 
     0.75: 134.9
     }
}
# Recency için çeyrekliğe göre sınıfların belirlenmesi
def RClass(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


# Frequency ve Monetary için çeyrekliğe göre sınıfların belirlenmesi
def FMClass(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1

rfmSeg = rfmTable
rfmSeg['R_Quartile'] = rfmSeg['recency'].apply(RClass, args=('recency', quart,))
rfmSeg['F_Quartile'] = rfmSeg['frequency'].apply(FMClass, args=('frequency', quart,))
rfmSeg['M_Quartile'] = rfmSeg['monetary_value'].apply(FMClass, args=('monetary_value', quart,))


# In[ ]:


rfmSeg['RFMScore'] = rfmSeg.R_Quartile.map(str)                             + rfmSeg.F_Quartile.map(str)                             + rfmSeg.M_Quartile.map(str)
rfmSeg.head()

