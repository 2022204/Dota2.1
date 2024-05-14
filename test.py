from helper import (
    checkuser,
    hashed_password,
    get_history,
    get_heroes,
    get_items,
    get_items_by_ids,
    get_tradeOffers,
    get_users,
    get_challenges,
    merge_items_by_challenge,
    get_npc
)
from fight import and_the_winner_is
import json
from datetime import datetime

import database_updated_file as db
import os
from dotenv import load_dotenv

load_dotenv(".env.local")
conn = db.establish_connection(os.getenv("uri"))


print(db.select_data(conn, "SELECT * FROM npc"))