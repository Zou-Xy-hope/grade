import Webservice
# import Read
# import company
# import pandas as pd
# from DBservice import DB
# import numpy as np
# 启动实施（只在当前模块运行）

app = Webservice.get_app()
# db = DB()

if __name__ == '__main__':
    app.run()
    # Webservice.read_loader(5)
    # db.search('平安银行')
    # df = pd.read_csv('D:/study/data/train.csv')
    # company.save(df)
    # Read.read()
    # data = np.random.randn(10, 11)
    # print(data)

