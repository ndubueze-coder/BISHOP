
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # Recommended for CREATE DATABASE/SCHEMA
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
import sys

import psycopg2.extras # Import sys for exiting if database creation fails

# --- Database Connection Parameters ---
# Replace with your actual database credentials for BOTH databases

# Connection details for the SOURCE database (dvdrental)
SOURCE_DB_HOST = "localhost" # e.g., "localhost" or an IP address
SOURCE_DB_NAME = "dvd_rentals" # The database containing the film table
SOURCE_DB_USER = "postgres" # Your PostgreSQL username for dvdrental
SOURCE_DB_PASSWORD = "bishop5070" # Your PostgreSQL password for dvdrental
SOURCE_DB_PORT = "5432" # Your PostgreSQL port

# Connection details for the TARGET database (my_database)
TARGET_DB_HOST = "localhost" # Usually the same host as dvdrental, but can be different
TARGET_DB_NAME = "my_database" # The database you want to create/connect to
TARGET_DB_USER = "postgres" # Your PostgreSQL username for my_database (can be the same as dvdrental user)
TARGET_DB_PASSWORD = "bishop5070" # Your PostgreSQL password for my_database
TARGET_DB_PORT = "5432" # Your PostgreSQL port

# Define the source schema/table
SOURCE_SCHEMA = "public" # The schema where the 'film' table is located in dvdrental
SOURCE_FILM_TABLE = "film"

# Define the new schema and tables within my_database
NEW_SCHEMA = "new_schema"
TARGET_FILM_TABLE = "film1"
TARGET_DATA_TABLE = "my_data"

# Define the structure of the film table from dvdrental for recreation in my_database
# This is a common structure for the dvdrental film table.
# We define it manually here to create the table in the target database.
FILM_TABLE_SCHEMA_SQL = """
    CREATE TABLE {schema}.{table} (
        film_id INTEGER PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        release_year INTEGER,
        language_id SMALLINT NOT NULL,
        rental_duration SMALLINT NOT NULL,
        rental_rate NUMERIC(4,2) NOT NULL,
        length SMALLINT,
        replacement_cost NUMERIC(5,2) NOT NULL,
        rating VARCHAR(10), -- Can be enum or text depending on dvdrental setup
        last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        special_features TEXT[], -- This is an array type
        fulltext TSVECTOR NOT NULL
    );
"""

# --- Database Creation Function (Connects to 'postgres' db) ---
def create_database_if_not_exists(db_host, db_user, db_password, db_port, new_db_name):
    """Connects to the default maintenance database (postgres) to create a new database."""
    conn = None
    try:
        # Connect to the default 'postgres' database to be able to create a new database
        print(f"Attempting to connect to 'postgres' database at {db_host}:{db_port} as user {db_user}...")
        conn = psycopg2.connect(host=db_host, database="postgres", user=db_user, password=db_password, port=db_port)
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), (new_db_name,))
        exists = cursor.fetchone()

        if not exists:
            print(f"Database '{new_db_name}' does not exist. Creating...")
            # Create the new database
            cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(new_db_name)))
            print(f"Database '{new_db_name}' created successfully.")
        else:
            print(f"Database '{new_db_name}' already exists.")

        cursor.close()
        return True # Indicate success

    except psycopg2.OperationalError as e:
        print(f"Operational error while connecting to 'postgres' or creating '{new_db_name}': {e}")
        print("Please ensure PostgreSQL is running, your connection parameters for the default database are correct, and the user has privileges to create databases.")
        return False # Indicate failure
    except Exception as e:
        print(f"An unexpected error occurred during database creation check: {e}")
        return False # Indicate failure
    finally:
        if conn:
            conn.close()

