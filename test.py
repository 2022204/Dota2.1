from dotenv import load_dotenv
import database_updated_file as db
import os
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))

rows = db.select_data(conn, f"SELECT * FROM users where user_id = {1}")

print(rows)
print(rows[0][0],rows[0][2])