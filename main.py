from database_connection import init_connection
from inventory_manager import create_entry, delete_entry, search_inventory
from login import login
from metadata_manager import create_table, get_all_tables, get_table_with_values, delete_table


print(""" 
╦┌┐┌┬  ┬┌─┐┌┐┌┬┐┌─┐┬─┐┬ ┬  ╔╦╗┌─┐┌┐┌┌─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┬┐  ╔═╗┬ ┬┌─┐┌┬┐┌─┐┌┬┐
║│││└┐┌┘├┤ ││││ │ │├┬┘└┬┘  ║║║├─┤│││├─┤│ ┬├┤ │││├┤ ││││   ╚═╗└┬┘└─┐ │ ├┤ │││
╩┘└┘ └┘ └─┘┘└┘┴ └─┘┴└─ ┴   ╩ ╩┴ ┴┘└┘┴ ┴└─┘└─┘┴ ┴└─┘┘└┘┴   ╚═╝ ┴ └─┘ ┴ └─┘┴ ┴
""")

value = "logged_out"

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


# CODE STARTS HERE
# initiate the database connection
init_connection()
bootstrap()