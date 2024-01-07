# 导入Flask类库
import torch
import utils
from Set import DataSet
from flask import Flask, request
from flask_cors import CORS
from DBservice import DB, to_json
from Read import read
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import os

from model import DNN
from sklearn import preprocessing
from torch.utils.data import DataLoader
from handle import Dispose

# 创建应用实例
app = Flask(__name__)
CORS(app)

db = DB()

test_df, train_df = read()


def loader():
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
    trainloader = DataLoader(train_set, batch_size=64, shuffle=True, drop_last=True)
    net = DNN(input_size, output_size)
    PATH = './mnist_net.pth'
    net.load_state_dict(torch.load(PATH))
    test_set = DataSet(test_data, test_label)
    testloader = DataLoader(test_set, batch_size=64, shuffle=True, drop_last=True)
    return trainloader, testloader, net, data, label


train_loader, test_loader, net, all_data, all_label = loader()

executor = ThreadPoolExecutor(10)


def get_data(colnum):
    data = all_data[colnum - 1]
    print(type(all_label))
    data = data[np.newaxis, :]
    label = all_label.loc[colnum - 1]
    myset = DataSet(data, label)
    loader = DataLoader(myset, batch_size=1, shuffle=True, drop_last=True)
    return loader


def to_tuple(dataframe):
    headers = ['name', 'value']
    cols = train_df.columns
    result = []
    for i in range(len(cols)):
        col = cols[i]
        dat = str(dataframe[i])
        result.append((col, dat))
    result = to_json(result, headers)
    return result


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


@app.route('/load')
def a():
    result = db.search_name()
    return result.getData()


@app.route('/load/<company>')
def c(company):
    result = db.search_time(company)
    return result.getData()


@app.route('/load/<company>/<time>')
def f(company, time):
    index, rat = db.search_index(company, time)
    data = train_df.loc[index - 1]
    result = to_tuple(data)
    return [{'data': result.getData(), 'index': index}]


@app.route('/result/<index>')
def g(index):
    loader = get_data(int(index))
    acc, pre = utils.test(net, loader)
    pre = pre.item() + 1
    result = to_json([(acc, pre)], ['accuracy', 'predict'])
    return result.getData()


@app.route('/model/<epochs>')
def accuracy(epochs):
    group = db.submit()
    executor.submit(read_loader, epochs, group)
    return str(group)
    # thread.start()
    # read_loader()


@app.route('/accuracy/<group>')
def b(group):
    d = db.search1(group)
    return d.getData()


@app.route("/file", methods=["POST", "GET"])
def file_receive():
    print(request)
    file = request.files.get("file")
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    print("获取上传文件的名称为[%s]\n" % file_name)
    path = os.getcwd() + "/upload/" + file_name
    file.save(path)  # 保存文件
    token = db.sub_token()
    executor.submit(sub_loader, path, "(1)" + file_name, token)
    return str(token)


@app.route('/predict/<token>')
def pre(token):
    result = db.get_pre(token)
    data = result.getData()
    if data == ():
        return {
            'code': 201,
            'msg': "未测试完成"
        }
    return {
        'code': 200,
        'data': data
    }


def read_loader(epochs, group):
    utils.train(net, db, train_loader, test_loader, int(group), int(epochs))


def sub_loader(path, name, token):
    dp = Dispose()
    dp.read(path)
    dp.set_name(name)
    dp.fill()
    loader = dp.load()
    print(loader)
    acc, pre = utils.test(net, loader)
    db.set_pre(token, pre.item() + 1)
