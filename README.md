# iLEARN — Interactive E-Learning Platform

A full-stack e-learning web application built as a final year project.

## Tech Stack
- **Backend:**  Python 3 · Flask · SQLite
- **Frontend:** HTML5 · CSS3 · Vanilla JavaScript
- **Auth:**     Session-based login · SHA-256 password hashing
- **APIs:**     RESTful JSON endpoints · Browser Notification API

## Features
- User registration & login (public sign-up, anyone can create a profile)
- 5 courses · 36 deep lessons · 72 quiz questions
- Animated lessons: typewriter code blocks, flip cards, step-by-step walkthroughs
- Progress tracking per lesson and per course
- Browser push notifications for study reminders
- AI study assistant chatbot (keyword-based; ready for OpenAI/Claude integration)
- Fully responsive design

## Courses
| Course | Lessons | Quiz Qs |
|---|---|---|
| 🐍 Python Programming | 8 | 18 |
| ⚡ JavaScript | 8 | 15 |
| 🎨 CSS & Web Design | 7 | 13 |
| ☕ Java Programming | 7 | 15 |
| 📊 Data Science & Analytics | 6 | 11 |

## Setup & Running

### 1. Install Python dependency
```
pip install flask
```

### 2. Run the server
```
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

### Default admin account
- Username: `admin`
- Password: `ilearn123`

Or click **Create Account** to register your own profile.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/complete_lesson` | Mark a lesson as complete |
| GET  | `/api/reminders` | Get all reminders for current user |
| POST | `/api/add_reminder` | Create a new study reminder |
| DELETE | `/api/delete_reminder/<id>` | Delete a reminder |
| POST | `/api/chat` | AI chatbot query |
| GET  | `/api/progress` | Overall progress data |

## Project Structure
```
ilearn/
├── app.py              ← Flask app, all routes, DB init, seed data
├── database.db         ← Auto-created on first run
├── requirements.txt
├── templates/
│   ├── login.html      ← Login + register (tabbed, single page)
│   ├── dashboard.html  ← Home page with course cards and reminders
│   ├── course.html     ← Course overview with lesson list
│   ├── lesson.html     ← Lesson content + quiz + AI chatbot
│   └── quiz.html       ← Standalone quiz page
├── static/
│   ├── css/main.css    ← Full design system (CSS variables, animations)
│   └── js/main.js      ← Toast, Quiz, Chatbot, Reminders, Notification API
└── models/
    ├── user.py
    └── course.py
```
