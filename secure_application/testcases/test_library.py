import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from database import initialize_database, get_connection

def test_database_initialization():
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    books = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    members = cursor.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    
    conn.close()
    assert books > 0
    assert members > 0
