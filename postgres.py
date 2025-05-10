# import psycopg2

# # define connection parameters 
# conn_params = {
#     'dbname': 'your_database_name',
#     'user': 'your_username',
#     'password': 'your_username',
#     'host': 'localhost',
#     'port': 5434    # default postgreSQL port
# }

# try:
#     # Establish the connection 
#     conn = psycopg2.connect(**conn_params)
#     print("connection successfull using psycopg2")

#     # create a cursor to execut SQL querie
#     cursor = conn.cursor()

#     # Example: fetch postgreSQL version
#     cursor.execute("SELECT version();")
#     print(cursor.fetchone())

#     # close cursor and connection 
#     cursor.close()
#     conn.close()

# except Exception as e:
#     print("Error connecting to postgreSQL using pcycopg2:", e)





