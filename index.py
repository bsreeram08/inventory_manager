import csv
from hashlib import new
import random
import string
from string import Template
from multiprocessing import connection
from typing import Any
import mysql.connector as mysql_connector
# from cryptography.fernet import Fernet
from tabulate import tabulate

parent_table_name = "inventory_table"
metadata_table_name = "metadata_table"
table_name = "list_table"
# key = b'rPuxmfV-imRkOA7sXAcCFWCLzl1NCKwifrTpH6KA3X4='
# fernet = Fernet(key)
# encryptedUsername = b'gAAAAABi9SVug0gzYaps5x4vKcWXzL5T3dHTYKB4fGhB4QAwx4XpovbplHnpmRDhK3VbD9C6OZKjTx-UdRXislq-wqLnUYu42Q=='
# encryptedPassword = b'gAAAAABi9SVuBRXULUyblDkTUIn3kUyxWqjkxtTcQ5eE2rN3hUEJFd4Ydbdi5Uwu3aKh1zMX_hYdaag1g8gPZPTn3zraNAGl9g=='
value = "logged_out"
parent_table_name_metadata = "metadata_table"
parent_table_name_inventory = "inventory_table"
list_type_names = ["String", "Integer"]

def print_and_raise(_exception):
    print(_exception)
    raise _exception


def init_connection():
    global connection
    connection = mysql_connector.connect(host="localhost", user="root", password="sreeram123",
                                         database="inventory_management")
    if connection.is_connected():
        print("Connection Successful with the database")
        # setup cursor
        setup_cursor()
    else:
        print("Connection failed to be initiated")


def setup_cursor():
    global cursor
    cursor = get_connection().cursor()


# Getters

def get_connection():
    if connection is None:
        print_and_raise("Connection is not initiated.")
    return connection


def get_cursor():
    if cursor is None:
        print_and_raise("Cursor is null, connection was not Executed Successfully")
    return cursor


def execute_query(query: str, params: Any):
    get_cursor().execute(query, params)
    get_connection().commit()


def fetch_query(query: str):
    get_cursor().execute(query)
    return get_cursor().fetchall()


def fetch_query_with_param(query: str, param: Any):
    print(query,param)
    get_cursor().execute(query, param)
    return get_cursor().fetchall()


def get_table(table_id: str):
    query = Template("SELECT * from $table_name where table_id = %s").substitute(table_name=metadata_table_name)
    _table_metadata = fetch_query_with_param(query, [table_id])
    if len(_table_metadata) == 0:
        print_and_raise("No table with given table id found.")
    table_metadata = _table_metadata[0]
    table_name = table_metadata[1]
    list_id = table_metadata[2]
    list_metadata = get_list(list_id)
    list_values = list_metadata[0]
    list_value_types = list_metadata[1]
    print("*********************************")
    print("{:<15} {:<15} {:<15}".format("Table ID", "Table Name", "Table Columns"))
    print("{:<15} {:<15} {:<15}".format(table_id, table_name, str(list_values)))
    print("*********************************")
    return [table_id, table_name, list_values, list_value_types]


def create_entry(table_id: str):
    table_metadata = get_table(table_id)
    print(table_metadata)
    table_id = table_metadata[0]
    table_name = table_metadata[1]
    column_names = table_metadata[2]
    column_types = table_metadata[3]

    list_values = []
    print("Inserting into table_name".replace("table_name", table_name))
    for i in range(0, len(column_names)):
        value = input("Enter data for VALUE : ".replace("VALUE", str(column_names[i])))
        list_values.append(value)
    list_id = create_list(list_values, column_types)
    insert_query = Template("INSERT INTO $table_name (table_id,list_id) VALUES(%s,%s)").substitute(
        table_name=parent_table_name_inventory)
    execute_query(insert_query, (table_id, list_id))
    print("Values inserted to table successfully")


def get_table_entries(table_id: str) -> list:
    get_all_tuples_query = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name_inventory)
    list_ids = fetch_query_with_param(get_all_tuples_query, [table_id])
    values = []
    for i in range(0, len(list_ids)):
        value_metadata = get_list(list_ids[i][0])
        value = [list_ids[i][0], value_metadata[0]]
        values.append(value)
    return values


def get_entry(list_id: str) -> list:
    return get_list(list_id)


def delete_entry(list_id: str):
    query = Template("DELETE FROM $table_name where list_id = %s").substitute(table_name=parent_table_name_inventory)
    execute_query(query, [list_id])
    print("Deleted row Successfully")
    return delete_list(list_id)


