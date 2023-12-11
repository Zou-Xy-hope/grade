import pymysql
import logging
from Result import Result
import json
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
columns = ['time', 'company', 'company_code', 'company_type', 'ratting', 'ROA', 'ROE', 'total_asset',
           'asset_liability_ratio', 'current_ratio', 'tangible_equity_debt_ratio', 'total_liabilities',
           'total_profit_per_quarter', 'sq_net_cash_flows', 'sq._operating_income',
           'return_on_capital']

lock = threading.Lock()

class DB:
    def __init__(self):
        logger.info("创建连接")
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.db = 'company'
        self.charset = 'utf8'
        self.mysql_conn = None
        self.connect()

    def connect(self):
        try:
            self.mysql_conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.db,
                charset=self.charset
            )
            logger.info("连接成功")
        except Exception as e:
            logger.warning(e)

    def close(self):
        if self.mysql_conn:
            self.mysql_conn.close()
            self.mysql_conn = None

    def execute(self, sql, args=None, commit=False):
        try:
            with self.mysql_conn.cursor() as cursor:
                lock.acquire()
                cursor.execute(sql, args)
                lock.release()
                if commit:
                    self.mysql_conn.commit()
                    logger.info(f"执行 SQL 语句：{sql}，参数：{args}，数据提交成功")
                    return Result(True)
                else:
                    result = cursor.fetchall()
                    logger.info(f"执行 SQL 语句：{sql}，参数：{args}，查询到的数据为：{result}")
                    return Result(result == (), result)
        except Exception as e:
            logger.info(f"执行 SQL 语句出错：{e}")
            self.mysql_conn.rollback()
            return Result(False)

    def search(self, company):
        sql = "SELECT * FROM company WHERE company=%s"
        args = company
        result = self.execute(sql, args)
        result = to_json(result.getData(), columns)
        # 脱敏
        return result

    def search_all(self):
        sql = "SELECT * FROM company LIMIT 500"
        result = self.execute(sql)
        result = to_json(result.getData(), columns)
        # 脱敏
        return result

    def insert(self, args):
        sql = "INSERT INTO company(`time`, `company`, `company_code`, `company_type`, `ratting`, `ROA`, `ROE`, `total_asset`,`asset_liability_ratio`, `current_ratio`, `tangible_equity_debt_ratio`, `total_liabilities`,`total_profit_per_quarter`, `sq_net_cash_flows`, `sq._operating_income`,`sq_net_cash`,`return_on_capital`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        result = self.execute(sql, args, True)
        return result

    def insert1(self, args):
        sql = "INSERT INTO accuracy(`id`,`accuracy`) VALUES(%s, %s) "
        result = self.execute(sql, args, True)
        return result

    def search1(self):
        sql = "SELECT * FROM accuracy"
        result = self.execute(sql)
        result = to_json(result.getData(), ['id', 'accuracy'])
        # 脱敏
        return result


def to_json(data, col):
    if data is None:
        return Result(False)
    strings = []
    for item in data:
        dic = {}
        for index in range(len(col)):
            key = col[index]
            value = item[index]
            dic[key] = value
        s = json.dumps(dic)
        strings.append(s)
    return Result(True, strings)
