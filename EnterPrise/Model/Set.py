import torch
from torch.utils.data import Dataset, DataLoader


class DataSet(Dataset):
    def __init__(self, data_features, data_target):
        x = data_features
        y = data_target.values
        x_data = x.reshape(-1, x.shape[1])
        y_data = y.reshape(-1)
        self.features = torch.from_numpy(x_data).float()
        self.target = torch.from_numpy(y_data)
        self.len = self.features.shape[0]

    def __getitem__(self, index):
        x = self.features[index]
        y = self.target[index]
        return x, y

    def __len__(self):
        return self.len
