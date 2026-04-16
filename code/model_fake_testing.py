import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F

class FFNN(nn.Module):

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
    

def main():
    ffnn = FFNN(128, 7, 0.5)

    data = pd.read_csv(".\\data_2.csv")
    data = data.sample(frac=1)

    X, Y = data[data.columns[2:]], data[data.columns[0]]
    
    X = torch.tensor(X.values, dtype=torch.float, device='cuda')
    Y = torch.tensor(Y.values, dtype=torch.int64, device='cuda')

    ffnn = ffnn.to('cuda')

    loss_fn = torch.nn.CrossEntropyLoss().to('cuda')
    optimizer = torch.optim.Adam(ffnn.parameters(), lr=0.001)

    epochs = 300

    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()

        Y_hat = ffnn(X)

        loss = loss_fn(Y_hat, Y)
        loss.backward()

        optimizer.step()

        accuracy = torch.mean((torch.argmax(Y_hat, dim=1) == Y).float())
        
        if epoch % 10 == 0:
            print(f'Step: {epoch}, Loss: {loss.item()}, Accuracy: {accuracy}')
    
    torch.save(ffnn.state_dict(), '.\\model.pickle')


if __name__ == '__main__':
    main()
