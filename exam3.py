import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # For CREATE DATABASE
import os
import logging
import sys

# --- Configuration ---
URL = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
LOG_FILE = "bank_processor.log"
TABLE_NAME = "largest_banks"
SCHEMA_NAME = "public" # Or another schema if you prefer

# PostgreSQL Database Connection Parameters
# You MUST replace these with your actual PostgreSQL credentials
DB_HOST = "localhost"
DB_NAME = "bank_data_db" # A new database name for this project
DB_USER = "postgres" # Default PostgreSQL user
DB_PASSWORD = "bishop5070" # Replace with your actual password
DB_PORT = "5432"

# Exchange rates provided (USD to other currencies)
EXCHANGE_RATES = {
    "EUR": 0.93,  # $1 USD = 0.93 Euro
    "GBP": 0.80,  # $1 USD = 0.80 Pound
    "INR": 82.95  # $1 USD = 82.95 INR
}

# --- Logging Setup ---
# Create a custom handler to write logs to the GUI text widget
class TextWidgetHandler(logging.Handler):
    def _init_(self, text_widget):
        super()._init_()
        self.text_widget = text_widget
        self.text_widget.config(state='disabled') # Disable editing by user

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state='normal') # Enable editing temporarily
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END) # Auto-scroll to the bottom
        self.text_widget.config(state='disabled') # Disable editing again

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO) # Set minimum logging level

# Create file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO) # Log INFO and above to file

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)

# --- Database Utility Function (for checking/creating database) ---
def create_database_if_not_exists(db_host, db_user, db_password, db_port, new_db_name):
    """Connects to the default maintenance database (postgres) to create a new database."""
    conn = None
    try:
        # Connect to the default 'postgres' database to be able to create a new database
        logger.info(f"Attempting to connect to 'postgres' database at {db_host}:{db_port} as user {db_user} to check/create '{new_db_name}'...")
        conn = psycopg2.connect(host=db_host, database="postgres", user=db_user, password=db_password, port=db_port)

        # Explicitly set autocommit mode for this connection BEFORE executing CREATE DATABASE
        conn.autocommit = True

        cursor = conn.cursor()

        # Check if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), (new_db_name,))
        exists = cursor.fetchone()

        if not exists:
            logger.info(f"Database '{new_db_name}' does not exist. Creating...")
            # Create the new database - this command requires autocommit mode
            cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(new_db_name)))
            logger.info(f"Database '{new_db_name}' created successfully.")
        else:
            logger.info(f"Database '{new_db_name}' already exists.")

        cursor.close()
        return True # Indicate success

    except psycopg2.OperationalError as e:
        logger.error(f"Operational error while connecting to 'postgres' or creating '{new_db_name}': {e}")
        logger.error("Please ensure PostgreSQL is running, your connection parameters for the default database are correct, and the user has privileges to create databases.")
        return False # Indicate failure
    except Exception as e:
        logger.error(f"An unexpected error occurred during database creation check: {e}")
        return False # Indicate failure
    finally:
        if conn:
            conn.close()
            logger.info("Database creation check connection closed.")


# --- Core Logic Functions ---

