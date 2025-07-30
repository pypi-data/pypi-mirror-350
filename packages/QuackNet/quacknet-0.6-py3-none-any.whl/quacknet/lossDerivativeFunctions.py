import numpy as np
from quacknet.activationDerivativeFunctions import SoftMaxDerivative

def MSEDerivative(value, trueValue, sizeOfLayer):
    return 2 * (value - trueValue) / sizeOfLayer

def MAEDerivative(value, trueValue, sizeOfLayer):
    #summ = value - trueValue
    #if(summ > 0):
    #    return 1 / sizeOfLayer
    #elif(summ < 0):
    #    return -1 / sizeOfLayer
    #return 0
    return np.sign(value - trueValue) / sizeOfLayer

def CrossEntropyLossDerivative(value, trueVale, activationDerivative):
    if(activationDerivative == SoftMaxDerivative):
        return value - trueVale
    return -1 * (trueVale / value)
