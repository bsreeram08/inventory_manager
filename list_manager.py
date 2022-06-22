import random
import string
from string import Template

from database_connection import executeQuery, fetchQuery, getCursor

tableName = "list_table"

def getList(listId:str) -> list:
    query = Template("SELECT * FROM list_table WHERE list_id = '$listId';").substitute(listId=listId)
    return fetchQuery(query)

def createList(_list: list, _list_value_type:list) -> str:
    listId = generateId()
    templateQuery = Template("INSERT INTO $tableName (list_id, item_index, value, value_type) VALUES( %s, %s, %s, %s)")
    for i in range(0, len(_list)):
        query = (templateQuery.substitute(
            tableName=tableName, 
            )
        )
        executeQuery(query,(listId,i,_list[i],_list_value_type[i]))
    return listId # list id


def generateId(size=6, chars=string.ascii_uppercase + string.digits) -> str: 
    return ''.join(random.choice(chars) for _ in range(size))

