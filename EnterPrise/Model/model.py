import torch.nn as nn
import torch
from torch.nn.utils.rnn import pack_padded_sequence


class DNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DNN, self).__init__()
        hidden_size1 = 128
        hidden_size2 = 64
        self.linear1 = nn.Linear(input_size, hidden_size1)
        self.linear2 = nn.Linear(hidden_size1, hidden_size2)
        self.linear3 = nn.Linear(hidden_size2, output_size)
        self.activate = nn.ReLU()

    def forward(self, x):
        x = self.activate(self.linear1(x))
        x = self.activate(self.linear2(x))
        x = self.linear3(x)
        return x
