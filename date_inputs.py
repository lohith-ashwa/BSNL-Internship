# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:48:08 2023

@author: lohit
"""

import mysql.connector
import pandas as pd
import datetime
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
# Connecting to database uing mysql connector
#For this we need our host name,, user name, password, and the data base name 
#data base name is used to store data in that particular database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lohithashwa",
    database="msoftx_final"
)
cursor = mydb.cursor()
# ask user if they want to analyze a single date or a date range
date_type = input("Enter date type (individual or range): ")

if date_type == "individual":
    # ask user for the date to analyze
    date_str = input("Enter date to analyze (YYYY-MM-DD): ")
    # convert date string to datetime object
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    # create query to get data for the specified date
    query = f"SELECT * FROM PMRESULT_83888088 WHERE DATE_FORMAT(`Result Time`, '%Y-%m-%d') = '{date_str}';"
    data = pd.read_sql(query, mydb)
    data2=data
    for col_name in data.columns:
        if col_name != 'Result Time' and col_name != 'Granularity Period' and col_name != 'Object Name' and col_name != 'Reliability':
            data[col_name] = pd.to_numeric(data[col_name])
    # start doing the analysis from here
    data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    
    
    
    
    
    # Faults, which is the biggest contributor 
    
    
elif date_type == "range":
    # ask user for the start and end dates and whether to analyze the data cumulatively or separately
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    analysis_type = input("Enter analysis type (cumulative or separate): ")
    # convert start and end date strings to datetime objects
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    # create a list of datetime objects for each day in the date range
    date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)]
    if analysis_type == "cumulative":
        # create a cumulative query to get all data between start and end date
        query = f"SELECT * FROM PMRESULT_83888088 WHERE `Result Time` BETWEEN '{start_date_str} 00:00' AND '{end_date_str} 23:00';"
        data = pd.read_sql(query, mydb)
        for col_name in data.columns:
            if col_name != 'Result Time' and col_name != 'Granularity Period' and col_name != 'Object Name' and col_name != 'Reliability':
                data[col_name] = pd.to_numeric(data[col_name])
        data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
        data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
        def compute_new_column(x):
            # compute the new value based on existing columns
            return ((x['Answer Traffic'])*60) / (x['Answer Times'])

    
        # apply the function to the existing columns
        data['Average Call Duration'] = data.apply(compute_new_column, axis=1)
        data2=data
        print(data.dtypes)
        #storing unaffected dataframe in data2
    
        # 1. Day wise average call duration in the mentioned date range
        
        
        """
        data['Result Time'] = data['Result Time'].str.slice(stop=-5)
        data['Result Time'] = data['Result Time'].str[8:]    
        avg_call_dur_daywise = data.groupby('Result Time')['Average Call Duration'].mean()
        plt.plot(avg_call_dur_daywise)
        plt.xlabel('Date')
        plt.ylabel('Average Call Duration')
        plt.show()
        





    # 2. Just ensuring that call loss due to overload is zero    
        
        if (data2['Call Loss due to Overload'] != 0).any():
            print("Call Loss Due To Overload Reported")
            non_zero_rows = data2.loc[data2['Call Loss due to Overload']!= 0]
            print(non_zero_rows['Result Time'])
        else:
            print("No call loss due to overload")        
      
        """

    # 3. MASTER PLOT 
        data3=data2
        print("Following is the list of parameters.")
        print(data3.columns)
        x=input("Enter the variable to be plotted on X-axis: ")
        y=input("Enter the variable to be plotted on Y-axis: ")
        if x=='Result Time':
            print("Enter the granularity i.e., on what basis should " +y+" be cumulated")
            print("1. Hourwise")
            print("2. Daywise")
            print("3. Days of the week wise")
            ch=int(input("Enter the desired serial number from above: "))
            def func_a():
                data3['Result Time'] = data['Result Time'].str[11:]
                data3['Result Time'] = data['Result Time'].str.slice(stop=-3)
                x_time = data3.groupby('Result Time')[y].mean()
                plt.plot(x_time)
                plt.xlabel('Hours of the Day')
                plt.ylabel(y)
                plt.show()
                
            def func_b():
                data3['Result Time'] = data3['Result Time'].str.slice(stop=-5)
                data3['Result Time'] = data3['Result Time'].str[8:]    
                x_time= data3.groupby('Result Time')[y].mean()
                plt.plot(x_time)
                plt.xlabel('Days of the Month')
                plt.ylabel(y)
                plt.show()
                
            
            def func_c():
                data3['Result Time'] = data3['Result Time'].str.slice(stop=-5)
                # Convert the date_column to datetime format
                data3['Result Time'] = pd.to_datetime(data3['Result Time'])
                
                # Extract the day of the week from the date_column
                data3['day_of_week'] = data3['Result Time'].dt.day_name()
                grouped_df = data3.groupby('day_of_week')[y].mean().reset_index()
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                # Create a barplot with the day_of_week column as the x-axis and the value_column as the y-axis
                sns.barplot(x='day_of_week', y=y, data=grouped_df, order=day_order)
                plt.xlabel('Days of the Week')
                plt.ylabel(y)
                plt.show()
                
                
            
            # create a dictionary mapping the input values to the corresponding functions
            functions = {
                1: func_a,
                2: func_b,
                3: func_c
            }
            functions.get(ch, lambda: print("Invalid value"))()
            

        
               







            
                
            
            
        
        
        
    elif analysis_type == "separate":
        # iterate over each day in the date range and query the database for each day
        for date in date_range:
            # create a query for the current day
            query = f"SELECT * FROM PMRESULT_83888088 WHERE DATE_FORMAT(`Result Time`, '%Y-%m-%d') = '{date.strftime('%Y-%m-%d')}';"
            data = pd.read_sql(query, mydb)
            for col_name in data.columns:
                if col_name != 'Result Time' and col_name != 'Granularity Period' and col_name != 'Object Name' and col_name != 'Reliability':
                    data[col_name] = pd.to_numeric(data[col_name])
            # start doing the individual analysis evertime one day's data is read. 
            
          
            
else:
    print("Please enter only either 'individual' or 'range'")
