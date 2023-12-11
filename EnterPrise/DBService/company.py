from DBservice import DB

columns = ['time',
           '证券简称',
           '证券代码',
           'company_type',
           'ratting',
           '单季度.总资产净利率ROA',
           '资产总计',
           '资产负债率',
           '流动比率',
           '单季度.净资产收益率ROE',
           '有形净值债务率',
           '负债合计',
           '单季度.利润总额',
           '单季度.投资活动产生的现金流量净额',
           '单季度.营业收入',
           '单季度.经营活动产生的现金流量净额',
           '资本收益率'
           ]


def save(dataframe):
    db = DB()
    df = dataframe[columns]
    # print(df.dtypes)
    args = []
    for index, row in df.iterrows():
        args = get_data(row)
        db.insert(args)


def get_data(row):
    data = []
    for col in columns:
        data.append(row[col])
    return data
