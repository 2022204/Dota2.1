from dotenv import load_dotenv
import database_updated_file as db
import os
from helper import hashed_password, get_history, get_heroes, get_items_by_ids, get_items, get_list, get_tradeOffers, get_users
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))
user_id = 1
# items = db.select_data(conn, f"SELECT item_id from UserItems WHERE user_id = %s", (user_id,))
# print(items)
# item_list = get_list(items)

# print(item_list)

# cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
# print(cash)

# db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash+1, user_id))

# cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
user_id = 5

# print(get_tradeOffers(db.select_data(conn, f"SELECT * FROM tradeOffers WHERE status = 'pending' and user_id = %s",(user_id, ))))

# print(get_heroes(db.select_data(conn, f"SELECT * FROM heroes")))
# print(get_users(db.select_data(conn, f"SELECT * FROM users WHERE user_id != %s", (user_id, ))))
print(get_heroes(db.select_data(conn, f"SELECT * FROM heroes WHERE hero_id IN (SELECT hero_id FROM Userheroes WHERE user_id = %s)", (user_id, ))))