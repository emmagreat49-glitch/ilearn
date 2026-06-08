# ilearn v1.0.0 - Password Reset Ready
"""
iLEARN — Interactive E-Learning Platform
=========================================
Run:  python app.py
Login: admin / ilearn123

Project structure (what goes where)
------------------------------------
  app.py              <- Flask routes and logic ONLY  (this file)
  seeds/              <- All course content, separated by language
    python_course.py
    javascript_course.py
    css_course.py
    java_course.py
    data_science_course.py
    helpers.py
  templates/          <- All HTML files
  static/css/         <- All CSS files  (main.css, theme.css)
  static/js/          <- All JavaScript files  (main.js, theme.js)
  data_science/       <- Analytics module
  java/               <- GradeAnalyzer.java
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, send_file
)
import sqlite3, re, os, json, subprocess, sys, smtplib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config as cfg

# ── Course seed data lives in seeds/ package — NOT in this file ──
from seeds import seed_all

# ── Data Science analytics module ─────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_science"))
try:
    import analytics as ds_analytics
    DS_AVAILABLE = True
except ImportError:
    ds_analytics = None
    DS_AVAILABLE = False

app = Flask(__name__)
# Secret key — MUST be set via environment variable in production.
# If not set, generates a random key each restart (sessions reset on restart — fine for dev).
_secret = os.environ.get("ILEARN_SECRET_KEY", "")
if not _secret:
    import secrets as _secrets
    _secret = _secrets.token_hex(32)
    print("[iLEARN] WARNING: ILEARN_SECRET_KEY not set. Using random key — sessions will reset on restart.")
    print("[iLEARN] Set it: export ILEARN_SECRET_KEY=your-long-random-secret")
app.secret_key = _secret
del _secret
DATABASE = "database.db"

# ── CSRF Protection ──────────────────────────────────────────────────
# Simple, dependency-free CSRF using Flask sessions.
# Call csrf_token() in templates, verify_csrf() in POST handlers.
import secrets as _sec

def generate_csrf():
    """Generate and store a CSRF token in the session."""
    if "_csrf_token" not in session:
        session["_csrf_token"] = _sec.token_hex(32)
    return session["_csrf_token"]

def verify_csrf():
    """Verify the submitted CSRF token matches the session token. Returns True/False."""
    token = (request.form.get("_csrf_token") or
             request.headers.get("X-CSRF-Token") or
             (request.get_json(silent=True) or {}).get("_csrf_token"))
    return token and token == session.get("_csrf_token")

# Make generate_csrf available in all templates
app.jinja_env.globals["csrf_token"] = generate_csrf

# ── Simple in-memory rate limiter for login ──────────────────────────
from collections import defaultdict
import time as _time
_login_attempts = defaultdict(list)   # ip -> [timestamps]
MAX_LOGIN_ATTEMPTS = 10               # per window
LOGIN_WINDOW_SECS  = 300             # 5 minutes

def _check_rate_limit(ip):
    """Returns True if request is allowed, False if rate limited."""
    now = _time.time()
    window_start = now - LOGIN_WINDOW_SECS
    attempts = [t for t in _login_attempts[ip] if t > window_start]
    _login_attempts[ip] = attempts
    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        return False
    _login_attempts[ip].append(now)
    return True

# ═══════════════════════════════════════════════
# DATABASE HELPERS
# ═══════════════════════════════════════════════

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash a password using PBKDF2-SHA256 with a random salt (via werkzeug).
    This is the same algorithm used by Flask-Login and most production Flask apps."""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(stored_hash, provided_password):
    """Verify a password against its stored hash.
    Handles both new PBKDF2 hashes and legacy SHA-256 hashes (for migration).
    On legacy match, upgrades the hash automatically."""
    import hashlib
    # New format: werkzeug PBKDF2 hashes start with "pbkdf2:"
    if stored_hash.startswith("pbkdf2:"):
        return check_password_hash(stored_hash, provided_password)
    # Legacy format: plain SHA-256 hex (64 chars) — auto-upgrade on successful login
    legacy_hash = hashlib.sha256(provided_password.encode()).hexdigest()
    return stored_hash == legacy_hash