def delete_inventory(table_id: str):
    query = Template("DELETE FROM $table_name where table_id = %s").substitute(table_name=parent_table_name_inventory)
    get_all_tuples_query = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name_inventory)
    list_ids = fetch_query_with_param(get_all_tuples_query, [table_id])
    for i in range(0, len(list_ids)):
        delete_list(list_ids[i][0])
    execute_query(query, [table_id])

def search_inventory(table_id:str, term:str):
    get_list_ids = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name_inventory)
    list_id = fetch_query_with_param(get_list_ids, [table_id])
    return search_list(list_id,term)



def get_list(list_id: str) -> list:
    query = Template("SELECT * FROM list_table WHERE list_id = '$list_id';").substitute(list_id=list_id)
    result = fetch_query(query)
    _list = []
    _list_types = []
    for i in range(0, len(result)):
        _list.append(result[i][2])
        _list_types.append(result[i][3])
    # print(_list)
    # print(_list_types)
    return [_list, _list_types]


def create_list(_list: list, _list_value_type: list) -> str:
    list_id = generate_id()
    template_query = Template(
        "INSERT INTO $table_name (list_id, item_index, value, value_type) VALUES( %s, %s, %s, %s)")
    for i in range(0, len(_list)):
        query = (template_query.substitute(
            table_name=table_name,
        )
        )
        execute_query(query, (list_id, i, _list[i], _list_value_type[i]))
    return list_id  # list id


