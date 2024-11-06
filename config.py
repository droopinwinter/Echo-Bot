from sqlalchemy import create_engine
import pymssql

# 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
con_Stock = pymssql.connect(host="127.0.0.1:1433", user='sa', password='abc123', database='Stock',charset='GBK')
cur_Stock = con_Stock.cursor()

eng_Stock  = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/Stock?charset=GBK")
eng_analsy = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/analsy?charset=GBK")
