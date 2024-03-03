import psycopg2
def main():
    query = input("Query: ")
    type_q = int(input("Query type(1. Select, 2.Update/insert/delete): "))
    if type_q == 1:
        print(execute_postgresql_query(query, "SELECT"))
    else:
        execute_postgresql_query("INSERT INTO maps (map_type, map_area) VALUES (%s,%s)", "ELSE", params = ('fire',123))
        print("Successfully executed")
def execute_postgresql_query(query, query_type, params=()):
    """
    Lets run some QUERIES
    """
    # Preset connection details
    dbname = 'game'
    user = 'postgres'
    password = 'hasan'
    host = 'localhost'  # The network address of your database server
    
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        print("Connected to the database successfully.")
        cursor = conn.cursor()
        cursor.execute(query, params)
        if query_type == "SELECT":
            result = cursor.fetchall()
            return result  # Return query results only for SELECT operations.
        else:
            conn.commit()  # For INSERT, UPDATE, DELETE, commit changes but return None.
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



if __name__ == ("__main__"):
    main()