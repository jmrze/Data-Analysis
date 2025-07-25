# Abstract

This analysis is concerned with an inital exploration of the Pima diabetes dataset that captures several physiological features of women with and without diabetes in a subset of the indian Pima population. Following initial analysis for correlation of features with diabetes outcome (0 = non-diabetic, 1 = diabetic), the data was split into training and test sets in order to train a single-hidden layer neural network for diabetes outcome prediction on the basis of the recorded variables. The final neural network model was able to predict diabetes outcome with an accuracy of **74%**.

# Overview
This analysis primarily covers the following areas:
- Data analysis with Pandas
- Visualisation with Matplotlib/Seaborn
- Principal component analysis with SciKit-Learn
- Neural Network modelling with Keras

## Summary
To summarise, the model here consists of an input layer, a single hidden layer, and an output layer, for use in binary classification of diabetes status of a sample of Pima indian women (n = 768) based upon 8 distinct features. The constructed model consists of an a hidden layer which applies a ReLU function firstly, and then passes this processed data to a sigmoid activation layer to convert the data to a non-linear format in order to predict the probability of diabetes outcome (0 being non-diabetic, and 1 being diabetic).

Data were firstly separated into the target ('Outcome') and features (8 remaining variables) and then split into a training/test split at a ratio of 7:3. The model was then trained upon this data with 100 epochs and a batch size of 10 and evaluated against the target test split. Evaluation of the model found that accuracy was c. 75% over multiple recompilations with an accuracy, precision, recall and f1 score that all approximated 62.5%.

In conclusion, this neural network model is able to predict Diabetes status on the basis of 8 physiological health features in a set of Pima indian women with an accuracy of approximately 75%.

# Files
- pima_neural.net.ipynb - Jupyter lab notebook containing annotated code and a concise concluding report
- pima_neuralnet.py - python script to run the neural network independently
- diabetes_pima.csv - csv file containing the analysed data
