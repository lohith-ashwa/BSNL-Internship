"""
SEGMENT 1
This segment of code is responsible for extracting files of "pmresult_83888088" 
type and store the entire month's data as a single table'
"""
# SQL command to be executed before exuting the following code:
# create database msoftx_final; 
import os
import pandas as pd
import csv
import mysql.connector
import sqlite3
from sqlalchemy import create_engine
import MySQLdb

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lohithashwa",
    database="msoftx_final"
)

mycursor = mydb.cursor()
k=1
conn =  create_engine('mysql+mysqldb://root:lohithashwa@localhost/msoftx_final')
table_name="PMRESULT_83888314"
oby="Result Time"
src_path_days= "C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/bca-data/"
list_of_days = os.listdir(src_path_days)
for days in list_of_days:
    src_path_hours="C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/bca-data/" + str(days)
    list_of_hours=os.listdir(src_path_hours)
    for hours in list_of_hours:
        os.chdir(src_path_hours)
        if hours.startswith("pmresult_83888314"):
            df2=pd.read_csv(hours)
            New = df2.drop(labels=[0])
            New_Data = New.reset_index(drop=True)    
            New_Data = New_Data.rename(columns=lambda x:x[:46])
            column_names = list(New_Data.columns)
            New_Data.columns = New_Data.columns.str.strip()
            if k==1:
                conn =  create_engine('mysql+mysqldb://root:lohithashwa@localhost/msoftx_final')
                New_Data.to_sql(table_name, conn, if_exists='replace', index=False)
                sql_create_table = f"CREATE TABLE {table_name} ({','.join(column_names)})"
                k=0
            else:
                New_Data.to_sql(table_name, conn, if_exists='append', index=False)
              
query = f"SELECT * FROM PMRESULT_83888314;"
data = pd.read_sql(query, mydb)
            

             