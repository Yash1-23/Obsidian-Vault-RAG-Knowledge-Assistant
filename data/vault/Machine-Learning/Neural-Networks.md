# Neural Networks

## Overview

A neural network is a machine learning model composed of interconnected computational units called neurons.

Neural networks are widely used in computer vision, natural language processing, speech recognition, and other AI applications.

## Basic Architecture

A simple neural network contains:

- Input layer
- Hidden layers
- Output layer

Each neuron receives inputs, applies weights and a bias, and passes the result through an activation function.

## Training

During training, the model makes predictions and compares them with the expected outputs.

The difference is represented by a loss function.

An optimization algorithm updates the model's parameters to reduce the loss.

A simplified training loop is:

Input → Model → Prediction → Loss → Backpropagation → Parameter Update

## Activation Functions

Common activation functions include:

- ReLU
- Sigmoid
- Tanh
- Softmax

ReLU is widely used in hidden layers of deep neural networks.

## Deep Learning

Deep learning refers to neural networks with multiple layers.

Deeper networks can learn hierarchical representations of complex data.

For example, in image recognition:

Early layers may learn edges.

Middle layers may learn shapes.

Later layers may learn objects.

## CNNs

Convolutional Neural Networks are specialized neural networks commonly used for image processing.

CNNs use convolutional filters to learn spatial features from images.

Applications include:

- Image classification
- Object detection
- Image segmentation
- Face recognition

## Transfer Learning

Transfer learning uses a model pretrained on a large dataset and adapts it to a new task.

This can reduce training time and the amount of required labeled data.

Common pretrained architectures include ResNet, EfficientNet, and Vision Transformers.