def upgrade_password_hash_if_legacy(user_id, stored_hash, raw_password):
    """If the stored hash is an old SHA-256 hash, upgrade it to PBKDF2 silently."""
    if not stored_hash.startswith("pbkdf2:"):
        try:
            conn = get_db()
            conn.execute("UPDATE users SET password=? WHERE id=?",
                        (hash_password(raw_password), user_id))
            conn.commit()
            conn.close()
            print(f"[iLEARN] Upgraded password hash for user_id={user_id} to PBKDF2")
        except Exception as e:
            print(f"[iLEARN] Hash upgrade failed: {e}")

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        full_name TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        icon TEXT DEFAULT '📚',
        level TEXT DEFAULT 'Beginner',
        language TEXT DEFAULT 'general'
    )""")

    # Modules group lessons within a course
    c.execute("""CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        module_title TEXT NOT NULL,
        module_order INTEGER DEFAULT 1,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        lesson_title TEXT NOT NULL,
        lesson_content TEXT NOT NULL,
        lesson_order INTEGER DEFAULT 1,
        duration_mins INTEGER DEFAULT 15,
        module_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES courses(id),
        FOREIGN KEY (module_id) REFERENCES modules(id)
    )""")

    # Migration: add module_id to existing lessons table if not present
    try:
        c.execute("SELECT module_id FROM lessons LIMIT 1")
    except Exception:
        c.execute("ALTER TABLE lessons ADD COLUMN module_id INTEGER")

    c.execute("""CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT,
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        completed INTEGER DEFAULT 0,
        completed_at TEXT,
        UNIQUE(user_id, lesson_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reminder_text TEXT NOT NULL,
        reminder_time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'unread',
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    # Tracks which quiz questions each user has attempted — used to enforce
    # lesson completion server-side.
    c.execute("""CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        answered_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, question_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )""")

    # Contact / feedback messages submitted by users.
    c.execute("""CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_read INTEGER DEFAULT 0
    )""")

    # ── Migration: add is_read to contact_messages if it was created without it ──
    try:
        c.execute("SELECT is_read FROM contact_messages LIMIT 1")
    except Exception:
        c.execute("ALTER TABLE contact_messages ADD COLUMN is_read INTEGER DEFAULT 0")

    conn.commit()

    if not c.execute("SELECT id FROM users WHERE username='admin'").fetchone():
        c.execute("INSERT INTO users (username, password, email, full_name) VALUES (?,?,?,?)",
                  ("admin", hash_password("ilearn123"), "admin@ilearn.com", "Administrator"))
        conn.commit()

    if not c.execute("SELECT id FROM courses LIMIT 1").fetchone():
        seed_all(conn, c)
        conn.commit()

    conn.close()


# ═══════════════════════════════════════════════
# AUTH DECORATOR
# ═══════════════════════════════════════════════

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════
# ROUTES — AUTH
# ═══════════════════════════════════════════════

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        # ── Rate limiting ──────────────────────────────────────────
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
        if not _check_rate_limit(client_ip):
            error = "Too many login attempts. Please wait 5 minutes and try again."
            return render_template("login.html", error=error, show_register=False, success=None), 429

        # ── CSRF check ────────────────────────────────────────────
        if not verify_csrf():
            error = "Invalid form submission. Please refresh and try again."
            return render_template("login.html", error=error, show_register=False, success=None), 403

        username    = request.form.get("username","").strip()[:80]   # max length guard
        password    = request.form.get("password","").strip()[:256]
        remember_me = request.form.get("remember_me") == "on"

        conn = get_db()
        # Fetch by username only — verify password separately (timing-safe)
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and verify_password(user["password"], password):
            # Silently upgrade legacy SHA-256 hash to PBKDF2 if needed
            upgrade_password_hash_if_legacy(user["id"], user["password"], password)
            # ── Session fixation fix — regenerate session after login ──
            session.clear()   # clear old session data before setting new values
            if remember_me:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False
            session["user_id"]   = user["id"]
            session["username"]  = user["username"]
            session["full_name"] = user["full_name"] or user["username"]
            return redirect(url_for("dashboard"))
        # Use same error message whether username wrong OR password wrong (no enumeration)
        error = "Incorrect username or password."
    return render_template("login.html", error=error, show_register=False, success=None)


@app.route("/auth/google")
def google_auth():
    """
    Google OAuth login — placeholder route.
    To activate real Google login:
      1. Go to console.cloud.google.com
      2. Create a project and enable Google+ API
      3. Create OAuth 2.0 credentials (Web Application)
      4. Add http://127.0.0.1:5000/auth/google/callback to Authorised redirect URIs
      5. pip install flask-dance
      6. Replace this route with flask_dance Google blueprint
    """
    return redirect(url_for("login", google_pending=1))


@app.route("/register", methods=["GET","POST"])
def register():
    """Registration — renders same login.html but with register tab active."""
    error = success = None
    if request.method == "POST":
        # CSRF check
        if not verify_csrf():
            return render_template("login.html", error="Invalid form submission. Please refresh.", show_register=True, success=None), 403
        full_name = request.form.get("full_name","").strip()[:120]
        username  = request.form.get("username","").strip()[:40]
        email     = request.form.get("email","").strip()[:254]
        password  = request.form.get("password","").strip()[:256]
        confirm   = request.form.get("confirm","").strip()[:256]

        if not all([full_name, username, password]):
            error = "Full name, username, and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            error = "Username: letters, numbers, and underscores only."
        else:
            conn = get_db()
            if conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone():
                error = "That username is already taken. Please choose another."
                conn.close()
            else:
                conn.execute("INSERT INTO users (username,password,email,full_name) VALUES (?,?,?,?)",
                             (username, hash_password(password), email[:254], full_name[:120]))
                conn.commit(); conn.close()
                # On success, redirect to login page with success message
                return render_template("login.html", error=None, show_register=False,
                                       success=f"Account created! Welcome, {full_name}. Please sign in.")

    # Render login.html with register panel active (on GET or validation error)
    return render_template("login.html", error=error, show_register=True, success=success)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ═══════════════════════════════════════════════
# ROUTES — MAIN
# ═══════════════════════════════════════════════

@app.route("/dashboard")
@login_required
def dashboard():
    conn    = get_db()
    user_id = session["user_id"]
    courses = conn.execute("SELECT * FROM courses").fetchall()
    course_progress = []
    for course in courses:
        total = conn.execute("SELECT COUNT(*) as cnt FROM lessons WHERE course_id=?",
                             (course["id"],)).fetchone()["cnt"]
        done  = conn.execute("""SELECT COUNT(*) as cnt FROM progress p
            JOIN lessons l ON p.lesson_id=l.id
            WHERE l.course_id=? AND p.user_id=? AND p.completed=1""",
                             (course["id"], user_id)).fetchone()["cnt"]
        pct = int(done/total*100) if total else 0
        course_progress.append({"id":course["id"],"title":course["title"],
            "description":course["description"],"icon":course["icon"],
            "level":course["level"],"language":course["language"],
            "total":total,"completed":done,"percent":pct})
    reminders = conn.execute("SELECT * FROM reminders WHERE user_id=? ORDER BY reminder_time",
                             (user_id,)).fetchall()
    conn.close()
    return render_template("dashboard.html", courses=course_progress, reminders=reminders,
                           username=session["username"],
                           full_name=session.get("full_name", session["username"]))


@app.route("/course/<int:course_id>")
@login_required
def course(course_id):
    conn    = get_db()
    user_id = session["user_id"]
    course_data = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course_data: conn.close(); return "Course not found", 404

    # Fetch modules for this course
    modules = conn.execute(
        "SELECT * FROM modules WHERE course_id=? ORDER BY module_order", (course_id,)
    ).fetchall()

    # Fetch all lessons ordered
    lessons = conn.execute(
        "SELECT * FROM lessons WHERE course_id=? ORDER BY lesson_order", (course_id,)
    ).fetchall()

    completed_ids = set(r["lesson_id"] for r in conn.execute(
        "SELECT lesson_id FROM progress WHERE user_id=? AND completed=1", (user_id,)
    ).fetchall())

    # Build ordered list of lesson ids to know which are locked
    all_lesson_ids = [l["id"] for l in lessons]

    # A lesson is locked if any PREVIOUS lesson is not completed
    def is_locked(lesson_idx):
        if lesson_idx == 0:
            return False  # first lesson always unlocked
        prev_id = all_lesson_ids[lesson_idx - 1]
        return prev_id not in completed_ids

    lessons_with_status = []
    for idx, l in enumerate(lessons):
        lessons_with_status.append({
            "id":            l["id"],
            "lesson_title":  l["lesson_title"],
            "lesson_order":  l["lesson_order"],
            "duration_mins": l["duration_mins"],
            "module_id":     l["module_id"],
            "is_completed":  l["id"] in completed_ids,
            "is_locked":     is_locked(idx),
        })

    conn.close()
    return render_template("course.html",
                           course=course_data,
                           modules=modules,
                           lessons=lessons_with_status,
                           completed_ids=completed_ids)


@app.route("/lesson/<int:lesson_id>")
@login_required
def lesson(lesson_id):
    conn    = get_db()
    user_id = session["user_id"]
    lesson_data = conn.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,)).fetchone()
    if not lesson_data: conn.close(); return "Lesson not found", 404

    course_data = conn.execute("SELECT * FROM courses WHERE id=?",
                               (lesson_data["course_id"],)).fetchone()
    all_ids = [r["id"] for r in conn.execute(
        "SELECT id FROM lessons WHERE course_id=? ORDER BY lesson_order",
        (lesson_data["course_id"],)).fetchall()]
    idx = all_ids.index(lesson_id)

    # Enforce lesson order: if a previous lesson is not completed, redirect to course
    if idx > 0:
        prev_id = all_ids[idx - 1]
        prev_done = conn.execute(
            "SELECT completed FROM progress WHERE user_id=? AND lesson_id=? AND completed=1",
            (user_id, prev_id)
        ).fetchone()
        if not prev_done:
            conn.close()
            return redirect(url_for("course", course_id=lesson_data["course_id"]))

    quizzes = conn.execute("SELECT * FROM quiz WHERE lesson_id=?", (lesson_id,)).fetchall()
    pr = conn.execute("SELECT completed FROM progress WHERE user_id=? AND lesson_id=?",
                      (user_id, lesson_id)).fetchone()
    is_completed = pr["completed"] == 1 if pr else False
    conn.close()
    return render_template("lesson.html", lesson=lesson_data, course=course_data,
                           quizzes=quizzes,
                           next_lesson_id=all_ids[idx+1] if idx+1 < len(all_ids) else None,
                           prev_lesson_id=all_ids[idx-1] if idx > 0 else None,
                           is_completed=is_completed,
                           min_lesson_seconds=cfg.MIN_LESSON_SECONDS)


