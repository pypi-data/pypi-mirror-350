# QuackNet

The **QuackNet** is a python based library designed for building and training neural networks and convolutional networks from scratch. It offers foundational implementations of key components such as forward propagation, backpropagation and optimisation algorithms, without relying on machine learning frameworks like TensorFlow or Pytorch

## Why this Library?

This project was developed to:

-   **Deepen understanding** of neural network by implementing them from scratch
-   **Provide a lightweight alternative** to large scale frameworks for educational purposes
-   **Offer flexibility** for experimentation with custom architectures

## Features

**1. Custom Implementation:**
-   Fully handwritten implementations for neural network layers, activation functions and loss functions.
-   No reliance on external libraries for machine learning (except for numpy)

**2. Core neural network functionality:**
-   Support for common activation functions (eg.Leaky ReLU, Sigmoid, Softmax)
-   Multiple loss functions with derivatives (eg. MSE, MAE, Cross entropy)

**3. Training:**
-   includes backpropagation for gradient calculation and parameter updates
-   ability to experiment with different optimisation techniques.

## Highlights

-   **Custom Architectures:** Define and train neural networks with fully customisable architectures
-   **Optimisation Algorithms:** Includes Gradient Descent, Stochastic Gradient Descent and Adam optimiser for efficient training
-   **Loss and Activation Functions:** Prebuilt support for common loss and activation functions with the option to make your own
-   **Layer Support:**
    -   Fully Connected (Dense)
    -   Convolutional
    -   Pooling (max and Average)
    -   Global Average Pooling
    -   Activation layer
-   **Evaluation Tools:** Includes metrics for model evaluation such as accuracy and loss
-   **Save and Load:** Save weights and biases for reuse for further training
-   **Demo Projects:** Includes example implementations such as MNIST digit classification

## Roadmap
- [X] **Forward propagation**
    Implemented the feed forward pass for neural network layers
- [X] **Activation functions**
    Added support for Leaky ReLU, Sigmoid, Softmax and others
- [X] **Loss functions**
    Implemented MSE, MAE and cross entropy loss with their derivatives
- [X] **Backpropagation**
    Completed backpropagation for gradient calculation and parameter updates
- [X] **Optimisers**
    Added support for batching, stochastic gradient descent and gradient descent
- [X] **Convolutional Neural Network**
    Implemented kernels, pooling and dense layers for Convolutional Neural Network
- [X] **Visualisation tools**  
    Added support for visualising training, such as loss and accuracy graphs
- [X] **Benchmark against PyTorch/TensorFlow**
    Benchmark against popular machine learning frameworks on MNIST library
- [X] **Add Adams optimiser**  
    Implement the Adam optimiser to improve training performance and convergence
- [X] **Data augmentation**
    add data augmentation such as flipping, rotation and cropping
- [X] **Input Data augmentation:**
    add normalisation of pixels and one hot labels
- [ ] **Skin Lesion detector**    
    use the neural network library to create a model for detecting skin lesions using HAM10000 for skin lesion images
- [ ] **Additional activation functions**  
    implement advanced activation functions (eg. GELU and Swish)

## Usage
Here is an example of how to create and train a simple neural network using the library:
```python
from quacknet.main import Network

# Define a neural network architecture
n = Network(
    lossFunc = "cross entropy",
    learningRate = 0.01,
    optimisationFunc = "sgd", #stochastic gradient descent
)
n.addLayer(3, "relu") # Input layer
n.addLayer(2, "relu") # Hidden layer
n.addLayer(1, "softmax") # Output layer
n.createWeightsAndBiases()

# Example data
inputData = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
labels = [[1], [0]]

# Train the network
accuracy, averageLoss = n.train(inputData, labels, epochs = 10)

# Evaluate
print(f"Accuracy: {accuracy}%")
print(f"Average loss: {averageLoss}")
```

## Examples

-   [Simple Neural Network Example](/ExampleCode/NNExample.py): A basic neural network implementation demonstrating forward and backpropagation
-   [Convolutional Neural Network Example](/ExampleCode/CNNExample.py): Shows how to use the convolutional layers in the library
-   [MNIST Neural Network Example](/ExampleCode/MNISTExample/mnistExample.py): Shows how to use neural network to train on MNIST

## Code structure

### Neural Network Class
-   **Purpose** Handles fully connected layers for standard neural network
-   **Key Components:**
    -   Layers: Dense Layer
    -   Functions: Forward propagation, backpropagation
    -   Optimisers: SGD, GD, GD using batching

### Convolutional Neural Network Class
-   **Purpose** Specialised for image data processing using convolutional layers
-   **Key Components:**
    -   Layers: Convolutional, pooling, dense and activation layers
    -   Functions: Forward propagation, backpropagation, flattening, global average pooling
    -   Optimsers: Adams optimiser, SGD, GD, GD using batching

## Benchmark

The library was benchmarked on the MNIST dataset using the following setup:

-   **Model Architecture:** 784 (input) → 128 → 64 → 10 (output)
-   **Activation Function:** Leaky Relu for input and hidden layer, and softmax for hidden layer
-   **Optimiser:** Batches
-   **Batch Size:** 64
-   **Learning rate:** 0.01
-   **Epochs** 10

### Results:
-   **Training accuracy:** 97.1%
-   **Average Loss:** 0.10
-   **Training Time:** 30 seconds per epoch

### Code:

The code for this benchmark can be found [here](benchmarkFolder/MNISTBenchmark/mnistExample.py)

### Training Performance

Below is the graph showing the training accuracy and loss over 10 epochs, across 5 runs:

![Training Accuaracy](benchmarkFolder/MNISTBenchmark/benchmark.png)

## Benchmark Against Pytorch and Tensorflow

The library was benchmarked on the MNIST dataset using the following setup:

-   **Neural Network Model Architecture:** 784 (input) → 128 → 64 → 10 (output)
-   **Activation Function:** Leaky Relu for input and hidden layer, and softmax for hidden layer
-   **Optimiser:** Batches
-   **Batch Size:** 64
-   **Learning rate:** 0.01
-   **Epochs** 10

### Results For QuackNet:
-   **Training Accuracy:** 97.1%
-   **Average Loss:** 0.10

### Results For Pytorch:
-   **Training Accuracy:** 93.4%
-   **Average Loss:** 0.23

### Results For Tensorflow:
-   **Training Accuracy:** 95.1%
-   **Average Loss:** 0.17

### Code:

-   The code for the QuackNet benchmark can be found [here](benchmarkFolder/MNISTBenchmark/mnistExample.py)
-   The code for the Pytorch benchmark can be found [here](benchmarkFolder/MNISTBenchmark/pytorchBenchmark.py)
-   The code for the Tensorflow benchmark can be found [here](benchmarkFolder/MNISTBenchmark/tensorflowBenchmark.py)

### Training Performance

Below is the graph showing the training accuracy and loss over 10 epochs, across 5 runs:

![Training Accuaracy](benchmarkFolder/MNISTBenchmark/frameworkBenchmark.png)