def scrape_bank_data(url):
    """Scrapes bank data from the given URL."""
    logger.info(f"Attempting to scrape data from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        logger.info("Successfully fetched the page content.")

        # Use pandas to read HTML tables
        tables = pd.read_html(response.text)

        df = None
        for i, table in enumerate(tables):
            table_columns_lower = [col.lower() for col in table.columns]
            if any('rank' in col for col in table_columns_lower) and \
               any('bank name' in col for col in table_columns_lower) and \
               any('market cap' in col and ('us$' in col or 'usd' in col) for col in table_columns_lower):
                df = table
                logger.info(f"Identified the correct table (Table index {i}).")
                break

        if df is None:
            logger.error("Could not find the table with expected columns on the page.")
            return None

        # Clean up column names to make them easier to work with
        # Based on the URL, the columns are typically: Rank, Bank name, Market cap (US$ billion), Footnote
        # We need to be careful if the structure changes slightly.
        # Let's try to dynamically find the market cap column based on keywords
        market_cap_col = None
        for col in df.columns:
            if 'market cap' in col.lower() and ('us$' in col.lower() or 'usd' in col.lower()):
                market_cap_col = col
                break

        if market_cap_col is None:
             logger.error("Could not find the 'Market cap (US$ billion)' column.")
             return None

        # Rename columns for consistency
        df.rename(columns={
            df.columns[0]: 'Rank', # Assuming first column is Rank
            df.columns[1]: 'Bank name', # Assuming second column is Bank name
            market_cap_col: 'Market cap (US$ billion)'
        }, inplace=True)

        # Select the core columns we need
        df = df[['Rank', 'Bank name', 'Market cap (US$ billion)']]

        # Clean the 'Market cap (US$ billion)' column: remove commas and convert to numeric
        df['Market cap (US$ billion)'] = df['Market cap (US$ billion)'].astype(str).str.replace(',', '', regex=False)
        df['Market cap (US$ billion)'] = pd.to_numeric(df['Market cap (US$ billion)'], errors='coerce') # Coerce errors to NaN

        # Drop rows where Market Cap could not be converted (e.g., header rows repeated in the table)
        df.dropna(subset=['Market cap (US$ billion)'], inplace=True)

        # Convert Rank to integer, coercing errors
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce').astype('Int64') # Use Int64 to allow NaN

        logger.info("Successfully scraped and cleaned initial data.")
        logger.info(f"Scraped data preview:\n{df.head()}")

        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        return None

def transform_data(df, rates):
    """Transforms the DataFrame by adding market cap in other currencies."""
    if df is None or df.empty:
        logger.warning("No data to transform.")
        return None

    logger.info("Starting data transformation...")

    transformed_df = df.copy() # Work on a copy to not modify the original DataFrame

    # Calculate market cap in other currencies
    try:
        # Ensure the USD column exists before calculating
        if 'Market cap (US$ billion)' not in transformed_df.columns:
            logger.error("USD market cap column not found for transformation.")
            return None

        transformed_df['Market cap (EUR billion)'] = (transformed_df['Market cap (US$ billion)'] * rates['EUR']).round(2)
        transformed_df['Market cap (GBP billion)'] = (transformed_df['Market cap (US$ billion)'] * rates['GBP']).round(2)
        transformed_df['Market cap (INR billion)'] = (transformed_df['Market cap (US$ billion)'] * rates['INR']).round(2)

        logger.info("Successfully transformed data.")
        logger.info(f"Transformed data preview:\n{transformed_df.head()}")

        return transformed_df

    except KeyError as e:
        logger.error(f"Missing exchange rate for currency: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred during data transformation: {e}")
        return None

def load_to_database_psycopg2(df, db_host, db_name, db_user, db_password, db_port, schema_name, table_name):
    """Loads the DataFrame into the PostgreSQL database using psycopg2."""
    if df is None or df.empty:
        logger.warning("No data to load to database.")
        return

    # Ensure the target database exists first
    db_ready = create_database_if_not_exists(db_host, db_user, db_password, db_port, db_name)
    if not db_ready:
        logger.error(f"Target database '{db_name}' is not ready. Cannot proceed with loading.")
        return

    conn = None
    cursor = None
    try:
        logger.info(f"Attempting to connect to target database '{db_name}' at {db_host}:{db_port} as user {db_user}...")
        # Connect to the target database (which is now confirmed to exist)
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, port=db_port)
        # Set isolation level for the data loading transaction - autocommit=False is the default
        # conn.set_isolation_level(psycopg2.extensions.READ_COMMITTED) # Using the constant name is preferred if available
        # If the constant name still causes issues, you can use the integer value 1:
        # conn.set_isolation_level(1) # 1 corresponds to READ COMMITTED

        # Note: By default, psycopg2 connections are not in autocommit mode,
        # which is correct for transactions where you commit or rollback.
        # So, we don't need to explicitly set conn.autocommit = False here.


        cursor = conn.cursor()
        logger.info("Database connection successful.")

        # Create schema if it doesn't exist (optional, but good practice)
        logger.info(f"Creating schema '{schema_name}' if it doesn't exist...")
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(schema_name)))
        logger.info(f"Schema '{schema_name}' created or already exists.")

        # Define the CREATE TABLE SQL statement
        # Ensure column names and types match the DataFrame columns
        create_table_sql = sql.SQL("""
            CREATE TABLE {schema}.{table} (
                id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
                rank INTEGER,
                bank_name VARCHAR(255),
                market_cap_usd_billion NUMERIC(20, 2), -- Use NUMERIC for currency
                market_cap_eur_billion NUMERIC(20, 2),
                market_cap_gbp_billion NUMERIC(20, 2),
                market_cap_inr_billion NUMERIC(20, 2)
            );
        """).format(
            schema=sql.Identifier(schema_name),
            table=sql.Identifier(table_name)
        )

        # Drop table if it exists to replace data (or use IF NOT EXISTS and handle duplicates)
        logger.info(f"Dropping existing table '{schema_name}.{table_name}' if it exists...")
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS {schema}.{table};").format(
            schema=sql.Identifier(schema_name), table=sql.Identifier(table_name)))
        logger.info(f"Existing table '{schema_name}.{table_name}' dropped.")

        # Create the table
        logger.info(f"Creating table '{schema_name}.{table_name}'...")
        cursor.execute(create_table_sql)
        logger.info(f"Table '{schema_name}.{table_name}' created.")

        # Prepare data for insertion
        # We need to convert DataFrame rows to a list of tuples
        data_to_insert = [tuple(row) for row in df[['Rank', 'Bank name', 'Market cap (US$ billion)',
                                                    'Market cap (EUR billion)', 'Market cap (GBP billion)',
                                                    'Market cap (INR billion)']].values]

        # Define the INSERT statement
        # We exclude the 'id' column as it's SERIAL and auto-generated
        insert_sql = sql.SQL("""
            INSERT INTO {schema}.{table} (rank, bank_name, market_cap_usd_billion, market_cap_eur_billion, market_cap_gbp_billion, market_cap_inr_billion)
            VALUES (%s, %s, %s, %s, %s, %s);
        """).format(
            schema=sql.Identifier(schema_name),
            table=sql.Identifier(table_name)
        )

        # Use executemany for efficient bulk insertion
        if data_to_insert:
            logger.info(f"Inserting {len(data_to_insert)} rows into '{schema_name}.{table_name}'...")
            cursor.executemany(insert_sql, data_to_insert)
            logger.info(f"Successfully inserted {len(data_to_insert)} rows.")
        else:
            logger.warning("No data rows to insert.")


        # Commit the transaction
        conn.commit()
        logger.info("\nData loading transaction committed successfully.")

    except psycopg2.OperationalError as e:
        logger.error(f"Operational error during database loading: {e}")
        logger.error("Please check database connection parameters, user privileges, and ensure the database is accessible.")
        if conn:
             conn.rollback() # Roll back the transaction on error
             logger.error("Transaction rolled back.")
    except psycopg2.ProgrammingError as e:
        logger.error(f"Database programming error during loading: {e}")
        if conn:
             conn.rollback() # Roll back the transaction on error
             logger.error("Transaction rolled back.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during database loading: {e}")
        if conn:
             conn.rollback() # Roll back the transaction on error
             logger.error("Transaction rolled back.")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed.")


