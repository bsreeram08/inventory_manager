import random
from re import template
import string
from string import Template

from database_connection import execute_query, fetch_query, get_cursor

table_name = "list_table"


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


def search_list(list_id:str, search_term:str):
    template_query = Template("SELECT * FROM $table_name WHERE list_id = '$list_id' AND $table_name MATCH '$search_term';")
    query = template_query.substitute(table_name=table_name, list_id = list_id, search_term=search_term)
    result = fetch_query(query)
    _list = []
    _list_types = []
    for i in range(0, len(result)):
        _list.append(result[i][2])
        _list_types.append(result[i][3])
    # print(_list)
    # print(_list_types)
    return [_list, _list_types]