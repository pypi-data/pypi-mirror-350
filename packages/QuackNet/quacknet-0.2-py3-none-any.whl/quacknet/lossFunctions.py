import math
import numpy as np

def MSELossFunction(predicted, true):
    return np.mean((np.array(true) - np.array(predicted)) ** 2)

def MAELossFunction(predicted, true):
    return np.mean(np.abs(np.array(true) - np.array(predicted)))

def CrossEntropyLossFunction(predicted, true):
    predicted = np.clip(predicted, 1e-10, 1-1e-10)
    return -np.sum(np.array(true) * np.log(predicted))
