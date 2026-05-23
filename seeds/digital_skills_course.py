"""iLEARN — Digital Skills & Productivity course seed."""
from .helpers import insert_lessons_and_quizzes


def seed_digital_skills(conn, c):
    c.execute(
        "INSERT INTO courses (title, description, icon, level, language) VALUES (?,?,?,?,?)",
        (
            "Digital Skills & Productivity",
            "Master the tools and skills that every professional needs in a digital workplace. Covers spreadsheets, data tools, communication platforms, cybersecurity basics, and personal productivity systems.",
            "monitor",
            "Beginner",
            "digital",
        ),
    )
    cid = c.lastrowid

    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Spreadsheets & Data Tools", 1))
    mod1 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Digital Communication", 2))
    mod2 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Cybersecurity Essentials", 3))
    mod3 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Productivity Systems", 4))
    mod4 = c.lastrowid

    lessons = [
        (1, "Spreadsheets — From Basics to Power User", mod1, """
<h2>Mastering Spreadsheets</h2>
<p>Spreadsheets (Excel, Google Sheets) are the most widely used data tools in the world. Every professional who can use them effectively has a major advantage.</p>

<h3>Essential Formulas</h3>
<pre><code>=SUM(A1:A10)          — adds a range of numbers
=AVERAGE(B1:B20)      — calculates the mean
=COUNT(C1:C50)        — counts cells with numbers
=COUNTA(C1:C50)       — counts non-empty cells
=MAX(D1:D100)         — largest value
=MIN(D1:D100)         — smallest value
=IF(A1>50,"Pass","Fail")  — conditional logic
=VLOOKUP(value, range, col_index, FALSE) — look up a value
=COUNTIF(A:A, "Yes")  — count matching cells
=SUMIF(A:A, "Sales", B:B) — sum where condition is met</code></pre>

<h3>Pivot Tables</h3>
<p>Pivot tables are the most powerful feature in Excel/Sheets. They summarise thousands of rows into meaningful insights in seconds.</p>
<ol style="color:var(--text-2);padding-left:1.4rem;margin:.8rem 0">
  <li>Select your data range (include headers)</li>
  <li>Insert → Pivot Table</li>
  <li>Drag fields to Rows, Columns, and Values</li>
  <li>Change the summary function (Sum, Count, Average)</li>
</ol>

<h3>Data Validation & Conditional Formatting</h3>
<pre><code>Data Validation:
- Restrict a cell to only accept numbers between 1–100
- Create a dropdown list from a range of values
- Show an error message for invalid input

Conditional Formatting:
- Highlight cells above average in green
- Show red/amber/green traffic lights based on value
- Create a heat map of performance data</code></pre>

<div class="concept-box">
  <div class="cb-title">Pro Tips</div>
  <ul>
    <li>Use Ctrl+Shift+L to add filters to any table</li>
    <li>Use Ctrl+T to convert a range to a formatted table</li>
    <li>Named ranges make formulas readable: =SUM(Revenue) instead of =SUM(B2:B100)</li>
  </ul>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a spreadsheet of 20 student scores with name, score, and grade columns</li>
    <li>Use IF() to automatically assign grades (A=90+, B=80+, C=70+, D=60+, F=below 60)</li>
    <li>Add conditional formatting to highlight failing students in red</li>
    <li>Create a pivot table showing average score by grade</li>
  </ol>
</div>
""", 30),
        (2, "Professional Digital Communication", mod2, """
<h2>Digital Communication in the Workplace</h2>
<p>How you communicate digitally determines how you are perceived professionally. Poor digital communication is one of the top reasons people struggle in modern workplaces.</p>

<h3>Professional Email Structure</h3>
<pre><code>Subject: [Action Required] Q3 Report Review — Deadline Friday

Hi [Name],

I hope this finds you well.

[Context — one sentence]
I'm reaching out regarding the Q3 performance report due this Friday.

[Main Point — be direct]
I need your team's figures by Thursday EOD to complete the consolidation.

[Specific Ask]
Could you share the regional breakdowns by Thursday 5pm?

[Next Step]
I'll send you the final consolidated report by Friday morning.

Best regards,
[Your Name]
[Title | Company | Phone]</code></pre>

<h3>Slack & Team Messaging Best Practices</h3>
<div class="concept-box">
  <div class="cb-title">Rules for Async Communication</div>
  <ul>
    <li><strong>Use threads</strong> — always reply in thread to keep channels clean</li>
    <li><strong>Be specific</strong> — "Can you help?" is unhelpful. "Can you review the pricing section of the proposal by 3pm?" is actionable</li>
    <li><strong>Status updates</strong> — set your status so colleagues know your availability</li>
    <li><strong>Avoid @channel</strong> — only use for genuine emergencies affecting everyone</li>
  </ul>
</div>

<h3>Video Call Professionalism</h3>
<ul style="color:var(--text-2);padding-left:1.4rem;margin:.8rem 0">
  <li>Test audio and video before the meeting starts</li>
  <li>Use a neutral, tidy background or virtual background</li>
  <li>Mute yourself when not speaking in group calls</li>
  <li>Have your camera at eye level, not looking up from below</li>
  <li>Send an agenda beforehand for meetings you organise</li>
  <li>Follow up with action items and owners within 24 hours</li>
</ul>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Rewrite this email to be professional: "hey can u send me the file asap its urgent thx"</li>
    <li>Write a professional email requesting a meeting with your manager to discuss a project update</li>
    <li>Create a template for a weekly status update message</li>
  </ol>
</div>
""", 25),
        (3, "Cybersecurity — Protecting Yourself Online", mod3, """
<h2>Cybersecurity Essentials</h2>
<p>Cyber attacks are the fastest growing crime in the world. Understanding how to protect yourself and your organisation is no longer optional for any professional.</p>

<h3>Password Security</h3>
<pre><code># Weak passwords (avoid these patterns)
"password123"          — common word + numbers
"alice1990"            — name + birth year
"ilearn@2024"          — company name + year

# Strong password principles
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Unique for every account
- Use a password manager (Bitwarden, 1Password)

# Even better: passphrases
"Purple-Mango-Sunrise-47!"  — easy to remember, hard to crack</code></pre>

<h3>Phishing — The Biggest Threat</h3>
<div class="concept-box warning">
  <div class="cb-title">How to Spot a Phishing Email</div>
  <ul>
    <li><strong>Urgency</strong> — "Your account will be closed in 24 hours!"</li>
    <li><strong>Suspicious sender</strong> — support@paypa1.com (note the number 1)</li>
    <li><strong>Hover before clicking</strong> — the displayed link and actual URL don't match</li>
    <li><strong>Requests for credentials</strong> — legitimate services never ask for passwords via email</li>
    <li><strong>Generic greeting</strong> — "Dear Customer" instead of your name</li>
  </ul>
</div>

<h3>Essential Security Habits</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Habit</th><th style="padding:8px;text-align:left">Why it matters</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Enable 2FA everywhere</td><td style="padding:8px">Even if your password is stolen, attacker can't log in</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Update software regularly</td><td style="padding:8px">Patches close vulnerabilities attackers exploit</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Use a VPN on public WiFi</td><td style="padding:8px">Prevents eavesdropping on unencrypted networks</td></tr>
  <tr><td style="padding:8px">Back up your data (3-2-1 rule)</td><td style="padding:8px">3 copies, 2 different media, 1 offsite</td></tr>
</table>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Audit your 5 most important accounts — do they all have unique, strong passwords?</li>
    <li>Enable 2-factor authentication on your email account if you haven't already</li>
    <li>Look up Have I Been Pwned (haveibeenpwned.com) to check if your email was in a data breach</li>
    <li>Identify 3 phishing red flags in a suspicious email you have received</li>
  </ol>
</div>
""", 30),
        (4, "Personal Productivity Systems", mod4, """
<h2>Personal Productivity</h2>
<p>Productivity is not about working more hours — it is about achieving more of what matters. The most effective professionals use deliberate systems to manage their time, energy, and attention.</p>

<h3>The GTD System (Getting Things Done)</h3>
<pre><code>GTD has 5 steps:

1. CAPTURE — write down everything on your mind
   (use one inbox: notebook, app, or folder)

2. CLARIFY — for each item, ask:
   - Is it actionable? If no → trash, reference, or someday list
   - Can it be done in 2 minutes? If yes → do it NOW
   - Will it take longer? → schedule it or delegate it

3. ORGANISE — put tasks in the right lists
   - Next Actions (what you can do right now)
   - Projects (requires more than one step)
   - Waiting For (delegated items)
   - Calendar (date-specific)

4. REFLECT — weekly review of all lists

5. ENGAGE — choose what to work on based on context, time, energy</code></pre>

<h3>Time Blocking</h3>
<div class="concept-box">
  <div class="cb-title">Sample Productive Day Structure</div>
  <table style="width:100%;border-collapse:collapse">
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">8:00–10:00</td><td style="padding:6px">Deep Work — hardest task, no notifications</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">10:00–11:00</td><td style="padding:6px">Email & messages — process inbox</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">11:00–13:00</td><td style="padding:6px">Meetings & collaboration</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">14:00–16:00</td><td style="padding:6px">Deep Work — second focus block</td></tr>
    <tr><td style="padding:6px;color:var(--blue)">16:00–17:00</td><td style="padding:6px">Admin, planning, end-of-day review</td></tr>
  </table>
</div>

<h3>Digital Tools for Productivity</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Tool</th><th style="padding:8px;text-align:left">Best for</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Notion / Obsidian</td><td style="padding:8px">Note-taking, knowledge base, project docs</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Todoist / Things</td><td style="padding:8px">Task management, GTD implementation</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Google Calendar</td><td style="padding:8px">Time blocking, scheduling</td></tr>
  <tr><td style="padding:8px">Focus@Will / Brain.fm</td><td style="padding:8px">Background music designed for concentration</td></tr>
</table>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Do a full brain dump — write down every task, project, worry, and idea in your head right now</li>
    <li>Process each item through the GTD Clarify step</li>
    <li>Design your ideal work day using time blocking</li>
    <li>Choose one productivity tool and set it up properly with your current projects and tasks</li>
  </ol>
</div>
""", 30),
    ]

    quizzes = {
        1: [
            ("What does the Excel VLOOKUP function do?",
             "Performs vertical calculations on a column",
             "Looks up a value in a table and returns a corresponding value from another column",
             "Counts values that meet a condition", "B",
             "VLOOKUP searches for a value in the first column of a range and returns a value from a specified column in the same row."),
            ("What is the main advantage of a Pivot Table?",
             "It makes data look more colourful",
             "It summarises large datasets into meaningful aggregations without formulas",
             "It prevents editing of the original data", "B",
             "Pivot tables let you summarise, group, and analyse thousands of rows of data in seconds by dragging and dropping fields."),
        ],
        2: [
            ("What makes a professional email effective?",
             "Using lots of formatting and bullet points",
             "A clear subject, direct main point, specific ask, and stated next step",
             "Being as long and detailed as possible", "B",
             "Professional emails should respect the reader's time: clear subject, context in one sentence, one main point, one specific ask, and who does what next."),
            ("What is the best practice when replying in a team chat like Slack?",
             "Always start a new message in the main channel",
             "Reply in the thread to keep channels organised",
             "Use @channel to ensure everyone sees it", "B",
             "Threading keeps conversations organised. Starting new messages in the main channel creates noise and makes it hard to follow context."),
        ],
        3: [
            ("What is two-factor authentication (2FA)?",
             "Using two different passwords",
             "A second verification step (like a code sent to your phone) in addition to your password",
             "Logging in from two different devices", "B",
             "2FA requires something you know (password) and something you have (phone code). Even if your password is stolen, attackers cannot access your account."),
            ("Which of these is a phishing red flag?",
             "An email from your bank using your full name",
             "An email creating urgency, using a slightly wrong sender domain, and asking you to click a link",
             "A newsletter you subscribed to", "B",
             "Phishing emails typically combine urgency, suspicious sender addresses, and requests to click links or provide credentials."),
        ],
        4: [
            ("In the GTD system, what should you do with a task that takes less than 2 minutes?",
             "Add it to your project list",
             "Do it immediately",
             "Schedule it for later in the week", "B",
             "The 2-minute rule: if an action takes less than 2 minutes, do it now. The overhead of tracking it is greater than the time it takes."),
            ("What is time blocking?",
             "Blocking websites to prevent distraction",
             "Scheduling specific tasks in dedicated calendar blocks to protect focused work time",
             "Limiting the time spent on social media", "B",
             "Time blocking means assigning specific tasks to specific calendar slots, treating them like meetings you cannot miss."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid
