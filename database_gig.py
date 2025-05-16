import sqlite3
from datetime import datetime


# Database connection function
def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect("data/freelance.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_gig_tables():
    """Initialize the gig-related tables in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create gig_picks table if it doesn't exist
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

    # Create gig_comments table if it doesn't exist
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

    # Create gig_files table if it doesn't exist
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
    conn.close()


# Gig picking functions
def pick_gig(user_id, gig_id):
    """Pick a gig by a user

    Args:
        user_id (int): User ID
        gig_id (int): Gig ID

    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First check if this user already picked this gig
        cursor.execute("SELECT 1 FROM gig_picks WHERE user_id = ? AND gig_id = ?", (user_id, gig_id))
        if cursor.fetchone():
            # Already picked
            conn.close()
            return True

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO gig_picks (user_id, gig_id, created_at)
                       VALUES (?, ?, ?)
                       """, (user_id, gig_id, created_at))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error picking gig: {e}")
        conn.close()
        return False


def unpick_gig(user_id, gig_id):
    """Unpick a gig by a user

    Args:
        user_id (int): User ID
        gig_id (int): Gig ID

    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM gig_picks WHERE user_id = ? AND gig_id = ?", (user_id, gig_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error unpicking gig: {e}")
        conn.close()
        return False


def has_user_picked_gig(user_id, gig_id):
    """Check if a user has picked a gig

    Args:
        user_id (int): User ID
        gig_id (int): Gig ID

    Returns:
        bool: True if picked, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM gig_picks WHERE user_id = ? AND gig_id = ?", (user_id, gig_id))
    result = cursor.fetchone() is not None

    conn.close()
    return result


def get_gig_picks_count(gig_id):
    """Get the number of users who picked a gig

    Args:
        gig_id (int): Gig ID

    Returns:
        int: Number of users who picked the gig
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM gig_picks WHERE gig_id = ?", (gig_id,))
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_user_picked_gigs(user_id):
    """Get gigs picked by a user

    Args:
        user_id (int): User ID

    Returns:
        list: List of gig dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
            SELECT g.id, \
                   g.user_id, \
                   g.title, \
                   g.description, \
                   g.price_min, \
                   g.price_max,
                   g.duration, \
                   g.created_at, \
                   g.status, \
                   u.username
            FROM gigs g
                     JOIN users u ON g.user_id = u.id
                     JOIN gig_picks gp ON g.id = gp.gig_id
            WHERE gp.user_id = ?
            ORDER BY gp.created_at DESC \
            """

    cursor.execute(query, (user_id,))
    gigs = [dict(row) for row in cursor.fetchall()]

    # Get skills for each gig
    for gig in gigs:
        cursor.execute("""
                       SELECT s.id, s.name, s.category
                       FROM skills s
                                JOIN gig_skills gs ON s.id = gs.skill_id
                       WHERE gs.gig_id = ?
                       """, (gig['id'],))
        gig['skills'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return gigs


# Gig comments functions
def add_gig_comment(user_id, gig_id, content):
    """Add a comment to a gig

    Args:
        user_id (int): User ID
        gig_id (int): Gig ID
        content (str): Comment content

    Returns:
        int: The ID of the created comment, or None if creation failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO gig_comments (user_id, gig_id, content, created_at)
                       VALUES (?, ?, ?, ?)
                       """, (user_id, gig_id, content, created_at))

        comment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return comment_id
    except Exception as e:
        print(f"Error adding comment: {e}")
        conn.close()
        return None


def get_gig_comments(gig_id):
    """Get comments for a gig

    Args:
        gig_id (int): Gig ID

    Returns:
        list: List of comment dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT c.id, c.user_id, c.content, c.created_at, u.username
                   FROM gig_comments c
                            JOIN users u ON c.user_id = u.id
                   WHERE c.gig_id = ?
                   ORDER BY c.created_at ASC
                   """, (gig_id,))

    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return comments


# Gig files functions
def add_gig_file(user_id, gig_id, filename, file_data, description=None):
    """Add a file to a gig

    Args:
        user_id (int): User ID
        gig_id (int): Gig ID
        filename (str): Name of the file
        file_data (bytes): Binary file data
        description (str, optional): File description

    Returns:
        int: The ID of the uploaded file, or None if upload failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO gig_files (user_id, gig_id, filename, file_data, description, uploaded_at)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (user_id, gig_id, filename, file_data, description, uploaded_at))

        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    except Exception as e:
        print(f"Error uploading file: {e}")
        conn.close()
        return None


def get_gig_files(gig_id):
    """Get files for a gig

    Args:
        gig_id (int): Gig ID

    Returns:
        list: List of file dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT f.id, f.user_id, f.filename, f.file_data, f.description, f.uploaded_at, u.username
                   FROM gig_files f
                            JOIN users u ON f.user_id = u.id
                   WHERE f.gig_id = ?
                   ORDER BY f.uploaded_at DESC
                   """, (gig_id,))

    files = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return files


# Initialize tables when this module is imported
if __name__ == "__main__":
    init_gig_tables()