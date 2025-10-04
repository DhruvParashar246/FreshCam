import sqlite3
import os
from contextlib import contextmanager
from typing import Optional

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'pantry_db.sqlite')


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create pantry_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pantry_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fruit_name TEXT NOT NULL,
                stage INTEGER NOT NULL,
                confidence REAL NOT NULL,
                expiry_date TEXT NOT NULL,
                added_date TEXT NOT NULL,
                image_path TEXT,
                notes TEXT
            )
        ''')
        
        print("✅ Database initialized successfully")


def dict_from_row(row) -> dict:
    """Convert sqlite3.Row to dictionary."""
    return dict(zip(row.keys(), row)) if row else None


def execute_query(query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False):
    """
    Execute a SQL query and return results.
    
    Args:
        query: SQL query string
        params: Query parameters
        fetch_one: Return single row
        fetch_all: Return all rows
    
    Returns:
        Query results or None
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch_one:
            row = cursor.fetchone()
            return dict_from_row(row)
        elif fetch_all:
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
        else:
            return cursor.lastrowid
