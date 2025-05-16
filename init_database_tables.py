import sqlite3
import os

# Make sure data directory exists
os.makedirs("data", exist_ok=True)

# Database path
DB_PATH = "data/freelance.db"


def initialize_gig_tables():
    """
    Initialize the gig database tables if they don't exist.
    This script should be run once to set up the necessary tables.
    """

    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Creating gig_picks table...")
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS gig_picks
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       gig_id
                       INTEGER
                       NOT
                       NULL,
                       created_at
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       gig_id
                   ) REFERENCES gigs
                   (
                       id
                   ),
                       UNIQUE
                   (
                       user_id,
                       gig_id
                   )
                       )
                   ''')

    print("Creating gig_comments table...")
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS gig_comments
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       gig_id
                       INTEGER
                       NOT
                       NULL,
                       content
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       gig_id
                   ) REFERENCES gigs
                   (
                       id
                   )
                       )
                   ''')

    print("Creating gig_files table...")
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS gig_files
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       gig_id
                       INTEGER
                       NOT
                       NULL,
                       filename
                       TEXT
                       NOT
                       NULL,
                       file_data
                       BLOB
                       NOT
                       NULL,
                       description
                       TEXT,
                       uploaded_at
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       gig_id
                   ) REFERENCES gigs
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    print("Database tables created successfully!")
    conn.close()


if __name__ == "__main__":
    initialize_gig_tables()
    print("Database initialization complete. You can now run the application.")