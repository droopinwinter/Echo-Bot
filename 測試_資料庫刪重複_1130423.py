import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")

    sql2 = 'select * FROM [Stock].[dbo].[Ticker] '
    Ticker = pd.read_sql(sql2, engine)
except Exception as errMsg: # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

for i in Ticker.Stock:
    print('Stock_'+i)
    try:
        sql4 = \
            "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER ("+\
            "	    PARTITION BY [date] ORDER BY (SELECT NULL)"+\
            "	) FROM [Stock].[dbo]."+'AnalysDay_'+ i.strip()+\
            ") AS T WHERE DupRank > 1"
 
        cursor.execute(sql4)
        conn.commit()
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('資料庫刪重複＿_發生錯誤-'+i.strip() , errMsg)     