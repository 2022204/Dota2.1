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
    # Execute queries or perform database operations here
    cur = conn.cursor()
    
    # Create tables
    queries = [
        '''
        CREATE TABLE Users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255) UNIQUE NOT NULL,
            gold REAL
        )
        ''',
        '''
        CREATE TABLE Heroes (
            hero_id SERIAL PRIMARY KEY,
            cost REAL,
            health VARCHAR(200),
            statetype INT,
            user_id INT,
            CONSTRAINT fk_constraint_users FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
        ''',
        '''
        CREATE TABLE Items (
            item_id SERIAL PRIMARY KEY,
            HP REAL,
            cost REAL,
            attackspeed REAL,
            damage REAL,
            hero_id INT,
            CONSTRAINT fk_constraint_heroes FOREIGN KEY(hero_id) REFERENCES Heroes(hero_id)
        )
        ''',
        '''
        CREATE TABLE Maps (
            map_id SERIAL PRIMARY KEY,
            type VARCHAR(200),
            size REAL
        )
        ''',
        '''
        CREATE TABLE NPC (
            npc_id SERIAL PRIMARY KEY,
            gold_value REAL,
            hp REAL,
            damage VARCHAR(200),
            attackspeed REAL,
            armor REAL,
            map_id INT,
            hero_id INT,
            CONSTRAINT fk_constraint_maps FOREIGN KEY(map_id) REFERENCES Maps(map_id),
            CONSTRAINT fk_constraint_heroes FOREIGN KEY(hero_id) REFERENCES Heroes(hero_id)
        )
        ''',
        '''
        CREATE TABLE Powers (
            power_id INT PRIMARY KEY,
            effect VARCHAR(255),
            Type VARCHAR(255),
            hero_id INT,
            CONSTRAINT fk_constraint_heroes_powers FOREIGN KEY(hero_id) REFERENCES Heroes(hero_id)
        )
        ''',
        '''
        CREATE TABLE All_Fights (
            fight_id SERIAL PRIMARY KEY,
            details VARCHAR(255),
            user_id INT,
            CONSTRAINT fk_constraint_users FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
        '''
    ]

    for query in queries:
        cur.execute(query)
        conn.commit()  # Commit each query

    print("Tables created successfully.")
    
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