# --- Function to fetch data and aggregates from the source database ---
def fetch_data_from_source(db_host, db_name, db_user, db_password, db_port, source_schema, source_table):
    """Connects to the source database and fetches film data and aggregate statistics."""
    conn = None
    cursor = None
    film_data = []
    aggregate_stats = None

    try:
        print(f"\nConnecting to source database '{db_name}'...")
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, port=db_port)
        print("Source database connection successful.")

        cursor = conn.cursor()

        # Fetch all data from the film table
        print(f"Fetching data from {source_schema}.{source_table}...")
        fetch_film_sql = sql.SQL("SELECT * FROM {schema}.{table};").format(
            schema=sql.Identifier(source_schema),
            table=sql.Identifier(source_table)
        )
        cursor.execute(fetch_film_sql)
        film_data = cursor.fetchall()
        print(f"Fetched {len(film_data)} rows from {source_schema}.{source_table}.")

        # Calculate aggregate statistics
        print(f"Calculating aggregate statistics from {source_schema}.{source_table}...")
        calculate_stats_sql = sql.SQL("""
            SELECT
                COUNT(*) AS tot_row,
                COUNT(DISTINCT rating) AS dist_rating,
                SUM(length) AS tot_length,
                AVG(length),
                ROUND(AVG(length)::NUMERIC, 2) AS round_avg
            FROM {schema}.{table};
        """).format(
             schema=sql.Identifier(source_schema),
             table=sql.Identifier(source_table)
        )
        cursor.execute(calculate_stats_sql)
        aggregate_stats = cursor.fetchone()
        print("Aggregate statistics calculated.")

        return film_data, aggregate_stats # Return fetched data and stats

    except psycopg2.OperationalError as e:
        print(f"Operational error while connecting to source database '{db_name}': {e}")
        print("Please ensure the source database is accessible and connection parameters are correct.")
        return None, None # Indicate failure
    except psycopg2.ProgrammingError as e:
        print(f"Database programming error while fetching from source: {e}")
        return None, None # Indicate failure
    except Exception as e:
        print(f"An unexpected error occurred while fetching from source: {e}")
        return None, None # Indicate failure
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Source database connection closed.")

