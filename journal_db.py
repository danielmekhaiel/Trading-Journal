import sqlite3
import pandas as pd

DB_NAME = "trading_journal.db"

def init_db():
    """Initializes the SQLite database and creates the trades table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            side TEXT NOT NULL,          # 'CALL' or 'PUT'
            setup TEXT NOT NULL,         # e.g., 'Break-Imbalance-Retest'
            contracts INTEGER NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL NOT NULL,
            max_contract_price REAL,     # High watermark of the contract for runner tracking
            pnl REAL NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_trade(date, ticker, side, setup, contracts, entry_price, exit_price, max_contract_price, pnl, notes):
    """Inserts a new trade record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (date, ticker, side, setup, contracts, entry_price, exit_price, max_contract_price, pnl, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, ticker, side, setup, contracts, entry_price, exit_price, max_contract_price, pnl, notes))
    conn.commit()
    conn.close()

def get_all_trades():
    """Retrieves all trades from the database as a Pandas DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM trades ORDER BY date DESC", conn)
    conn.close()
    return df
