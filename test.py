from dotenv import load_dotenv
import database_updated_file as db
import os
from helper import hashed_password, get_history, get_heroes
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))


password = hashed_password("hasan")

table = 'users'
username = 'hasan'
gold = 500


# data = {
#     "INSERT INTO users (username, password, gold) VALUES (%s, %s, %s)": [
#         (username, password, 1200),
#         ("farza", hashed_password("farza"), 1000),
#         ("murtaza", hashed_password("murtaza"), 900)
#     ]
# }

# # db.insert_data(conn, table, data)
# print(db.select_data(conn, f"SELECT * FROM users WHERE user_id = 1"))

# row = db.select_data(conn, f"SELECT user_id FROM users where username = %s AND password = %s",(username, password))
# print(row[0][0])
# hash = hashed_password("hasan")
# username = "hasan"
# user_id = db.select_data(conn, f"SELECT user_id from users where username = %s AND password = %s", (username, hash))
# # print(user_id)
user_Id = 5
# history = db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (user_Id, ) )



# duels = get_history(history)
# print(duels)

# hero_list = db.select_data(conn, f"SELECT * FROM heroes")
# print(hero_list)
# def get_heroes(hero_list):
#     heroes = []
#     for item in hero_list:
#         hero_dict = {
#             'hero_id': item[0],
#             'heroname': item[1],
#             'description': item[3],
#             'health': item[4],
#             'armor': item[5],
#             'attackspeed': item[6],
#             'damage': item[7],
#             'cost': item[2]
#         }
#         heroes.append(hero_dict)
# #     return heroes

# hero_id = 1
# cost = db.select_data(conn, f"SELECT cost from heroes WHERE hero_id = %s",(hero_id, ))[0][0]
# print(cost)
user_id = 1
# cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
# print(cash)
db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(1200, user_id))




