"""
此类用于数据库查询数据后的传输和封装，便于统一规范
code：代表查询成功与否
data：代表数据
"""


class Result:
    def __init__(self, code, data=None):
        self.code = code
        self.data = data

    def getCode(self):
        return self.code

    def getData(self):
        return self.data

    def setCode(self, code):
        self.code = code

    def setData(self, data):
        self.data = data
