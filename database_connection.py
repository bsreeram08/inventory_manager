from multiprocessing import connection
from typing import Any
import mysql.connector as mysql_connector


def print_and_raise(_exception):
    print(_exception)
    raise _exception


def init_connection():
    global connection
    connection = mysql_connector.connect(host="localhost", user="root", password="beetablet123$$",
                                         database="inventory_management")
    if connection.is_connected():
        print("Connection Successful with the database")
        # setup cursor
        setup_cursor()
    else:
        print("Conncetion failed to be initiated")


def setup_cursor():
    global cursor
    cursor = get_connection().cursor()


# Gettors

def get_connection():
    if connection is None:
        print_and_raise("Connection is not initiated.")
    return connection;


def get_cursor():
    if cursor is None:
        print_and_raise("Cursor is null, connection was not Executed Successfullt")
    return cursor


def execute_query(query: str, params: Any):
    get_cursor().execute(query, params)
    get_connection().commit()


def fetch_query(query: str):
    get_cursor().execute(query)
    return get_cursor().fetchall()


def fetch_query_with_param(query: str, param: Any):
    get_cursor().execute(query, param)
    return get_cursor().fetchall()
