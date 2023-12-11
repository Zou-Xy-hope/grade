import pandas as pd
import numpy as np
import warnings

import torch
from Set import DataSet
from torch.utils.data import DataLoader
from model import DNN
import utils
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

warnings.filterwarnings('ignore')

root = "D:/study/CHR3/"
original = "D:/study/data/original.csv"
merge = "D:/study/data/merge.csv"
train = "D:/study/data/train.csv"
test = "D:/study/data/test.csv"
columns = ['time', '总资产周转率', '现金持有率', '单季度.销售毛利率', '单季度.总现金流', '单季度.总资产净利率ROA',
           '非流动负债合计', '存货周转率', '单季度.筹资活动产生的现金流量净额', '单季度.销售净利率', '单季度.营业成本',
           '资产总计', '资产负债率',
           '流动比率',
           '单季度.净资产收益率ROE', '营业周期', '有形净值债务率', '流动负债合计',
           '负债合计', '单季度.利润总额', '产权比率', '有息负债率', '股东权益周转率',
           '授信环比变动', '速动比率', '所有者权益合计', '应收账款周转率', '单季度.投资活动产生的现金流量净额',
           '抵押比率',
           '流动资产周转率', '单季度.营业收入', '非流动资产合计', '单季度.经营活动产生的现金流量净额',
           '资本收益率',
           '保守速动比率',
           '证券代码', '证券简称', 'company_type', 'ratting', '留存收益', '总资产', '现金', '流动负债',
           '经营活动产生的现金流量净额',
           '总负债', '单季度.净利润', '债务', '息税前利润(TTM)', '营运现金流',
           '单季度.销售费用']
value = ['ratting']
drop = ['time', 'company_type', 'ratting', '证券代码', '证券简称', '债务']


def read(path=None):
    test_df = pd.read_csv(test)
    train_df = pd.read_csv(train)
    return test_df, train_df
    # df = pd.read_csv(train)
    # test_df = pd.read_csv(test)
    # data = df.drop(drop, axis=1)
    # test_data = test_df.drop(drop, axis=1)
    #
    # label = df[value]
    # label[value] = label[value].apply(lambda x: x - 1)
    # test_label = test_df[value]
    # test_label[value] = test_label[value].apply(lambda x: x - 1)
    #
    # label[value] = label[value].astype('long')
    # test_label[value] = test_label[value].astype('long')
    # input_size = len(data.columns)
    # output_size = 19
    #
    # # 标准化
    # transfer = preprocessing.StandardScaler()
    # data = transfer.fit_transform(data)
    # test_data = transfer.transform(test_data)
    #
    # train_set = DataSet(data, label)
    #
    # train_loader = DataLoader(train_set, batch_size=64, shuffle=True, drop_last=True)
    # net = DNN(input_size, output_size)
    #
    # PATH = './mnist_net.pth'
    # net.load_state_dict(torch.load(PATH))
    # # net = DNN(input_size, output_size)
    #
    # test_set = DataSet(test_data, test_label)
    # test_loader = DataLoader(test_set, batch_size=64, shuffle=True, drop_last=True)
    #
    # net = utils.train(net, train_loader, test_loader, 100)
    #


def read_loader(epochs):
    df = pd.read_csv(train)
    test_df = pd.read_csv(test)
    data = df.drop(drop, axis=1)
    test_data = test_df.drop(drop, axis=1)
    label = df[value]
    label[value] = label[value].apply(lambda x: x - 1)
    test_label = test_df[value]
    test_label[value] = test_label[value].apply(lambda x: x - 1)
    label[value] = label[value].astype('long')
    test_label[value] = test_label[value].astype('long')
    input_size = len(data.columns)
    output_size = 19
    # 标准化
    transfer = preprocessing.StandardScaler()
    data = transfer.fit_transform(data)
    test_data = transfer.transform(test_data)
    train_set = DataSet(data, label)
    train_loader = DataLoader(train_set, batch_size=64, shuffle=True, drop_last=True)
    net = DNN(input_size, output_size)
    PATH = './mnist_net.pth'
    net.load_state_dict(torch.load(PATH))
    test_set = DataSet(test_data, test_label)
    test_loader = DataLoader(test_set, batch_size=64, shuffle=True, drop_last=True)
    net = utils.train(net, train_loader, test_loader, epochs)


def split(dataframe, rate):
    train_df, test_df = train_test_split(dataframe, test_size=rate)
    return train_df, test_df


def drop_zero(dataframe, col_name, value):
    dataframe = dataframe = dataframe.loc[~(dataframe[col_name] == value)]
    return dataframe


def classify(dataframe):
    classes = []
    times = dataframe["time"]
    for time in times:
        year = time[0:4]
        if year in classes:
            continue
        classes.append(year)
    df = pd.DataFrame()
    for clazz in classes:
        mask = [True if i.startswith(clazz) else False for i in dataframe["time"]]
        data = dataframe[mask]
        for index, row in data.iterrows():
            data.at[index, 'time'] = clazz
        cols = average(data)
        df = df._append(cols, ignore_index=True)
    return df


def create(length, element):
    a = []
    for i in range(length):
        a.append(element)
    return a


def average(df):
    resistance = ['time', '证券代码', "证券简称", "company_type", "ratting"]
    size = len(df)
    df0 = df[resistance].iloc[0]
    df1 = df.drop(resistance, axis=1)
    print(df1)
    df1 = df1.apply(lambda x: x.sum())
    df2 = pd.concat([df0, df1])
    return df2
