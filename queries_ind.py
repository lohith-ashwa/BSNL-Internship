# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:14:29 2023

@author: lohit
"""

import os
import pandas as pd
import csv
import mysql.connector
import sqlite3
from sqlalchemy import create_engine
import MySQLdb
import matplotlib.pyplot as plt

dest_path= "C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/MSOFTX_20230101"
os.chdir("C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/MSOFTX_20230101")
list_of_files = os.listdir(dest_path)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lohithashwa",
    database="msoftx_final"
)

cursor=mydb.cursor()
#analyzing pmresult_83888088
i=0
df1=pd.DataFrame()
all=[]
for file1 in list_of_files:
    if file1.startswith("pmresult_83888088"):
        table_name = file1.replace('.csv', '')
        s="select * from %s;" %table_name
        query=s;
        df1=pd.read_sql(query,mydb)
        all.append(df1)
data = pd.concat(all)
data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
data['Answer Traffic'] = pd.to_numeric(data['Answer Traffic'])
data['Answer Times'] = pd.to_numeric(data['Answer Times'])
def compute_new_column(x):
    # compute the new value based on existing columns
    return ((x['Answer Traffic'])*60) / (x['Answer Times'])

# apply the function to the existing columns
data['average_call_duration'] = data.apply(compute_new_column, axis=1)
data['Result Time'] = pd.to_datetime(data['Result Time'])
data['Hour']=data['Result Time'].dt.hour

t1=data.loc[data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
t2=data.loc[data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
y =t1['average_call_duration']
z = t2['average_call_duration']
x=t1['Hour']
# Plot a simple line chart
plt.plot(x, y, 'c',label='HYD')

# Plot another line on the same chart/graph
plt.plot(x, z, 'y',label='BLR')

plt.legend()
plt.show()
