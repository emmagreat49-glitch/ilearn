"""
iLEARN — Data Science Analytics Module
═══════════════════════════════════════════════════════════════════
Language   : Python 3 (Data Science stack)
Libraries  : pandas, matplotlib, seaborn
Purpose    : Reads live data from SQLite, generates statistical
             charts and insights for the admin analytics dashboard.

Distinct tech role in project:
  - Flask (app.py)  → Web server, routing, session management
  - This module     → Pure data science: statistics + visualisation
  - GradeAnalyzer   → Java: grade computation, JSON report generation
  - CSS (main.css)  → All visual styling
  - JS (main.js)    → Browser interactions, notifications, animations
═══════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import io
import base64
import json
from datetime import datetime, timedelta

import pandas as pd
import matplotlib
matplotlib.use("Agg")           # non-interactive backend (server-safe)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Consistent visual theme ─────────────────────────────────────
PALETTE    = ["#4facfe", "#a78bfa", "#34d399", "#fbbf24", "#f87171", "#22d3ee"]
BG_DARK    = "#0c1424"
BG_CARD    = "#111927"
TEXT_COLOR = "#e2e8f0"
GRID_COLOR = "#1e2d44"

def _apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor":  BG_DARK,
        "axes.facecolor":    BG_CARD,
        "axes.edgecolor":    GRID_COLOR,
        "axes.labelcolor":   TEXT_COLOR,
        "axes.titlecolor":   "#ffffff",
        "xtick.color":       TEXT_COLOR,
        "ytick.color":       TEXT_COLOR,
        "text.color":        TEXT_COLOR,
        "grid.color":        GRID_COLOR,
        "grid.linewidth":    0.6,
        "font.family":       "DejaVu Sans",
        "font.size":         10,
        "axes.titlesize":    13,
        "axes.titleweight":  "bold",
        "figure.dpi":        120,
    })

# ── Database helpers ─────────────────────────────────────────────

def _get_data(db_path: str = "database.db") -> dict:
    """Load all relevant tables into pandas DataFrames."""
    if not os.path.exists(db_path):
        return {}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    data = {
        "users":    pd.read_sql("SELECT * FROM users",    conn),
        "courses":  pd.read_sql("SELECT * FROM courses",  conn),
        "lessons":  pd.read_sql("SELECT * FROM lessons",  conn),
        "progress": pd.read_sql("SELECT * FROM progress", conn),
        "quiz":     pd.read_sql("SELECT * FROM quiz",     conn),
    }
    conn.close()
    return data


def _fig_to_base64(fig) -> str:
    """Convert a matplotlib figure to a base64 PNG string for HTML embedding."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"


# ════════════════════════════════════════════════════════════════
# CHART 1 — Course Completion Rates (horizontal bar)
# ════════════════════════════════════════════════════════════════

