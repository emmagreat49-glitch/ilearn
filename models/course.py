"""
models/course.py
Course and lesson model helper functions for iLEARN.
"""


def get_all_courses(conn):
    """Return all courses."""
    return conn.execute("SELECT * FROM courses").fetchall()


def get_course(conn, course_id: int):
    """Return a single course by ID."""
    return conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()


def get_lessons_for_course(conn, course_id: int):
    """Return all lessons for a course, ordered."""
    return conn.execute(
        "SELECT * FROM lessons WHERE course_id=? ORDER BY lesson_order", (course_id,)
    ).fetchall()


def get_lesson(conn, lesson_id: int):
    """Return a single lesson by ID."""
    return conn.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,)).fetchone()


def get_quiz_for_lesson(conn, lesson_id: int):
    """Return all quiz questions for a lesson."""
    return conn.execute("SELECT * FROM quiz WHERE lesson_id=?", (lesson_id,)).fetchall()


def get_course_progress(conn, course_id: int, user_id: int) -> dict:
    """
    Return progress stats for a user in a course.
    Returns: { total, completed, percent }
    """
    total = conn.execute(
        "SELECT COUNT(*) as cnt FROM lessons WHERE course_id=?", (course_id,)
    ).fetchone()["cnt"]

    completed = conn.execute(
        """SELECT COUNT(*) as cnt FROM progress p
           JOIN lessons l ON p.lesson_id = l.id
           WHERE l.course_id=? AND p.user_id=? AND p.completed=1""",
        (course_id, user_id)
    ).fetchone()["cnt"]

    return {
        "total": total,
        "completed": completed,
        "percent": int(completed / total * 100) if total > 0 else 0
    }
