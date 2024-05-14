import psycopg2
from urllib.parse import urlparse

def establish_connection(uri):
    try:
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

        print("Connection to the database is successful.")
        return conn
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database.")
        print(e)
        return None

def execute_queries(conn, queries):
    try:
        # Execute queries
        cur = conn.cursor()
        for query in queries:
            cur.execute(query)
            conn.commit()  
        print("Queries executed successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to execute queries.")
        print(e)
    finally:
        # Close cursor
        cur.close()

def insert_data(conn, table, data):
    try:
        cur = conn.cursor()
        for query, values in data.items():
            cur.executemany(query, values)
        conn.commit()  
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to insert data.")
        print(e)
        print("\n--------------------------------------------\n")

    finally:
        cur.close()



def update_data(conn, query, values):
    try:
        # Update data in the database
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        print("Data updated successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to update data.")
        print(e)
        print("\n--------------------------------------------\n")
    finally:
        # Close cursor
        cur.close()

def delete_data(conn, query, values):
    try:
        # Delete data from the database
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        print("Data deleted successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to delete data.")
        print(e)
        print("\n--------------------------------------------\n")    
    finally:
        # Close cursor
        cur.close()

def select_data(conn, query, params=None):
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error: Unable to fetch data.")
        print(e)
    finally:
        # Close cursor
        cur.close()

