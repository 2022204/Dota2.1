from dotenv import load_dotenv
import database_updated_file as db
import os
from helper import hashed_password, get_history, get_heroes, get_items_by_ids, get_items, get_list
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))
user_id = 5
# items = db.select_data(conn, f"SELECT item_id from UserItems WHERE user_id = %s", (user_id,))
# print(items)
# item_list = get_list(items)

# print(item_list)

# cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
# print(cash)

# db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash+1, user_id))

# cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
print(db.select_data(conn, f"SELECT * FROM UserItems"))
item_id = 7
cost = db.select_data(conn, f"SELECT cost from items WHERE item_id = %s",(item_id, ))[0][0]

db.delete_data(conn,f"DELETE FROM UserItems where user_id = %s AND item_id = %s", (user_id, item_id))
cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
print(cash)
db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash+cost, user_id))
cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]

print(db.select_data(conn, f"SELECT * FROM UserItems"))
print(cash)
# print(cash)