# --- GUI Application Class ---

class BankProcessorGUI(tk.Tk):
    def _init_(self):
        super()._init_()

        self.title("Bank Data Processor (PostgreSQL)") # Updated title
        self.geometry("800x600")

        # Configure grid column to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row for the log area

        # --- Widgets ---
        self.control_frame = tk.Frame(self, bg="#e0e0e0") # Light grey background for control frame
        self.control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Button Styling
        button_style = {
            'fg': 'white', # White text
            'bg': '#4CAF50', # Green background
            'activeforeground': 'white',
            'activebackground': '#388E3C', # Darker green when active
            'bd': 0, # No border
            'relief': 'flat', # Flat look
            'padx': 10,
            'pady': 5,
            'font': ('Arial', 10, 'bold')
        }

        self.scrape_button = tk.Button(self.control_frame, text="Scrape & Process Data", command=self.on_scrape_button_click, **button_style)
        self.scrape_button.pack(side=tk.LEFT, padx=5)

        self.load_db_button = tk.Button(self.control_frame, text="Load to PostgreSQL DB", command=self.on_load_db_button_click, **button_style)
        self.load_db_button.pack(side=tk.LEFT, padx=5)
        self.load_db_button.config(state='disabled', bg='#9E9E9E', activebackground='#757575') # Grey out when disabled

        # Add Exit button
        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.on_exit_button_click,
                                     fg='white', bg='#F44336', # Red background
                                     activeforeground='white', activebackground='#D32F2F', # Darker red
                                     bd=0, relief='flat', padx=10, pady=5, font=('Arial', 10, 'bold'))
        self.exit_button.pack(side=tk.RIGHT, padx=5)


        self.log_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', bg="#f5f5f5", fg="#333333") # Light background, dark text
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Internal State ---
        self.processed_data = None # To hold the DataFrame after scraping and transformation

        # --- Set up GUI Logging Handler ---
        self.gui_handler = TextWidgetHandler(self.log_text)
        self.gui_handler.setLevel(logging.INFO) # Log INFO and above to GUI
        self.gui_handler.setFormatter(formatter) # Use the same formatter
        logger.addHandler(self.gui_handler)

        # Initial log message
        logger.info("GUI started. Ready to process bank data for PostgreSQL.")

    def on_scrape_button_click(self):
        """Handles the button click for scraping and processing."""
        logger.info("-" * 30)
        logger.info("Starting data scraping and processing...")
        self.processed_data = None # Clear previous data
        self.load_db_button.config(state='disabled', bg='#9E9E9E', activebackground='#757575') # Grey out when disabled

        # Step 1: Scrape data
        df_scraped = scrape_bank_data(URL)

        if df_scraped is not None:
            # Step 2: Transform data
            self.processed_data = transform_data(df_scraped, EXCHANGE_RATES)

            if self.processed_data is not None:
                logger.info("Data processing complete.")
                self.load_db_button.config(state='normal', bg='#4CAF50', activebackground='#388E3C') # Re-colour when enabled
            else:
                 logger.error("Data transformation failed.")
        else:
            logger.error("Data scraping failed.")

        logger.info("-" * 30)


    def on_load_db_button_click(self):
        """Handles the button click for loading data to the database."""
        if self.processed_data is not None:
            logger.info("-" * 30)
            logger.info("Starting data loading to PostgreSQL database...")
            load_to_database_psycopg2(self.processed_data, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, SCHEMA_NAME, TABLE_NAME)
            logger.info("Database loading process finished.")
            logger.info("-" * 30)
        else:
            logger.warning("No processed data available to load to the database. Please scrape and process first.")

    def on_exit_button_click(self):
        """Handles the button click for exiting the application."""
        logger.info("Exiting application.")
        self.destroy() # Close the main window


# --- Main Execution ---
if __name__ == "__main__":
    # Ensure psycopg2 is installed
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2 library not found.")
        print("Please install it using: pip install psycopg2-binary")
        sys.exit(1)


    app = BankProcessorGUI()
    app.mainloop()

    # Clean up file handler when the GUI closes
    logger.removeHandler(file_handler)
    file_handler.close()