def chart_course_completion(data: dict) -> str:
    _apply_dark_theme()

    if data.get("progress") is None or data["progress"].empty:
        return _empty_chart("No progress data yet")

    courses  = data["courses"]
    lessons  = data["lessons"]
    progress = data["progress"]

    rows = []
    for _, course in courses.iterrows():
        lesson_ids = lessons[lessons["course_id"] == course["id"]]["id"].tolist()
        total      = len(lesson_ids)
        if total == 0:
            continue
        completed = progress[
            (progress["lesson_id"].isin(lesson_ids)) &
            (progress["completed"] == 1)
        ]["user_id"].nunique()
        pct = round(completed / max(1, data["users"].shape[0]) * 100, 1)
        rows.append({"course": course["title"].replace(" & ", "\n& "),
                     "pct": pct})

    if not rows:
        return _empty_chart("No completions recorded yet")

    df = pd.DataFrame(rows).sort_values("pct", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(df["course"], df["pct"],
                   color=PALETTE[:len(df)], height=0.55,
                   edgecolor="none")

    for bar, val in zip(bars, df["pct"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val}%", va="center", color=TEXT_COLOR, fontsize=9)

    ax.set_xlim(0, 115)
    ax.set_xlabel("Completion Rate (%)")
    ax.set_title("Course Completion Rate by Course")
    ax.axvline(70, color="#fbbf24", linewidth=1, linestyle="--", alpha=0.5)
    ax.text(71, -0.6, "Target 70%", color="#fbbf24", fontsize=8)
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return _fig_to_base64(fig)


# ════════════════════════════════════════════════════════════════
# CHART 2 — Quiz Score Distribution (histogram + KDE)
# ════════════════════════════════════════════════════════════════

def chart_score_distribution(data: dict) -> str:
    _apply_dark_theme()

    progress = data.get("progress")
    if progress is None or progress.empty:
        return _empty_chart("No quiz data yet")

    completed = progress[progress["completed"] == 1]
    if completed.empty:
        return _empty_chart("No completed lessons yet")

    # Use lesson completion percentage as a proxy score
    lessons  = data["lessons"]
    users    = data["users"]

    scores = []
    for uid in completed["user_id"].unique():
        user_done  = completed[completed["user_id"] == uid]["lesson_id"].tolist()
        total_less = len(lessons)
        if total_less > 0:
            scores.append(len(user_done) / total_less * 100)

    if len(scores) < 2:
        return _empty_chart("Need more students to show distribution")

    scores_series = pd.Series(scores)

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(scores_series, bins=min(12, len(scores)),
            color="#4facfe", edgecolor="#0c1424", alpha=0.75, density=True)

    try:
        scores_series.plot.kde(ax=ax, color="#00f2fe", linewidth=2.5, label="KDE")
    except Exception:
        pass

    mean_s   = scores_series.mean()
    median_s = scores_series.median()

    ax.axvline(mean_s,   color="#fbbf24", linewidth=2, linestyle="--",
               label=f"Mean {mean_s:.1f}%")
    ax.axvline(median_s, color="#34d399", linewidth=2, linestyle=":",
               label=f"Median {median_s:.1f}%")

    ax.set_xlabel("Completion Score (%)")
    ax.set_ylabel("Density")
    ax.set_title("Distribution of Student Completion Scores")
    ax.legend(facecolor=BG_CARD, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return _fig_to_base64(fig)


# ════════════════════════════════════════════════════════════════
# CHART 3 — Student Enrolment Over Time (line chart)
# ════════════════════════════════════════════════════════════════

def chart_enrolment_over_time(data: dict) -> str:
    _apply_dark_theme()

    users = data.get("users")
    if users is None or users.empty:
        return _empty_chart("No user data")

    if "created_at" not in users.columns or users["created_at"].isna().all():
        # Simulate monthly data if no timestamps
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        import numpy as np
        rng = len(users)
        cum = sorted([max(1, int(rng * (i+1)/12)) for i in range(12)])
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(months, cum, color="#4facfe", linewidth=2.5, marker="o",
                markersize=6, markerfacecolor="#00f2fe")
        ax.fill_between(months, cum, alpha=0.12, color="#4facfe")
        ax.set_title("Simulated Cumulative Enrolments")
        ax.set_ylabel("Total Students")
        ax.grid(alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        return _fig_to_base64(fig)

    users["created_at"] = pd.to_datetime(users["created_at"], errors="coerce")
    users = users.dropna(subset=["created_at"])
    users["month"] = users["created_at"].dt.to_period("M")
    monthly = users.groupby("month").size().cumsum().reset_index()
    monthly.columns = ["month", "count"]
    monthly["month_str"] = monthly["month"].astype(str)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(monthly["month_str"], monthly["count"],
            color="#4facfe", linewidth=2.5, marker="o",
            markersize=7, markerfacecolor="#00f2fe")
    ax.fill_between(monthly["month_str"], monthly["count"],
                    alpha=0.12, color="#4facfe")
    plt.xticks(rotation=30, ha="right")
    ax.set_title("Cumulative Student Enrolments Over Time")
    ax.set_ylabel("Total Students")
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return _fig_to_base64(fig)


# ════════════════════════════════════════════════════════════════
# CHART 4 — Top 10 Most Engaged Students (horizontal bar)
# ════════════════════════════════════════════════════════════════

def chart_top_students(data: dict) -> str:
    _apply_dark_theme()

    progress = data.get("progress")
    users    = data.get("users")
    if progress is None or progress.empty or users is None:
        return _empty_chart("No progress data yet")

    completed = progress[progress["completed"] == 1]
    if completed.empty:
        return _empty_chart("No completed lessons yet")

    counts = completed.groupby("user_id").size().reset_index()
    counts.columns = ["user_id", "lessons_done"]
    counts = counts.merge(users[["id", "username", "full_name"]], 
                          left_on="user_id", right_on="id")
    counts["label"] = counts.apply(
        lambda r: r["full_name"] if pd.notna(r["full_name"]) and r["full_name"]
                  else r["username"], axis=1)
    counts = counts.nlargest(10, "lessons_done").sort_values("lessons_done")

    fig, ax = plt.subplots(figsize=(8, max(3, len(counts) * 0.55)))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(counts))]
    bars = ax.barh(counts["label"], counts["lessons_done"],
                   color=colors, height=0.6, edgecolor="none")

    for bar, val in zip(bars, counts["lessons_done"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", color=TEXT_COLOR, fontsize=9)

    ax.set_xlabel("Lessons Completed")
    ax.set_title("Top 10 Most Engaged Students")
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return _fig_to_base64(fig)


# ════════════════════════════════════════════════════════════════
# CHART 5 — Lessons Per Course (pie / donut)
# ════════════════════════════════════════════════════════════════

def chart_lessons_per_course(data: dict) -> str:
    _apply_dark_theme()

    courses = data.get("courses")
    lessons = data.get("lessons")
    if courses is None or lessons is None:
        return _empty_chart("No data")

    counts = lessons.groupby("course_id").size().reset_index()
    counts.columns = ["course_id", "count"]
    counts = counts.merge(courses[["id", "title"]], left_on="course_id", right_on="id")

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        counts["count"], labels=counts["title"],
        autopct="%1.0f%%", colors=PALETTE[:len(counts)],
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2},
        pctdistance=0.78, startangle=90,
        textprops={"color": TEXT_COLOR, "fontsize": 9}
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("#ffffff")

    # Draw the centre hole (donut)
    centre = plt.Circle((0, 0), 0.48, color=BG_DARK)
    ax.add_patch(centre)
    ax.text(0, 0, f"{len(lessons)}\nLessons",
            ha="center", va="center", fontsize=12,
            fontweight="bold", color="#ffffff")

    ax.set_title("Lesson Distribution Across Courses")
    fig.tight_layout()
    return _fig_to_base64(fig)


# ════════════════════════════════════════════════════════════════
# SUMMARY STATISTICS (for dashboard cards)
# ════════════════════════════════════════════════════════════════

def compute_summary_stats(data: dict) -> dict:
    if not data:
        return {}

    users    = data.get("users",    pd.DataFrame())
    courses  = data.get("courses",  pd.DataFrame())
    lessons  = data.get("lessons",  pd.DataFrame())
    progress = data.get("progress", pd.DataFrame())

    completed = progress[progress["completed"] == 1] if not progress.empty else pd.DataFrame()

    # Overall completion rate
    total_possible = len(users) * len(lessons)
    total_done     = len(completed) if not completed.empty else 0
    completion_rate = round(total_done / max(1, total_possible) * 100, 1)

    # Most popular course
    most_popular = "N/A"
    if not completed.empty and not lessons.empty and not courses.empty:
        popular = (completed
                   .merge(lessons[["id", "course_id"]], left_on="lesson_id", right_on="id")
                   .groupby("course_id").size().idxmax())
        course_row = courses[courses["id"] == popular]
        if not course_row.empty:
            most_popular = course_row.iloc[0]["title"]

    # Active users (completed at least 1 lesson)
    active = completed["user_id"].nunique() if not completed.empty else 0

    return {
        "total_users":       len(users),
        "total_courses":     len(courses),
        "total_lessons":     len(lessons),
        "total_completions": total_done,
        "completion_rate":   completion_rate,
        "active_users":      active,
        "most_popular":      most_popular,
        "quiz_questions":    len(data.get("quiz", pd.DataFrame())),
    }


# ════════════════════════════════════════════════════════════════
# EXPORT — Generate CSV for Java GradeAnalyzer
# ════════════════════════════════════════════════════════════════

def export_scores_csv(data: dict, output_path: str = "data_science/scores.csv"):
    """
    Exports student-course completion data to CSV.
    This CSV is consumed by GradeAnalyzer.java to produce grade reports.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    users    = data.get("users",    pd.DataFrame())
    courses  = data.get("courses",  pd.DataFrame())
    lessons  = data.get("lessons",  pd.DataFrame())
    progress = data.get("progress", pd.DataFrame())

    if users.empty or courses.empty or lessons.empty:
        return

    rows = []
    for _, user in users.iterrows():
        for _, course in courses.iterrows():
            course_lessons = lessons[lessons["course_id"] == course["id"]]
            total = len(course_lessons)
            if total == 0:
                continue

            if not progress.empty:
                done = progress[
                    (progress["user_id"] == user["id"]) &
                    (progress["lesson_id"].isin(course_lessons["id"])) &
                    (progress["completed"] == 1)
                ]
                completed_count = len(done)
                completed_at = done["completed_at"].max() if not done.empty else ""
            else:
                completed_count = 0
                completed_at = ""

            score = round(completed_count / total * 100, 1)

            rows.append({
                "username":          user["username"],
                "full_name":         user.get("full_name", user["username"]) or user["username"],
                "course":            course["title"],
                "score":             score,
                "lessons_completed": completed_count,
                "total_lessons":     total,
                "completed_at":      completed_at,
            })

    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)


# ════════════════════════════════════════════════════════════════
# MAIN ENTRY — called by Flask /analytics route
# ════════════════════════════════════════════════════════════════

def generate_analytics(db_path: str = "database.db") -> dict:
    """
    Main function called by Flask.
    Returns a dict with all chart images (base64) and summary stats.
    """
    data = _get_data(db_path)

    if not data:
        return {"error": "Could not load database", "charts": {}, "stats": {}}

    # Export CSV for Java component
    try:
        export_scores_csv(data)
    except Exception as e:
        print(f"[analytics] CSV export warning: {e}")

    stats = compute_summary_stats(data)

    charts = {}
    generators = {
        "completion":    chart_course_completion,
        "distribution":  chart_score_distribution,
        "enrolment":     chart_enrolment_over_time,
        "top_students":  chart_top_students,
        "lessons_pie":   chart_lessons_per_course,
    }

    for name, fn in generators.items():
        try:
            charts[name] = fn(data)
        except Exception as e:
            print(f"[analytics] Chart '{name}' failed: {e}")
            charts[name] = _empty_chart(f"Chart error: {name}")

    return {"charts": charts, "stats": stats}


def _empty_chart(message: str) -> str:
    _apply_dark_theme()
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.text(0.5, 0.5, message, ha="center", va="center",
            color="#64748b", fontsize=12, transform=ax.transAxes)
    ax.set_axis_off()
    fig.tight_layout()
    return _fig_to_base64(fig)


# ── Run standalone for testing ───────────────────────────────────
if __name__ == "__main__":
    print("iLEARN Analytics Module — standalone test")
    result = generate_analytics()
    print(f"Stats: {result.get('stats')}")
    print(f"Charts generated: {list(result.get('charts', {}).keys())}")
    print("Done.")