def generate_id(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def delete_list(list_id: str):
    query = Template("DELETE FROM $table_name where list_id = %s").substitute(table_name=table_name)
    execute_query(query, [list_id])

def search_list(list_id, search_term: str):
    result = []
    for i in range(0,len(list_id)):
        template_query = Template("SELECT * FROM $table_name WHERE list_id = '$list_id';")
        query = template_query.substitute(table_name=table_name, list_id=list_id[i][0])
        _res = fetch_query(query)
        for j in range(0,len(_res)):
            if search_term in _res[j][2]:
                result.append(_res)
                break
    _list = []
    for i in range(0, len(result)):
        res = []
        for j in range(0,len(result[i])):
            res.append(result[i][j][2])
        _list.append(res)

    print(_list)

    return [_list]

def login():
    existing_user = input('Do you already have an account? [0-Yes] : ')
    if existing_user == '0':
        username = input('Enter your username : ')
        password = input('Enter your password : ')
        with open('accounts.csv',mode='r') as f:
            accounts = csv.reader(f,delimiter=',')
            for account in accounts:
                print(account)
                if account == [username,password]:
                    print("User Logged in Successfully")
                    return True
        print("Incorrect Username or password.")
        return False
    else:
        new_username = input("Enter you new username:")
        new_password = input("Enter you new password:")
        with open('accounts.csv',mode='r') as f:
            accounts = csv.reader(f,delimiter=',')
            for account in accounts:
                if account[0] == new_username:
                    print("User Already Exists Please Login.")
                    return login()
            with open('accounts.csv',mode='a',newline='') as write:
                writer=csv.writer(write,delimiter=',')
                writer.writerow([new_username,new_password])
                print('User Created successfully, please login')
                return login()
    return False;

    # if(username == fernet.decrypt(encryptedUsername).decode() and password == fernet.decrypt(encryptedPassword).decode()):
    #     return True
    # else:
    #     print('Invalid Username or password.')
    #     return False


def create_table() -> str:
    table_name = input("Enter table Name : ")
    no_of_columns = int(input("Enter the number of columns : "))
    _list = []
    _list_type = []
    for i in range(0, no_of_columns):
        value = input("Enter column NUMBER : ".replace("NUMBER", str(i)))
        print("Column Types : \n1) String\n2) Integer")
        value_type = int(input("Enter the column NUMBER type :".replace("NUMBER", str(i))))
        print(value_type)
        if value_type != 1 and value_type != 2:
            print_and_raise("Invalid type for column NUMBER".replace("NUMBER", str(i)))
        _list.append(value)
        _list_type.append(list_type_names[value_type - 1])
    print("*********************************")
    print(table_name)
    print(_list)
    print(_list_type)
    print("*********************************")
    table_id = generate_id()
    list_id = create_list(_list, _list_type)
    insert_query = Template(
        "INSERT INTO $table_name (table_id, table_name, list_id_params) VALUES(%s,%s,%s)").substitute(
        table_name=parent_table_name_metadata)
    execute_query(insert_query, (table_id, table_name, list_id))
    print("Table Created Successfully")
    return table_id


def delete_table(table_id: str):
    query = Template("DELETE FROM $table_name where table_id = %s").substitute(table_name=parent_table_name_metadata)
    table_metadata = get_table(table_id)
    print(table_metadata)
    table_name = table_metadata[1]
    print("*********************************")
    print(Template("Deleting Table with name : $table_name, and id : $table_id").substitute(table_id=table_id,
                                                                                          table_name=table_name))
    execute_query(query, [table_id])
    delete_inventory(table_id)
    print("*********************************")
    print("Table Deleted Successfully")


def get_all_tables():
    query = Template("SELECT table_id, table_name from $table_name;").substitute(table_name=parent_table_name_metadata)
    tables = fetch_query(query)
    print("*********************************")
    print("{:<15} {:<15} ".format("Table ID", "Table Name"))
    for i in range(0, len(tables)):
        print("{:<15} {:<15} ".format(tables[i][0], tables[i][1]))
    print("*********************************")


def get_table(table_id: str):
    query = Template("SELECT * from $table_name where table_id = %s").substitute(table_name=parent_table_name_metadata)
    _table_metadata = fetch_query_with_param(query, [table_id])
    if len(_table_metadata) == 0:
        print_and_raise("No table with given table id found.")
    table_metadata = _table_metadata[0]
    table_name = table_metadata[1]
    list_id = table_metadata[2]
    list_metadata = get_list(list_id)
    list_values = list_metadata[0]
    list_value_types = list_metadata[1]
    print("*********************************")
    print("{:<15} {:<15} {:<15}".format("Table ID", "Table Name", "Table Columns"))
    print("{:<15} {:<15} {:<15}".format(table_id, table_name, str(list_values)))
    print("*********************************")
    return [table_id, table_name, list_values, list_value_types]


def get_table_with_values(table_id: str):
    table_metadata = get_table(table_id)
    table_id = table_metadata[0]
    table_name = table_metadata[1]
    list_values = ["Row ID", table_metadata[2]]
    table_entries = get_table_entries(table_id)
    print("*********************************")
    print("Table TABLE_NAME".replace("TABLE_NAME", table_name))
    print(tabulate(table_entries, headers=list_values))
    print("*********************************")




print(""" 
╦┌┐┌┬  ┬┌─┐┌┐┌┬┐┌─┐┬─┐┬ ┬  ╔╦╗┌─┐┌┐┌┌─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┬┐  ╔═╗┬ ┬┌─┐┌┬┐┌─┐┌┬┐
║│││└┐┌┘├┤ ││││ │ │├┬┘└┬┘  ║║║├─┤│││├─┤│ ┬├┤ │││├┤ ││││   ╚═╗└┬┘└─┐ │ ├┤ │││
╩┘└┘ └┘ └─┘┘└┘┴ └─┘┴└─ ┴   ╩ ╩┴ ┴┘└┘┴ ┴└─┘└─┘┴ ┴└─┘┘└┘┴   ╚═╝ ┴ └─┘ ┴ └─┘┴ ┴
""")



def match_option(option: int):
    if option == 1:
        return get_all_tables()
    elif option == 2:
        table_id = input("Enter Table ID : ")
        return get_table_with_values(table_id)
    elif option == 3:
        table_id = input("Enter Table ID : ")
        search_term = input("Search Term : ")
        return search_inventory(table_id,search_term)
    elif option == 4:
        table_id = input("Enter Table ID : ")
        return create_entry(table_id)
    elif option == 5:
        return create_table()
    elif option == 6:
        table_id = input("Enter Table ID : ")
        return delete_table(table_id)
    elif option == 7:
        list_id = input("Enter Row ID : ")
        return delete_entry(list_id)
    else:
        return "Incorrect Input!!"



def bootstrap():
    global value
    if(value == "logged_out"):
        if login()==True:
            value = 'logged_in'
        else:
            return
        
    print("Inventory Manager.")

    print("Options Available")
    print("1) List All Tables")
    print("2) List values of Table")
    print("3) Search for a value")
    print("4) Add Value to Table")
    print("5) Create Table")
    print("6) Delete Table")
    print("7) Delete Value in Table")
    print("8) Stop")

    option = int(input("Enter your option : "))
    if option == 8:
        print("THANK YOU!")
        return
    match_option(option)
    bootstrap()


# CODE STARTS HERE
# initiate the database connection
init_connection()
bootstrap()
