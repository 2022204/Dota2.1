from dotenv import load_dotenv
import database_updated_file as db
import os
from datetime import datetime
from helper import hashed_password, get_challenges, get_history, get_heroes, get_items_by_ids, get_items, get_list, get_tradeOffers, get_users, difference_of_lists
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))
print(db.select_data(conn, "SELECT * FROM history WHERE user_id = %s",(1, )))

