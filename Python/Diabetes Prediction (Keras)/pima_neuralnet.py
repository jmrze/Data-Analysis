# library
import pandas as pd
import numpy as np
import keras as keras
from keras.models import Sequential
from keras.layers import Dense

# dataset
#df = pd.read_csv('/home/james/Documents/analysis/python/Diabetes_practice/diabetes_pima.csv')
df = pd.read_csv('diabetes_pima.csv')

# input/target split
features = df.drop(columns='Outcome')
target = df['Outcome']

# model definition
model = Sequential()
model.add(keras.layers.Input(shape=(features.shape[1],))) # defne input layer shape
model.add(keras.layers.Dense(8, activation='relu')) # relu function for 8 inputs
model.add(keras.layers.Dense(1, activation='sigmoid')) # sigmoid activation fxn

# model compilation
model.compile(loss='binary_crossentropy', # compile model
              optimizer='adam', # adam gradient descent algorithm
              metrics=['accuracy']) # reporting accuracy as metric

# fitting model
model.fit(features, target,
          epochs=150,
          batch_size=10)

# model evaluation
_, accuracy = model.evaluate(features, target)
print('Accuracy: %.2f' % (accuracy*100)) # 76.69% accuracy

# prediction
predictions = (model.predict(features) > 0.5).astype(int)

for i in range(10):
    print('%s => %d (expected %d)' % (features[i].tolist(), predictions[i], target[i]))