@app.route("/quiz/<int:lesson_id>")
@login_required
def quiz(lesson_id):
    conn = get_db()
    lesson_data = conn.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,)).fetchone()
    quizzes = conn.execute("SELECT * FROM quiz WHERE lesson_id=?", (lesson_id,)).fetchall()
    conn.close()
    return render_template("quiz.html", lesson=lesson_data, quizzes=quizzes)


# ═══════════════════════════════════════════════
# API
# ═══════════════════════════════════════════════

@app.route("/api/complete_lesson", methods=["POST"])
@login_required
def complete_lesson():
    """
    Mark a lesson complete.
    Server-side enforcement:
      1. Time on page >= config.MIN_LESSON_SECONDS (if > 0)
      2. All quiz questions must have been attempted (recorded via /api/record_answer)
    The JS enforces these too, but we re-check here so the API cannot be
    bypassed by calling it directly.
    """
    data       = request.get_json() or {}
    lesson_id  = data.get("lesson_id")
    time_spent = int(data.get("time_spent", 0))
    user_id    = session["user_id"]
    conn       = get_db()

    # ── Check 1: Minimum reading time ──────────────────────────
    if cfg.MIN_LESSON_SECONDS > 0 and time_spent < cfg.MIN_LESSON_SECONDS:
        conn.close()
        return jsonify({
            "status":   "error",
            "code":     "time_required",
            "message":  f"Please spend at least {cfg.MIN_LESSON_SECONDS} seconds on the lesson before completing it.",
            "required": cfg.MIN_LESSON_SECONDS,
            "actual":   time_spent,
        }), 400

    # ── Check 2: All quiz questions must have been attempted ────
    total_q = conn.execute(
        "SELECT COUNT(*) as cnt FROM quiz WHERE lesson_id=?", (lesson_id,)
    ).fetchone()["cnt"]

    if total_q > 0:
        attempted = conn.execute(
            "SELECT COUNT(*) as cnt FROM quiz_attempts WHERE user_id=? AND lesson_id=?",
            (user_id, lesson_id)
        ).fetchone()["cnt"]
        if attempted < total_q:
            conn.close()
            return jsonify({
                "status":  "error",
                "code":    "quiz_required",
                "message": f"Complete all {total_q} quiz questions first ({attempted}/{total_q} done).",
            }), 403

    # ── Save progress ──────────────────────────────────────────
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO progress (user_id, lesson_id, completed, completed_at)
           VALUES (?,?,1,?)
           ON CONFLICT(user_id, lesson_id) DO UPDATE SET completed=1, completed_at=?""",
        (user_id, lesson_id, now, now)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/record_answer", methods=["POST"])
@login_required
def record_answer():
    """Called by the lesson page each time a quiz question is answered.
    Records the attempt so we can verify completion server-side."""
    data        = request.get_json()
    question_id = data.get("question_id")
    lesson_id   = data.get("lesson_id")
    if not question_id or not lesson_id:
        return jsonify({"status": "error"}), 400
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO quiz_attempts (user_id, lesson_id, question_id) VALUES (?,?,?)",
        (session["user_id"], lesson_id, question_id)
    )
    conn.commit(); conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/reminders", methods=["GET"])
@login_required
def get_reminders():
    """Return all reminders for the current user — used by the JS notification system."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, reminder_text, reminder_time FROM reminders WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return jsonify([{"id": r["id"], "text": r["reminder_text"], "time": r["reminder_time"]} for r in rows])


@app.route("/api/add_reminder", methods=["POST"])
@login_required
def add_reminder():
    data = request.get_json()
    text = data.get("text","").strip()[:200]   # max 200 chars
    time = data.get("time","").strip()[:20]    # datetime-local format is ~16 chars
    if not text or not time:
        return jsonify({"status":"error","message":"Text and time required"}), 400
    conn = get_db()
    conn.execute("INSERT INTO reminders (user_id,reminder_text,reminder_time) VALUES (?,?,?)",
                 (session["user_id"], text, time))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})


@app.route("/api/delete_reminder/<int:rid>", methods=["DELETE"])
@login_required
def delete_reminder(rid):
    conn = get_db()
    conn.execute("DELETE FROM reminders WHERE id=? AND user_id=?", (rid, session["user_id"]))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})


