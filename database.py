import sqlite3
import os
import hashlib
import pandas as pd
from datetime import datetime

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

DB_PATH = "data/freelance.db"


def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       email
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password_hash
                       TEXT
                       NOT
                       NULL,
                       full_name
                       TEXT,
                       bio
                       TEXT,
                       join_date
                       TEXT
                       NOT
                       NULL,
                       profile_picture
                       TEXT
                   )
                   ''')

    # Skills table (predefined skills)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS skills
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       category
                       TEXT
                       NOT
                       NULL
                   )
                   ''')

    # User_Skills (many-to-many relationship)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_skills
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
                       skill_id
                       INTEGER
                       NOT
                       NULL,
                       proficiency_level
                       TEXT
                       NOT
                       NULL,
                       years_experience
                       INTEGER,
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
                       skill_id
                   ) REFERENCES skills
                   (
                       id
                   ),
                       UNIQUE
                   (
                       user_id,
                       skill_id
                   )
                       )
                   ''')

    # Gigs table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS gigs
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
                       title
                       TEXT
                       NOT
                       NULL,
                       description
                       TEXT
                       NOT
                       NULL,
                       price_min
                       REAL
                       NOT
                       NULL,
                       price_max
                       REAL
                       NOT
                       NULL,
                       duration
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TEXT
                       NOT
                       NULL,
                       status
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
                   )
                       )
                   ''')

    # Gig_Skills (many-to-many relationship)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS gig_skills
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       gig_id
                       INTEGER
                       NOT
                       NULL,
                       skill_id
                       INTEGER
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       gig_id
                   ) REFERENCES gigs
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       skill_id
                   ) REFERENCES skills
                   (
                       id
                   ),
                       UNIQUE
                   (
                       gig_id,
                       skill_id
                   )
                       )
                   ''')

    # Courses table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS courses
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT
                       NOT
                       NULL,
                       description
                       TEXT
                       NOT
                       NULL,
                       provider
                       TEXT
                       NOT
                       NULL,
                       url
                       TEXT
                       NOT
                       NULL,
                       difficulty_level
                       TEXT
                       NOT
                       NULL,
                       duration
                       TEXT
                       NOT
                       NULL,
                       price
                       REAL
                   )
                   ''')

    # Course_Skills (many-to-many relationship)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS course_skills
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       course_id
                       INTEGER
                       NOT
                       NULL,
                       skill_id
                       INTEGER
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       course_id
                   ) REFERENCES courses
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       skill_id
                   ) REFERENCES skills
                   (
                       id
                   ),
                       UNIQUE
                   (
                       course_id,
                       skill_id
                   )
                       )
                   ''')

    # Posts table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS posts
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
                       content
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TEXT
                       NOT
                       NULL,
                       image_url
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   )
                       )
                   ''')

    # Likes table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS likes
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
                       post_id
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
                       post_id
                   ) REFERENCES posts
                   (
                       id
                   ),
                       UNIQUE
                   (
                       user_id,
                       post_id
                   )
                       )
                   ''')

    # Comments table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS comments
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
                       post_id
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
                       post_id
                   ) REFERENCES posts
                   (
                       id
                   )
                       )
                   ''')

    # Commit changes and close connection
    conn.commit()

    # Insert default skills if the skills table is empty
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        insert_default_skills(conn)

    # Insert sample courses if the courses table is empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        insert_sample_courses(conn)

    conn.close()


