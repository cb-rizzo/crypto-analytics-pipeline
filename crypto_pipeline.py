import os
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Configure the logging system (to track events cleanly instead of using print)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables from the .env file (for local testing)
load_dotenv()

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def fetch_crypto_price(symbol="BTCUSDT"):
    """Extracts the current cryptocurrency price from Binance's public API."""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        logging.info(f"Querying Binance API for {symbol}...")
        response = requests.get(url, timeout=10)
        # Raise an exception if the status code is not 200 (success)
        response.raise_for_status()
        
        data = response.json()
        price = float(data["price"])
        logging.info(f"Price fetched successfully: {price} for {symbol}")
        return symbol, price
    except requests.exceptions.RequestException as e:
        logging.error(f"Network or connection error while querying Binance: {e}")
        return None, None
    except (KeyError, ValueError) as e:
        logging.error(f"Error processing Binance JSON response: {e}")
        return None, None

def save_to_postgres(symbol, price):
    """Saves the record incrementally to PostgreSQL."""
    if not DATABASE_URL:
        logging.error("DATABASE_URL environment variable not found.")
        return

    if price is None:
        logging.warning("No price to save due to a previous error.")
        return

    try:
        # Create the SQLAlchemy engine connection
        engine = create_engine(DATABASE_URL)
        
        # Structure the data using Pandas
        df = pd.DataFrame([{
            "symbol": symbol,
            "price": price,
            "timestamp": pd.Timestamp.now()
        }])

        with engine.begin() as connection:
            # Create the table if it doesn't exist (safe automated table creation)
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS crypto_prices (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20),
                    price NUMERIC,
                    timestamp TIMESTAMP
                );
            """))
            
            # Save the DataFrame to the 'crypto_prices' table (using append to build historical data)
            df.to_sql("crypto_prices", con=connection, if_exists="append", index=False)
            
        logging.info("Data successfully saved to PostgreSQL!")

    except Exception as e:
        logging.error(f"Error connecting or saving to the database: {e}")

if __name__ == "__main__":
    logging.info("Starting cryptocurrency pipeline execution...")
    sym, prc = fetch_crypto_price("BTCUSDT")
    save_to_postgres(sym, prc)
    logging.info("Pipeline finished.")