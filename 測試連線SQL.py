import pyodbc
  
  
class MSSQL:
    def __init__(self, IP, UserID, Pwd, db):
        self.host=IP;
        self.user=UserID;
        self.password=Pwd;
        self.dbname=db;
  
    def __getConnect(self):
        if not self.dbname:
            raise(NameError,"db name undefine error")
        else:
            connSTR="Driver={ODBC Driver 17 for SQL Server};SERVER=%s,1433;DATABASE=%s;UID=%s;PWD=%s" % (self.host, self.dbname, self.user, self.password)
            #example: Driver={ODBC Driver 11 for SQL Server};SERVER=127.0.0.1,1433;DATABASE=MyTestDB;UID=sa;PWD=Abc123
            self.conn = pyodbc.connect(connSTR);
            cu= self.conn.cursor();
        if not cu:
            raise(NameError,"db connect error");
        else:
            return cu;
  
    def ExecuteTableQuery(self,selectSql):
        cuu = self.__getConnect();
        selectRows = cuu.execute(selectSql);
        resList=selectRows.fetchall();
        self.conn.close();
        return resList;
  
    def ExecuteNonQuery(self,sql):
        cuu = self.__getConnect();
        cuu.execute(sql);
        self.conn.commit();
        self.conn.close();
  
    def PrintODBCDrivers(self):
        print(pyodbc.drivers() );


#import DBHelp_SqlServer
  
  
#db=MSSQL(IP="192.9.10.63", UserID="sysuser", Pwd="sysuser", db="mascheck");
db=MSSQL(IP="127.0.0.1", UserID="sa", Pwd="abc123", db="fina");

#sqlinsert="select top 3 * FROM [fina].[dbo].[SPX_d]"
#db.ExecuteNonQuery(sql=sqlinsert);
  
sql1="select top 3 * FROM [fina].[dbo].[SPX_d]";
#sql1="select top 3 * FROM [mascheck].[dbo].[IWORKLST]";
datatable = db.ExecuteTableQuery(selectSql=sql1);
print(datatable);