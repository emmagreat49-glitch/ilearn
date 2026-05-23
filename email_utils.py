"""
iLEARN — Email Utilities
========================
Handles all outgoing email: reminder alerts and feedback notifications.

To enable email, set these in config.py OR as environment variables:
  SMTP_HOST      e.g. smtp.gmail.com
  SMTP_PORT      587
  SMTP_USER      your sending email address
  SMTP_PASSWORD  your app password (NOT your login password)
  ADMIN_EMAIL    where admin notifications go

Gmail quick-start:
  1. Enable 2-Step Verification on your Google account
  2. Go to myaccount.google.com → Security → App Passwords
  3. Generate a password for "Mail" / "Other"
  4. Paste it as SMTP_PASSWORD
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config as cfg


def _is_configured():
    """Returns True only if all SMTP credentials are set."""
    return all([cfg.SMTP_HOST, cfg.SMTP_USER, cfg.SMTP_PASSWORD])


def _send(to_addr: str, subject: str, html_body: str, plain_body: str) -> bool:
    """
    Core send function. Returns True on success, False on failure.
    Never raises — all errors are caught and printed.
    """
    if not _is_configured():
        print("[iLEARN email] SMTP not configured — skipping email send.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"iLEARN <{cfg.SMTP_USER}>"
        msg["To"]      = to_addr

        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body,  "html"))

        with smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(cfg.SMTP_USER, cfg.SMTP_PASSWORD)
            server.sendmail(cfg.SMTP_USER, [to_addr], msg.as_string())

        print(f"[iLEARN email] ✅ Sent to {to_addr}: {subject}")
        return True

    except Exception as e:
        print(f"[iLEARN email] ❌ Failed to send to {to_addr}: {e}")
        return False


# ─────────────────────────────────────────────────────────
# PUBLIC FUNCTIONS
# ─────────────────────────────────────────────────────────

def send_reminder_email(to_addr: str, learner_name: str,
                        reminder_text: str, reminder_time: str) -> bool:
    """
    Send a study reminder email to a learner.
    Called by the background reminder checker.
    """
    subject = "⏰ iLEARN Study Reminder"

    plain = (
        f"Hi {learner_name},\n\n"
        f"This is your iLEARN study reminder:\n\n"
        f"  📚 {reminder_text}\n"
        f"  🕐 Scheduled for: {reminder_time}\n\n"
        f"Open iLEARN now and keep learning!\n\n"
        f"— The iLEARN Team"
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background:#060b14; color:#e2e8f0; margin:0; padding:0; }}
    .wrap {{ max-width:520px; margin:40px auto; }}
    .card {{ background:#111927; border:1px solid rgba(99,179,237,0.15); border-radius:16px; overflow:hidden; }}
    .header {{ background:linear-gradient(135deg,#4facfe,#00f2fe); padding:28px 32px; }}
    .header h1 {{ margin:0; color:#fff; font-size:1.4rem; }}
    .header p  {{ margin:4px 0 0; color:rgba(255,255,255,0.85); font-size:0.9rem; }}
    .body {{ padding:28px 32px; }}
    .reminder-box {{
      background:#1e2d44; border:1px solid rgba(99,179,237,0.2);
      border-left:4px solid #4facfe; border-radius:10px;
      padding:16px 20px; margin:20px 0;
    }}
    .reminder-text {{ font-size:1.05rem; font-weight:600; color:#e2e8f0; margin-bottom:6px; }}
    .reminder-time {{ font-size:0.82rem; color:#94a3b8; font-family:monospace; }}
    .cta {{ display:inline-block; margin-top:24px; padding:12px 28px;
            background:linear-gradient(135deg,#4facfe,#00f2fe);
            color:#060b14; font-weight:700; border-radius:8px;
            text-decoration:none; font-size:0.95rem; }}
    .footer {{ padding:16px 32px; font-size:0.75rem; color:#64748b; border-top:1px solid rgba(99,179,237,0.1); }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="header">
        <h1>⏰ Study Reminder</h1>
        <p>iLEARN — Interactive E-Learning Platform</p>
      </div>
      <div class="body">
        <p>Hi <strong>{learner_name}</strong>,</p>
        <p>This is your scheduled study reminder:</p>
        <div class="reminder-box">
          <div class="reminder-text">📚 {reminder_text}</div>
          <div class="reminder-time">🕐 {reminder_time}</div>
        </div>
        <p style="color:#94a3b8; font-size:0.9rem;">
          Open iLEARN now and continue where you left off. Consistent study sessions
          are the fastest path to mastery.
        </p>
        <a href="http://localhost:5000/dashboard" class="cta">Go to Dashboard →</a>
      </div>
      <div class="footer">
        You received this because you set up a reminder on iLEARN.
        Log in to manage your reminders.
      </div>
    </div>
  </div>
</body>
</html>
"""
    return _send(to_addr, subject, html, plain)


def send_feedback_notification(admin_email: str, sender_name: str,
                                sender_email: str, subject: str,
                                message: str) -> bool:
    """
    Notify admin when a learner submits feedback.
    """
    email_subject = f"[iLEARN Feedback] {subject}"

    plain = (
        f"New iLEARN feedback submission\n\n"
        f"From:    {sender_name} <{sender_email}>\n"
        f"Subject: {subject}\n\n"
        f"{message}\n\n"
        f"---\nView all: http://localhost:5000/admin/feedback"
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background:#060b14; color:#e2e8f0; }}
    .wrap {{ max-width:520px; margin:40px auto; }}
    .card {{ background:#111927; border:1px solid rgba(99,179,237,0.15); border-radius:16px; overflow:hidden; }}
    .header {{ background:linear-gradient(135deg,#a78bfa,#7c3aed); padding:22px 28px; }}
    .header h1 {{ margin:0; color:#fff; font-size:1.2rem; }}
    .body {{ padding:24px 28px; font-size:0.93rem; }}
    .field {{ margin-bottom:14px; }}
    .label {{ font-size:0.75rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:3px; }}
    .value {{ color:#e2e8f0; }}
    .msg-box {{ background:#1e2d44; border-radius:8px; padding:14px 16px; color:#e2e8f0; white-space:pre-wrap; word-break:break-word; margin-top:6px; }}
    .cta {{ display:inline-block; margin-top:20px; padding:10px 24px;
            background:linear-gradient(135deg,#a78bfa,#7c3aed);
            color:#fff; font-weight:700; border-radius:8px; text-decoration:none; }}
  </style>
</head>
<body>
  <div class="wrap"><div class="card">
    <div class="header"><h1>💬 New Feedback Submission</h1></div>
    <div class="body">
      <div class="field"><div class="label">From</div><div class="value">{sender_name} &lt;{sender_email}&gt;</div></div>
      <div class="field"><div class="label">Subject</div><div class="value">{subject}</div></div>
      <div class="field"><div class="label">Message</div><div class="msg-box">{message}</div></div>
      <a href="http://localhost:5000/admin/feedback" class="cta">View All Feedback →</a>
    </div>
  </div></div>
</body>
</html>
"""
    return _send(admin_email, email_subject, html, plain)