def insert_default_skills(conn):
    """Insert default skills into the skills table"""
    skills_data = [
        # Programming
        ("Python", "Programming"),
        ("JavaScript", "Programming"),
        ("Java", "Programming"),
        ("C#", "Programming"),
        ("PHP", "Programming"),
        ("Ruby", "Programming"),
        ("Swift", "Programming"),
        ("Kotlin", "Programming"),
        ("Go", "Programming"),
        ("Rust", "Programming"),

        # Web Development
        ("HTML/CSS", "Web Development"),
        ("React", "Web Development"),
        ("Angular", "Web Development"),
        ("Vue.js", "Web Development"),
        ("Node.js", "Web Development"),
        ("Django", "Web Development"),
        ("Flask", "Web Development"),
        ("WordPress", "Web Development"),
        ("Shopify", "Web Development"),

        # Mobile Development
        ("iOS Development", "Mobile Development"),
        ("Android Development", "Mobile Development"),
        ("React Native", "Mobile Development"),
        ("Flutter", "Mobile Development"),

        # Data Science
        ("Data Analysis", "Data Science"),
        ("Machine Learning", "Data Science"),
        ("Deep Learning", "Data Science"),
        ("Natural Language Processing", "Data Science"),
        ("Computer Vision", "Data Science"),
        ("Statistics", "Data Science"),
        ("R", "Data Science"),
        ("Tableau", "Data Science"),
        ("Power BI", "Data Science"),

        # Design
        ("UI Design", "Design"),
        ("UX Design", "Design"),
        ("Graphic Design", "Design"),
        ("Logo Design", "Design"),
        ("Illustration", "Design"),
        ("Adobe Photoshop", "Design"),
        ("Adobe Illustrator", "Design"),
        ("Figma", "Design"),
        ("Sketch", "Design"),

        # Writing
        ("Content Writing", "Writing"),
        ("Copywriting", "Writing"),
        ("Technical Writing", "Writing"),
        ("Creative Writing", "Writing"),
        ("SEO Writing", "Writing"),
        ("Editing", "Writing"),
        ("Proofreading", "Writing"),

        # Marketing
        ("Digital Marketing", "Marketing"),
        ("Social Media Marketing", "Marketing"),
        ("SEO", "Marketing"),
        ("SEM", "Marketing"),
        ("Email Marketing", "Marketing"),
        ("Content Marketing", "Marketing"),
        ("Affiliate Marketing", "Marketing"),
        ("Google Analytics", "Marketing"),

        # Video & Audio
        ("Video Editing", "Video & Audio"),
        ("Animation", "Video & Audio"),
        ("Voice Over", "Video & Audio"),
        ("Audio Editing", "Video & Audio"),
        ("Music Production", "Video & Audio"),

        # Business
        ("Project Management", "Business"),
        ("Business Analysis", "Business"),
        ("Virtual Assistance", "Business"),
        ("Accounting", "Business"),
        ("Financial Analysis", "Business"),
        ("Customer Service", "Business"),
        ("Sales", "Business"),
        ("HR Management", "Business")
    ]

    cursor = conn.cursor()
    for name, category in skills_data:
        cursor.execute("INSERT INTO skills (name, category) VALUES (?, ?)", (name, category))

    conn.commit()


