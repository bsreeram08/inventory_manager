from multiprocessing import connection
from typing import Any
import mysql.connector as mysqlConnector

def printAndRasie(_exception):
    print(_exception);
    raise _exception
    
def initConnection():
    global connection
    connection = mysqlConnector.connect(host="localhost",user="root",password="beetablet123$$",database="inventory_management")
    if connection.is_connected():
        print("Connection Successful with the database")
        # setup cursor
        setupCursor()
    else:
        print("Conncetion failed to be initiated")
        
def setupCursor():
    global cursor
    cursor = getConnection().cursor()
    
# Gettors

def getConnection():
    if connection is None:
        printAndRasie("Connection is not initiated.")
    return connection;

def getCursor():
    if cursor is None:
        printAndRasie("Cursor is null, connection was not Executed Successfullt")
    return cursor

def executeQuery(query: str, params:Any):
    getCursor().execute(query,params)
    getConnection().commit()
    
def fetchQuery(query: str):
    getCursor().execute(query)
    return getCursor().fetchall()