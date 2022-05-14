import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import MinMaxScaler


dataset_train = pd.read_csv('./2022-04-19/04-19\'s candle_stick.csv')
#print(dataset_train.head())

training_set = dataset_train.iloc[:,1:2].values
print(training_set)
print(training_set.shape)

scaler = MinMaxScaler(feature_range = (0,1))
scaled_training_set = scaler.fit_transformation(training_set)

print(scaled_training_set)