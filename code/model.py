import torch
import torch.nn as nn
import torch.nn.functional as F
import tkinter as tk
import os
from csv_handle import csvHandle
from tkinter import ttk


class FeedForwardNeuralNetwork(nn.Module):

    def __init__(self, hidden_layer_size: int, output_size: int, dropout: float=None):
        """
        Feed forward neural network with 3 linear layers
        First layer: 42 inputs, hidden_layer_size outputs
        Second layer: hidden_layer_size inputs, hidden_layer_size / 2 outputs
        Third layer: hidden_layer_size / inputs, output_size outputs
        Each layer uses the ReLU activation function
        Dropout determines what percentage of the neurones are turned off during training each epoch
        """
        super().__init__()
        self.l1 = nn.Linear(42, hidden_layer_size)
        self.l2 = nn.Linear(hidden_layer_size, hidden_layer_size)
        self.l3 = nn.Linear(hidden_layer_size, hidden_layer_size // 2)
        self.l4 = nn.Linear(hidden_layer_size // 2, output_size)
        if dropout:
            self.d1 = nn.Dropout(dropout)
            self.d2 = nn.Dropout(dropout)
        else:
            self.d1 = self.d2 = None

    def forward(self, X):
        """
        Forward pass of the neural network
        """
        X = F.relu(self.l1(X))
        X = F.relu(self.l2(X))
        if self.d1:
            X = self.d1(X)
        X = F.relu(self.l3(X))
        if self.d2:
            X = self.d2(X)
        X = F.relu(self.l4(X))
        # return F.softmax(X)
        return X


class Model:

    def __init__(self, device: str, output_size: int, path: str):
        """
        A class that containst a FeedForwardNeuralNetwork
        Enables label prediction and retraining of the network
        device can be either cuda or cpu, which determines which one the model will run on
        output_size determines how many possible labels the network can output
        """
        self.device = device
        self.FFNN = FeedForwardNeuralNetwork(128, output_size, 0.5)
        if os.path.exists(".\\model.pickle"):
            self.FFNN.load_state_dict(torch.load(".\\model.pickle", weights_only=False, map_location=torch.device(device)))
        self.handle = csvHandle(path)

    def predict(self, landmarks: list[float], centroid: list[int, int], stop: int):
        """
        Gets the output from the neural network and performs an argmax to get the label it chose
        Returns landmarks, centroid, and stop
        """
        self.FFNN = self.FFNN.to(self.device)
        self.FFNN.eval()
        # The input tensor must be on the same device as the model in order to run
        landmarks = torch.tensor(landmarks, dtype=torch.float).to(self.device)
        y = self.FFNN(landmarks)

        label = torch.argmax(y).item()
        return label, centroid, stop

    def retrain(self, bar: ttk.Progressbar) -> None:
        """
        Retrains the model using all data available in the csv file
        Will also step a progressbar at each step to give the user an indication of how long it will take
        The number of epochs used = 300 * (n - (n % 5)) where n is the number of labels
        """
        X, Y = self.handle.prepare_data()

        n = self.handle.count_labels()

        # A new FFNN must be created as to not reuse the previous weights, as they will not work in case the amount of labels has increased
        self.FFNN = FeedForwardNeuralNetwork(128, n, 0.5)

        loss_fn = nn.CrossEntropyLoss()
        # Everything must be transferred to the same device in order to work
        self.FFNN = self.FFNN.to(self.device)
        loss_fn = loss_fn.to(self.device)

        X = torch.tensor(X, dtype=torch.float).to(self.device)
        Y = torch.tensor(Y, dtype=torch.int64).reshape(-1).to(self.device)

        optimiser = torch.optim.Adam(self.FFNN.parameters())

        n = self.handle.count_labels()
        epochs = 300 * (n - (n % 5))
        # This way the bar has an equal number of steps as epochs, so each epoch only bar.step() must be called, no extra maths
        # 1 has to be added to epochs to stop it from resetting back to 0 when it reaches the final epoch
        bar.config({"maximum": epochs + 1})

        for epoch in range(epochs):
            optimiser.zero_grad()

            Y_pred = self.FFNN(X)

            loss = loss_fn(Y_pred, Y)

            loss.backward()
            optimiser.step()
            bar.step()

        torch.save(self.FFNN.state_dict(), '.\\model.pickle')
        bar.step()
