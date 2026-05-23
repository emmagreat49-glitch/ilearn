"""iLEARN — Career Paths course seed."""
from .helpers import insert_lessons_and_quizzes


def seed_career_paths(conn, c):
    c.execute(
        "INSERT INTO courses (title, description, icon, level, language) VALUES (?,?,?,?,?)",
        (
            "Career Paths in Tech",
            "Navigate the tech industry with confidence. Learn about the most in-demand roles, build a professional portfolio, master technical interviews, and create a career development plan.",
            "briefcase",
            "Beginner",
            "career",
        ),
    )
    cid = c.lastrowid

    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Understanding Tech Roles", 1))
    mod1 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Building Your Portfolio", 2))
    mod2 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Job Search & Interviews", 3))
    mod3 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Professional Growth", 4))
    mod4 = c.lastrowid

    lessons = [
        (1, "Tech Career Landscape — Roles & Salaries", mod1, """
<h2>The Tech Career Landscape</h2>
<p>The tech industry offers some of the highest-paying and fastest-growing career paths in the world. Understanding the landscape helps you choose the right path and set realistic expectations.</p>

<h3>Core Technical Roles</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)">
    <th style="padding:8px;text-align:left">Role</th>
    <th style="padding:8px;text-align:left">What they do</th>
    <th style="padding:8px;text-align:left">Key skills</th>
  </tr>
  <tr style="border-bottom:1px solid var(--border)">
    <td style="padding:8px">Software Engineer</td>
    <td style="padding:8px">Build and maintain software systems</td>
    <td style="padding:8px">Python/JS/Java, algorithms, system design</td>
  </tr>
  <tr style="border-bottom:1px solid var(--border)">
    <td style="padding:8px">Data Analyst</td>
    <td style="padding:8px">Analyse data to inform decisions</td>
    <td style="padding:8px">SQL, Excel/Python, statistics, visualisation</td>
  </tr>
  <tr style="border-bottom:1px solid var(--border)">
    <td style="padding:8px">Data Scientist</td>
    <td style="padding:8px">Build predictive models and ML systems</td>
    <td style="padding:8px">Python, ML, statistics, communication</td>
  </tr>
  <tr style="border-bottom:1px solid var(--border)">
    <td style="padding:8px">UX/UI Designer</td>
    <td style="padding:8px">Design user experiences and interfaces</td>
    <td style="padding:8px">Figma, user research, prototyping</td>
  </tr>
  <tr style="border-bottom:1px solid var(--border)">
    <td style="padding:8px">Product Manager</td>
    <td style="padding:8px">Define what to build and why</td>
    <td style="padding:8px">Strategy, communication, analytics, empathy</td>
  </tr>
  <tr>
    <td style="padding:8px">DevOps / Cloud Engineer</td>
    <td style="padding:8px">Deploy and maintain infrastructure</td>
    <td style="padding:8px">AWS/GCP, Docker, Kubernetes, CI/CD</td>
  </tr>
</table>

<h3>Choosing Your Path</h3>
<div class="concept-box">
  <div class="cb-title">Questions to Guide Your Choice</div>
  <ol>
    <li>Do you prefer building things or analysing things?</li>
    <li>Are you more comfortable with people or with code?</li>
    <li>Do you prefer depth (expert in one area) or breadth (knowing many areas)?</li>
    <li>What problems do you find genuinely interesting?</li>
    <li>What lifestyle do you want? (startups vs corporations, remote vs office)</li>
  </ol>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Research average salaries for 3 tech roles in your country using LinkedIn Salary or Glassdoor</li>
    <li>For each role, list 5 companies in your country that hire for it</li>
    <li>Based on the questions above, write a paragraph explaining which path interests you most and why</li>
  </ol>
</div>
""", 25),
        (2, "Building a Professional Portfolio", mod2, """
<h2>Building Your Portfolio</h2>
<p>Your portfolio is your most important career asset. It shows employers what you can actually do, not just what you claim on a CV.</p>

<h3>What to Include</h3>
<div class="concept-box">
  <div class="cb-title">Portfolio Components</div>
  <ul>
    <li><strong>Personal site</strong> — yourname.dev or GitHub Pages (free)</li>
    <li><strong>GitHub profile</strong> — with a complete README and pinned repos</li>
    <li><strong>3–5 projects</strong> — quality over quantity, with descriptions and live demos</li>
    <li><strong>LinkedIn</strong> — complete profile with skills, certifications, recommendations</li>
    <li><strong>CV/Resume</strong> — one page, ATS-friendly format</li>
  </ul>
</div>

<h3>What Makes a Strong Project</h3>
<pre><code>A good portfolio project has:

1. A clear problem it solves
   "I built X to help [specific user] do [specific thing]"

2. Real technology used correctly
   - Not just tutorials copied verbatim
   - Demonstrates decision-making and problem-solving

3. Clean, documented code
   - README explaining the project, how to run it, decisions made
   - Comments explaining non-obvious logic

4. Live demo or screenshots
   - Deploy it! Employers want to see it working

5. Challenges you faced and how you solved them
   - Shows growth mindset and persistence</code></pre>

<h3>GitHub Profile README</h3>
<pre><code># Hi, I'm Alice 👋

## About Me
- Data Analyst at XYZ | iLEARN Graduate
- Passionate about turning data into decisions

## Tech Stack
Python | Pandas | SQL | Tableau | Excel

## Featured Projects
- [Sales Dashboard](link) — Interactive dashboard analysing 2 years of retail data
- [Student Performance Model](link) — ML model predicting exam outcomes

## Currently Learning
Machine Learning with scikit-learn</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a GitHub account (if you don't have one) and set up your profile README</li>
    <li>Choose one project you have built during this course — write a clear README for it</li>
    <li>Deploy one project to GitHub Pages or Netlify so it is live online</li>
    <li>Update your LinkedIn with your skills and link to your GitHub</li>
  </ol>
</div>
""", 30),
        (3, "Job Search Strategy & Technical Interviews", mod3, """
<h2>Job Search & Technical Interviews</h2>
<p>Getting a tech job is a skill in itself. Most candidates are rejected not because they lack skills, but because they approach the process poorly. This lesson covers proven strategies.</p>

<h3>Job Search Strategy</h3>
<div class="concept-box">
  <div class="cb-title">The 70/30 Rule</div>
  <p>70% of jobs are never publicly advertised. Focus on:</p>
  <ul>
    <li><strong>Network</strong> — reach out to people in roles you want. Ask for a 20-minute call, not a job.</li>
    <li><strong>LinkedIn</strong> — connect with recruiters, engage with content in your field</li>
    <li><strong>Job boards</strong> — LinkedIn Jobs, Indeed, company career pages directly</li>
    <li><strong>Referrals</strong> — ask your network if they know of openings. Employee referrals get 5x more interviews.</li>
  </ul>
</div>

<h3>Tailoring Your Application</h3>
<pre><code>For every application:

1. Read the job description carefully
2. Identify the 5 most important requirements
3. Ensure your CV uses their exact keywords (ATS systems filter by keywords)
4. Write a cover letter that connects your specific experience to their specific needs
5. Research the company — know their product, values, and recent news

Generic applications get generic responses (none).</code></pre>

<h3>Technical Interview Types</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Type</th><th style="padding:8px;text-align:left">What to expect</th><th style="padding:8px;text-align:left">Preparation</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Coding challenge</td><td style="padding:8px">Solve a problem in code (30–60 min)</td><td style="padding:8px">Practice on HackerRank, LeetCode</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Take-home project</td><td style="padding:8px">Build something over 2–7 days</td><td style="padding:8px">Treat it like a real deliverable</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Whiteboard/system design</td><td style="padding:8px">Design a system or architecture</td><td style="padding:8px">Study system design patterns</td></tr>
  <tr><td style="padding:8px">Behavioural</td><td style="padding:8px">Tell me about a time when…</td><td style="padding:8px">Prepare 8–10 STAR stories</td></tr>
</table>

<h3>The STAR Method</h3>
<pre><code>STAR = Situation, Task, Action, Result

Q: "Tell me about a time you solved a difficult problem."

S: "During my final year project, our app had a critical bug..."
T: "I was responsible for the authentication system."
A: "I debugged the issue by adding logging, identified a race condition..."
R: "Fixed it in 4 hours, app passed all tests, project got an A."</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Write 5 STAR stories from your academic or work experience</li>
    <li>Find 3 job postings for roles you want — identify the top 5 keywords in each</li>
    <li>Practice a 30-minute coding challenge on HackerRank</li>
    <li>Research one company you'd like to work for and write a tailored cover letter opening paragraph</li>
  </ol>
</div>
""", 35),
        (4, "Professional Growth & Continuous Learning", mod4, """
<h2>Professional Growth</h2>
<p>The tech industry moves fast. The professionals who thrive long-term are not those with the most knowledge today, but those with the best systems for continuously learning and growing.</p>

<h3>The T-Shaped Professional</h3>
<div class="concept-box">
  <div class="cb-title">T-Shape Model</div>
  <p>The most valuable professionals have:</p>
  <ul>
    <li><strong>Depth</strong> (the vertical bar) — deep expertise in one or two core areas</li>
    <li><strong>Breadth</strong> (the horizontal bar) — working knowledge of adjacent skills</li>
  </ul>
  <p>Example: A data analyst with deep expertise in Python and SQL, but also working knowledge of machine learning, data engineering, and business strategy.</p>
</div>

<h3>Creating a Learning System</h3>
<pre><code>Weekly learning routine:

Monday   — Read 1 technical article in your field (30 min)
Wednesday — Work on a side project or tutorial (60 min)
Friday   — Engage with community: answer a question on Stack Overflow,
            post something on LinkedIn, or attend a meetup

Monthly:
- Complete one online course section
- Read one book chapter (technical or career-related)
- Connect with 5 people in your field on LinkedIn

Annually:
- Attend one conference or large online event
- Review and update your portfolio
- Set 3 professional goals for the next year</code></pre>

<h3>Building Your Personal Brand</h3>
<pre><code>Why it matters:
"Your reputation precedes you. Build it deliberately."

How to start:
1. Pick one platform (LinkedIn is best for most tech roles)
2. Post about what you are learning — weekly
3. Share projects and what you learned building them
4. Comment thoughtfully on others' posts
5. Write case studies of problems you have solved

The goal is not followers — it is to be known in your field
so opportunities find you rather than you chasing them.</code></pre>

<div class="concept-box">
  <div class="cb-title">Resources for Continuous Learning</div>
  <table style="width:100%;border-collapse:collapse">
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">Coursera / edX</td><td style="padding:6px">University-quality courses, many free to audit</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">YouTube</td><td style="padding:6px">Sentdex, Corey Schafer, Traversy Media, freeCodeCamp</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:6px;color:var(--blue)">Newsletters</td><td style="padding:6px">Morning Brew, Data Elixir, TLDR, JavaScript Weekly</td></tr>
    <tr><td style="padding:6px;color:var(--blue)">Communities</td><td style="padding:6px">Dev.to, Hashnode, Discord servers, local meetups</td></tr>
  </table>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Draw your own T-shape: what is your current depth? What breadth areas do you want to build?</li>
    <li>Design a weekly learning routine you can realistically maintain</li>
    <li>Write your first LinkedIn post sharing something you learned in this course</li>
    <li>Set 3 professional goals for the next 12 months using the SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound)</li>
  </ol>
</div>
""", 30),
    ]

    quizzes = {
        1: [
            ("What is the main difference between a Data Analyst and a Data Scientist?",
             "Data Analysts earn more",
             "Data Analysts focus on analysing historical data for insights; Data Scientists build predictive models",
             "They are the same role", "B",
             "Data Analysts primarily work with existing data to answer business questions. Data Scientists build ML models to predict future outcomes."),
            ("Which factor should guide your choice of tech career path?",
             "Which role pays the most",
             "A combination of your interests, strengths, and lifestyle preferences",
             "Which role is easiest to get into", "B",
             "The best career path is one that aligns with what you find genuinely interesting and are willing to work hard at, not just the highest salary."),
        ],
        2: [
            ("What makes a portfolio project stand out to employers?",
             "Using the latest and most complex technology",
             "A clear problem statement, real implementation, clean code, live demo, and documentation",
             "Having the most lines of code", "B",
             "Employers want to see you can solve real problems, write maintainable code, and communicate your work clearly — not just complexity for its own sake."),
            ("What should a GitHub profile README include?",
             "A list of all your university grades",
             "A brief bio, tech stack, featured projects with links, and what you're currently learning",
             "Only your work history", "B",
             "A good profile README tells visitors who you are, what you can do, and what you're building — turning your GitHub into a professional landing page."),
        ],
        3: [
            ("What is the STAR method used for?",
             "Structuring technical code documentation",
             "Answering behavioural interview questions with Situation, Task, Action, Result",
             "Rating job applications", "B",
             "STAR gives a clear structure for telling professional stories in interviews, ensuring you cover context, your role, what you did, and the outcome."),
            ("Why should you tailor every job application?",
             "It takes less time than a generic application",
             "ATS systems filter by keywords, and personalised applications show genuine interest",
             "Employers prefer longer applications", "B",
             "Most applications are filtered by Applicant Tracking Systems before a human reads them. Using the exact keywords from the job description improves your chances significantly."),
        ],
        4: [
            ("What is the T-shaped professional model?",
             "A professional with exactly two skills",
             "Deep expertise in one area combined with broad working knowledge of adjacent areas",
             "A professional who changes careers every year", "B",
             "T-shaped professionals are highly valued because they can contribute deeply in their core area while collaborating effectively across teams with different specialisations."),
            ("What is the most effective way to build a personal brand in tech?",
             "Collecting as many LinkedIn connections as possible",
             "Consistently sharing what you are learning and building, demonstrating real expertise over time",
             "Posting every day regardless of content quality", "B",
             "Reputation is built through consistently demonstrating knowledge and helping others, not through follower counts. Quality and consistency over time is what matters."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid
