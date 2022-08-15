# Python-Stock-Trading-Bot
### This is a personal project to predict prices of stocks before buying and selling via real time data using python. This project is still in development but it mines data using the TD Ameritrade API before passing said data through a tensor flow LSTM model, harnessing the power of machine learning. Antwon makes predictions on 85% of 5 years of training data. Then, uses the remaining 15% to validate predictions. All data is relevant and the last prediction was for the current date the image was uploaded. 

![ntflx30jun](https://user-images.githubusercontent.com/84476080/176819775-2a6d8953-4a75-43a3-b6b9-1199876cbb50.jpeg)
<img width="1107" alt="coke" src="https://user-images.githubusercontent.com/84476080/176821326-33d2d457-6c49-4e77-900d-32b1ab660435.png">

<img width="906" alt="tesla" src="https://user-images.githubusercontent.com/84476080/176822574-8a106518-ac7d-49c7-8bf5-16c713902a3f.png">


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
import math
from sklearn.preprocessing import MinMaxScaler

# This makes the chart look so much better


data=pd.read_csv("data.csv")
#Print rows & Columns = print(data.shape)
dates = data[' Date']
ticker = data[' Name'][0]



#data.plot(' Date',' Close',color="red")
#plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees

# 1. Filter out the closing market price data

# 2. Convert the data into array for easy evaluation
data =  data.filter([' Close'])
dataset = data.values

# 3. Scale/Normalize the data to make all values between 0 and 1 (inclusive)
# Its just good practice that "might help the model"
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
 
# 4. Creating training data size : 80% of the data
training_data_len = math.ceil(len(dataset) *.8)
train_data = scaled_data[0:training_data_len  , : ]
 
# 5. Separating the data into x and y data
#independent var (feature)
x_train_data= []
#dependent var (feature)
y_train_data =[]
for i in range(60,len(train_data)):
    x_train_data=list(x_train_data)
    y_train_data=list(y_train_data)
    x_train_data.append(train_data[i-60:i,0]) #position 0 - 59
    y_train_data.append(train_data[i,0]) #position 60
    
 
# Converting the training x and y values to numpy arrays
x_train_data1, y_train_data1 = np.array(x_train_data), np.array(y_train_data)

# Reshaping training x and y data to make the calculations easier
# number of rows = shape[0], columns = shape[1]
x_train_data = np.reshape(x_train_data1, (x_train_data1.shape[0],x_train_data1.shape[1],1))


# Build Model!
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train_data.shape[1],1)))
model.add(LSTM(units=50, return_sequences=False)) # This is false because its the last LSTM layer!
model.add(Dense(units=25)) # Densly connected neural network with 25 neurons
model.add(Dense(units=1))

# Optimizer helps optimize the loss function, and this tells us how well we did in training
model.compile(optimizer='adam', loss='mean_squared_error')
# "Fit" is another word for "TRAIN" (the model)
# Epoch is the number of iterations when data set is passed forward and backward through the model
model.fit(x_train_data, y_train_data1, batch_size=1, epochs=1)



# Now create TESTING data set
#From index.lenth - 60 to the end of array, with all columns
test_data = scaled_data[training_data_len - 60: , : ]

# Will contain first 60
x_test = []
# Will contain 61st
y_test =  dataset[training_data_len: , : ]
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])
 
# Convert the values into arrays for easier computation
x_test = np.array(x_test)
# We need 3 columns not two thus "reshape". The number of features is just the close price, thus 1!
# **** Thus think about adding more features might be that easy!
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
 
# Making predictions on the testing data
predictions = model.predict(x_test)
# Essentially unscale the values. We want these values to be the same that y_test dataset*
predictions = scaler.inverse_transform(predictions)

# (RMSE is a good measure of accuracy, its the standard deviation of the residuals)
# Evaluate the model. The lower the better!
rmse = np.sqrt(np.mean(predictions - y_test)**2)

#Value of 0 means the predictions were perfect...
print(rmse)



# Plot the data
train = data[:training_data_len]
# this is the training data
valid = data[training_data_len:]
valid['Predictions'] = predictions

# Visualize the data
plt.style.use("fivethirtyeight")
plt.figure(figsize=(28,28))
plt.title(ticker)

x_ticks  = np.array(x_test)
loc = range(len(dates))
labels = dates
plt.xticks(ticks=loc,labels=labels, rotation='vertical')
plt.xlabel('Date', fontsize=38)
plt.ylabel('Close Price USD ($)')
plt.plot(train[' Close'])
plt.plot(valid[[' Close', 'Predictions']])
plt.legend(['Training Data', 'Actual Closing', 'Predicted Closing'], loc='upper right')
plt.show()


# Visualize via table
print(valid.head())
print(valid.tail())

# Predict specific day
day_quote = pd.read_csv("data.csv")
# create new data fram
new_df = day_quote.filter([' Close'])
last_60 = new_df[-60:].values
last_60_scaled = scaler.transform(last_60)
X_test = []
X_test.append(last_60_scaled)
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1],1))
pred_price = model.predict(X_test)
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)
