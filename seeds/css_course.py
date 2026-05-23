"""iLEARN — CSS & Web Design course seed data."""
from .helpers import insert_lessons_and_quizzes

def seed_css(conn, c):
    c.execute("INSERT INTO courses (title,description,icon,level,language) VALUES (?,?,?,?,?)",
              ("CSS & Web Design","Go beyond basic styling. Master the Box Model, Specificity, Flexbox, CSS Grid, responsive design with media queries, and professional animation techniques used in real products.","🎨","Beginner to Advanced","css"))
    cid = c.lastrowid

    lessons = [
        (1,"The Box Model, Cascade & Specificity","""
<h2>The CSS Box Model</h2>
<p>Every HTML element is rendered as a <strong>rectangular box</strong>. Understanding how that box is constructed is fundamental to being able to predict and control layout. The CSS Box Model has four layers, from inside out:</p>

<table class="lesson-table">
  <tr><th>Layer</th><th>What It Is</th><th>CSS Properties</th></tr>
  <tr><td><strong>Content</strong></td><td>Actual text, image, or child element area</td><td>width, height, min-width, max-width</td></tr>
  <tr><td><strong>Padding</strong></td><td>Space between content and border (inside the border)</td><td>padding, padding-top/right/bottom/left</td></tr>
  <tr><td><strong>Border</strong></td><td>Visible outline of the element</td><td>border, border-width, border-style, border-color</td></tr>
  <tr><td><strong>Margin</strong></td><td>Space outside the border (gap between elements)</td><td>margin, margin-top/right/bottom/left</td></tr>
</table>

<div class="code-block"><pre><code>.card {
    width: 320px;
    height: auto;

    padding: 24px;              /* All sides */
    padding: 16px 24px;         /* Vertical | Horizontal */
    padding: 8px 16px 12px 20px;/* Top Right Bottom Left — clock order */

    border: 2px solid #00d4b4;
    border-radius: 12px;        /* Rounds corners */
    border-top: 4px solid red;  /* Individual sides */

    margin: 0 auto;             /* 0 top/bottom, auto left/right = centres */
    margin-bottom: 1.5rem;
}

/* ── box-sizing — the most important reset ──
   By default (content-box), padding and border ADD to the width.
   A 320px element with 24px padding becomes 368px wide. Confusing!

   border-box makes width INCLUDE padding and border.
   This is so essential it's applied universally in all modern projects: */
*,
*::before,
*::after {
    box-sizing: border-box;
}</code></pre></div>

<h3>The Cascade and Specificity</h3>
<p>When multiple CSS rules target the same element, the browser uses three factors to decide which wins: <strong>Origin</strong> (where the CSS comes from), <strong>Specificity</strong> (how targeted the selector is), and <strong>Order</strong> (which comes last).</p>

<div class="code-block"><pre><code>/* Specificity is calculated as a 4-part score: (inline, ID, class, element)

   element    p           = (0, 0, 0, 1)   score: 1
   class      .card        = (0, 0, 1, 0)   score: 10
   ID         #header      = (0, 1, 0, 0)   score: 100
   inline     style=""     = (1, 0, 0, 0)   score: 1000
   !important               = always wins (use very sparingly)
*/

/* Examples */
p                { color: black; }      /* (0,0,0,1) */
.highlight       { color: blue;  }      /* (0,0,1,0) — wins over p */
#main .highlight { color: teal;  }      /* (0,1,1,0) — wins over .highlight */

/* When specificity is EQUAL, the last rule in the file wins */
.card { background: red; }
.card { background: blue; }   /* This one applies */

/* Pseudo-classes count as a class */
a:hover              { color: teal;  }  /* (0,0,1,1) */
nav a:hover          { color: amber; }  /* (0,0,1,2) — wins */

/* Pseudo-elements count as element */
p::first-line        { font-size: 1.2em; }  /* (0,0,0,2) */</code></pre></div>
        """,20),

        (2,"Flexbox — One-Dimensional Layouts","""
<h2>CSS Flexbox</h2>
<p>Flexbox (Flexible Box Layout Module) is a <strong>one-dimensional layout model</strong> — it handles items along a single axis (row or column) at a time. It eliminates the need for float hacks and makes alignment, spacing, and ordering trivially simple.</p>

<h3>Core Concept: Container and Items</h3>
<p>Flexbox works in two levels: the <strong>flex container</strong> (parent) and <strong>flex items</strong> (direct children). All flex properties apply to one or the other — not both.</p>

<div class="code-block"><pre><code">/* ── CONTAINER PROPERTIES ── */
.container {
    display: flex;       /* or inline-flex */

    /* Direction of main axis */
    flex-direction: row;             /* → default */
    flex-direction: row-reverse;     /* ← */
    flex-direction: column;          /* ↓ */
    flex-direction: column-reverse;  /* ↑ */

    /* Allow items to wrap to next line */
    flex-wrap: nowrap;    /* Default — single line */
    flex-wrap: wrap;      /* Multi-line */

    /* Shorthand */
    flex-flow: row wrap;

    /* MAIN axis alignment (direction of flex-direction) */
    justify-content: flex-start;    /* Pack at start */
    justify-content: flex-end;      /* Pack at end */
    justify-content: center;        /* Centre */
    justify-content: space-between; /* First/last at edges, rest equal gaps */
    justify-content: space-around;  /* Equal space around each item */
    justify-content: space-evenly;  /* Exactly equal space everywhere */

    /* CROSS axis alignment (perpendicular to main) */
    align-items: stretch;    /* Default — fill cross-axis */
    align-items: flex-start; /* Align to top (if row) */
    align-items: flex-end;   /* Align to bottom */
    align-items: center;     /* Centre on cross axis */
    align-items: baseline;   /* Align text baselines */

    /* Gap between items */
    gap: 24px;
    gap: 16px 32px;   /* row-gap column-gap */
}</code></pre></div>

<div class="code-block"><pre><code">/* ── ITEM PROPERTIES ── */
.item {
    /* flex-grow: proportion of EXTRA space to consume (default 0) */
    flex-grow: 1;      /* Take all available space */
    flex-grow: 2;      /* Take twice as much as flex-grow:1 siblings */

    /* flex-shrink: how much to shrink when space is TIGHT (default 1) */
    flex-shrink: 0;    /* Never shrink (useful for fixed sidebars) */

    /* flex-basis: initial size before grow/shrink is applied */
    flex-basis: 200px;  /* Start at 200px, then flex */
    flex-basis: 0;      /* Start at 0, grow based on flex-grow */
    flex-basis: auto;   /* Use natural content size */

    /* Shorthand: grow shrink basis */
    flex: 1;            /* = 1 1 0 — grow, shrink, basis 0 */
    flex: 0 0 260px;    /* Fixed 260px, no grow or shrink */
    flex: none;         /* = 0 0 auto — completely rigid */

    /* Override align-items for just this item */
    align-self: center;

    /* Reorder visually (without changing HTML) */
    order: 2;           /* Default is 0; lower = earlier */
}

/* ── Real-world patterns ── */
/* Navbar */
nav { display: flex; justify-content: space-between; align-items: center; }

/* Equal-width columns */
.cols > * { flex: 1; }

/* Fixed sidebar + fluid main */
.layout  { display: flex; }
.sidebar { flex: 0 0 260px; }  /* Fixed 260px */
.main    { flex: 1; overflow: hidden; }

/* Perfect centring */
.centre { display: flex; justify-content: center; align-items: center; min-height: 100vh; }</code></pre></div>
        """,25),

        (3,"CSS Grid — Two-Dimensional Layouts","""
<h2>CSS Grid Layout</h2>
<p>CSS Grid is a <strong>two-dimensional layout system</strong> — it controls rows AND columns simultaneously. While Flexbox is ideal for one-dimensional components (navbars, card rows), Grid is designed for complete page layouts and complex two-dimensional arrangements.</p>

<h3>Defining the Grid</h3>
<div class="code-block"><pre><code">.container {
    display: grid;

    /* Define columns */
    grid-template-columns: 200px 1fr 1fr;          /* Fixed + flexible */
    grid-template-columns: repeat(3, 1fr);          /* 3 equal columns */
    grid-template-columns: repeat(4, minmax(0, 1fr)); /* Equal, no overflow */
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* Responsive! */

    /* Define rows */
    grid-template-rows: auto 1fr auto;   /* header, main, footer */
    grid-auto-rows: minmax(100px, auto); /* Auto-created rows get min height */

    /* Gap */
    gap: 24px;
    column-gap: 32px;
    row-gap: 16px;
}

/* Named grid areas — reads like a visual layout */
.page {
    display: grid;
    grid-template-areas:
        "header  header  header"
        "sidebar main    main  "
        "sidebar footer  footer";
    grid-template-columns: 240px 1fr 1fr;
    grid-template-rows: 64px 1fr 48px;
    min-height: 100vh;
}

/* Assign elements to areas */
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }</code></pre></div>

<h3>Placing and Spanning Items</h3>
<div class="code-block"><pre><code">.featured {
    /* grid-column: start-line / end-line */
    grid-column: 1 / 3;       /* From line 1 to line 3 (spans 2 tracks) */
    grid-column: 2 / -1;      /* From column 2 to the last line */

    /* Using span keyword */
    grid-column: span 2;       /* Take 2 column tracks */
    grid-row: span 3;          /* Take 3 row tracks */

    /* Shorthand: row-start / col-start / row-end / col-end */
    grid-area: 1 / 1 / 3 / 3;
}

/* Alignment WITHIN grid cells */
.item {
    justify-self: center;    /* Horizontal alignment in cell */
    align-self: end;         /* Vertical alignment in cell */
}

/* Alignment of ALL items */
.container {
    justify-items: center;
    align-items: center;
}

/* Auto-placement algorithm */
.masonry-like {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-auto-flow: dense;  /* Fill gaps when items span multiple tracks */
}</code></pre></div>
        """,25),

        (4,"Responsive Design, Custom Properties & Animations","""
<h2>Responsive Design</h2>
<p>A responsive layout adapts to any screen size — mobile, tablet, desktop, 4K monitor. The three pillars are: <em>fluid grids</em>, <em>flexible images</em>, and <em>media queries</em>. The modern approach is <strong>mobile-first</strong>.</p>

<h3>Media Queries</h3>
<div class="code-block"><pre><code">/* Mobile-first: write mobile styles without a query,
   then progressively ENHANCE for larger screens */

/* Base (mobile — no query needed) */
.container { padding: 1rem; }
.grid { grid-template-columns: 1fr; }
.sidebar { display: none; }

/* Small tablets (640px+) */
@media (min-width: 640px) {
    .container { padding: 1.5rem; }
    .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktops (1024px+) */
@media (min-width: 1024px) {
    .container { max-width: 1200px; margin: 0 auto; }
    .grid { grid-template-columns: repeat(3, 1fr); }
    .sidebar { display: block; }
}

/* Other media features */
@media (prefers-color-scheme: dark)  { /* Dark mode styles */ }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
@media print { .navbar, .sidebar { display: none; } }
@media (orientation: landscape) { /* Landscape mobile */ }</code></pre></div>

<h3>CSS Custom Properties (Variables)</h3>
<div class="code-block"><pre><code">/* Define on :root for global scope */
:root {
    --color-primary:  #00d4b4;
    --color-bg:       #0d1b2a;
    --color-surface:  #162233;
    --color-text:     #e8edf2;
    --font-display:   'Sora', sans-serif;
    --radius:         12px;
    --shadow:         0 4px 24px rgba(0,0,0,0.4);
    --transition:     all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Use them everywhere */
.card {
    background:    var(--color-surface);
    border-radius: var(--radius);
    box-shadow:    var(--shadow);
    transition:    var(--transition);
}
.card:hover { background: var(--color-primary); }

/* Override for components or themes */
.dark-card { --color-surface: #0a1628; }

/* Update with JavaScript */
document.documentElement.style.setProperty("--color-primary", "#ff6b6b");</code></pre></div>

<h3>Transitions and Animations</h3>
<div class="code-block"><pre><code">/* Transitions — smooth changes on state change */
.btn {
    background: var(--color-primary);
    transform: translateY(0);
    box-shadow: none;
    transition:
        background 0.2s ease,
        transform  0.25s cubic-bezier(0.4, 0, 0.2, 1),
        box-shadow 0.25s ease;
}
.btn:hover {
    background: #00a88e;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,212,180,0.3);
}

/* Keyframe animations */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

.card {
    animation: fadeSlideIn 0.4s ease forwards;
}
/* Staggered entrance with nth-child + animation-delay */
.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 100ms; }
.card:nth-child(3) { animation-delay: 200ms; }

.spinner {
    animation: spin 0.7s linear infinite;
}</code></pre></div>
        """,25),
    ]

    quizzes = {
        1:[
            ("What does box-sizing: border-box do?","Adds extra space around the element","Makes width include padding and border (not just content)","Removes all margins from the element","B","With border-box, the width you set IS the total element width including padding and border. This makes layout far more predictable and is standard in all modern CSS frameworks."),
            ("When two CSS rules have equal specificity, which one applies?","The first rule in the file","The one with more properties","The last rule in the file","C","The cascade: when origin and specificity are equal, CSS applies the rule that appears LAST in the stylesheet."),
        ],
        2:[
            ("flex-grow: 2 on one item and flex-grow: 1 on another means:","The first item is always exactly twice as wide","The first item gets twice as much of the EXTRA available space","The first item starts at 200% width","B","flex-grow is proportional — it divides up the remaining space (after flex-basis sizes are applied). flex-grow:2 gets 2 shares, flex-grow:1 gets 1 share of the leftover space."),
            ("How do you perfectly centre content both horizontally and vertically with Flexbox?","Add margin: auto to every child","Set justify-content: center AND align-items: center on the container","Set text-align: center on the container","B","justify-content centres along the main axis, align-items centres along the cross axis. Together they achieve perfect 2D centering of all flex children."),
        ],
        3:[
            ("What does grid-column: span 2 mean?","Place the item in column 2","Make the item span 2 column tracks wide","Add 2px gap before the column","B","The span keyword tells an item to span that many grid tracks. grid-column: span 2 means the item occupies 2 adjacent columns."),
            ("What is the auto-fill keyword in repeat(auto-fill, minmax(280px, 1fr)) for?","Creates a fixed number of columns","Creates as many columns as fit, each at least 280px wide","Fills the grid with placeholder elements","B","auto-fill tells the browser to create as many column tracks as fit in the container, each sized according to minmax(). This creates a responsive grid with NO media queries needed."),
        ],
        4:[
            ("What is the mobile-first approach?","Build for desktop then add styles to shrink for mobile","Write base styles for mobile, then use min-width media queries to enhance for larger screens","Use JavaScript to detect device type","B","Mobile-first means your default CSS targets the smallest screen. min-width media queries then progressively add layout enhancements as the screen gets larger. This generally produces cleaner, more performant CSS."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


# ═══════════════════════════════════════════════
# JAVA COURSE
# ═══════════════════════════════════════════════


def extend_css(conn, c, cid):
    lessons = [
        (4, "Flexbox — Complete Mastery", """
<h2>CSS Flexbox — Complete Guide</h2>
<p>Flexbox is the most practical CSS layout system for one-dimensional layouts — rows OR columns. Once you truly understand it, 80% of layout challenges become trivial.</p>

<div class="concept-box">
  <div class="cb-title">The Two Axes</div>
  <p>Every flexbox layout has a <strong>main axis</strong> (direction items flow) and a <strong>cross axis</strong> (perpendicular to it). <code>justify-content</code> controls the main axis. <code>align-items</code> controls the cross axis. When you change <code>flex-direction</code>, the axes swap.</p>
</div>

<h3>Container Properties</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code=".container {
  display: flex;

  /* Main axis direction */
  flex-direction: row;           /* → default  */
  flex-direction: row-reverse;   /* ←          */
  flex-direction: column;        /* ↓           */
  flex-direction: column-reverse;/* ↑           */

  /* Main axis alignment */
  justify-content: flex-start;    /* pack to start     */
  justify-content: flex-end;      /* pack to end       */
  justify-content: center;        /* centre            */
  justify-content: space-between; /* equal gaps between*/
  justify-content: space-around;  /* equal gaps around */
  justify-content: space-evenly;  /* perfectly even    */

  /* Cross axis alignment */
  align-items: stretch;    /* fill cross axis (default) */
  align-items: flex-start; /* top                        */
  align-items: center;     /* middle                     */
  align-items: flex-end;   /* bottom                     */

  /* Wrapping */
  flex-wrap: nowrap;  /* single line (default) */
  flex-wrap: wrap;    /* wrap to next line     */

  /* Shorthand */
  gap: 16px;          /* space BETWEEN items   */
}"></code></pre></div>

<h3>Item Properties</h3>
<div class="code-block"><pre><code>.item {
  /* flex-grow: how much spare space does this item take? */
  flex-grow: 1;    /* take all available space */
  flex-grow: 0;    /* don't grow (default) */

  /* flex-shrink: can this item shrink if needed? */
  flex-shrink: 1;  /* can shrink (default) */
  flex-shrink: 0;  /* never shrink */

  /* flex-basis: initial size before grow/shrink */
  flex-basis: 200px;
  flex-basis: 50%;
  flex-basis: auto; /* use width/height (default) */

  /* Shorthand: flex: grow shrink basis */
  flex: 1;           /* = flex: 1 1 0  — grow and shrink equally */
  flex: 0 0 200px;   /* fixed 200px, no grow/shrink */

  /* Override cross-axis alignment for just this item */
  align-self: center;
}</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Challenges</div>
  <ol>
    <li>Build a navigation bar with logo on the left, links in the centre, and a button on the right — using only flexbox.</li>
    <li>Create a card grid where each card grows equally to fill the row.</li>
    <li>Build a vertically and horizontally centred modal overlay.</li>
    <li>Create a sticky footer layout where the main content stretches to fill the viewport.</li>
  </ol>
</div>
""", 40),
        (5, "CSS Grid & Responsive Design", """
<h2>CSS Grid & Responsive Design</h2>
<p>Grid is the first CSS layout system designed specifically for two-dimensional layouts. Combined with media queries and modern units, it makes building responsive interfaces straightforward and declarative.</p>

<h3>Grid Fundamentals</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code=".grid {
  display: grid;

  /* Define columns */
  grid-template-columns: 200px 1fr 1fr;        /* 3 cols: fixed + 2 equal */
  grid-template-columns: repeat(3, 1fr);       /* 3 equal columns */
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* responsive! */

  /* Define rows */
  grid-template-rows: auto 1fr auto;   /* header, content, footer */

  /* Gaps */
  gap: 20px;           /* row and column gap */
  row-gap: 16px;
  column-gap: 24px;
}

/* Placing items */
.hero    { grid-column: 1 / -1; }           /* span all columns */
.sidebar { grid-column: 1 / 2; grid-row: 2 / 4; }
.main    { grid-column: 2 / -1; }

/* Named areas — most readable approach */
.layout {
  grid-template-areas:
    &quot;header header header&quot;
    &quot;sidebar main   main  &quot;
    &quot;footer  footer footer&quot;;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }"></code></pre></div>

<h3>Responsive Design with Modern CSS</h3>
<div class="code-block"><pre><code>/* Mobile-first approach: design for mobile, scale UP */
.container { padding: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .container { padding: 2rem; }
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
  .grid { grid-template-columns: repeat(3, 1fr); }
}

/* Modern fluid typography */
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }

/* Container queries (newer — check support) */
@container (min-width: 400px) {
  .card { display: flex; }
}</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Challenges</div>
  <ol>
    <li>Build a full page layout with header, sidebar, main content, and footer using <code>grid-template-areas</code>.</li>
    <li>Create a responsive photo gallery that shows 1 column on mobile, 2 on tablet, 4 on desktop.</li>
    <li>Build a magazine-style article layout with a large featured image spanning multiple columns.</li>
  </ol>
</div>
""", 45),
        (6, "CSS Animations, Variables & Architecture", """
<h2>CSS Animations, Custom Properties & Architecture</h2>
<p>Modern CSS goes far beyond styling. With custom properties (variables), animations, and smart architecture patterns, CSS becomes a powerful design system layer.</p>

<h3>CSS Custom Properties (Variables)</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="/* Define on :root — globally available */
:root {
  --color-primary:    #4facfe;
  --color-bg:         #060b14;
  --color-text:       #e2e8f0;
  --font-size-base:   1rem;
  --spacing-md:       1rem;
  --radius:           10px;
  --shadow:           0 4px 20px rgba(0,0,0,0.4);
  --transition:       all 0.25s ease;
}

/* Use anywhere */
.button {
  background: var(--color-primary);
  border-radius: var(--radius);
  padding: var(--spacing-md) calc(var(--spacing-md) * 2);
  box-shadow: var(--shadow);
  transition: var(--transition);
}

/* Override for dark/light themes or components */
.dark-card {
  --color-bg: #1a1a2e;
  background: var(--color-bg);   /* uses local override */
}

/* JavaScript can read and write CSS variables */
document.documentElement.style.setProperty(&quot;--color-primary&quot;, &quot;#ff6b6b&quot;);"></code></pre></div>

<h3>Keyframe Animations</h3>
<div class="code-block"><pre><code>@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1);    opacity: 1; }
  50%       { transform: scale(1.05); opacity: 0.8; }
}

.card {
  animation: fadeSlideUp 0.5s ease forwards;
  animation-delay: 0.1s;   /* stagger with nth-child */
}

.live-dot {
  animation: pulse 2s ease-in-out infinite;
}

/* Staggered animations with nth-child */
.card:nth-child(1) { animation-delay: 0.0s; }
.card:nth-child(2) { animation-delay: 0.1s; }
.card:nth-child(3) { animation-delay: 0.2s; }</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Challenges</div>
  <ol>
    <li>Build a complete design system with CSS variables: colours, spacing scale, typography scale, shadows. Switch between light and dark mode by toggling a class on <code>&lt;body&gt;</code>.</li>
    <li>Create a card component with a hover animation — lift, shadow, and colour transition.</li>
    <li>Build an animated loading skeleton screen (the grey shimmer effect you see on social feeds).</li>
    <li>Create a hero section with a staggered entrance animation for each element.</li>
  </ol>
</div>
""", 45),
    ]
    quizzes = {
        4: [
            ("In Flexbox, which property controls alignment along the MAIN axis?", "align-items", "align-content", "justify-content", "C", "justify-content controls how items are distributed along the main axis (the direction of flex-direction). align-items controls the cross axis."),
            ("What does `flex: 1` mean in shorthand?", "flex-grow: 1 only", "flex: 1 1 0 — grow, shrink, basis zero", "flex-basis: 1px", "B", "`flex: 1` expands to `flex-grow: 1; flex-shrink: 1; flex-basis: 0`. Items with equal flex values share available space equally."),
        ],
        5: [
            ("Which CSS Grid value creates as many columns as fit, each at least 250px wide?", "repeat(3, 250px)", "repeat(auto-fill, minmax(250px, 1fr))", "auto-columns: 250px", "B", "repeat(auto-fill, minmax(250px, 1fr)) is the standard responsive grid pattern. auto-fill creates as many columns as fit; minmax sets the minimum and maximum size."),
            ("In mobile-first responsive design, which media query breakpoint do you start with?", "The largest screen size", "The smallest screen size", "1024px always", "B", "Mobile-first means writing base styles for small screens, then using min-width media queries to progressively enhance for larger screens. This results in cleaner, more performant CSS."),
        ],
        6: [
            ("How do you define a CSS custom property (variable)?", "var: --color: red;", "--color-primary: #4facfe; on :root", "$color: #4facfe;", "B", "CSS custom properties are defined with a double-dash prefix (--) inside any selector. Defining them on :root makes them available globally throughout the stylesheet."),
            ("Which CSS rule defines an animation sequence from start to finish?", "@animation", "@keyframes", "@transition", "B", "@keyframes defines the steps of an animation. You give it a name, then reference that name in the animation property of any selector."),
        ],
    }
    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


