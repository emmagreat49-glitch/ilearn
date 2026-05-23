"""
iLEARN — Configuration
=======================
Edit this file to configure AI, email, and other settings.

EMAIL SETUP (Gmail):
  1. myaccount.google.com > Security > 2-Step Verification (enable)
  2. Search "App Passwords" > create one > paste as SMTP_PASSWORD
  3. Fill in SMTP_USER and ADMIN_EMAIL below

AI CHATBOT:
  Get a free key at console.anthropic.com or platform.openai.com
  Set AI_PROVIDER = "anthropic" or "openai" and paste your key as AI_API_KEY
"""

import os

# ── AI ────────────────────────────────────────
AI_PROVIDER     = os.environ.get("ILEARN_AI_PROVIDER", "")
AI_API_KEY      = os.environ.get("ILEARN_AI_KEY",      "")
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
OPENAI_MODEL    = "gpt-4o-mini"

# ── Email / SMTP ──────────────────────────────
# Leave SMTP_USER empty to disable all email (app still works without it)
SMTP_HOST     = os.environ.get("ILEARN_SMTP_HOST",  "smtp.gmail.com")
SMTP_PORT     = int(os.environ.get("ILEARN_SMTP_PORT", 587))
SMTP_USER     = os.environ.get("ILEARN_SMTP_USER",  "")   # your Gmail address
SMTP_PASSWORD = os.environ.get("ILEARN_SMTP_PASS",  "")   # Gmail App Password
ADMIN_EMAIL   = os.environ.get("ILEARN_ADMIN_EMAIL","")   # where admin alerts go

# ── Lesson Completion ─────────────────────────
MIN_LESSON_SECONDS = 30   # seconds on page before Mark Complete unlocks (0 = off)
