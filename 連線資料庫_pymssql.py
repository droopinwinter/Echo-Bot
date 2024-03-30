import pymssql
from sqlalchemy import create_engine
import pandas as pd





SQL_QUERY = """
SELECT 
TOP 5 [kdatetime] FROM FROM [Test].[dbo].[SPX_d] ;
"""

try:
    # 初始化数据库连接引擎
    # create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数)
    
    #engine = create_engine("mssql+pymssql://sysuser:sysuser@192.9.10.63:1433/mascheck?charset=GBK")
    engine = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/fina?charset=GBK")

    # 读取的sql语句 testc表中的前3条数据
    sql = 'select top 3 * FROM [fina].[dbo].[SPX_d] '
    #sql1="select top 3 * FROM [mascheck].[dbo].[IWORKLST]"
    # 第一个参数：查询sql语句
    # 第二个参数：engine，数据库连接引擎
    pd_read_sql = pd.read_sql(sql, engine)
    print(pd_read_sql)
 
    '''
      #conn = pymssql.connect(server='127.0.0.1:1433',database='test')    
    conn = pymssql.connect(host="127.0.0.1:1433", user='sa', password='abc123', database='master')    
    #conn = pymssql.connect(server = '資訊室-26兆慶',database= 'Test')
    cursor = conn.cursor(as_dict=True)
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
    for r in records:
        print(f"{r['ACCESS_NO']}")    
    '''
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)




#conn = pymssql.connect(server = '資訊室-26兆慶',database= 'Test')
#print(pymssql.connect())


