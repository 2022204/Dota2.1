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
            conn.commit()  # Commit each query
        print("Queries executed successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to execute queries.")
        print(e)
    finally:
        # Close cursor
        cur.close()

def insert_data(conn, table, data):
    try:
        # Insert data into specified table
        cur = conn.cursor()
        for query, values in data.items():
            cur.executemany(query, values)
        conn.commit()  # Commit the transaction after all data insertion
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error: Unable to insert data.")
        print(e)
    finally:
        # Close cursor
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
    finally:
        # Close cursor
        cur.close()

def select_data(conn, query):
    try:
        # Select data from the database
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error: Unable to select data.")
        print(e)
    finally:
        cur.close()

# # Example usage:
# uri = "postgresql://dbms_owner:mWs2AfUrNK7T@ep-muddy-meadow-a5wol2jq.us-east-2.aws.neon.tech/dbms?sslmode=require"
# conn = establish_connection(uri)

# if conn:
#     # Example queries and data
#     create_table_queries = [
#         '''
#         CREATE TABLE IF NOT EXISTS test_table (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255)
#         )
#         '''
#     ]
#     execute_queries(conn, create_table_queries)

#     insert_data_queries = {
#     "INSERT INTO test_table (name) VALUES (%s)": [('John',), ('Alice',)]
# }
    
#     insert_data(conn, "test_table", insert_data_queries)

#     # Example update query
#     update_query = "UPDATE test_table SET name = %s WHERE id = %s"
#     update_values = ('Bob', 1)
#     update_data(conn, update_query, update_values)

#     # Example delete query
#     delete_query = "DELETE FROM test_table WHERE id = %s"
#     delete_values = (2,)
#     delete_data(conn, delete_query, delete_values)

#     # Example select query
#     select_query = "SELECT * FROM test_table"
#     select_data(conn, select_query)

#     # Close connection
#     conn.close()

# query = "SELECT * FROM Heros"

# print(select_data(conn, query))

