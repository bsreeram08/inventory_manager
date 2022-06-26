from string import Template

from database_connection import print_and_raise, execute_query, fetch_query, fetch_query_with_param
from inventory_manager import get_table_entries, delete_inventory
from list_manager import generate_id, create_list, get_list
from tabulate import tabulate

parent_table_name = "metadata_table"
list_type_names = ["String", "Integer"]


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
        table_name=parent_table_name)
    execute_query(insert_query, (table_id, table_name, list_id))
    print("Table Created Successfully")
    return table_id


def delete_table(table_id: str):
    query = Template("DELETE FROM $table_name where table_id = %s").substitute(table_name=parent_table_name)
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
    query = Template("SELECT table_id, table_name from $table_name;").substitute(table_name=parent_table_name)
    tables = fetch_query(query)
    print("*********************************")
    print("{:<15} {:<15} ".format("Table ID", "Table Name"))
    for i in range(0, len(tables)):
        print("{:<15} {:<15} ".format(tables[i][0], tables[i][1]))
    print("*********************************")


def get_table(table_id: str):
    query = Template("SELECT * from $table_name where table_id = %s").substitute(table_name=parent_table_name)
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
