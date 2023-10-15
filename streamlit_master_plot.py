import streamlit as st
import pandas as pd
import mysql.connector
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

st.title("Reports on PMRESULT_83888089 and PMRESULT_83888088")
# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lohithashwa",
    database="msoftx_final"
)
c = mydb.cursor()

# Create a dropdown menu for selecting a table
c.execute("SHOW TABLES")
tables = [table[0] for table in c.fetchall()]
table_name = st.selectbox('Select a table:', tables)
st.markdown("<span style='font-size: 28px;'>**Data Visualisation**</span>", unsafe_allow_html=True)
# Create a dropdown menu for selecting the city
city = st.selectbox('Select a city:',['','HYD only', 'BLR only', 'Combined', 'Individual'])

date_type = st.radio('Select date input type:', ['Single date', 'Date range','Specific Dates'])
default_date = datetime.date(2023, 1, 1)

default_start_hour=0
start_hour = st.slider("Select the START hour", 0, 23, default_start_hour)
default_end_hour=23
end_hour = st.slider("Select the END hour", 0, 23, default_end_hour)

if date_type == "Single date":
    # Display a date picker and get the selected date
    selected_date = st.date_input("Select a date", value=default_date)

    # Format the selected date as a string in the format %Y-%m-%d
    date_str = selected_date.strftime("%Y-%m-%d")

    # Construct the SQL query to filter the results by the selected date
    query = f"SELECT * FROM {table_name} WHERE DATE_FORMAT(`Result Time`, '%Y-%m-%d') = '{date_str}' AND HOUR(`Result Time`) BETWEEN {start_hour} AND {end_hour};"

    c.execute(query)
    results = c.fetchall()
    data = pd.DataFrame(results, columns=[i[0] for i in c.description])
    for col_name in data.columns:
        if col_name != 'Result Time' and col_name != 'Granularity Period' and col_name != 'Object Name' and col_name != 'Reliability':
            data[col_name] = pd.to_numeric(data[col_name])
    data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    def compute_new_column(x):
        #compute the new value based on existing columns
        return ((x['Answer Traffic'])*60) / (x['Answer Times'])
    data['Average Call Duration'] = data.apply(compute_new_column, axis=1)
    x = st.selectbox("Select X-axis", data.columns)
    y = st.selectbox("Select Y-axis", data.columns)    
    if city!='Individual':
        if city=='HYD only':
            data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0' ) ].index)
        elif city=='BLR only':
            data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0' ) ].index)
        
        if x=='Result Time' or y=='Result Time':
            data['Result Time1'] = data['Result Time'].str[11:]
            data['Result Time2'] = data['Result Time1'].str.slice(stop=-3)
            if x=='Result Time':
                x_time = data.groupby('Result Time2')[y].mean()
                st.line_chart(x_time)
            else:
                y_time = data.groupby('Result Time2')[x].mean()
                st.line_chart(y_time)
        else:
            fig, ax = plt.subplots()
            ax.plot(data[x], data[y])
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f'{x} vs {y}')
            ax.legend()
            # Display the plot in Streamlit
            st.pyplot(fig)
    else:
        if x=='Result Time':
            t1=data.loc[data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
            t2=data.loc[data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
            t1['Result Time1'] = t1['Result Time'].str[11:]
            t1['Result Time2'] = t1['Result Time1'].str.slice(stop=-3)
            t2['Result Time1'] = t2['Result Time'].str[11:]
            t2['Result Time2'] = t2['Result Time1'].str.slice(stop=-3)
            y1 =t1[y]
            z1 = t2[y]
            x1=t1['Result Time2']
            fig, ax = plt.subplots()
            ax.plot(x1, y1, label='HYD')
            ax.plot(x1, z1, label='BLR')
            ax.set_xlabel('Hour')
            ax.set_ylabel(y)
            ax.legend()
            st.pyplot(fig)
        else:
            st.write('Invalid Input, Please give only Result Time in X-Axis')



elif date_type == "Date range":
    # Display a date picker and get the selected date
    selected_date_start = st.date_input("Select a START date", value=pd.to_datetime('2023-01-01'))
    # Format the selected date as a string in the format %Y-%m-%d
    date_str_start = selected_date_start.strftime("%Y-%m-%d")
    # Display a date picker and get the selected date
    selected_date_end = st.date_input("Select a END date", value=pd.to_datetime('2023-01-20'))
    # Format the selected date as a string in the format %Y-%m-%d
    date_str_end = selected_date_end.strftime("%Y-%m-%d")
    query = f"SELECT * FROM {table_name} WHERE `Result Time` BETWEEN '{date_str_start} 00:00' AND '{date_str_end} 23:00'AND HOUR(`Result Time`) BETWEEN {start_hour} AND {end_hour};"

    c.execute(query)
    results = c.fetchall()
    data = pd.DataFrame(results, columns=[i[0] for i in c.description])    
    for col_name in data.columns:
        if col_name != 'Result Time' and col_name != 'Granularity Period' and col_name != 'Object Name' and col_name != 'Reliability':
            data[col_name] = pd.to_numeric(data[col_name])
    data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=1, STATICAREAX=32' ) ].index)
    data2=data.copy()
    def compute_new_column(x):
        #compute the new value based on existing columns
        return ((x['Answer Traffic'])*60) / (x['Answer Times'])
    data['Average Call Duration'] = data.apply(compute_new_column, axis=1)
    x = st.selectbox("Select X-axis", data.columns)
    y = st.selectbox("Select Y-axis", data.columns) 
    if city!='Individual':
        if city=='HYD only':
            data = data.drop(data.loc[(data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0' ) ].index)
        elif city=='BLR only':
            data = data.drop(data.loc[(data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0' ) ].index)
        time_scale = st.radio('Select the time scale :', ['Hourwise', 'Daywise','Days of the week'])
        if time_scale=='Hourwise':
            if x=='Result Time' or y=='Result Time':
                data['Result Time1'] = data['Result Time'].str[11:]
                data['Result Time2'] = data['Result Time1'].str.slice(stop=-3)
                if x=='Result Time':
                    x_time = data.groupby('Result Time2')[y].mean()
                    st.line_chart(x_time)
                else:
                    y_time = data.groupby('Result Time2')[x].mean()
                    st.line_chart(y_time)
        elif time_scale=='Daywise':
            data['Result Time1'] = data['Result Time'].str.slice(stop=-5)
            data['Result Time2'] = data['Result Time1'].str[8:]    
            x_time= data.groupby('Result Time2')[y].mean()
            st.line_chart(x_time)
            
        elif time_scale=='Days of the week':
            # Slice the time column and convert to datetime format
            data['Result Time1'] = data['Result Time'].str.slice(stop=-5)
            data['Result Time2'] = pd.to_datetime(data['Result Time1'])

            # Extract the day of the week and calculate the mean value of y
            data['day_of_week'] = data['Result Time2'].dt.day_name()
            grouped_df = data.groupby('day_of_week')[y].mean().reset_index()

            # Set the order of the days of the week
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            # Create a barplot with Seaborn and Matplotlib
            fig, ax = plt.subplots()
            sns.barplot(x='day_of_week', y=y, data=grouped_df, order=day_order, ax=ax)
            ax.set_xlabel('Days of the Week')
            ax.set_ylabel(y)
            
            # Display the plot using Streamlit
            st.pyplot(fig)

            
    else:
        time_scale = st.radio('Select the time scale :', ['Hourwise', 'Daywise','Days of the week'])
        if x=='Result Time':
            if time_scale=='Hourwise':
                if x=='Result Time':
                    data['Result Time1'] = data['Result Time'].str[11:]
                    data['Result Time2'] = data['Result Time1'].str.slice(stop=-3)
                    t1=data.loc[data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
                    t2=data.loc[data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
                    y1 = t1.groupby('Result Time2')[y].mean()
                    z1 = t2.groupby('Result Time2')[y].mean()
                    #y1 =t1[y]
                    #z1 = t2[y]
                    x1=t1['Result Time2']
                    fig, ax = plt.subplots()
                    ax.plot(y1.index, y1.values, label='HYD')
                    ax.plot(z1.index, z1.values, label='BLR')
                    ax.set_xlabel('Hour')
                    ax.set_ylabel(y)
                    ax.legend()
                    st.pyplot(fig)
                    
            elif time_scale=='Daywise':
                data['Result Time1'] = data['Result Time'].str.slice(stop=-5)
                data['Result Time2'] = data['Result Time1'].str[8:]    
                time="Days of the Month"  
                t1=data.loc[data['Object Name'] == 'HYD-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
                t2=data.loc[data['Object Name'] == 'BLR-MSOFTX/Local Zone of caller:LABEL=0, STATICAREAX=0']
                y1 = t1.groupby('Result Time2')[y].mean()
                z1 = t2.groupby('Result Time2')[y].mean()
                #y1 =t1[y]
                #z1 = t2[y]
                x1=t1['Result Time2']
                fig, ax = plt.subplots()
                ax.plot(y1.index, y1.values, label='HYD')
                ax.plot(z1.index, z1.values, label='BLR')
                ax.set_xlabel("Days of the Month")
                ax.set_ylabel(y)
                ax.legend()
                st.pyplot(fig)
        else:
            st.write('Invalid Input, Please give only Result Time in X-Axis')
elif date_type=="Specific Dates":
    from datetime import timedelta
    # Get number of days from user
    num_of_days = st.number_input("Enter number of days:", min_value=1)
    
    # Get start date from user
    start_date = st.date_input("Enter start date:")
    
    # Create an empty list to store the dates
    dates = []
    
    # Loop through the number of days and get the date for each day
    for i in range(num_of_days):
        # Calculate date by adding i days to start date
        current_date = start_date + timedelta(days=i)
        # Display date input widget for the current date and append to the list
        dates.append(st.date_input(f"Date {i+1}:", value=current_date))
    
    # Display the list of dates
    st.write("Selected dates:", dates)
        