# --- Function to setup target database and insert data ---
def setup_target_database_and_insert(db_host, db_name, db_user, db_password, db_port, new_schema, target_film_table, target_data_table, film_data, aggregate_stats):
    """Connects to the target database and inserts the fetched data and statistics."""
    conn = None
    cursor = None
    try:
        print(f"\nConnecting to target database '{db_name}'...")
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, port=db_port)
        conn.set_isolation_level(1) # Set isolation level
        print("Target database connection successful.")

        cursor = conn.cursor()

        # Create new schema if it doesn't exist
        print(f"Creating schema '{new_schema}' if it doesn't exist...")
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(new_schema)))
        print(f"Schema '{new_schema}' created or already exists.")

        # Drop tables if they exist to allow rerunning the script easily
        print(f"Dropping existing tables '{new_schema}.{target_film_table}' and '{new_schema}.{target_data_table}' if they exist...")
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS {schema}.{film_table};").format(
            schema=sql.Identifier(new_schema), film_table=sql.Identifier(target_film_table)))
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS {schema}.{data_table};").format(
            schema=sql.Identifier(new_schema), data_table=sql.Identifier(target_data_table)))
        print("Existing tables dropped.")


        # Create target film table
        print(f"Creating table '{new_schema}.{target_film_table}'...")
        create_film_table_sql = sql.SQL(FILM_TABLE_SCHEMA_SQL).format(
             schema=sql.Identifier(new_schema),
             table=sql.Identifier(target_film_table)
        )
        cursor.execute(create_film_table_sql)
        print(f"Table '{new_schema}.{target_film_table}' created.")

        # Insert film data into the target table
        if film_data:
            print(f"Inserting {len(film_data)} rows into '{new_schema}.{target_film_table}'...")
            # Construct the INSERT statement with placeholders for all columns
            # Assumes the order of columns in film_data matches the CREATE TABLE statement
            insert_film_sql = sql.SQL("INSERT INTO {schema}.{table} VALUES ({values});").format(
                schema=sql.Identifier(new_schema),
                table=sql.Identifier(target_film_table),
                values=sql.SQL(', ').join(sql.Placeholder() * len(film_data[0])) # Create placeholders for each column
            )
            # Use executemany for efficient bulk insertion
            cursor.executemany(insert_film_sql, film_data)
            print(f"Successfully inserted {len(film_data)} rows.")
        else:
            print("No film data to insert.")


        # Create 'my_data' table
        print(f"Creating table '{new_schema}.{target_data_table}'...")
        create_my_data_table_sql = sql.SQL("""
            CREATE TABLE {schema}.{table} (
                tot_row INTEGER,
                dist_rating INTEGER,
                tot_length INTEGER,
                avg_length NUMERIC,
                round_avg NUMERIC(10, 2)
            );
        """).format(
            schema=sql.Identifier(new_schema),
            table=sql.Identifier(target_data_table)
        )
        cursor.execute(create_my_data_table_sql)
        print(f"Table '{new_schema}.{target_data_table}' created.")

        # Insert statistics into my_data table
        if aggregate_stats:
             print(f"Inserting statistics into '{new_schema}.{target_data_table}'...")
             insert_stats_sql = sql.SQL("""
                 INSERT INTO {schema}.{table} (tot_row, dist_rating, tot_length, avg_length, round_avg)
                 VALUES (%s, %s, %s, %s, %s);
             """).format(
                 schema=sql.Identifier(new_schema),
                 table=sql.Identifier(target_data_table)
             )
             cursor.execute(insert_stats_sql, aggregate_stats) # aggregate_stats is already a tuple
             print("Statistics inserted successfully.")
        else:
             print("No aggregate statistics to insert.")


        # Commit the transaction
        conn.commit()
        print("\nAll target database operations completed successfully and committed.")

    except psycopg2.OperationalError as e:
        print(f"Operational error while connecting to target database '{db_name}': {e}")
        print("Please ensure the target database is accessible and connection parameters are correct.")
        if conn:
             conn.rollback() # Roll back the transaction on error
             print("Transaction rolled back.")
    except psycopg2.ProgrammingError as e:
        print(f"Database programming error while setting up target database or inserting: {e}")
        if conn:
             conn.rollback() # Roll back the transaction on error
             print("Transaction rolled back.")
    except Exception as e:
        print(f"An unexpected error occurred during target database operations: {e}")
        if conn:
             conn.rollback() # Roll back the transaction on error
             print("Transaction rolled back.")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Target database connection closed.")

# --- Main execution ---
if __name__ == "__main__":
    # 1. Ensure the target database exists
    print("--- Starting Database Setup ---")
    db_created_or_exists = create_database_if_not_exists(TARGET_DB_HOST, TARGET_DB_USER, TARGET_DB_PASSWORD, TARGET_DB_PORT, TARGET_DB_NAME)

    if not db_created_or_exists:
        print("\nExiting: Could not access or create the target database.")
        sys.exit(1) # Exit if the target database is not ready

    # 2. Fetch data and aggregates from the source database (dvdrental)
    print("\n--- Fetching Data from Source Database ---")
    film_data, aggregate_stats = fetch_data_from_source(SOURCE_DB_HOST, SOURCE_DB_NAME, SOURCE_DB_USER, SOURCE_DB_PASSWORD, SOURCE_DB_PORT, SOURCE_SCHEMA, SOURCE_FILM_TABLE)

    if film_data is None or aggregate_stats is None:
         print("\nExiting: Could not fetch data or statistics from the source database.")
         sys.exit(1) # Exit if data fetching failed

    # 3. Setup the target database and insert the fetched data
    print("\n--- Setting up Target Database and Inserting Data ---")
    setup_target_database_and_insert(TARGET_DB_HOST, TARGET_DB_NAME, TARGET_DB_USER, TARGET_DB_PASSWORD, TARGET_DB_PORT, NEW_SCHEMA, TARGET_FILM_TABLE, TARGET_DATA_TABLE, film_data, aggregate_stats)

    print("\n--- Script Finished ---")