def insert_sample_courses(conn):
    """Insert sample courses into the courses table"""
    courses_data = [
        # Programming courses
        ("Python for Beginners", "Learn Python programming from scratch with hands-on projects", "Udemy",
         "https://udemy.com/python-beginners", "Beginner", "10 hours", 19.99),
        ("Advanced JavaScript", "Master modern JavaScript with advanced concepts and patterns", "Coursera",
         "https://coursera.org/advanced-js", "Advanced", "20 hours", 49.99),
        ("Java Masterclass", "Complete Java programming bootcamp with real-world applications", "Udemy",
         "https://udemy.com/java-masterclass", "Intermediate", "30 hours", 29.99),

        # Web Development
        ("Full Stack Web Development", "Learn front-end and back-end web development with MERN stack", "Udemy",
         "https://udemy.com/fullstack-web", "Intermediate", "40 hours", 39.99),
        ("React - The Complete Guide", "Dive into React, Redux, and build powerful single-page applications", "Udemy",
         "https://udemy.com/react-complete-guide", "Intermediate", "25 hours", 24.99),
        ("Django for Web Development", "Build web applications with Python and Django framework", "Coursera",
         "https://coursera.org/django-web", "Intermediate", "15 hours", 29.99),

        # Mobile Development
        ("iOS App Development with Swift", "Build iOS apps with Swift and UIKit", "Udacity",
         "https://udacity.com/ios-swift", "Intermediate", "20 hours", 199.00),
        ("Android Development Masterclass", "Create Android apps with Kotlin from scratch", "Udemy",
         "https://udemy.com/android-kotlin", "Intermediate", "25 hours", 24.99),
        ("React Native - Mobile Apps", "Build native mobile apps for iOS and Android with React Native", "Udemy",
         "https://udemy.com/react-native-apps", "Intermediate", "20 hours", 29.99),

        # Data Science
        ("Data Science Specialization", "Master data science skills with R and Python", "Coursera",
         "https://coursera.org/data-science-spec", "Advanced", "60 hours", 99.00),
        ("Machine Learning A-Z", "Learn and implement machine learning algorithms", "Udemy",
         "https://udemy.com/machine-learning-az", "Intermediate", "30 hours", 34.99),
        ("Deep Learning Fundamentals", "Master neural networks and deep learning frameworks", "edX",
         "https://edx.org/deep-learning", "Advanced", "40 hours", 49.00),

        # Design
        ("UI/UX Design Bootcamp", "Master user interface and user experience design", "Udemy",
         "https://udemy.com/uiux-bootcamp", "Beginner", "20 hours", 29.99),
        ("Graphic Design Masterclass", "Learn graphic design principles and Adobe Creative Suite", "Skillshare",
         "https://skillshare.com/graphic-design", "Beginner", "15 hours", 15.00),
        ("Figma - UI/UX Design", "Create modern interfaces with Figma design tool", "Udemy",
         "https://udemy.com/figma-design", "Beginner", "10 hours", 19.99),

        # Writing
        ("Content Writing Masterclass", "Create engaging content for blogs and websites", "Udemy",
         "https://udemy.com/content-writing", "Beginner", "8 hours", 19.99),
        ("Copywriting for Conversion", "Write copy that sells and converts", "Skillshare",
         "https://skillshare.com/copywriting", "Intermediate", "5 hours", 10.00),
        ("Technical Writing", "Learn to write clear technical documentation", "Udemy",
         "https://udemy.com/technical-writing", "Intermediate", "12 hours", 24.99),

        # Marketing
        ("Digital Marketing Specialization", "Master all aspects of digital marketing", "Coursera",
         "https://coursera.org/digital-marketing", "Intermediate", "30 hours", 49.00),
        ("Social Media Marketing", "Grow your business with social media strategies", "Udemy",
         "https://udemy.com/social-media-marketing", "Beginner", "15 hours", 19.99),
        ("SEO 2023: Complete Guide", "Master search engine optimization techniques", "Udemy",
         "https://udemy.com/seo-complete", "Intermediate", "10 hours", 24.99),

        # Video & Audio
        ("Video Editing with Premiere Pro", "Master video editing with Adobe Premiere Pro", "Udemy",
         "https://udemy.com/premiere-pro", "Intermediate", "15 hours", 24.99),
        ("Animation Fundamentals", "Learn 2D and 3D animation principles", "Skillshare",
         "https://skillshare.com/animation", "Beginner", "10 hours", 15.00),
        ("Voice Over Masterclass", "Become a professional voice over artist", "Udemy", "https://udemy.com/voice-over",
         "Beginner", "8 hours", 19.99),

        # Business
        ("Project Management Professional", "Prepare for PMP certification", "Udemy", "https://udemy.com/pmp-prep",
         "Advanced", "25 hours", 29.99),
        ("Business Analysis Fundamentals", "Learn essential business analysis skills", "Coursera",
         "https://coursera.org/business-analysis", "Intermediate", "20 hours", 39.00),
        ("Virtual Assistant - Start a VA Business", "Build your virtual assistant business from scratch", "Udemy",
         "https://udemy.com/virtual-assistant", "Beginner", "10 hours", 19.99)
    ]

    cursor = conn.cursor()
    for title, description, provider, url, difficulty_level, duration, price in courses_data:
        cursor.execute("""
                       INSERT INTO courses (title, description, provider, url, difficulty_level, duration, price)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (title, description, provider, url, difficulty_level, duration, price))

    # Link courses to relevant skills
    course_skills = [
        # Python course skills
        (1, 1),  # Python for Beginners - Python

        # Advanced JavaScript course skills
        (2, 2),  # Advanced JavaScript - JavaScript

        # Java Masterclass course skills
        (3, 3),  # Java Masterclass - Java

        # Full Stack Web Development course skills
        (4, 2),  # Full Stack - JavaScript
        (4, 11),  # Full Stack - HTML/CSS
        (4, 12),  # Full Stack - React
        (4, 15),  # Full Stack - Node.js

        # React course skills
        (5, 2),  # React - JavaScript
        (5, 12),  # React - React

        # Django course skills
        (6, 1),  # Django - Python
        (6, 16),  # Django - Django

        # iOS Development course skills
        (7, 7),  # iOS - Swift
        (7, 21),  # iOS - iOS Development

        # Android Development course skills
        (8, 8),  # Android - Kotlin
        (8, 22),  # Android - Android Development

        # React Native course skills
        (9, 2),  # React Native - JavaScript
        (9, 23),  # React Native - React Native

        # Data Science Specialization course skills
        (10, 1),  # Data Science - Python
        (10, 25),  # Data Science - Data Analysis
        (10, 30),  # Data Science - R

        # Machine Learning course skills
        (11, 1),  # ML - Python
        (11, 26),  # ML - Machine Learning

        # Deep Learning course skills
        (12, 1),  # DL - Python
        (12, 27),  # DL - Deep Learning

        # UI/UX Design Bootcamp course skills
        (13, 34),  # UI/UX - UI Design
        (13, 35),  # UI/UX - UX Design

        # Graphic Design Masterclass course skills
        (14, 36),  # Graphic Design - Graphic Design
        (14, 39),  # Graphic Design - Adobe Photoshop
        (14, 40),  # Graphic Design - Adobe Illustrator

        # Figma course skills
        (15, 34),  # Figma - UI Design
        (15, 41),  # Figma - Figma

        # Content Writing Masterclass course skills
        (16, 44),  # Content Writing - Content Writing

        # Copywriting for Conversion course skills
        (17, 45),  # Copywriting - Copywriting

        # Technical Writing course skills
        (18, 46),  # Technical Writing - Technical Writing

        # Digital Marketing Specialization course skills
        (19, 51),  # Digital Marketing - Digital Marketing

        # Social Media Marketing course skills
        (20, 52),  # SMM - Social Media Marketing

        # SEO course skills
        (21, 53),  # SEO - SEO

        # Video Editing course skills
        (22, 59),  # Video Editing - Video Editing

        # Animation Fundamentals course skills
        (23, 60),  # Animation - Animation

        # Voice Over Masterclass course skills
        (24, 61),  # Voice Over - Voice Over

        # Project Management Professional course skills
        (25, 66),  # PMP - Project Management

        # Business Analysis Fundamentals course skills
        (26, 67),  # BA - Business Analysis

        # Virtual Assistant course skills
        (27, 68)  # VA - Virtual Assistance
    ]

    for course_id, skill_id in course_skills:
        cursor.execute("INSERT INTO course_skills (course_id, skill_id) VALUES (?, ?)", (course_id, skill_id))

    conn.commit()


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, email, password, full_name=None, bio=None):
    """Create a new user in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        password_hash = hash_password(password)
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO users (username, email, password_hash, full_name, bio, join_date)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (username, email, password_hash, full_name, bio, join_date))

        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def validate_login(username, password):
    """Validate user login credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user['password_hash'] == hash_password(password):
        return user['id']
    return None


def get_user_by_id(user_id):
    """Get user details by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email, full_name, bio, join_date, profile_picture FROM users WHERE id = ?",
                   (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None


def get_skills():
    """Get all skills from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category FROM skills ORDER BY category, name")
    skills = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return skills


def get_skills_by_category():
    """Get all skills organized by category"""
    skills = get_skills()
    skills_by_category = {}

    for skill in skills:
        category = skill['category']
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    return skills_by_category


def get_user_skills(user_id):
    """Get skills for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT s.id, s.name, s.category, us.proficiency_level, us.years_experience
                   FROM skills s
                            JOIN user_skills us ON s.id = us.skill_id
                   WHERE us.user_id = ?
                   ORDER BY s.category, s.name
                   """, (user_id,))

    user_skills = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return user_skills


def update_user_skills(user_id, skills_data):
    """Update user skills

    Args:
        user_id (int): The user ID
        skills_data (list): List of dicts with keys: skill_id, proficiency_level, years_experience
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, delete existing skills for the user
    cursor.execute("DELETE FROM user_skills WHERE user_id = ?", (user_id,))

    # Then, insert the new skills
    for skill in skills_data:
        cursor.execute("""
                       INSERT INTO user_skills (user_id, skill_id, proficiency_level, years_experience)
                       VALUES (?, ?, ?, ?)
                       """, (user_id, skill['skill_id'], skill['proficiency_level'], skill['years_experience']))

    conn.commit()
    conn.close()


def create_gig(user_id, title, description, price_min, price_max, duration, skill_ids):
    """Create a new gig

    Args:
        user_id (int): User ID of the gig creator
        title (str): Title of the gig
        description (str): Description of the gig
        price_min (float): Minimum price
        price_max (float): Maximum price
        duration (str): Expected duration (e.g., "1 day", "1 week")
        skill_ids (list): List of skill IDs associated with the gig

    Returns:
        int: The ID of the created gig, or None if creation failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO gigs (user_id, title, description, price_min, price_max, duration, created_at,
                                         status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (user_id, title, description, price_min, price_max, duration, created_at, "active"))

        gig_id = cursor.lastrowid

        # Insert gig skills
        for skill_id in skill_ids:
            cursor.execute("INSERT INTO gig_skills (gig_id, skill_id) VALUES (?, ?)", (gig_id, skill_id))

        conn.commit()
        return gig_id
    except sqlite3.Error:
        conn.rollback()
        return None
    finally:
        conn.close()


def get_gigs(limit=10, offset=0, user_id=None, skill_ids=None):
    """Get gigs with optional filtering

    Args:
        limit (int): Maximum number of gigs to return
        offset (int): Offset for pagination
        user_id (int, optional): Filter by user ID
        skill_ids (list, optional): Filter by skill IDs

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
                     JOIN users u ON g.user_id = u.id \
            """

    params = []
    where_clauses = []

    if user_id:
        where_clauses.append("g.user_id = ?")
        params.append(user_id)

    if skill_ids:
        query += """
            JOIN gig_skills gs ON g.id = gs.gig_id
        """
        where_clauses.append("gs.skill_id IN ({})".format(','.join(['?'] * len(skill_ids))))
        params.extend(skill_ids)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " GROUP BY g.id ORDER BY g.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
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


def get_recommended_gigs(user_id, limit=10):
    """Get recommended gigs based on user skills

    Args:
        user_id (int): User ID
        limit (int): Maximum number of gigs to recommend

    Returns:
        list: List of recommended gig dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user's skill IDs
    cursor.execute("SELECT skill_id FROM user_skills WHERE user_id = ?", (user_id,))
    user_skill_ids = [row[0] for row in cursor.fetchall()]

    if not user_skill_ids:
        conn.close()
        return []

    # Get gigs that match the user's skills, excluding their own gigs
    query = """
        SELECT g.id, g.user_id, g.title, g.description, g.price_min, g.price_max, 
               g.duration, g.created_at, g.status, u.username,
               COUNT(DISTINCT gs.skill_id) AS matching_skills
        FROM gigs g
        JOIN users u ON g.user_id = u.id
        JOIN gig_skills gs ON g.id = gs.gig_id
        WHERE gs.skill_id IN ({}) AND g.user_id != ?
        GROUP BY g.id
        ORDER BY matching_skills DESC, g.created_at DESC
        LIMIT ?
    """.format(','.join(['?'] * len(user_skill_ids)))

    params = user_skill_ids + [user_id, limit]
    cursor.execute(query, params)
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


def get_recommended_courses(user_id, limit=10):
    """Get recommended courses based on user skills

    Args:
        user_id (int): User ID
        limit (int): Maximum number of courses to recommend

    Returns:
        list: List of recommended course dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user's skills
    cursor.execute("""
                   SELECT us.skill_id, us.proficiency_level
                   FROM user_skills us
                   WHERE us.user_id = ?
                   """, (user_id,))
    user_skills = cursor.fetchall()

    if not user_skills:
        conn.close()
        return []

    # Get user's skill IDs
    user_skill_ids = [skill[0] for skill in user_skills]

    # Get courses that match the user's skills or are related to user's field
    query = """
        SELECT c.id, c.title, c.description, c.provider, c.url, c.difficulty_level, c.duration, c.price,
               COUNT(DISTINCT cs.skill_id) AS matching_skills
        FROM courses c
        JOIN course_skills cs ON c.id = cs.course_id
        WHERE cs.skill_id IN ({})
        GROUP BY c.id
        ORDER BY 
            CASE 
                WHEN c.difficulty_level = 'Beginner' THEN 1
                WHEN c.difficulty_level = 'Intermediate' THEN 2
                WHEN c.difficulty_level = 'Advanced' THEN 3
                ELSE 4
            END,
            matching_skills DESC
        LIMIT ?
    """.format(','.join(['?'] * len(user_skill_ids)))

    params = user_skill_ids + [limit]
    cursor.execute(query, params)
    courses = [dict(row) for row in cursor.fetchall()]

    # Get skills for each course
    for course in courses:
        cursor.execute("""
                       SELECT s.id, s.name, s.category
                       FROM skills s
                                JOIN course_skills cs ON s.id = cs.skill_id
                       WHERE cs.course_id = ?
                       """, (course['id'],))
        course['skills'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return courses


def create_post(user_id, content, image_url=None):
    """Create a new post

    Args:
        user_id (int): User ID of the post creator
        content (str): Content of the post
        image_url (str, optional): URL of an image for the post

    Returns:
        int: The ID of the created post, or None if creation failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO posts (user_id, content, created_at, image_url)
                       VALUES (?, ?, ?, ?)
                       """, (user_id, content, created_at, image_url))

        post_id = cursor.lastrowid
        conn.commit()
        return post_id
    except sqlite3.Error:
        conn.rollback()
        return None
    finally:
        conn.close()


def get_posts(limit=10, offset=0, user_id=None):
    """Get posts with optional filtering

    Args:
        limit (int): Maximum number of posts to return
        offset (int): Offset for pagination
        user_id (int, optional): Filter by user ID

    Returns:
        list: List of post dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
            SELECT p.id, p.user_id, p.content, p.created_at, p.image_url, u.username
            FROM posts p
                     JOIN users u ON p.user_id = u.id \
            """

    params = []
    if user_id:
        query += " WHERE p.user_id = ?"
        params.append(user_id)

    query += " ORDER BY p.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    posts = [dict(row) for row in cursor.fetchall()]

    # Get like count for each post
    for post in posts:
        cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id = ?", (post['id'],))
        post['like_count'] = cursor.fetchone()[0]

        # Get comments for each post
        cursor.execute("""
                       SELECT c.id, c.user_id, c.content, c.created_at, u.username
                       FROM comments c
                                JOIN users u ON c.user_id = u.id
                       WHERE c.post_id = ?
                       ORDER BY c.created_at ASC
                       """, (post['id'],))
        post['comments'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return posts


def like_post(user_id, post_id):
    """Like a post

    Args:
        user_id (int): User ID
        post_id (int): Post ID

    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO likes (user_id, post_id, created_at)
                       VALUES (?, ?, ?)
                       """, (user_id, post_id, created_at))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # User already liked the post
        return False
    finally:
        conn.close()


def unlike_post(user_id, post_id):
    """Unlike a post

    Args:
        user_id (int): User ID
        post_id (int): Post ID

    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))

    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def add_comment(user_id, post_id, content):
    """Add a comment to a post

    Args:
        user_id (int): User ID
        post_id (int): Post ID
        content (str): Comment content

    Returns:
        int: The ID of the created comment, or None if creation failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                       INSERT INTO comments (user_id, post_id, content, created_at)
                       VALUES (?, ?, ?, ?)
                       """, (user_id, post_id, content, created_at))

        comment_id = cursor.lastrowid
        conn.commit()
        return comment_id
    except sqlite3.Error:
        conn.rollback()
        return None
    finally:
        conn.close()


def has_user_liked_post(user_id, post_id):
    """Check if a user has liked a post

    Args:
        user_id (int): User ID
        post_id (int): Post ID

    Returns:
        bool: True if the user has liked the post, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
    result = cursor.fetchone() is not None

    conn.close()
    return result


# If this file is run directly, initialize the database
if __name__ == "__main__":
    init_db()