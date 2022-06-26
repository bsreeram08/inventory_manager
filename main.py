from database_connection import init_connection
from inventory_manager import create_entry, get_table_entries, delete_entry
from list_manager import create_list, get_list

# initiate the database connection
from metadata_manager import create_table, get_all_tables, get_table, get_table_with_values, delete_table


def bootstrap():
    print("Inventory Manager.")

    print("Options Available")
    print("1) List All Tables")
    print("2) List values of Table")
    print("3) Add Value to Table")
    print("4) Create Table")
    print("5) Delete Table")
    print("6) Delete Value in Table")
    print("7) Stop")

    option = int(input("Enter your option : "))
    if option == 7:
        print("Bye Bye")
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
init_connection()
bootstrap()
