"""
iLEARN — Course Seed Package
Each module contains one course's seed function.
"""
from .data_analysis_course    import seed_data_analysis
from .web_development_course  import seed_web_development
from .ai_fundamentals_course  import seed_ai_fundamentals
from .digital_skills_course   import seed_digital_skills
from .career_paths_course     import seed_career_paths


def seed_all(conn, c):
    """Seed all courses into the database. Called once on first run."""
    seed_data_analysis(conn, c)
    seed_web_development(conn, c)
    seed_ai_fundamentals(conn, c)
    seed_digital_skills(conn, c)
    seed_career_paths(conn, c)
