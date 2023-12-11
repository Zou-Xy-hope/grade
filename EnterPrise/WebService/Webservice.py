# 导入Flask类库
import math
import random
import time

import torch
import utils
from Set import DataSet
from flask import Flask
from flask_cors import CORS
from DBservice import DB, to_json
from Read import read
from concurrent.futures import ThreadPoolExecutor

from model import DNN
from sklearn import preprocessing
from torch.utils.data import DataLoader

# 创建应用实例
app = Flask(__name__)
CORS(app)

db = DB()

test_df, train_df = read()

executor = ThreadPoolExecutor(5)

# 本文件用于部署后端服务
# 后端需要完成的功能：
# 1、查询数据总数（展示时脱敏）
# 2、查询某一企业数据（展示时脱敏并展示图标
# 3、输入数据跑模型
# 视图函数（路由）

def get_app():
    return app


@app.route('/showall')
def search_all():
    # 数据库查询并返回
    result = db.search_all()
    return result.getData()


@app.route('/search/<company>')
def search(company):
    # 查询数据库并返回
    result = db.search(company)
    return result.getData()


@app.route('/model/<epochs>')
def accuracy(epochs):
    executor.submit(read_loader, epochs)
    return 'a'
    # thread.start()
    # read_loader()


@app.route('/accuracy')
def b():
    d = db.search1()
    return d.getData()


def read_loader(epochs):
    drop = ['time', 'company_type', 'ratting', '证券代码', '证券简称', '债务']
    value = ['ratting']
    data = train_df.drop(drop, axis=1)
    test_data = test_df.drop(drop, axis=1)
    label = train_df[value]
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
    utils.train(net, db, train_loader, test_loader, int(epochs))
