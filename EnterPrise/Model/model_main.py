import torch
import utils
from Set import DataSet
from model import DNN
from sklearn import preprocessing
from torch.utils.data import DataLoader


class control():
    def __init__(self):
        self.filepath = None

    def run(self, feature):
        input_size = len(feature.columns)
        output_size = 19
        transfer = preprocessing.StandardScaler()
        data = transfer.fit_transform(feature)
        net = DNN(input_size, output_size)
        PATH = './mnist_net.pth'
        net.load_state_dict(torch.load(PATH))
        net = DNN(input_size, output_size)
        result = utils.predict(net, feature)
        return result
