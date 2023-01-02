import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from sqlalchemy.engine import URL
import urllib
import os

server = "{}.database.windows.net".format(dbhost=os.environ['DBHOST'])
database = os.environ['DBNAME']
username = os.environ['DBUSER']
password = os.environ['DBPASS']

driver = '{ODBC Driver 17 for SQL Server}'

odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
connection_url = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
engine = _sql.create_engine(
    connection_url,
)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()