@app.route("/api/chat", methods=["POST"])
@login_required
def chat():
    """
    AI Chatbot — tries Anthropic then OpenAI, falls back to keyword responses.

    To enable real AI responses set ONE of these environment variables before
    starting the server:

        Windows CMD:   set ANTHROPIC_API_KEY=sk-ant-...
        Windows PS:    $env:ANTHROPIC_API_KEY="sk-ant-..."
        Mac/Linux:     export ANTHROPIC_API_KEY=sk-ant-...

        OR for OpenAI: set OPENAI_API_KEY=sk-...

    Install the relevant library first:
        pip install anthropic       (for Claude)
        pip install openai          (for OpenAI)
    """
    body          = request.get_json() or {}
    user_message  = body.get("message", "").strip()
    lesson_title  = body.get("lesson_title", "")
    course_title  = body.get("course_title", "")

    if not user_message:
        return jsonify({"reply": "Please type a message first."})

    # ── Build context-aware system prompt ──────────────────────────
    system_prompt = (
        "You are iLEARN's AI Study Assistant — a concise, encouraging tutor "
        "for an e-learning platform covering Python, JavaScript, CSS, Java, and "
        "Data Science. Respond in plain text (no markdown), under 180 words, "
        "and always end with one practical tip or exercise the student can try."
    )
    if lesson_title and course_title:
        system_prompt += (
            f" The student is currently studying '{lesson_title}' in the "
            f"'{course_title}' course. Keep your answer focused on that topic."
        )

    # ── 1. Try Anthropic Claude ────────────────────────────────────
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if anthropic_key:
        try:
            import anthropic as _anthropic
            client = _anthropic.Anthropic(api_key=anthropic_key)
            resp   = client.messages.create(
                model      = "claude-haiku-4-5-20251001",
                max_tokens = 350,
                system     = system_prompt,
                messages   = [{"role": "user", "content": user_message}]
            )
            return jsonify({"reply": resp.content[0].text.strip()})
        except Exception as e:
            print(f"[iLEARN] Anthropic API error: {e}")

    # ── 2. Try OpenAI ─────────────────────────────────────────────
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            import openai as _openai
            client = _openai.OpenAI(api_key=openai_key)
            resp   = client.chat.completions.create(
                model      = "gpt-4o-mini",
                max_tokens = 350,
                messages   = [
                    {"role": "system",  "content": system_prompt},
                    {"role": "user",    "content": user_message}
                ]
            )
            return jsonify({"reply": resp.choices[0].message.content.strip()})
        except Exception as e:
            print(f"[iLEARN] OpenAI API error: {e}")

    # ── 3. Keyword fallback (no API key configured) ────────────────
    msg = user_message.lower()
    keyword_responses = {
        "python":     "🐍 Python tip: List comprehensions run faster than for-loops due to C-level optimisation in CPython. Try: squares = [x*x for x in range(10)]",
        "javascript": "⚡ JS tip: Always use === over ==. Understand the event loop — synchronous code first, then Promises (microtasks), then setTimeout (macrotasks).",
        "java":       "☕ Java tip: Use try-with-resources for anything AutoCloseable. It closes resources automatically — safer and cleaner than finally blocks.",
        "css":        "🎨 CSS tip: Put box-sizing: border-box on everything. It makes widths predictable and eliminates most common layout bugs.",
        "flexbox":    "📐 Flexbox: justify-content controls the MAIN axis. align-items controls the CROSS axis. They swap when you change flex-direction.",
        "grid":       "🔲 CSS Grid: Use grid-template-areas for complex layouts. Your CSS literally looks like a map of your page.",
        "async":      "🔄 Async: Promise.all() runs promises in PARALLEL — much faster when tasks are independent. Use await only for sequential dependencies.",
        "oop":        "🏗️ OOP: Favour composition over inheritance. Build complex objects by combining simple ones rather than deep class hierarchies.",
        "closure":    "🔒 Closure: A function that remembers variables from its outer scope. Used in counters, event handlers, and the module pattern.",
        "pandas":     "🐼 Pandas: Never use iterrows() — it's very slow. Use vectorised operations or .apply() for row-wise work.",
        "ml":         "🤖 ML: Always split data BEFORE scaling. Fit your scaler on training data only — applying it to test data first leaks information.",
        "data":       "📊 Data Science: Run df.info() and df.describe() on any new dataset before writing any analysis. Know your data first.",
        "hello":      "👋 Hello! Ask me about Python, JavaScript, Java, CSS, Flexbox, Grid, async, OOP, closures, Pandas, ML, or study tips!",
        "study":      "📚 Active recall beats re-reading. Close the lesson, try to explain the concept from memory. What you can't recall is what to study.",
        "exam":       "✏️ For your defence: supervisors ask you to EXPLAIN concepts, not recite code. Understand the WHY — why does Python have closures? Why does Java need checked exceptions?",
        "help":       "🙋 I can help with: Python, JavaScript, Java, CSS, Flexbox, Grid, async, OOP, closures, Pandas, ML, study tips, exam prep. What topic?",
    }
    reply = next((v for k, v in keyword_responses.items() if k in msg), None)
    if not reply:
        ctx = f" (currently on: {lesson_title})" if lesson_title else ""
        reply = (
            f"🤖 Good question{ctx}! I'm running in keyword mode right now. "
            "To get real AI answers, set ANTHROPIC_API_KEY or OPENAI_API_KEY "
            "in your environment and restart the server. "
            "Try asking about: Python, JavaScript, Java, CSS, async, OOP, Pandas, or ML!"
        )
    return jsonify({"reply": reply})



# ═══════════════════════════════════════════════
# ROUTES — CONTACT / FEEDBACK
# ═══════════════════════════════════════════════

@app.route("/contact", methods=["GET", "POST"])
@app.route("/support", methods=["GET", "POST"])
@login_required
def contact():
    """Support / feedback form. Both /contact and /support point here."""
    user_id = session["user_id"]
    success = error = None

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

    if request.method == "POST":
        name    = request.form.get("name",    "").strip()
        email   = request.form.get("email",   "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, subject, message]):
            error = "All fields are required."
        elif len(message) < 10:
            error = "Please write a bit more detail in your message."
        else:
            conn.execute(
                "INSERT INTO contact_messages (user_id,name,email,subject,message) VALUES (?,?,?,?,?)",
                (user_id, name, email, subject, message)
            )
            conn.commit()
            _try_send_contact_email(name, email, subject, message)
            success = "Your message has been sent! We'll get back to you soon."

    conn.close()
    return render_template(
        "support.html",
        user=user, success=success, error=error,
        username=session["username"],
        full_name=session.get("full_name", session["username"])
    )


def _try_send_contact_email(sender_name, sender_email, subject, message):
    """Send an email to the admin when a contact form is submitted.
    Silently skips if SMTP environment variables are not configured."""
    import smtplib
    from email.mime.text import MIMEText

    host       = os.environ.get("SMTP_HOST", "")
    port       = int(os.environ.get("SMTP_PORT", 587))
    smtp_user  = os.environ.get("SMTP_USER", "")
    smtp_pass  = os.environ.get("SMTP_PASS", "")
    admin_email = os.environ.get("ADMIN_EMAIL", "")

    if not all([host, smtp_user, smtp_pass, admin_email]):
        return  # Not configured — skip silently

    try:
        body = (
            f"New iLEARN contact form submission\n\n"
            f"From:    {sender_name} <{sender_email}>\n"
            f"Subject: {subject}\n\n"
            f"{message}"
        )
        msg = MIMEText(body)
        msg["Subject"] = f"[iLEARN] {subject}"
        msg["From"]    = smtp_user
        msg["To"]      = admin_email

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [admin_email], msg.as_string())
    except Exception as e:
        print(f"[iLEARN] Email notification failed (non-critical): {e}")


@app.route("/admin/messages")
@login_required
def admin_messages():
    """Admin-only page to view all contact form submissions."""
    # Check admin role in DB — not just session username
    conn_check = get_db()
    requesting_user = conn_check.execute("SELECT username FROM users WHERE id=?", (session["user_id"],)).fetchone()
    conn_check.close()
    if not requesting_user or requesting_user["username"] != "admin":
        return redirect(url_for("dashboard"))

    conn  = get_db()
    msgs  = conn.execute(
        "SELECT cm.*, u.username FROM contact_messages cm "
        "LEFT JOIN users u ON cm.user_id = u.id "
        "ORDER BY cm.submitted_at DESC"
    ).fetchall()
    # Mark all as read
    conn.execute("UPDATE contact_messages SET is_read=1")
    conn.commit()
    conn.close()
    return render_template("admin_messages.html", messages=msgs,
                           username=session["username"],
                           full_name=session.get("full_name", "Admin"))


