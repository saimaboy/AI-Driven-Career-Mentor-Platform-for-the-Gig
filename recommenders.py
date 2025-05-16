# freelance_mongo/recommenders.py

import database as db

# Map user proficiency → allowed course difficulty levels
_PROFICIENCY_TO_DIFFICULTY = {
    "Beginner":     ["Beginner"],
    "Intermediate": ["Beginner", "Intermediate"],
    "Advanced":     ["Intermediate", "Advanced"],
    "Expert":       ["Advanced", "Expert"],
}

# Difficulty sort order
_DIFFICULTY_ORDER = {
    "Beginner":     1,
    "Intermediate": 2,
    "Advanced":     3,
    "Expert":       4,
}

def recommend_gigs(user_id, limit=5):
    """Recommend gigs for a user based on their skills

    Args:
        user_id (int): User ID
        limit (int): Maximum number of gigs to recommend

    Returns:
        list: List of recommended gig dictionaries
    """
    # Get the user's skills
    user_skills = db.get_user_skills(user_id)

    if not user_skills:
        return []

    # Get recommended gigs
    recommended_gigs = db.get_recommended_gigs(user_id, limit)

    # Sort by number of matching skills
    return recommended_gigs

def recommend_courses(user_id, limit=10):
    """Recommend courses based on the user's existing skills and proficiency."""
    user_skills = db.get_user_skills(user_id)
    if not user_skills:
        return []

    # 1) Gather their skill IDs and allowed difficulties
    user_skill_ids = [s["id"] for s in user_skills]
    allowed_diffs = set()
    for s in user_skills:
        allowed_diffs.update(_PROFICIENCY_TO_DIFFICULTY.get(s["proficiency_level"], []))
    if not allowed_diffs:
        allowed_diffs = {"Beginner"}

    # 2) Build SQL with placeholders
    skill_ph = ",".join("?" * len(user_skill_ids))
    diff_ph  = ",".join("?" * len(allowed_diffs))
    sql = f"""
    SELECT
      c.id,
      c.title,
      c.description,
      c.provider,
      c.url,
      c.difficulty_level,
      c.duration,
      c.price,
      COUNT(DISTINCT cs.skill_id) AS matching_skills
    FROM courses c
    JOIN course_skills cs ON c.id = cs.course_id
    WHERE cs.skill_id IN ({skill_ph})
      AND c.difficulty_level IN ({diff_ph})
    GROUP BY c.id
    ORDER BY
      matching_skills DESC,
      CASE c.difficulty_level
        WHEN 'Beginner' THEN 1
        WHEN 'Intermediate' THEN 2
        WHEN 'Advanced' THEN 3
        WHEN 'Expert' THEN 4
        ELSE 5
      END ASC
    LIMIT ?
    """

    params = user_skill_ids + list(allowed_diffs) + [limit]
    conn  = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    courses = [dict(row) for row in cursor.fetchall()]

    # 3) Attach each course's skill list
    for course in courses:
        cursor.execute("""
          SELECT s.id, s.name, s.category
          FROM skills s
          JOIN course_skills cs ON s.id = cs.skill_id
          WHERE cs.course_id = ?
        """, (course["id"],))
        course["skills"] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return courses


def get_skill_gap_courses(user_id, limit=5):
    """Recommend courses teaching skills in the user's own categories they don't yet have."""
    user_skills = db.get_user_skills(user_id)
    if not user_skills:
        return []

    user_skill_ids = {s["id"] for s in user_skills}
    user_categories = {s["category"] for s in user_skills}

    conn = db.get_db_connection()
    cursor = conn.cursor()

    # 1) Find all skill IDs in courses that are in the user's categories
    cat_ph = ",".join("?" * len(user_categories))
    cursor.execute(f"""
      SELECT DISTINCT s.id
      FROM skills s
      JOIN course_skills cs ON s.id = cs.skill_id
      WHERE s.category IN ({cat_ph})
    """, tuple(user_categories))
    cat_skill_ids = {row[0] for row in cursor.fetchall()}

    # 2) Remove skills the user already has
    missing_skills = [sid for sid in cat_skill_ids if sid not in user_skill_ids]

    gap_courses = []
    seen_courses = set()

    # 3) For each missing skill, pick the easiest (beginner-first) course
    for sid in missing_skills:
        cursor.execute(f"""
          SELECT
            c.id,
            c.title,
            c.description,
            c.provider,
            c.url,
            c.difficulty_level,
            c.duration,
            c.price
          FROM courses c
          JOIN course_skills cs ON c.id = cs.course_id
          WHERE cs.skill_id = ?
          ORDER BY
            CASE c.difficulty_level
              WHEN 'Beginner' THEN 1
              WHEN 'Intermediate' THEN 2
              WHEN 'Advanced' THEN 3
              WHEN 'Expert' THEN 4
              ELSE 5
            END ASC
          LIMIT 1
        """, (sid,))
        row = cursor.fetchone()
        if not row:
            continue

        course = dict(row)
        if course["id"] in seen_courses:
            continue
        seen_courses.add(course["id"])

        # attach its skills
        cursor.execute("""
          SELECT s.id, s.name, s.category
          FROM skills s
          JOIN course_skills cs ON s.id = cs.skill_id
          WHERE cs.course_id = ?
        """, (course["id"],))
        course["skills"] = [dict(r) for r in cursor.fetchall()]

        gap_courses.append(course)
        if len(gap_courses) >= limit:
            break

    conn.close()
    return gap_courses
