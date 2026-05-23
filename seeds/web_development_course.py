"""iLEARN — Web Development course seed."""
from .helpers import insert_lessons_and_quizzes


def seed_web_development(conn, c):
    c.execute(
        "INSERT INTO courses (title, description, icon, level, language) VALUES (?,?,?,?,?)",
        (
            "Web Development",
            "Build real websites and web applications from scratch. Covers HTML structure, CSS styling, JavaScript interactivity, and modern development practices used in the industry.",
            "code-2",
            "Beginner to Intermediate",
            "web_dev",
        ),
    )
    cid = c.lastrowid

    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "HTML — Structure", 1))
    mod1 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "CSS — Styling & Layout", 2))
    mod2 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "JavaScript — Interactivity", 3))
    mod3 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Building Real Projects", 4))
    mod4 = c.lastrowid

    lessons = [
        (1, "HTML Foundations", mod1, """
<h2>HTML Foundations</h2>
<p>HTML (HyperText Markup Language) is the skeleton of every web page. It defines the structure and meaning of content using elements called tags.</p>

<h3>Document Structure</h3>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
  &lt;title&gt;My First Page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Hello, World!&lt;/h1&gt;
  &lt;p&gt;This is my first web page.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h3>Essential Tags</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Tag</th><th style="padding:8px;text-align:left">Purpose</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px"><code>&lt;h1&gt;–&lt;h6&gt;</code></td><td style="padding:8px">Headings (h1 = most important)</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px"><code>&lt;p&gt;</code></td><td style="padding:8px">Paragraph</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px"><code>&lt;a href=""&gt;</code></td><td style="padding:8px">Link</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px"><code>&lt;img src="" alt=""&gt;</code></td><td style="padding:8px">Image</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px"><code>&lt;ul&gt; / &lt;ol&gt; / &lt;li&gt;</code></td><td style="padding:8px">Lists</td></tr>
  <tr><td style="padding:8px"><code>&lt;div&gt; / &lt;span&gt;</code></td><td style="padding:8px">Generic containers</td></tr>
</table>

<h3>Semantic HTML</h3>
<pre><code>&lt;header&gt;  — top of page (logo, nav)
&lt;nav&gt;     — navigation links
&lt;main&gt;    — primary content
&lt;section&gt; — thematic group of content
&lt;article&gt; — self-contained piece (blog post, card)
&lt;aside&gt;   — secondary content (sidebar)
&lt;footer&gt;  — bottom of page</code></pre>

<div class="concept-box">
  <div class="cb-title">Why Semantic HTML Matters</div>
  <p>Semantic tags improve accessibility (screen readers understand your page), SEO (search engines rank you higher), and code readability. Never use &lt;div&gt; for everything.</p>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create an HTML file with a proper &lt;!DOCTYPE&gt;, &lt;head&gt;, and &lt;body&gt;</li>
    <li>Add a navigation bar using &lt;nav&gt; with 3 links</li>
    <li>Add a &lt;main&gt; section with a heading, paragraph, and image</li>
    <li>Add a &lt;footer&gt; with your name</li>
  </ol>
</div>
""", 25),
        (2, "CSS — Styling, Flexbox & Grid", mod2, """
<h2>CSS — Cascading Style Sheets</h2>
<p>CSS controls the visual presentation of HTML. It is what makes a page look professional instead of plain text.</p>

<h3>The Box Model</h3>
<pre><code>.card {
  width: 300px;
  padding: 20px;      /* space inside the border */
  border: 2px solid #ccc;
  margin: 16px;       /* space outside the border */
  box-sizing: border-box; /* padding included in width */
}</code></pre>

<h3>Flexbox — One Dimension</h3>
<pre><code>.navbar {
  display: flex;
  justify-content: space-between; /* main axis */
  align-items: center;            /* cross axis */
  gap: 1rem;
  padding: 1rem 2rem;
}

/* justify-content: flex-start | flex-end | center | space-between | space-around */
/* align-items:     flex-start | flex-end | center | stretch | baseline */</code></pre>

<h3>CSS Grid — Two Dimensions</h3>
<pre><code>.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 equal columns */
  gap: 1.5rem;
}

/* Auto-responsive grid (no media queries needed) */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}</code></pre>

<h3>Responsive Design</h3>
<pre><code>/* Mobile-first approach */
.container { width: 100%; padding: 1rem; }

@media (min-width: 768px) {
  .container { max-width: 1200px; margin: 0 auto; }
}

/* CSS Custom Properties */
:root {
  --primary: #4facfe;
  --bg: #060b14;
  --radius: 12px;
}
.btn { background: var(--primary); border-radius: var(--radius); }</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Style the HTML page from Lesson 1 — add fonts, colours, and spacing</li>
    <li>Build a responsive navigation bar using Flexbox</li>
    <li>Create a 3-column card grid using CSS Grid that collapses to 1 column on mobile</li>
    <li>Define 5 CSS custom properties (variables) and use them throughout your styles</li>
  </ol>
</div>
""", 35),
        (3, "JavaScript — DOM & Interactivity", mod3, """
<h2>JavaScript — Making Pages Interactive</h2>
<p>JavaScript is the programming language of the web. It runs in the browser and allows you to respond to user actions, update content, and build dynamic applications.</p>

<h3>The DOM</h3>
<pre><code>// Select elements
const btn    = document.getElementById("my-btn")
const cards  = document.querySelectorAll(".card")
const title  = document.querySelector("h1")

// Change content and style
title.textContent = "Updated Title"
title.style.color = "#4facfe"

// Add and remove CSS classes
btn.classList.add("active")
btn.classList.remove("hidden")
btn.classList.toggle("open")</code></pre>

<h3>Events</h3>
<pre><code>// Click event
btn.addEventListener("click", function() {
  console.log("Button clicked!")
})

// Input event
const input = document.querySelector("#search")
input.addEventListener("input", function(e) {
  console.log("Typed:", e.target.value)
})

// Form submission
const form = document.querySelector("form")
form.addEventListener("submit", function(e) {
  e.preventDefault()  // stop page reload
  const data = new FormData(form)
  console.log(data.get("name"))
})</code></pre>

<h3>Fetch API — Getting Data</h3>
<pre><code>// GET request
async function loadUsers() {
  const response = await fetch("https://jsonplaceholder.typicode.com/users")
  const users    = await response.json()
  users.forEach(user => {
    const li = document.createElement("li")
    li.textContent = user.name
    document.querySelector("#list").appendChild(li)
  })
}

loadUsers()</code></pre>

<div class="concept-box warning">
  <div class="cb-title">Always Use === Not ==</div>
  <p>The == operator performs type coercion which leads to bugs. <code>"5" == 5</code> is true in JavaScript, which is almost never what you want. Always use === for comparisons.</p>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a button that changes the background colour of the page when clicked</li>
    <li>Build a live character counter for a textarea input</li>
    <li>Fetch data from <code>https://jsonplaceholder.typicode.com/posts</code> and display the first 5 titles in a list</li>
    <li>Build a simple to-do list where you can add and remove items</li>
  </ol>
</div>
""", 35),
        (4, "Building a Complete Web Project", mod4, """
<h2>Building a Complete Web Project</h2>
<p>Now that you know HTML, CSS, and JavaScript, it is time to combine them into a real project. We will build a personal portfolio page — one of the most important things a developer can have.</p>

<h3>Project Structure</h3>
<pre><code>portfolio/
├── index.html
├── style.css
└── main.js</code></pre>

<h3>index.html</h3>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
  &lt;title&gt;My Portfolio&lt;/title&gt;
  &lt;link rel="stylesheet" href="style.css"&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;nav class="navbar"&gt;
    &lt;div class="brand"&gt;YourName.dev&lt;/div&gt;
    &lt;ul&gt;
      &lt;li&gt;&lt;a href="#about"&gt;About&lt;/a&gt;&lt;/li&gt;
      &lt;li&gt;&lt;a href="#projects"&gt;Projects&lt;/a&gt;&lt;/li&gt;
      &lt;li&gt;&lt;a href="#contact"&gt;Contact&lt;/a&gt;&lt;/li&gt;
    &lt;/ul&gt;
  &lt;/nav&gt;

  &lt;section id="about" class="hero"&gt;
    &lt;h1&gt;Hi, I'm &lt;span class="highlight"&gt;Alice&lt;/span&gt;&lt;/h1&gt;
    &lt;p&gt;Web Developer &amp; Data Analyst&lt;/p&gt;
    &lt;a href="#projects" class="btn"&gt;View My Work&lt;/a&gt;
  &lt;/section&gt;

  &lt;section id="projects" class="projects"&gt;
    &lt;h2&gt;Projects&lt;/h2&gt;
    &lt;div class="card-grid" id="project-grid"&gt;&lt;/div&gt;
  &lt;/section&gt;

  &lt;script src="main.js"&gt;&lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h3>main.js — Dynamic Project Cards</h3>
<pre><code>const projects = [
  { title: "Data Dashboard",   tech: "Python, Pandas",      link: "#" },
  { title: "Portfolio Site",   tech: "HTML, CSS, JS",       link: "#" },
  { title: "Task Manager App", tech: "JavaScript, LocalStorage", link: "#" },
]

const grid = document.getElementById("project-grid")

projects.forEach(p => {
  grid.innerHTML += `
    &lt;div class="card"&gt;
      &lt;h3&gt;${p.title}&lt;/h3&gt;
      &lt;p class="tech"&gt;${p.tech}&lt;/p&gt;
      &lt;a href="${p.link}" class="btn-sm"&gt;View →&lt;/a&gt;
    &lt;/div&gt;
  `
})</code></pre>

<div class="concept-box">
  <div class="cb-title">Deploying for Free</div>
  <p>Once your project is ready, deploy it for free on <strong>GitHub Pages</strong> or <strong>Netlify</strong>. Push your code to GitHub, connect it to Netlify, and your site is live in minutes.</p>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Build the complete portfolio page described above</li>
    <li>Add a dark/light mode toggle using JavaScript and CSS custom properties</li>
    <li>Add a contact form with validation (name, email, message all required)</li>
    <li>Deploy it to GitHub Pages or Netlify</li>
  </ol>
</div>
""", 40),
    ]

    quizzes = {
        1: [
            ("What is the correct HTML document structure?",
             "head inside body", "DOCTYPE, then html containing head and body", "body before head", "B",
             "A valid HTML document must have DOCTYPE, then an html element containing head (metadata) and body (visible content)."),
            ("Which tag makes a navigation landmark for screen readers?",
             "&lt;div class='nav'&gt;", "&lt;nav&gt;", "&lt;menu&gt;", "B",
             "The semantic &lt;nav&gt; element tells screen readers and search engines that this section contains navigation links."),
        ],
        2: [
            ("Which CSS property controls alignment along the MAIN axis in Flexbox?",
             "align-items", "justify-content", "flex-wrap", "B",
             "justify-content controls the main axis (horizontal in row, vertical in column). align-items controls the cross axis."),
            ("What does box-sizing: border-box do?",
             "Removes the border from elements",
             "Includes padding and border in the element's total width",
             "Adds a box shadow", "B",
             "Without border-box, padding is added ON TOP of the specified width. With it, padding is included in the width, making sizing predictable."),
        ],
        3: [
            ("What does e.preventDefault() do in a form submit handler?",
             "Submits the form faster",
             "Stops the browser from reloading the page on form submission",
             "Validates the form fields", "B",
             "By default, submitting a form causes a page reload. e.preventDefault() stops this, letting you handle the data with JavaScript instead."),
            ("What does === check compared to ==?",
             "=== is slower but more accurate",
             "=== checks both value AND type; == only checks value with type coercion",
             "They are identical", "B",
             "== coerces types ('5' == 5 is true). === does not ('5' === 5 is false). Always use === to avoid unexpected bugs."),
        ],
        4: [
            ("What is the correct way to link a CSS file to an HTML page?",
             "&lt;style src='style.css'&gt;",
             "&lt;link rel='stylesheet' href='style.css'&gt;",
             "&lt;css href='style.css'&gt;", "B",
             "The link element with rel='stylesheet' in the head section connects an external CSS file to the HTML page."),
            ("Which free platform can you use to deploy a static website?",
             "Only paid services support deployment",
             "GitHub Pages or Netlify",
             "You need a physical server", "B",
             "GitHub Pages and Netlify both offer free hosting for static websites. You can deploy directly from a GitHub repository."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid
