import psycopg2
from urllib.parse import urlparse

# PostgreSQL URI
uri = "postgresql://dbms_owner:mWs2AfUrNK7T@ep-muddy-meadow-a5wol2jq.us-east-2.aws.neon.tech/dbms?sslmode=require"

# Parse the URI
result = urlparse(uri)

# Extract required details
dbname = result.path[1:]
user = result.username
password = result.password
host = result.hostname
sslmode = "require" if result.query == "sslmode=require" else None

# Establish connection
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    sslmode=sslmode
)

# Check if connection is established
if conn is not None:
    print("Connection to the database is successful.")
    cur = conn.cursor()


    
    # Insert some data into Users table
    cur.execute("INSERT INTO Users (username, password, gold) VALUES (%s, %s, %s)", ('user1', 'password1', 100))
    cur.execute("INSERT INTO Users (username, password, gold) VALUES (%s, %s, %s)", ('user2', 'password2', 200))
    
    # Insert some data into Heroes table
    cur.execute("INSERT INTO Heroes (cost, health, statetype, user_id) VALUES (%s, %s, %s, %s)", (10.5, '100', 1, 1))
    
    # Commit the transaction after all data insertion
    conn.commit()

    print("Data inserted successfully.")
    
    # Close cursor
    cur.close()
else:
    print("Failed to establish connection to the database.")

# Close connection
conn.close()
