import torch.optim as optim
import matplotlib.pyplot as plt
from torch import nn
import torch


# 损失和优化函数

def train(net, db, train_loader, test_loader, epochs=1):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.05)
    for epoch in range(epochs):
        running_loss = 0.0
        for x, y in train_loader:
            optimizer.zero_grad()
            output = net(x)
            y = y.long()
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print("epoch = {0} ;loss = {1}".format(epoch, running_loss))
        acc = test(net, test_loader)
        db.insert1([epoch, acc])
    # PATH = './mnist_net.pth'
    # torch.save(net.state_dict(), PATH)
    # print("模型已保存在" + PATH)
    return net


def draw_train_process(title, iters, costs, accs, label_cost, lable_acc):
    plt.title(title, fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel("accuracy(\%)", fontsize=20)
    plt.plot(iters, costs, color='black', label=label_cost)
    plt.plot(iters, accs, color='grey', label=lable_acc)
    plt.legend()
    plt.grid()
    plt.show()


def draw_accuracy(title, accs, epochs):
    iters = range(epochs + 1)
    plt.title(title, fontsize=24)
    plt.xlabel("epochs", fontsize=20)
    plt.ylabel("accuracy(\%)", fontsize=20)
    plt.plot(iters, accs, color='grey', label="test_accuracy")
    plt.legend()
    plt.grid()
    plt.show()


def test(net, test_loader):
    correct = 0
    total = 0
    with torch.no_grad():  # 进行评测的时候网络不更新梯度
        for data in test_loader:
            datas, labels = data
            outputs = net(datas)
            # y_hat = torch.max(outputs.data, 1)
            # y = labels.detach().numpy()
            # predict = y_hat.indices.detach().numpy()
            # correct += acuuracy(y, predict)
            # total += labels.size(0)
            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print('Accuracy of the network on the  test data: %d %%' % (
            100 * correct / total))
    return 100 * correct / total


def acuuracy(y, y_pre):
    length = len(y)
    correct = 0
    for i in range(length):
        if y[i] == y_pre[i]:
            correct += 1
    return correct


def predict(net, feature):
    with torch.no_grad():
        output = net(feature)
        _, predicted = torch.max(output.data, dim=1)
        return predicted
