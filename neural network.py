import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import mysql.connector
from sklearn.preprocessing import StandardScaler


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



# Assuming the categorical variables are stored in a DataFrame called 'data'
input_data=data[['hour','weekday','month']]
input_data = pd.get_dummies(input_data, columns=['hour','weekday','month'])
output_data = data['Call Completion Rate'].to_frame()

# Scaling the data
# Normalize the 'continuous_var' column
scaler = StandardScaler()
output_data['Call Completion Rate'] = scaler.fit_transform(output_data[['Call Completion Rate']])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.25, random_state=42)

#TRY Azure
#TRY UCL LCL

# Define the model architecture
model = keras.Sequential()
model.add(layers.Dense(10, input_dim=X_train.shape[1], activation='relu'))
model.add(layers.Dense(1))

# Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))


# Evaluate the model on the test set
mse = model.evaluate(X_test, y_test)
rmse = np.sqrt(mse)
accuracy = 1 - (rmse / np.mean(output_data))

print(f'Test RMSE: {rmse:.2f}')
print(f'Test Accuraccy: ', accuracy.iloc(0,0 ))

