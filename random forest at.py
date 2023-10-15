import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lohithashwa",
    database="msoftx_final"
)
query = f"SELECT * FROM PMRESULT_83888088;"
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

data['hour'] = pd.to_datetime(data['Result Time']).dt.hour
data['weekday'] = pd.to_datetime(data['Result Time']).dt.weekday
data['month'] = pd.to_datetime(data['Result Time']).dt.month


# Define the input and output data
X = data[['hour','weekday','month']]
X = pd.get_dummies(X, columns=['hour','weekday','month'])
y = data['Answer Traffic']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,random_state=2)

# Define the random forest regressor model with hyperparameters
rf_model = RandomForestRegressor(n_estimators=70, max_depth=30, random_state=42)

# Fit the model on the training data
rf_model.fit(X_train, y_train)

# Evaluate the model on the testing data
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
accuracy = 1 - (rmse / np.mean(y))

print(f'Test RMSE: {rmse:.2f}')
print(f'Test Accuracy: {accuracy:.2%}')

diff = np.abs(y_test - y_pred)
pct_diff = 100 * diff / y_test