import database_updated_file as a

# Example URI for the database
uri = "postgresql://dbms_owner:mWs2AfUrNK7T@ep-muddy-meadow-a5wol2jq.us-east-2.aws.neon.tech/dbms?sslmode=require"

# Establishing connection to the database
conn = a.establish_connection(uri)

if conn:
    # Creating a table
    create_table_queries = [
        '''
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        )
        '''
    ]
    a.execute_queries(conn, create_table_queries)

    # Inserting data into the table
    insert_data_queries = {
        "INSERT INTO test_table (name) VALUES (%s)": [('John',), ('Alice',)]
    }
    a.insert_data(conn, "test_table", insert_data_queries)

    # Updating data in the table
    update_query = "UPDATE test_table SET name = %s WHERE id = %s"
    update_values = ('Bob', 1)
    a.update_data(conn, update_query, update_values)

    # Deleting data from the table
    delete_query = "DELETE FROM test_table WHERE id = %s"
    delete_values = (2,)
    a.delete_data(conn, delete_query, delete_values)

    # Selecting and printing data from the table
    select_query = "SELECT * FROM test_table"
    a.select_data(conn, select_query)

    # Closing connection
    conn.close()
