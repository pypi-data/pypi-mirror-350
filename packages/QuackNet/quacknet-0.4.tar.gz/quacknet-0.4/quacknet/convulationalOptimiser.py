import numpy as np

class CNNoptimiser:
    def AdamsOptimiserWithBatches(self, inputData, labels, weights, biases, batchSize, alpha, beta1, beta2, epsilon):
        firstMomentWeight, firstMomentBias = self.initialiseMoment(weights, biases)
        secondMomentWeight, secondMomentBias = self.initialiseMoment(weights, biases)
        weightGradients, biasGradients = self.initialiseGradients(weights, biases)
        allNodes = []
        for i in range(0, len(inputData), batchSize):
            batchData = inputData[i:i+batchSize]
            batchLabels = labels[i:i+batchSize]
            for j in range(len(batchData)):
                layerNodes = self.forward(batchData[j])
                allNodes.append(layerNodes)
                w, b = self.backpropagation(layerNodes, batchLabels[j])
                weightGradients, biasGradients = self.addGradients(weightGradients, biasGradients, w, b)
            weights, biases, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias = self._Adams(weightGradients, biasGradients, weights, biases, i + 1, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias, alpha, beta1, beta2, epsilon)
            weightGradients, biasGradients = self.initialiseGradients(weights, biases)
        return allNodes, weights, biases

    def AdamsOptimiserWithoutBatches(self, inputData, labels, weights, biases, alpha, beta1, beta2, epsilon):
        firstMomentWeight, firstMomentBias = self.initialiseMoment(weights, biases)
        secondMomentWeight, secondMomentBias = self.initialiseMoment(weights, biases)
        weightGradients, biasGradients = self.initialiseGradients(weights, biases)
        allNodes = []
        for i in range(len(inputData)):
            layerNodes = self.forward(inputData[i])
            allNodes.append(layerNodes)
            w, b = self.backpropagation(layerNodes, labels[i])
            weightGradients, biasGradients = self.addGradients(weightGradients, biasGradients, w, b)
            weights, biases, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias = self._Adams(weightGradients, biasGradients, weights, biases, i + 1, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias, alpha, beta1, beta2, epsilon)
            weightGradients, biasGradients = self.initialiseGradients(weights, biases)
        return allNodes, weights, biases

    def _Adams(self, weightGradients, biasGradients, weights, biases, timeStamp, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias, alpha, beta1, beta2, epsilon):
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                firstMomentWeight[i][j] = beta1 * np.array(firstMomentWeight[i][j]) + (1 - beta1) * weightGradients[i][j]
                secondMomentWeight[i][j] = beta2 * np.array(secondMomentWeight[i][j]) + (1 - beta2) * (weightGradients[i][j] ** 2)

                firstMomentWeightHat = firstMomentWeight[i][j] / (1 - beta1 ** timeStamp)
                secondMomentWeightHat = secondMomentWeight[i][j] / (1 - beta2 ** timeStamp)

                weights[i][j] -= alpha * firstMomentWeightHat / (np.sqrt(secondMomentWeightHat) + epsilon)
            
        for i in range(len(biases)):
            for j in range(len(biases[i])):
                firstMomentBias[i][j] = beta1 * np.array(firstMomentBias[i][j]) + (1 - beta1) * np.array(biasGradients[i][j])
                secondMomentBias[i][j] = beta2 * np.array(secondMomentBias[i][j]) + (1 - beta2) * (np.array(biasGradients[i][j]) ** 2)

                firstMomentBiasHat = firstMomentBias[i][j] / (1 - beta1 ** timeStamp)
                secondMomentBiasHat = secondMomentBias[i][j] / (1 - beta2 ** timeStamp)

                biases[i][j] -= alpha * firstMomentBiasHat / (np.sqrt(secondMomentBiasHat) + epsilon)
        return weights, biases, firstMomentWeight, firstMomentBias, secondMomentWeight, secondMomentBias

    def initialiseGradients(self, weights, biases):
        weightGradients, biasGradients = [], []
        for i in weights:
            w = []
            for j in i:
                w.append(np.zeros_like(j, dtype=np.float64))
            weightGradients.append(w)
        for i in biases:
            b = []
            for j in i:
                b.append(np.zeros_like(j, dtype=np.float64))
            biasGradients.append(b)
        return weightGradients, biasGradients

    def addGradients(self, weightGradients, biasGradients, w, b):
        for i in range(len(weightGradients)):
            for j in range(len(weightGradients[i])):
                weightGradients[i][j] += np.array(w[i][j])
            #weightGradients[i] = np.clip(weightGradients[i], -1, 1)

        for i in range(len(biasGradients)):
            for j in range(len(biasGradients[i])):
                biasGradients[i][j] += np.array(b[i][j])
            #biasGradients[i] = np.clip(biasGradients[i], -1, 1)
        return weightGradients, biasGradients

    def initialiseMoment(self, weights, biases):
        momentWeight = []
        momentBias = []
        for i in weights:
            w = []
            for j in i:
                w.append(np.zeros_like(j))
            momentWeight.append(w)
        for i in biases:
            b = []
            for j in i:
                b.append(np.zeros_like(j))
            momentBias.append(b)
        return momentWeight, momentBias

    