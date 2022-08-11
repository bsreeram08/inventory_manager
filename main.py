from database_connection import init_connection
from inventory_manager import create_entry, delete_entry
from metadata_manager import create_table, get_all_tables, get_table_with_values, delete_table

print(""" 
╦┌┐┌┬  ┬┌─┐┌┐┌┬┐┌─┐┬─┐┬ ┬  ╔╦╗┌─┐┌┐┌┌─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┬┐  ╔═╗┬ ┬┌─┐┌┬┐┌─┐┌┬┐
║│││└┐┌┘├┤ ││││ │ │├┬┘└┬┘  ║║║├─┤│││├─┤│ ┬├┤ │││├┤ ││││   ╚═╗└┬┘└─┐ │ ├┤ │││
╩┘└┘ └┘ └─┘┘└┘┴ └─┘┴└─ ┴   ╩ ╩┴ ┴┘└┘┴ ┴└─┘└─┘┴ ┴└─┘┘└┘┴   ╚═╝ ┴ └─┘ ┴ └─┘┴ ┴
""")

def bootstrap():
    print("OPTIONS AVAILABLE")
    print("1) To List All Tables")
    print("2) To List the values of Table")
    print("3) To Add Value to a Table")
    print("4) To Create a Table")
    print("5) To Delete a Table")
    print("6) Delete Value in a Table")
    print("7) Stop")

    option = int(input("Enter your option : "))
    if option == 7:
        print("THANK YOU!")
        return
    match_option(option)
    bootstrap()


def match_option(option: int):
    if option == 1:
        return get_all_tables()
    elif option == 2:
        table_id = input("Enter Table ID : ")
        return get_table_with_values(table_id)
    elif option == 3:
        table_id = input("Enter Table ID : ")
        return create_entry(table_id)
    elif option == 4:
        return create_table()
    elif option == 5:
        table_id = input("Enter Table ID : ")
        return delete_table(table_id)
    elif option == 6:
        list_id = input("Enter Row ID : ")
        return delete_entry(list_id)
    else:
        return "Incorrect Input!!"


# CODE STARTS HERE
# initiate the database connection
init_connection()
bootstrap()
