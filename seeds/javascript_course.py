"""iLEARN — JavaScript course seed data."""
from .helpers import insert_lessons_and_quizzes

def seed_javascript(conn, c):
    c.execute("INSERT INTO courses (title,description,icon,level,language) VALUES (?,?,?,?,?)",
              ("JavaScript","Master modern JavaScript from the type system and closures through async/await, the DOM, and ES6+ features. Understand how the language really works under the hood.","⚡","Beginner to Intermediate","javascript"))
    cid = c.lastrowid

    lessons = [
        (1,"JS Fundamentals & the Type System","""
<h2>JavaScript: The Language of the Web</h2>
<p>JavaScript is the only programming language that runs natively in all web browsers. Created by Brendan Eich in <strong>just 10 days</strong> in 1995, it has evolved dramatically. Today's JavaScript (ES6+) is a powerful, mature language used for frontend, backend (Node.js), mobile (React Native), and desktop (Electron) applications.</p>

<h3>var, let, and const — What Changed and Why</h3>
<div class="code-block"><pre><code>// var — function-scoped, hoisted, can be re-declared (legacy, avoid)
var x = 10;
var x = 20;    // No error — var allows re-declaration

// let — block-scoped, temporal dead zone, reassignable
let score = 0;
score = 100;   // OK

// const — block-scoped, must be initialised, binding is constant
const API_URL = "https://api.example.com";
// API_URL = "other";  // TypeError: Assignment to constant variable

// CRITICAL: const with objects — the BINDING is constant, not the content
const user = { name: "Alice" };
user.name = "Bob";     // ALLOWED — modifying the object's property
user.age  = 30;        // ALLOWED — adding a new property
// user = {};          // TypeError — can't reassign the const binding

// Block scoping demonstration
{
    let blockVar  = "I'm block-scoped";
    const blockConst = "Me too";
    var funcVar   = "I escape the block!";
}
// console.log(blockVar);  // ReferenceError
console.log(funcVar);      // "I escape the block!" — var ignores blocks</code></pre></div>

<h3>JavaScript's 8 Data Types</h3>
<div class="code-block"><pre><code>// Primitives (7) — immutable, compared by VALUE
let num   = 42;
let float = 3.14;         // JS has only ONE number type (64-bit float)
let text  = "Hello";
let flag  = true;
let empty = null;         // Intentional absence of value
let undef = undefined;    // Declared but not assigned
let sym   = Symbol("id"); // Unique identifier (ES6+)
let big   = 9007199254740993n; // BigInt for integers beyond 2^53 - 1

// Object type (1) — mutable, compared by REFERENCE
let obj   = { name: "Alice" };
let arr   = [1, 2, 3];         // typeof [] === "object"
let fn    = function() {};      // typeof fn === "function" (special case)

// typeof operator — runtime type checking
console.log(typeof 42);           // "number"
console.log(typeof "hello");      // "string"
console.log(typeof true);         // "boolean"
console.log(typeof null);         // "object" ← infamous JS bug, never fixed
console.log(typeof undefined);    // "undefined"
console.log(typeof Symbol());     // "symbol"
console.log(typeof {});           // "object"
console.log(typeof []);           // "object" — use Array.isArray() instead
console.log(typeof function(){}); // "function"</code></pre></div>

<h3>Type Coercion — The Root of Many Bugs</h3>
<div class="code-block"><pre><code>// Implicit coercion (JavaScript does this automatically)
console.log("5" + 3);        // "53" — + triggers string concatenation
console.log("5" - 3);        // 2    — - has no string meaning, converts
console.log("5" * "3");      // 15   — both become numbers
console.log(true + true);    // 2    — booleans become 0 or 1
console.log([] + {});        // "[object Object]"
console.log({} + []);        // 0 (in some contexts) or "[object Object]"

// == (loose equality) vs === (strict equality)
console.log(0 == false);         // true  — coerces both
console.log(0 === false);        // false — strict, different types
console.log("" == false);        // true
console.log("" === false);       // false
console.log(null == undefined);  // true  — special rule
console.log(null === undefined); // false

// RULE: ALWAYS use === unless you specifically need type coercion

// Safe explicit conversions
const n = Number("42");          // 42
const s = String(100);           // "100"
const b = Boolean(0);            // false
const i = parseInt("3.9px", 10); // 3 (second arg = radix)
const f = parseFloat("3.14em");  // 3.14</code></pre></div>
        """,20),

        (2,"Functions, Closures & the 'this' Keyword","""
<h2>Functions as First-Class Objects</h2>
<p>In JavaScript, functions are objects. They have properties, methods, can be passed around like variables, and form the foundation of nearly every design pattern in the language.</p>

<h3>Three Ways to Define Functions</h3>
<div class="code-block"><pre><code>// 1. Function Declaration — hoisted completely (callable before definition)
function greet(name) {
    return `Hello, ${name}!`;
}

// 2. Function Expression — assigned to a variable, NOT hoisted
const greet2 = function namedFn(name) {
    return `Hello, ${name}!`;
};

// 3. Arrow Function (ES6) — concise, lexical 'this'
const greet3 = (name) => `Hello, ${name}!`;

// Arrow shorthand examples
const square  = x => x * x;           // Single param, no parens needed
const add     = (a, b) => a + b;       // Two params
const noParam = () => "constant";      // No params need ()
const multi   = (x) => {              // Multi-line needs explicit return
    const doubled = x * 2;
    return doubled + 1;
};

// Default parameters
function createUser(name, role = "student", active = true) {
    return { name, role, active };   // Shorthand property names (ES6)
}
createUser("Alice");                 // { name: "Alice", role: "student", active: true }
createUser("Bob", "admin");</code></pre></div>

<h3>The 'this' Keyword — Context-Dependent</h3>
<div class="code-block"><pre><code>// 'this' refers to the object that CALLS the function
const counter = {
    count: 0,
    increment: function() {
        this.count++;          // 'this' = counter object
        console.log(this.count);
    }
};
counter.increment();   // 1

// Arrow functions do NOT have their own 'this'
// They INHERIT 'this' from the surrounding lexical scope
const timer = {
    seconds: 0,
    start() {
        setInterval(() => {
            this.seconds++;    // 'this' inherited from start() — refers to timer
            console.log(this.seconds);
        }, 1000);
    }
};

// Common bug with 'this' in callbacks
const obj = {
    name: "iLEARN",
    greetRegular: function() {
        setTimeout(function() {
            console.log(this.name);  // undefined! 'this' is window/undefined
        }, 100);
    },
    greetArrow: function() {
        setTimeout(() => {
            console.log(this.name);  // "iLEARN" — arrow inherits 'this'
        }, 100);
    }
};

// Explicit binding: call, apply, bind
function introduce(greeting, punctuation) {
    return `${greeting}, I'm ${this.name}${punctuation}`;
}
const person = { name: "Alice" };
introduce.call(person, "Hello", "!");    // Hello, I'm Alice!
introduce.apply(person, ["Hi", "."]);   // Hi, I'm Alice.
const boundFn = introduce.bind(person); // Returns new function with this fixed</code></pre></div>

<h3>Closures</h3>
<div class="code-block"><pre><code>// Closure: inner function retains access to outer scope after outer returns
function makeCounter(initial = 0) {
    let count = initial;   // Private — not accessible from outside

    return {
        increment: () => ++count,
        decrement: () => --count,
        reset:     () => { count = initial; },
        value:     () => count
    };
}

const c = makeCounter(10);
c.increment();   // 11
c.increment();   // 12
c.decrement();   // 11
console.log(c.value());   // 11
// count is inaccessible directly — only through the returned methods

// Classic closure gotcha in loops
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// Prints: 3, 3, 3 — all closures share the SAME var i

// Solution: use let (block-scoped, new binding per iteration)
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// Prints: 0, 1, 2</code></pre></div>
        """,25),

        (3,"The DOM & Event-Driven Programming","""
<h2>The Document Object Model</h2>
<p>The DOM is a <strong>tree-structured, in-memory representation</strong> of an HTML document. Every HTML element becomes a node in this tree. JavaScript can traverse, query, modify, add, and delete any node, making the page dynamic in real time.</p>

<h3>Querying the DOM</h3>
<div class="code-block"><pre><code">// Modern (preferred) — returns static NodeList or first match
const title   = document.querySelector("#main-title");
const buttons = document.querySelectorAll(".btn");        // NodeList
const first   = document.querySelector("nav > a:first-child");

// Convert NodeList to Array for array methods
const btnArray = Array.from(buttons);
const btnArray2 = [...buttons];   // Spread also works

// Legacy selectors (still widely used)
const byId    = document.getElementById("header");
const byClass = document.getElementsByClassName("card");  // Live HTMLCollection
const byTag   = document.getElementsByTagName("p");       // Live HTMLCollection

// DOM traversal
const parent   = element.parentElement;
const children = [...element.children];             // Direct children
const next     = element.nextElementSibling;
const prev     = element.previousElementSibling;
const closest  = element.closest(".card");          // Nearest ancestor matching</code></pre></div>

<h3>Creating and Modifying the DOM</h3>
<div class="code-block"><pre><code">const card = document.querySelector(".card");

// Content manipulation
card.textContent = "Safe text";              // Escapes HTML — safe
card.innerHTML   = "<b>Parsed HTML</b>";     // Parses HTML — careful with user input!

// Attributes
card.setAttribute("data-user-id", "42");
const id = card.getAttribute("data-user-id");
card.removeAttribute("disabled");
card.dataset.userId = "42";     // Shorthand for data-* attributes

// CSS Classes
card.classList.add("active", "highlight");
card.classList.remove("hidden");
card.classList.toggle("selected");
card.classList.contains("active");   // true/false
card.classList.replace("old", "new");

// Inline styles (use sparingly — prefer CSS classes)
card.style.transform = "translateY(-4px)";
card.style.cssText   = "color: red; font-size: 1.2rem;";

// Creating and inserting elements
const li = document.createElement("li");
li.textContent = "New Item";
li.className   = "lesson-item";
li.dataset.id  = "123";
document.querySelector("ul").appendChild(li);

// Modern insertion (cleaner than innerHTML)
card.insertAdjacentHTML("beforeend", "<span>Appended</span>");
parent.insertBefore(newEl, referenceEl);</code></pre></div>

<h3>Events and the Event System</h3>
<div class="code-block"><pre><code">const btn = document.querySelector("#submit");

// addEventListener is always preferred over onclick=""
btn.addEventListener("click", function(event) {
    event.preventDefault();   // Cancel default action (e.g. form submit)
    event.stopPropagation();  // Stop event bubbling to parent elements
    console.log(event.target, event.currentTarget);
});

// Event delegation — one handler for many children (efficient!)
document.querySelector("#course-list").addEventListener("click", (e) => {
    const card = e.target.closest(".course-card");
    if (card) {
        const courseId = card.dataset.courseId;
        navigateToCourse(courseId);
    }
});

// Keyboard events
document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey) sendMessage();
    if (e.key === "Escape") closeModal();
    if (e.code === "Space") e.preventDefault(); // Prevent page scroll
});

// Custom events — decoupled communication between components
const progressEvent = new CustomEvent("lessonCompleted", {
    detail: { lessonId: 42, score: 95 },
    bubbles: true
});
document.dispatchEvent(progressEvent);
document.addEventListener("lessonCompleted", (e) => {
    updateProgressBar(e.detail.lessonId, e.detail.score);
});</code></pre></div>
        """,25),

        (4,"Async JS — Promises & Async/Await","""
<h2>Asynchronous JavaScript</h2>
<p>JavaScript is <strong>single-threaded</strong> — it can only do one thing at a time. But it needs to handle I/O (network, disk, timers) without blocking the UI. The solution is an <strong>event loop</strong> with a non-blocking async model.</p>

<h3>The Event Loop Explained</h3>
<div class="code-block"><pre><code">console.log("1 — synchronous start");

setTimeout(() => console.log("4 — macrotask (timer)"), 0);

Promise.resolve().then(() => console.log("3 — microtask (promise)"));

console.log("2 — synchronous end");

// OUTPUT ORDER:
// 1 — synchronous start
// 2 — synchronous end
// 3 — microtask (promise)    ← microtasks run BEFORE macrotasks
// 4 — macrotask (timer)

// The event loop priority:
// 1. Synchronous code (call stack)
// 2. Microtask queue (Promises, queueMicrotask)
// 3. Macrotask queue (setTimeout, setInterval, I/O)</code></pre></div>

<h3>Promises — From Scratch</h3>
<div class="code-block"><pre><code>// A Promise represents an eventual value: pending → fulfilled | rejected
function fetchUserById(id) {
    return new Promise((resolve, reject) => {
        if (typeof id !== "number" || id <= 0) {
            reject(new Error("Invalid user ID"));
            return;
        }
        setTimeout(() => {
            resolve({ id, name: "Alice", role: "student" });
        }, 300);
    });
}

// Consuming promises — chaining
fetchUserById(1)
    .then(user => {
        console.log("User:", user.name);
        return fetchEnrolledCourses(user.id);  // Returns another promise
    })
    .then(courses => {
        console.log("Courses:", courses.length);
    })
    .catch(err => {
        console.error("Failed:", err.message);  // Catches ANY rejection in chain
    })
    .finally(() => {
        hideLoadingSpinner();  // Runs regardless of success or failure
    });</code></pre></div>

<h3>Async/Await — Modern Syntax</h3>
<div class="code-block"><pre><code">// async/await is syntactic sugar over Promises
// Every async function implicitly returns a Promise

async function loadDashboard(userId) {
    try {
        // await pauses the async function (not the whole thread)
        const user    = await fetchUserById(userId);
        const courses = await fetchCourses(user.id);

        return { user, courses };

    } catch (error) {
        console.error("Dashboard failed:", error.message);
        throw error;   // Re-throw to let callers handle it
    }
}

// Parallel execution — when requests are independent
async function loadAll(userId) {
    // Sequential (SLOW — each waits for the previous)
    // const user    = await fetchUser(userId);
    // const courses = await fetchCourses(userId);

    // Parallel (FAST — all start at the same time)
    const [user, courses, progress] = await Promise.all([
        fetchUser(userId),
        fetchCourses(userId),
        fetchProgress(userId)
    ]);
    return { user, courses, progress };
}

// Promise.allSettled — when you want ALL results, even if some fail
const results = await Promise.allSettled([p1, p2, p3]);
results.forEach(r => {
    if (r.status === "fulfilled") console.log("OK:", r.value);
    else console.log("Failed:", r.reason);
});

// Real-world Fetch usage
async function completeLesson(lessonId) {
    const response = await fetch("/api/complete_lesson", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ lesson_id: lessonId })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}</code></pre></div>
        """,30),

        (5,"ES6+ Features & Module System","""
<h2>Modern JavaScript Features (ES6+)</h2>
<p>ECMAScript 2015 (ES6) and subsequent yearly releases have fundamentally changed how JavaScript is written. These features are now standard in all professional codebases.</p>

<h3>Destructuring Assignment</h3>
<div class="code-block"><pre><code">// Array destructuring
const [first, second, ...rest] = [10, 20, 30, 40, 50];
// first=10, second=20, rest=[30,40,50]

// Skip elements
const [,, third] = [1, 2, 3];   // third = 3

// Object destructuring with renaming and defaults
const user = { name: "Alice", age: 30, role: "admin" };
const { name, age, role: userRole = "user", email = "n/a" } = user;
// name="Alice", age=30, userRole="admin", email="n/a" (default)

// Function parameter destructuring — cleaner API signatures
function renderCard({ title, description, level = "Beginner", icon = "📚" }) {
    return `<div>${icon} ${title} (${level}): ${description}</div>`;
}
renderCard({ title: "Python", description: "Learn Python", level: "Intermediate" });

// Nested destructuring
const { address: { city, country = "Nigeria" } } = {
    address: { city: "Lagos" }
};</code></pre></div>

<h3>Spread and Rest Operators</h3>
<div class="code-block"><pre><code">// Spread — expand iterable into individual elements
const arr1    = [1, 2, 3];
const arr2    = [4, 5, 6];
const merged  = [...arr1, ...arr2];       // [1,2,3,4,5,6]
const copy    = [...arr1];                // Shallow clone

const obj1   = { a: 1, b: 2 };
const obj2   = { c: 3, d: 4 };
const merged2 = { ...obj1, ...obj2 };    // { a:1, b:2, c:3, d:4 }
const updated = { ...obj1, b: 99 };     // Override: { a:1, b:99 }

// Spread in function calls
Math.max(...[3, 1, 4, 1, 5, 9]);        // 9

// Rest — collect remaining into array
function logAll(first, second, ...others) {
    console.log(first, second, others);
}
logAll(1, 2, 3, 4, 5);   // 1  2  [3, 4, 5]</code></pre></div>

<h3>ES Modules (ESM)</h3>
<div class="code-block"><pre><code">// utils.js — exporting
export const VERSION    = "2.0";
export const formatDate = d => d.toISOString().split("T")[0];
export class Logger {
    log(msg) { console.log(`[${new Date().toISOString()}] ${msg}`); }
}
export default class App { /* main class */ }   // One default per file

// main.js — importing
import App                      from "./utils.js";   // Default import
import { VERSION, formatDate }  from "./utils.js";   // Named imports
import * as Utils               from "./utils.js";   // Namespace (all exports)
import { formatDate as fmtDate} from "./utils.js";   // Rename on import

// Dynamic import (lazy loading — only loads when needed)
async function loadAnalytics() {
    const { Analytics } = await import("./analytics.js");
    Analytics.init();
}</code></pre></div>
        """,25),
    ]

    quizzes = {
        1:[
            ("What does typeof null return in JavaScript?","'null'","'undefined'","'object'","C","typeof null returns 'object' — a famous, unfixed bug from JavaScript's first version. Always use === null to check for null."),
            ("What is the difference between == and ===?","No real difference","=== checks value only","== allows type coercion; === requires same type AND value","C","== performs type coercion before comparing (0 == false is true). === is strict — same value AND same type required. Always prefer ===."),
            ("What happens when you do 'const user = {}; user.name = Alice'?","TypeError — const objects are frozen","It works — const prevents rebinding, not mutation","SyntaxError","B","const prevents reassigning the variable binding (user = {} would fail), but you can still mutate the object's properties."),
        ],
        2:[
            ("Why does the var-in-loop closure print '3, 3, 3' instead of '0, 1, 2'?","var is hoisted to global scope","All 3 closures share the same var i, which is 3 by the time callbacks run","var closures don't work in loops","B","var is function-scoped, not block-scoped. All 3 arrow functions close over the same i variable. By the time the setTimeout callbacks run, the loop has finished and i === 3."),
            ("Arrow functions differ from regular functions in that they:","Cannot return values","Have their own 'this' context","Inherit 'this' from their surrounding lexical scope","C","Arrow functions do not have their own 'this'. They capture 'this' from the enclosing lexical scope at the time of definition, not at the time of calling."),
        ],
        3:[
            ("What does event.stopPropagation() do?","Cancels the default browser action (like form submit)","Prevents the event from bubbling up to parent elements","Removes all listeners for this event","B","stopPropagation() halts bubbling up the DOM tree. preventDefault() cancels the browser's default action. They are independent — you can call both."),
            ("What is event delegation?","Firing events from multiple elements","Attaching one listener to a parent to handle events from child elements","Removing unused event listeners","B","Event delegation uses bubbling — child events bubble up to the parent. The parent checks event.target to know which child triggered it. One listener is more efficient than hundreds."),
        ],
        4:[
            ("What does Promise.all([p1, p2, p3]) do?","Runs promises sequentially","Resolves when ALL promises succeed; rejects if ANY one rejects","Returns whichever promise resolves first","B","Promise.all runs all promises concurrently and returns an array of results. Short-circuits with rejection if any single promise rejects. Use Promise.allSettled if you need all results regardless of failures."),
        ],
        5:[
            ("What does the spread operator (...) do with an array?","Creates a deep clone","Deletes elements","Expands elements into individual values","C","The spread operator expands an iterable into individual elements. Note: it creates a SHALLOW copy — nested objects are still shared by reference."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


# ═══════════════════════════════════════════════
# CSS COURSE
# ═══════════════════════════════════════════════


def extend_javascript(conn, c, cid):
    lessons = [
        (4, "Functions, Scope & Closures", """
<h2>Functions, Scope & Closures in JavaScript</h2>
<p>Understanding how JavaScript handles functions and scope is what separates beginners from confident developers. These concepts appear in every interview and every real codebase.</p>

<h3>Function Declarations vs Expressions vs Arrow Functions</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="// 1. Function Declaration — hoisted (can be called before it is defined)
function greet(name) {
  return `Hello, ${name}!`;
}

// 2. Function Expression — NOT hoisted
const multiply = function(a, b) {
  return a * b;
};

// 3. Arrow Function — concise, no own &quot;this&quot;
const square = (x) => x * x;
const add    = (a, b) => a + b;

// Multi-line arrow function
const processUser = (user) => {
  const name = user.name.toUpperCase();
  return { ...user, name };
};

console.log(greet(&quot;Alice&quot;));     // Hello, Alice!
console.log(square(5));          // 25"></code></pre></div>

<h3>Scope: var vs let vs const</h3>
<div class="code-block"><pre><code>// var — function-scoped, hoisted, can be redeclared (avoid in modern JS)
// let — block-scoped, not hoisted, can be reassigned
// const — block-scoped, must be initialised, cannot be reassigned

function scopeDemo() {
  if (true) {
    var   a = "var";    // accessible outside the if block
    let   b = "let";    // only inside this block
    const c = "const";  // only inside this block
  }
  console.log(a);   // "var"
  // console.log(b); // ReferenceError!
}

// Rule of thumb: use const by default; let when you need reassignment; never var</code></pre></div>

<h3>Closures</h3>
<div class="code-block"><pre><code>// A closure is a function that "remembers" variables from its outer scope
function makeCounter(start = 0) {
  let count = start;   // This variable is "closed over"

  return {
    increment() { return ++count; },
    decrement() { return --count; },
    value()     { return count; }
  };
}

const counter = makeCounter(10);
console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter.decrement()); // 11
// count is private — cannot be accessed directly from outside</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Write a <code>memoize(fn)</code> function that caches the results of expensive function calls using a closure.</li>
    <li>Create a <code>makeMultiplier(factor)</code> function that returns a new function multiplying any number by that factor.</li>
    <li>Build a simple event counter using closures — track how many times a button has been clicked.</li>
  </ol>
</div>
""", 40),
        (5, "Async JavaScript — Promises & Fetch", """
<h2>Asynchronous JavaScript</h2>
<p>JavaScript is single-threaded but non-blocking. Understanding async patterns is essential for any web developer — almost every real app fetches data from an API.</p>

<h3>The Problem: Callback Hell</h3>
<div class="code-block"><pre><code>// Old way — deeply nested callbacks (hard to read and maintain)
getUser(id, function(user) {
  getPosts(user.id, function(posts) {
    getComments(posts[0].id, function(comments) {
      // Pyramid of doom...
    });
  });
});</code></pre></div>

<h3>Promises — the Solution</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="// A Promise represents a value that will be available in the future
const fetchUser = (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: &quot;Alice&quot; });   // Success
      } else {
        reject(new Error(&quot;Invalid ID&quot;));   // Failure
      }
    }, 1000);
  });
};

// .then() / .catch() chaining
fetchUser(1)
  .then(user  => { console.log(user.name); return user; })
  .then(user  => console.log(&quot;Done with&quot;, user.id))
  .catch(err  => console.error(&quot;Error:&quot;, err.message))
  .finally(() => console.log(&quot;Always runs&quot;));"></code></pre></div>

<h3>async / await — Cleaner Syntax</h3>
<div class="code-block"><pre><code>// async/await is syntactic sugar over Promises — same behaviour, cleaner code
async function loadUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const user = await response.json();
    console.log(user.name);
    return user;

  } catch (error) {
    console.error("Failed to load user:", error);
    return null;
  }
}

// Run multiple requests IN PARALLEL (faster than sequential await)
async function loadDashboard() {
  const [user, posts, stats] = await Promise.all([
    fetch("/api/user").then(r => r.json()),
    fetch("/api/posts").then(r => r.json()),
    fetch("/api/stats").then(r => r.json()),
  ]);
  console.log(user, posts, stats);
}</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Fetch data from <code>https://jsonplaceholder.typicode.com/users</code> and display all user names on the page.</li>
    <li>Build a search form that fetches results from a public API as the user types (with a debounce function).</li>
    <li>Create a loading spinner that shows while data is being fetched and hides when done.</li>
  </ol>
</div>
""", 45),
        (6, "DOM Mastery & Building Real Features", """
<h2>DOM Mastery — Building Real UI Features</h2>
<p>The Document Object Model (DOM) is your interface to the webpage. Mastering it lets you build dynamic, interactive UIs without any framework.</p>

<h3>Efficient DOM Selection & Manipulation</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="// Modern DOM selection
const btn        = document.querySelector(&quot;#submit-btn&quot;);
const allCards   = document.querySelectorAll(&quot;.card&quot;);
const form       = document.forms[&quot;login-form&quot;];

// Modifying elements
btn.textContent  = &quot;New Label&quot;;
btn.innerHTML    = &quot;&lt;strong&gt;Bold Label&lt;/strong&gt;&quot;;
btn.classList.add(&quot;active&quot;);
btn.classList.toggle(&quot;hidden&quot;);
btn.setAttribute(&quot;aria-disabled&quot;, &quot;true&quot;);
btn.style.setProperty(&quot;--accent&quot;, &quot;#ff0&quot;);

// Creating and inserting elements (faster than innerHTML for many nodes)
const li = document.createElement(&quot;li&quot;);
li.className = &quot;list-item&quot;;
li.textContent = &quot;New Item&quot;;
document.querySelector(&quot;ul&quot;).appendChild(li);

// Event delegation — one listener handles many children
document.querySelector(&quot;#task-list&quot;).addEventListener(&quot;click&quot;, (e) => {
  if (e.target.matches(&quot;.delete-btn&quot;)) {
    e.target.closest(&quot;li&quot;).remove();
  }
  if (e.target.matches(&quot;.complete-btn&quot;)) {
    e.target.closest(&quot;li&quot;).classList.toggle(&quot;done&quot;);
  }
});"></code></pre></div>

<h3>Building a Live Search Filter</h3>
<div class="code-block"><pre><code>// Filter a list in real time as the user types
const searchInput = document.querySelector("#search");
const items       = document.querySelectorAll(".item");

searchInput.addEventListener("input", (e) => {
  const query = e.target.value.toLowerCase().trim();
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? "" : "none";
  });
});

// Local Storage — persist data across page reloads
function saveTasks(tasks) {
  localStorage.setItem("tasks", JSON.stringify(tasks));
}
function loadTasks() {
  return JSON.parse(localStorage.getItem("tasks") || "[]");
}</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Projects</div>
  <ol>
    <li><strong>Task Manager</strong> — Add, complete, and delete tasks. Save to localStorage so they persist on reload.</li>
    <li><strong>Live Search</strong> — Fetch a list of countries from an API and filter them in real time.</li>
    <li><strong>Dark Mode Toggle</strong> — Toggle a dark/light theme and save the preference to localStorage.</li>
    <li><strong>Form Validator</strong> — Validate name, email, and password fields with real-time feedback before submission.</li>
  </ol>
</div>
""", 50),
    ]
    quizzes = {
        4: [
            ("Which type of function does NOT have its own `this` binding?", "Function declaration", "Function expression", "Arrow function", "C", "Arrow functions inherit `this` from their surrounding lexical context. This makes them ideal for callbacks inside class methods, where you want `this` to refer to the class instance."),
            ("What is a closure in JavaScript?", "A way to close the browser window", "A function that remembers variables from its outer scope", "A method to end a loop", "B", "A closure is created whenever a function is defined inside another function. The inner function keeps a live reference to the outer function's variables, even after the outer function has returned."),
        ],
        5: [
            ("What does `async/await` syntax do in JavaScript?", "Makes code run faster", "Provides cleaner syntax for working with Promises", "Runs code on multiple threads", "B", "async/await is syntactic sugar over Promises. It makes asynchronous code look and behave like synchronous code, making it easier to read and reason about, especially for sequential operations."),
            ("Which method runs multiple Promises simultaneously and waits for all of them?", "Promise.race()", "Promise.any()", "Promise.all()", "C", "Promise.all() takes an array of Promises and returns a single Promise that resolves when ALL input Promises resolve, or rejects if any one fails. Ideal for parallel data fetching."),
        ],
        6: [
            ("Which method is most efficient for handling click events on many dynamically-added child elements?", "Add a listener to each child individually", "Event delegation on the parent", "Use setInterval to check for clicks", "B", "Event delegation attaches one listener to a parent and uses event.target to identify which child was clicked. This is more performant and automatically handles dynamically-added elements."),
            ("Which browser API allows you to persist data across page reloads?", "sessionStorage only", "cookies only", "localStorage", "C", "localStorage stores key-value pairs in the browser with no expiry date — data persists until explicitly cleared. sessionStorage clears when the tab is closed."),
        ],
    }
    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


