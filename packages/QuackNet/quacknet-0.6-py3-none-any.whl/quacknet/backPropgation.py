from quacknet.activationFunctions import relu, sigmoid, tanH, linear, softMax
from quacknet.activationDerivativeFunctions import ReLUDerivative, SigmoidDerivative, TanHDerivative, LinearDerivative, SoftMaxDerivative
from quacknet.lossDerivativeFunctions import MSEDerivative, MAEDerivative, CrossEntropyLossDerivative
from quacknet.lossFunctions import MSELossFunction, MAELossFunction, CrossEntropyLossFunction
import numpy as np

'''
output layer backpropogation for weights:
e = (dL/da) * f'(z)
e = error term
dL/da = derivative of the loss function
f'() = derivative of the activation function
z = the current layer's node (only one)

(dL/dW) = e * a
dL/dW  = derivative of loss function with respect to weight
e = error term
a = past layer's node value

nw = ow - r * (dL/dW)
nw = new weight
ow = old weight
r = learning rate
(dL/dW) = derivative of loss function with respect to weight

hidden layer backpropgation for weights:
e = SUM(e[l + 1][k] * w[l + 1][k]) * f'(z)
e = error term
SUM(e[l + 1][k] * w[l + 1][k]) = the sum of the next layers's error term for the current node multiplied by the weight in the nextlayer connected to the current one
f'() = derivative of the activation function
z = the current layer's node (only one)

(dL/dW) = e * a
dL/dW  = derivative of loss function with respect to weight
e = error term
a = past layer's node value

nw = ow - r * (dL/dW)
nw = new weight
ow = old weight
r = learning rate
(dL/dW) = derivative of loss function with respect to weight
'''

def outputLayerWeightChange(lossDerivative, activationDerivative, currentLayerNodes, pastLayerNodes, trueValues): 
    if(activationDerivative == SoftMaxDerivative and lossDerivative == CrossEntropyLossDerivative):
        errorTerms = currentLayerNodes - trueValues
    else:
        lossDerivativeValue = lossDerivative(currentLayerNodes, trueValues, len(currentLayerNodes))
        errorTerms = lossDerivativeValue * activationDerivative(currentLayerNodes)
    weightGradients = np.outer(pastLayerNodes, errorTerms)
    return weightGradients, errorTerms

def hiddenLayerWeightChange(pastLayerErrorTerms, pastLayerWeights, activationDerivative, currentLayerNodes, pastLayerNodes):
    errorTerms = (pastLayerErrorTerms @ pastLayerWeights.T) * activationDerivative(currentLayerNodes)
    weightGradients = np.outer(pastLayerNodes, errorTerms)
    return weightGradients, errorTerms

def outputLayerBiasChange(lossDerivative, activationDerivative, currentLayerNodes, trueValues):
    if(activationDerivative == SoftMaxDerivative and lossDerivative == CrossEntropyLossDerivative):
        errorTerms = currentLayerNodes - trueValues
    else:
        lossDerivativeValue = lossDerivative(currentLayerNodes, trueValues, len(currentLayerNodes))
        errorTerms = lossDerivativeValue * activationDerivative(currentLayerNodes)
    biasGradients = errorTerms
    return biasGradients, errorTerms


def hiddenLayerBiasChange(pastLayerErrorTerms, pastLayerWeights, activationDerivative, currentLayerNodes):
    errorTerms = (pastLayerErrorTerms @ pastLayerWeights.T) * activationDerivative(currentLayerNodes)
    biasGradients = errorTerms
    return biasGradients, errorTerms

def backPropgation(layerNodes, weights, biases, trueValues, layers, lossFunction, returnErrorTermForCNN = False):
    lossDerivatives = {
        MSELossFunction: MSEDerivative,
        MAELossFunction: MAEDerivative,
        CrossEntropyLossFunction: CrossEntropyLossDerivative,
    }
    activationDerivatives = {
        relu: ReLUDerivative,
        sigmoid: SigmoidDerivative,
        linear: LinearDerivative,
        tanH: TanHDerivative,
        softMax: SoftMaxDerivative,
    }
    w, weightErrorTerms = outputLayerWeightChange(lossDerivatives[lossFunction], activationDerivatives[layers[len(layers) - 1][1]], layerNodes[len(layerNodes) - 1], layerNodes[len(layerNodes) - 2], trueValues)
    b, biasErrorTerms = outputLayerBiasChange(lossDerivatives[lossFunction], activationDerivatives[layers[len(layers) - 1][1]], layerNodes[len(layerNodes) - 1], trueValues)
    hiddenWeightErrorTermsForCNNBackpropgation = weightErrorTerms
    weightGradients = [w]
    biasGradients = [b]
    for i in range(len(layers) - 2, 0, -1):
        w, weightErrorTerms = hiddenLayerWeightChange(
            weightErrorTerms, 
            weights[i], 
            activationDerivatives[layers[i][1]], 
            layerNodes[i], 
            layerNodes[i - 1]
        )
        b, biasErrorTerms = hiddenLayerBiasChange(
            biasErrorTerms, 
            weights[i], 
            activationDerivatives[layers[i][1]], 
            layerNodes[i]
        )
        weightGradients.append(w)
        biasGradients.append(b)
    weightGradients.reverse()
    biasGradients.reverse()
    if(returnErrorTermForCNN == True):
        return weightGradients, biasGradients, hiddenWeightErrorTermsForCNNBackpropgation
    return weightGradients, biasGradients
