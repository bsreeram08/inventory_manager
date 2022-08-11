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