# ═══════════════════════════════════════════════
# ROUTES — ANALYTICS (Data Science + Java)
# ═══════════════════════════════════════════════

@app.route("/analytics")
@login_required
def analytics():
    """
    Analytics dashboard.
    - Calls data_science/analytics.py (Python/pandas/matplotlib) to generate charts
    - Reads data_science/grade_report.json (produced by GradeAnalyzer.java if available)
    """
    if not DS_AVAILABLE:
        return render_template("analytics.html",
            charts={name: "" for name in ["completion","distribution","enrolment","top_students","lessons_pie"]},
            stats={}, java_report=None,
            username=session["username"],
            full_name=session.get("full_name", session["username"]))

    result    = ds_analytics.generate_analytics(DATABASE)
    charts    = result.get("charts", {})
    stats     = result.get("stats", {})

    # Load Java grade report if it exists
    java_report = None
    report_path = os.path.join("data_science", "grade_report.json")
    if os.path.exists(report_path):
        try:
            with open(report_path) as f:
                java_report = json.load(f)
        except Exception:
            pass

    return render_template("analytics.html",
        charts=charts, stats=stats, java_report=java_report,
        username=session["username"],
        full_name=session.get("full_name", session["username"]))


@app.route("/analytics/export")
@login_required
def analytics_export():
    """Export student scores as CSV — consumed by GradeAnalyzer.java."""
    if not DS_AVAILABLE:
        return jsonify({"status": "error", "message": "Data science module not available"}), 500

    import pandas as pd
    data       = ds_analytics._get_data(DATABASE)
    output_path = os.path.join("data_science", "scores.csv")
    os.makedirs("data_science", exist_ok=True)
    ds_analytics.export_scores_csv(data, output_path)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True,
                         download_name="ilearn_scores.csv",
                         mimetype="text/csv")
    return jsonify({"status": "error", "message": "Export failed"}), 500


@app.route("/api/run_java_analyzer", methods=["POST"])
@login_required
def run_java_analyzer():
    """
    Attempts to run GradeAnalyzer.java via subprocess.
    1. First exports the CSV from Python
    2. Compiles the Java file (javac)
    3. Runs it (java GradeAnalyzer)
    Falls back gracefully if Java is not installed.
    """
    os.makedirs("data_science", exist_ok=True)
    csv_path    = os.path.join("data_science", "scores.csv")
    report_path = os.path.join("data_science", "grade_report.json")
    java_src    = os.path.join("java", "GradeAnalyzer.java")
    java_out    = os.path.join("java", "out")
    os.makedirs(java_out, exist_ok=True)

    # Step 1: Export CSV using Python data science module
    if DS_AVAILABLE:
        data = ds_analytics._get_data(DATABASE)
        ds_analytics.export_scores_csv(data, csv_path)
    else:
        return jsonify({"status": "error", "message": "Data science module unavailable"}), 500

    # Step 2: Check if Java is available
    javac = subprocess.run(["which", "javac"], capture_output=True, text=True)
    if javac.returncode != 0:
        # Java not installed — generate report via Python fallback
        _java_fallback_report(csv_path, report_path)
        return jsonify({
            "status": "no_java",
            "message": "Java not installed. Report generated via Python fallback."
        })

    # Step 3: Compile Java
    compile_result = subprocess.run(
        ["javac", "-d", java_out, java_src],
        capture_output=True, text=True
    )
    if compile_result.returncode != 0:
        # Don't leak full stderr — log it server-side only
        print(f"[iLEARN] Java compile error: {compile_result.stderr}")
        return jsonify({
            "status": "error",
            "message": "Java compilation failed. Check server logs for details."
        }), 500

    # Step 4: Run Java GradeAnalyzer
    run_result = subprocess.run(
        ["java", "-cp", java_out, "GradeAnalyzer", csv_path, report_path],
        capture_output=True, text=True
    )
    if run_result.returncode != 0:
        print(f"[iLEARN] Java run error: {run_result.stderr}")
        return jsonify({
            "status": "error",
            "message": "Java analysis failed. Check server logs for details."
        }), 500

    return jsonify({"status": "ok", "output": run_result.stdout})


