from database_connection import initConnection
from list_manager import createList, getList

# initiate the database connection
initConnection()

# createList(["room_no", "room_type", "price"],["string","string","string"])
print(getList("CVWEEP"))