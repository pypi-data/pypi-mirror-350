import numpy as np

def ReLUDerivative(values):
    #return np.where(values > 0, 1, 0)
    return np.where(values > 0, 1, 0.01)  # This is leaky ReLU, to prevent weight gradeints all becoming 0

def sigmoid(values):
    return 1 / (1 + np.exp(-values))

def SigmoidDerivative(values):
    return sigmoid(values) * (1 - sigmoid(values))

def TanHDerivative(values):
    return 1 - (np.tanh(values) ** 2)

def LinearDerivative(values):
    return np.ones_like(values)

def SoftMaxDerivative(trueValue, values):
    #from .lossDerivativeFunctions import CrossEntropyLossDerivative
    #if(lossDerivative == CrossEntropyLossDerivative):
    #    return values - trueValue
    #summ = 0
    #for i in range(len(values)):
    #    if(currValueIndex == i):
    #        jacobianMatrix = values[currValueIndex] * (1 - values[currValueIndex])
    #    else:
    #        jacobianMatrix = -1 * values[currValueIndex] * values[i]
    #    summ += lossDerivative(values[i], trueValue[i], len(values)) * jacobianMatrix
    #return summ

    return values - trueValue #the simplification is due to cross entropy and softmax being used at the same time which is forced by library