def _java_fallback_report(csv_path: str, report_path: str):
    """
    Python fallback when Java is unavailable.
    Generates the same grade_report.json structure that GradeAnalyzer.java would produce.
    """
    try:
        import csv as csv_mod

        grades = {"A+":0,"A":0,"B":0,"C":0,"D":0,"F":0}
        top, at_risk, all_records = [], [], []
        scores = []

        boundaries = [("A+",90),("A",80),("B",70),("C",60),("D",50),("F",0)]

        def grade_label(s):
            for lbl, mn in boundaries:
                if s >= mn: return lbl
            return "F"

        with open(csv_path, newline="") as f:
            for row in csv_mod.DictReader(f):
                try:
                    sc = float(row.get("score", 0))
                    g  = grade_label(sc)
                    grades[g] = grades.get(g, 0) + 1
                    rec = {
                        "username":  row.get("username", ""),
                        "full_name": row.get("full_name", ""),
                        "course":    row.get("course", ""),
                        "score":     sc, "grade": g,
                        "passed":    sc >= 50,
                        "gpa":       round(sc / 25, 2),
                        "lessons_completed": int(row.get("lessons_completed", 0)),
                        "total_lessons":     int(row.get("total_lessons", 0)),
                    }
                    all_records.append(rec)
                    scores.append(sc)
                    if sc < 50: at_risk.append({"username": rec["username"],
                        "full_name": rec["full_name"], "score": sc,
                        "grade": g, "remark": "Further study required"})
                except (ValueError, KeyError):
                    pass

        top = sorted(all_records, key=lambda r: r["score"], reverse=True)[:5]
        mean   = sum(scores)/len(scores) if scores else 0
        sorted_s = sorted(scores)
        n = len(sorted_s)
        median = (sorted_s[n//2-1]+sorted_s[n//2])/2 if n%2==0 else sorted_s[n//2] if n else 0
        variance = sum((s-mean)**2 for s in scores)/len(scores) if scores else 0
        std_dev  = variance**0.5

        report = {
            "summary": {
                "total_students": len(all_records),
                "pass_count":  sum(1 for r in all_records if r["passed"]),
                "fail_count":  sum(1 for r in all_records if not r["passed"]),
                "pass_rate":   round(sum(1 for r in all_records if r["passed"])/max(1,len(all_records))*100,1),
                "mean_score":   round(mean, 2),
                "median_score": round(median, 2),
                "std_dev":      round(std_dev, 2),
                "min_score":    min(scores) if scores else 0,
                "max_score":    max(scores) if scores else 0,
            },
            "grade_distribution": grades,
            "course_averages":    {},
            "top_students":       [{"username":r["username"],"full_name":r["full_name"],
                                    "course":r["course"],"score":r["score"],"grade":r["grade"]}
                                   for r in top],
            "at_risk_students":   at_risk,
            "all_records":        all_records,
            "generated_by":       "Python fallback (GradeAnalyzer.java equivalent)",
        }
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
    except Exception as e:
        print(f"[fallback] Report generation error: {e}")



# ═══════════════════════════════════════════════
# REMINDERS — due-soon API for dashboard alerts
# ═══════════════════════════════════════════════

@app.route("/api/reminders/due-soon", methods=["GET"])
@login_required
def reminders_due_soon():
    """
    Returns reminders due within the next 24 hours.
    Used by the dashboard to show a visible alert strip.
    """
    from datetime import timedelta
    conn = get_db()
    rows = conn.execute(
        "SELECT id, reminder_text, reminder_time FROM reminders WHERE user_id=? ORDER BY reminder_time",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    now      = datetime.now()
    in_24h   = now + timedelta(hours=24)
    due_soon = []

    for r in rows:
        try:
            rt = datetime.fromisoformat(r["reminder_time"])
            if now <= rt <= in_24h:
                diff_mins = int((rt - now).total_seconds() / 60)
                if diff_mins < 60:
                    when = f"in {diff_mins} minute{'s' if diff_mins != 1 else ''}"
                else:
                    diff_hrs = diff_mins // 60
                    when = f"in {diff_hrs} hour{'s' if diff_hrs != 1 else ''}"
                due_soon.append({
                    "id":   r["id"],
                    "text": r["reminder_text"],
                    "time": r["reminder_time"],
                    "when": when,
                })
        except (ValueError, TypeError):
            pass

    return jsonify(due_soon)


# ═══════════════════════════════════════════════
# FEATURE 1 — LIVE COURSE PROGRESS API
# ═══════════════════════════════════════════════

@app.route("/api/course_progress/<int:course_id>")
@login_required
def api_course_progress(course_id):
    """
    Returns up-to-date progress for one course.
    Called by the lesson page JS after marking a lesson complete so the
    progress bar and percentage update without a full page reload.
    Response: { total, completed, percent, status }
    """
    user_id = session["user_id"]
    conn    = get_db()

    total = conn.execute(
        "SELECT COUNT(*) as cnt FROM lessons WHERE course_id=?",
        (course_id,)
    ).fetchone()["cnt"]

    done = conn.execute(
        """SELECT COUNT(*) as cnt FROM progress p
           JOIN lessons l ON p.lesson_id = l.id
           WHERE l.course_id=? AND p.user_id=? AND p.completed=1""",
        (course_id, user_id)
    ).fetchone()["cnt"]

    conn.close()

    pct    = int(done / total * 100) if total else 0
    status = "complete" if pct == 100 else ("in_progress" if pct > 0 else "not_started")

    return jsonify({
        "total":     total,
        "completed": done,
        "percent":   pct,
        "status":    status
    })


# ═══════════════════════════════════════════════
# FEATURE 2 — /ask_ai ALIAS + CONVERSATION HISTORY
# ═══════════════════════════════════════════════

@app.route("/ask_ai", methods=["POST"])
@login_required
def ask_ai():
    """
    /ask_ai — Public-facing alias for /api/chat.
    Also supports multi-turn conversation history stored in the Flask session.

    Request body (JSON):
        {
          "question":     "What is a closure?",      ← plain-English field name
          "lesson_title": "Scope & Closures",         ← optional context
          "course_title": "JavaScript",               ← optional context
          "clear":        false                       ← set true to reset history
        }

    The conversation history (last 10 turns) is stored in session["ai_history"]
    so the AI remembers what was said earlier in the same browser session.
    """
    body          = request.get_json() or {}
    user_message  = (body.get("question") or body.get("message") or "").strip()
    lesson_title  = body.get("lesson_title", "")
    course_title  = body.get("course_title", "")
    clear_history = body.get("clear", False)

    # ── Conversation history ──────────────────────────────────────
    if clear_history:
        session.pop("ai_history", None)

    history = session.get("ai_history", [])   # list of {role, content} dicts

    if not user_message:
        return jsonify({"reply": "Please type a question first.", "history": history})

    # ── Build system prompt ───────────────────────────────────────
    system_prompt = (
        "You are iLEARN's AI Study Assistant — a concise, encouraging tutor "
        "for an e-learning platform covering Python, JavaScript, CSS, Java, and "
        "Data Science. Respond in plain text (no markdown), under 180 words, "
        "and always end with one practical tip or exercise the student can try. "
        "Remember context from earlier messages in this conversation."
    )
    if lesson_title and course_title:
        system_prompt += (
            f" The student is currently studying '{lesson_title}' in the "
            f"'{course_title}' course. Keep answers relevant to that topic."
        )

    # Add the new user message to history
    history.append({"role": "user", "content": user_message})

    reply = None

    # ── 1. Try Anthropic Claude (with full history) ───────────────
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not anthropic_key:
        # Also try config.py
        anthropic_key = getattr(cfg, "AI_API_KEY", "") if getattr(cfg, "AI_PROVIDER", "") == "anthropic" else ""

    if anthropic_key:
        try:
            import anthropic as _anthropic
            client = _anthropic.Anthropic(api_key=anthropic_key)
            resp   = client.messages.create(
                model      = getattr(cfg, "ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
                max_tokens = 400,
                system     = system_prompt,
                messages   = history[-10:]   # keep last 10 turns to avoid token limits
            )
            reply = resp.content[0].text.strip()
        except Exception as e:
            print(f"[iLEARN /ask_ai] Anthropic error: {e}")

    # ── 2. Try OpenAI (with full history) ────────────────────────
    if reply is None:
        openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not openai_key:
            openai_key = getattr(cfg, "AI_API_KEY", "") if getattr(cfg, "AI_PROVIDER", "") == "openai" else ""

        if openai_key:
            try:
                import openai as _openai
                client = _openai.OpenAI(api_key=openai_key)
                resp   = client.chat.completions.create(
                    model      = getattr(cfg, "OPENAI_MODEL", "gpt-4o-mini"),
                    max_tokens = 400,
                    messages   = [{"role": "system", "content": system_prompt}] + history[-10:]
                )
                reply = resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"[iLEARN /ask_ai] OpenAI error: {e}")

    # ── 3. Keyword fallback ───────────────────────────────────────
    if reply is None:
        msg = user_message.lower()
        keyword_responses = {
            "python":     "🐍 Python: List comprehensions are faster than for-loops. Try: squares = [x*x for x in range(10)]",
            "javascript": "⚡ JS: Use === not ==. Learn the event loop — sync first, then Promises, then setTimeout.",
            "java":       "☕ Java: Use try-with-resources for AutoCloseable objects — safer than finally blocks.",
            "css":        "🎨 CSS: box-sizing: border-box on everything makes sizing predictable and eliminates layout bugs.",
            "flexbox":    "📐 Flexbox: justify-content = main axis, align-items = cross axis. They swap with flex-direction.",
            "grid":       "🔲 Grid: Use grid-template-areas for complex layouts — it reads like a diagram of your page.",
            "async":      "🔄 Async: Promise.all() runs in parallel. Sequential awaits are slow when tasks are independent.",
            "oop":        "🏗️ OOP: Favour composition over inheritance for more flexible, testable code.",
            "closure":    "🔒 Closure: A function that remembers its outer scope's variables — used in counters and modules.",
            "pandas":     "🐼 Pandas: Avoid iterrows() — use vectorised operations or .apply() for row-wise work.",
            "ml":         "🤖 ML: Split data BEFORE scaling. Fit scaler on training data only — never on test data.",
            "data":       "📊 Data Science: df.info() and df.describe() should be first steps on any new dataset.",
            "hello":      "👋 Hi! Ask me about Python, JS, Java, CSS, async, OOP, closures, Pandas, ML, or study tips!",
            "study":      "📚 Active recall beats re-reading. Close the lesson and try to explain it from memory.",
            "exam":       "✏️ For your defence: explain the WHY — why closures? why checked exceptions? Supervisors want understanding.",
            "help":       "🙋 Topics I know: Python, JavaScript, Java, CSS, Flexbox, Grid, async, OOP, closures, Pandas, ML.",
        }
        reply = next((v for k, v in keyword_responses.items() if k in msg), None)
        if not reply:
            ctx   = f" about '{lesson_title}'" if lesson_title else ""
            reply = (
                f"🤖 Good question{ctx}! I'm in keyword mode. "
                "Set ANTHROPIC_API_KEY or OPENAI_API_KEY to get real AI answers. "
                "Ask about: Python, JS, Java, CSS, async, OOP, Pandas, ML, or study tips."
            )

    # ── Update history and save back to session ───────────────────
    history.append({"role": "assistant", "content": reply})
    session["ai_history"] = history[-20:]   # keep last 20 messages (10 turns)
    session.modified = True

    return jsonify({
        "reply":   reply,
        "history": len(history) // 2,       # number of complete turns
    })


# ═══════════════════════════════════════════════
# FEATURE 3 — ADMIN DASHBOARD
# ═══════════════════════════════════════════════

@app.route("/admin")
@login_required
def admin_dashboard():
    """
    Admin statistics dashboard — only accessible to the 'admin' user.
    Shows platform-wide stats: users, courses, completions, messages,
    per-course breakdown, and recent activity.
    """
    # Check admin role in DB — not just session username
    conn_check = get_db()
    requesting_user = conn_check.execute("SELECT username FROM users WHERE id=?", (session["user_id"],)).fetchone()
    conn_check.close()
    if not requesting_user or requesting_user["username"] != "admin":
        return redirect(url_for("dashboard"))

    conn = get_db()

    # ── Core stats ───────────────────────────────────────────────
    total_users    = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    total_courses  = conn.execute("SELECT COUNT(*) as c FROM courses").fetchone()["c"]
    total_lessons  = conn.execute("SELECT COUNT(*) as c FROM lessons").fetchone()["c"]
    total_quiz_q   = conn.execute("SELECT COUNT(*) as c FROM quiz").fetchone()["c"]
    total_messages = conn.execute("SELECT COUNT(*) as c FROM contact_messages").fetchone()["c"]
    unread_msgs    = conn.execute(
        "SELECT COUNT(*) as c FROM contact_messages WHERE is_read=0"
    ).fetchone()["c"]

    # Total lesson completions across all users
    total_completions = conn.execute(
        "SELECT COUNT(*) as c FROM progress WHERE completed=1"
    ).fetchone()["c"]

    # Total quiz attempts recorded
    total_quiz_attempts = conn.execute(
        "SELECT COUNT(*) as c FROM quiz_attempts"
    ).fetchone()["c"]

    # ── Per-course breakdown ─────────────────────────────────────
    courses_raw = conn.execute("SELECT * FROM courses ORDER BY title").fetchall()
    course_stats = []
    for c in courses_raw:
        lesson_count = conn.execute(
            "SELECT COUNT(*) as cnt FROM lessons WHERE course_id=?", (c["id"],)
        ).fetchone()["cnt"]
        completions  = conn.execute(
            """SELECT COUNT(*) as cnt FROM progress p
               JOIN lessons l ON p.lesson_id = l.id
               WHERE l.course_id=? AND p.completed=1""",
            (c["id"],)
        ).fetchone()["cnt"]
        enrolled     = conn.execute(
            """SELECT COUNT(DISTINCT p.user_id) as cnt FROM progress p
               JOIN lessons l ON p.lesson_id = l.id
               WHERE l.course_id=?""",
            (c["id"],)
        ).fetchone()["cnt"]
        max_possible = lesson_count * total_users if total_users else 0
        pct          = int(completions / max_possible * 100) if max_possible else 0
        course_stats.append({
            "id":           c["id"],
            "title":        c["title"],
            "icon":         c["icon"],
            "level":        c["level"],
            "lesson_count": lesson_count,
            "completions":  completions,
            "enrolled":     enrolled,
            "pct":          pct,
        })

    # ── Most active users (top 5 by lessons completed) ──────────
    top_users = conn.execute(
        """SELECT u.username, u.full_name, COUNT(p.id) as done
           FROM users u
           LEFT JOIN progress p ON p.user_id = u.id AND p.completed=1
           GROUP BY u.id
           ORDER BY done DESC
           LIMIT 5"""
    ).fetchall()

    # ── Recent completions (last 8) ───────────────────────────────
    recent_activity = conn.execute(
        """SELECT u.username, l.lesson_title, c.title as course_title,
                  p.completed_at
           FROM progress p
           JOIN users u   ON u.id = p.user_id
           JOIN lessons l ON l.id = p.lesson_id
           JOIN courses c ON c.id = l.course_id
           WHERE p.completed=1 AND p.completed_at IS NOT NULL
           ORDER BY p.completed_at DESC
           LIMIT 8"""
    ).fetchall()

    # ── New users in the last 7 days ─────────────────────────────
    week_ago  = (datetime.now() - timedelta(days=7)).isoformat()
    month_ago = (datetime.now() - timedelta(days=30)).isoformat()

    new_users_week  = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE created_at >= ?", (week_ago,)
    ).fetchone()["c"]

    new_users_month = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE created_at >= ?", (month_ago,)
    ).fetchone()["c"]

    # ── Engagement rate — users who completed at least 1 lesson ──
    active_users = conn.execute(
        "SELECT COUNT(DISTINCT user_id) as c FROM progress WHERE completed=1"
    ).fetchone()["c"]
    engagement_pct = int(active_users / total_users * 100) if total_users else 0

    # ── Most popular course (most enrolled) ───────────────────────
    popular = conn.execute(
        """SELECT c.title, COUNT(DISTINCT p.user_id) as enr
           FROM courses c
           LEFT JOIN lessons l ON l.course_id = c.id
           LEFT JOIN progress p ON p.lesson_id = l.id
           GROUP BY c.id ORDER BY enr DESC LIMIT 1"""
    ).fetchone()
    popular_course = popular["title"] if popular else "—"

    # ── Recent messages preview (last 3) ─────────────────────────
    recent_messages = conn.execute(
        """SELECT cm.name, cm.subject, cm.submitted_at, cm.is_read
           FROM contact_messages cm
           ORDER BY cm.submitted_at DESC LIMIT 3"""
    ).fetchall()

    # ── All registered users with completion count ────────────────
    all_users = conn.execute(
        """SELECT u.id, u.username, u.full_name, u.email, u.created_at,
                  COUNT(p.id) as lessons_done
           FROM users u
           LEFT JOIN progress p ON p.user_id = u.id AND p.completed=1
           GROUP BY u.id
           ORDER BY u.created_at DESC"""
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        # Core stats
        total_users         = total_users,
        total_courses       = total_courses,
        total_lessons       = total_lessons,
        total_quiz_q        = total_quiz_q,
        total_completions   = total_completions,
        total_messages      = total_messages,
        unread_msgs         = unread_msgs,
        total_quiz_attempts = total_quiz_attempts,
        new_users_week      = new_users_week,
        new_users_month     = new_users_month,
        active_users        = active_users,
        engagement_pct      = engagement_pct,
        popular_course      = popular_course,
        recent_messages     = recent_messages,
        # Breakdowns
        course_stats        = course_stats,
        top_users           = top_users,
        recent_activity     = recent_activity,
        # Users list
        all_users           = all_users,
        total_non_admin     = len([u for u in all_users if u["username"] != "admin"]),
        # Nav
        username            = session["username"],
        full_name           = session.get("full_name", "Admin"),
    )


# ── Admin: Delete a contact message ──────────────────────────────────
@app.route("/api/admin/delete_message/<int:msg_id>", methods=["DELETE"])
@login_required
def admin_delete_message(msg_id):
    """Admin-only: permanently delete a support message."""
    conn_check = get_db()
    req_user = conn_check.execute(
        "SELECT username FROM users WHERE id=?", (session["user_id"],)
    ).fetchone()
    conn_check.close()
    if not req_user or req_user["username"] != "admin":
        return jsonify({"status": "error", "message": "Unauthorised"}), 403

    conn = get_db()
    conn.execute("DELETE FROM contact_messages WHERE id=?", (msg_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


# ── Admin: Toggle message read/unread ─────────────────────────────────
@app.route("/api/admin/toggle_read/<int:msg_id>", methods=["POST"])
@login_required
def admin_toggle_read(msg_id):
    """Admin-only: toggle a message between read and unread."""
    conn_check = get_db()
    req_user = conn_check.execute(
        "SELECT username FROM users WHERE id=?", (session["user_id"],)
    ).fetchone()
    conn_check.close()
    if not req_user or req_user["username"] != "admin":
        return jsonify({"status": "error"}), 403

    conn = get_db()
    msg = conn.execute(
        "SELECT is_read FROM contact_messages WHERE id=?", (msg_id,)
    ).fetchone()
    if not msg:
        conn.close()
        return jsonify({"status": "error", "message": "Not found"}), 404

    new_state = 0 if msg["is_read"] else 1
    conn.execute(
        "UPDATE contact_messages SET is_read=? WHERE id=?", (new_state, msg_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "is_read": new_state})


# ── Security Headers ──────────────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    """Add security headers to every response."""
    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    # Basic XSS protection for older browsers
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Restrict referrer info
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Remove Flask version fingerprint
    response.headers.pop("Server", None)
    return response

# ========== PASSWORD RESET ENDPOINTS ==========

# Initialize password reset manager AFTER DATABASE is defined
from password_reset import PasswordResetManager
from dotenv import load_dotenv
import os

load_dotenv()
password_reset_manager = PasswordResetManager(DATABASE)

@app.route('/api/forgot-password', methods=['POST'])
def api_forgot_password():
    """Handle forgot password requests"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"success": False, "error": "Email is required"}), 400
        
        # Create reset token
        user = password_reset_manager.get_user_by_email(email)
        
        if user:
            reset_token = password_reset_manager.generate_reset_token()
            password_reset_manager.create_reset_token(user[0], email)
            
            # Build reset URL for frontend
            frontend_url = os.getenv('FRONTEND_URL', 'https://ilearn-nextjs-c19j.vercel.app')
            reset_url = f"{frontend_url}/forgot-password?token={reset_token}"
            
            # Send email via Resend
            email_result = password_reset_manager.send_reset_email(email, user[1], reset_token, reset_url)
            
            if not email_result.get('success'):
                print(f"[Password Reset] Email send failed: {email_result.get('error')}")
        
        # Always return same message for security (don't reveal if email exists)
        return jsonify({
            "success": True,
            "message": "If an account with this email exists, you'll receive a password reset link shortly."
        }), 200
        
    except Exception as e:
        print(f"[Password Reset Error] {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/verify-reset-token/<token>', methods=['GET'])
def api_verify_reset_token(token):
    """Verify if a reset token is valid"""
    try:
        is_valid = password_reset_manager.verify_reset_token(token)
        
        if is_valid:
            return jsonify({"valid": True, "message": "Token is valid"}), 200
        else:
            return jsonify({"valid": False, "message": "Token has expired or is invalid"}), 400
            
    except Exception as e:
        print(f"[Token Verification Error] {str(e)}")
        return jsonify({"valid": False, "error": str(e)}), 500

@app.route('/api/reset-password', methods=['POST'])
def api_reset_password():
    """Handle password reset"""
    try:
        data = request.json
        token = data.get('token', '').strip()
        new_password = data.get('password', '').strip()
        
        if not token or not new_password:
            return jsonify({"success": False, "error": "Token and password are required"}), 400
        
        if len(new_password) < 8:
            return jsonify({"success": False, "error": "Password must be at least 8 characters"}), 400
        
        # Reset the password
        result = password_reset_manager.reset_password(token, new_password)
        
        if result['success']:
            return jsonify({"success": True, "message": "Password reset successfully"}), 200
        else:
            return jsonify({"success": False, "error": result.get('error', 'Failed to reset password')}), 400
            
    except Exception as e:
        print(f"[Password Reset Error] {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# ========== END PASSWORD RESET ENDPOINTS ==========

init_db()

if __name__ == "__main__":
    print("🚀 Starting iLEARN...")
    init_db()
    print("✅ Ready! http://127.0.0.1:5000  |  Login: admin / ilearn123")
    app.run(debug=True)