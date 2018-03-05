
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib as mpl
import numpy as np

df = pd.read_csv('data.csv', header=0, sep=',', encoding='latin1')
df.head(5)


# In[3]:


def CountSummary():
    orderedNo = df.loc[ (df['Quantity'] > 0)].count().InvoiceNo
    canceledNo = df.loc[ (df['Quantity'] < 0) & (df['InvoiceNo'].str[:1] == 'C')].count().InvoiceNo
    returnedNo = df.loc[ (df['Quantity'] < 0) & (df['InvoiceNo'].str[:1] != 'C')].count().InvoiceNo
    totalNo = df.loc[ (df['Quantity'] != 0)].count().InvoiceNo
    
    ordered_0_unitPriceNo = df.loc[ (df['Quantity'] > 0) & (df['UnitPrice'] == 0)].count().InvoiceNo
    canceled_0_unitPricedNo = df.loc[ (df['Quantity'] < 0) & (df['InvoiceNo'].str[:1] == 'C') & (df['UnitPrice'] == 0)].count().InvoiceNo
    returned_0_unitPricedNo = df.loc[ (df['Quantity'] < 0) & (df['InvoiceNo'].str[:1] != 'C') & (df['UnitPrice'] == 0)].count().InvoiceNo
    total_0_unitPriceNo = df.loc[(df['UnitPrice'] == 0.0)].count().InvoiceNo

    d = {'Count Type': ['Ordered', 'Canceled', 'Returned', 'Total'], 
         'Invoice Count': [orderedNo, canceledNo, returnedNo, totalNo],
         'Percentage': [orderedNo/totalNo, canceledNo/totalNo, returnedNo/totalNo, totalNo/totalNo],
         'UnitPrice=0': [ordered_0_unitPriceNo,canceled_0_unitPricedNo, returned_0_unitPricedNo, total_0_unitPriceNo]
         }
    dfNo = pd.DataFrame(data=d)
    print (dfNo)
    
print ('Before fixing UnitPrice column')
CountSummary()


# In[4]:


def fix_returned_unitPrice(row, df):

    idx = row.name
    stkCode = df.iloc[idx].StockCode
    unitP = df.loc[(df.index < idx) & (df['StockCode'].str[:12] == stkCode) & (df['UnitPrice'] != 0.0)].tail(1)

    if (len(unitP) == 1) :
        #print ('unitPrice found: index(0)=', unitP.index[0], 'UnitPrice=', unitP.iloc[0].UnitPrice, ', stkCode=', stkCode, ', idx=', idx)
        df.loc[df.index == idx, 'UnitPrice'] =  unitP.iloc[0].UnitPrice
    #else :
    #    print ('not found UnitPrice index=', idx, 'stkCode=', stkCode)    
            

df0 = df.loc[(df['Quantity'] < 0) & (df['InvoiceNo'].str[:1] != 'C') & (df['UnitPrice'] == 0.0)].apply(
    lambda r: fix_returned_unitPrice(r, df), axis=1
)

print ('After fixing UnitPrice column')
CountSummary()


# In[5]:


df['Sales']=df[['Quantity']].multiply(df['UnitPrice'], axis='index')
df.head(5)


# In[6]:


months = ['12/31/2010', '1/31/2011', '2/29/2011', '3/31/2011', '4/30/2011', '5/31/2011', '6/30/2011', '7/31/2011', '8/31/2011', '9/30/2011', '10/31/2011', '11/30/2011']
sales = [df.loc[(pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M').dt.month == 12), 'Sales'].sum()]
for month in range(1, 12):
    sales.append(df.loc[(pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M').dt.month == month), 'Sales'].sum())
df2 = pd.DataFrame( 
    {'Month': months,
     'Sales': sales
    })
df2


# In[8]:


df2.plot(kind='bar', x=df2['Month'], y='Sales')

