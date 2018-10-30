# -*- coding: utf-8 -*-

# coding: utf-8

# In[3]:


import pandas as pd


# In[71]:


data  = pd.read_csv("yellow_tripdata_2018-01.csv", usecols= ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID'])
data = data[data.tpep_pickup_datetime != data.tpep_dropoff_datetime]


# In[72]:


from datetime import datetime
import matplotlib.pyplot as plt

FMT = '%Y-%m-%d  %H:%M:%S'
pickup_time = pd.to_datetime(data['tpep_pickup_datetime'].str.strip(), format = FMT)
dropoff_time = pd.to_datetime(data['tpep_dropoff_datetime'].str.strip(), format = FMT)
delta = (dropoff_time - pickup_time).astype('timedelta64[m]')
delta


# In[74]:


agg = pd.DataFrame(abs(delta.value_counts()), columns = ['y'])
agg = agg[agg.index >= 0]


# In[75]:


less_ten = agg[agg.index <= 10]
less_ten = less_ten.sort_index()
percent1 = (less_ten.cumsum() / delta.size).tail(1).y.item()
percent1


# In[76]:


less_twenty = agg[agg.index <= 20]
less_twenty = less_twenty[less_twenty.index > 10]
less_twenty = less_twenty.sort_index()
percent2 = (less_twenty.cumsum() / delta.size).tail(1).y.item()
percent2


# In[77]:


more = agg[agg.index > 20]
more = more[more.index <= 30]

more = more.sort_index()
percent3 = (more.cumsum() / delta.size).tail(1).y.item()
percent3



more_hour = agg[agg.index > 30] 
more_hour = more_hour.sort_index()
percent4 = (more_hour.cumsum() / delta.size).tail(1).y.item()

d = {'Time Distribution in NY': [percent1, percent2, percent3, percent4]}
df = pd.DataFrame(data=d, index=['<= 10 min', '10 < min <= 20', '20 < min <= 30', 'min > 30'])
df['Time Distribution in NY'].plot.pie(autopct='%1.0f%%')




#In[78]:

#JOIN TABLES
data2 = pd.read_csv("taxi _zone_lookup.csv")

borough = data.join(data2.set_index('LocationID'), on='PULocationID')


# In[134]:


p1 = {}
p2 = {}
p3 = {}
p4 = {}
for i in range(265):
    
    bor = borough[borough.PULocationID == i+1]
    bor = bor[bor.tpep_pickup_datetime != bor.tpep_dropoff_datetime]
    pickup_time = pd.to_datetime(bor['tpep_pickup_datetime'].str.strip(), format = FMT)
    dropoff_time = pd.to_datetime(bor['tpep_dropoff_datetime'].str.strip(), format = FMT)
    delta = (dropoff_time - pickup_time).astype('timedelta64[m]')
    
    agg = pd.DataFrame(delta.value_counts(), columns = ['y'])
    agg = agg[agg.index >= 0]
    
    less_ten = agg[agg.index <= 10].sort_index()
    try:
        pr1 = (less_ten.cumsum() / delta.size).tail(1).y.item()
    except:
        pr1 = 0
    p1[str(i)] = pr1 
    less_twenty = agg[agg.index <= 20]
    less_twenty = less_twenty[less_twenty.index > 10].sort_index()
    try:
        pr2 = (less_twenty.cumsum() / delta.size).tail(1).y.item()
    except:
        pr2 = 0
    p2[str(i)] = pr2 
    more = agg[agg.index > 20]
    more = more[more.index <= 30].sort_index()
    try :
        pr3 = (more.cumsum() / delta.size).tail(1).y.item()
    except:
        pr3 = 0
    p3[str(i)] = pr3 
    more_hour = agg[agg.index > 30].sort_index()
    try :
        pr4 = (more_hour.cumsum() / delta.size).tail(1).y.item()
    except:
        pr4 = 0
    p4[i+1] = pr4


# In[223]:


my1 = pd.DataFrame.from_dict(p1, orient='index', dtype=None,columns=['a'])
my2= pd.DataFrame.from_dict(p2, orient='index', dtype=None,columns=['b'])
my3 = pd.DataFrame.from_dict(p3, orient='index', dtype=None,columns=['c'])
my4 = pd.DataFrame.from_dict(p4, orient='index', dtype=None,columns=['d'])
my1.plot()
(my1['a'].mean())
my2.plot()
my3.plot()
my4.plot()


# In[239]:


result = pd.concat([my1, my2, my3,], axis=1)
result.join(my4)


# In[245]:


my4 = my4.reset_index(drop=True)
result = result.reset_index(drop=True)
result = result.join(my4)


# In[251]:


result.plot(y = ['a', 'b'])
