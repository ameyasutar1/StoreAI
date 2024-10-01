import mysql.connector
from mysql.connector import Error

# Database connection parameters
db_user = "root"
db_password = "Aj213778*"
db_host = "localhost"
db_name = "Amv_Tshirts"

def get_table_names():
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        if connection.is_connected():
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # SQL query to get all table names
            cursor.execute("SHOW TABLES")

            # Fetch all table names
            tables = cursor.fetchall()

            # Print or return the table names
            print("Tables in the database:")
            for table in tables:
                print(table[0])  # Each table name comes as a tuple, so we access the first element

            # Close the cursor and connection
            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

# Call the function to get and display table names
get_table_names()
