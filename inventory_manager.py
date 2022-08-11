from string import Template

from database_connection import execute_query, fetch_query_with_param, print_and_raise
from list_manager import create_list, get_list, delete_list, search_list

parent_table_name = "inventory_table"
metadata_table_name = "metadata_table"


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
        table_name=parent_table_name)
    execute_query(insert_query, (table_id, list_id))
    print("Values inserted to table successfully")


def get_table_entries(table_id: str) -> list:
    get_all_tuples_query = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name)
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
    query = Template("DELETE FROM $table_name where list_id = %s").substitute(table_name=parent_table_name)
    execute_query(query, [list_id])
    print("Deleted row Successfully")
    return delete_list(list_id)


def delete_inventory(table_id: str):
    query = Template("DELETE FROM $table_name where table_id = %s").substitute(table_name=parent_table_name)
    get_all_tuples_query = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name)
    list_ids = fetch_query_with_param(get_all_tuples_query, [table_id])
    for i in range(0, len(list_ids)):
        delete_list(list_ids[i][0])
    execute_query(query, [table_id])


def search_inventory(table_id: str, term: str):
    get_list_ids = Template("SELECT list_id from $table_name where table_id = %s;").substitute(
        table_name=parent_table_name)
    list_ids = fetch_query_with_param(get_list_ids, [table_id])
    return search_list(list_ids, term)
