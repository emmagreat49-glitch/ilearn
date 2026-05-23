"""iLEARN — Python Programming course seed data."""
from .helpers import insert_lessons_and_quizzes

def seed_python(conn, c):
    c.execute("INSERT INTO courses (title,description,icon,level,language) VALUES (?,?,?,?,?)",
              ("Python Programming","A comprehensive Python course covering fundamentals through OOP, file handling, and real-world application patterns. Suitable for beginners and developers switching from other languages.","🐍","Beginner to Intermediate","python"))
    cid = c.lastrowid

    lessons = [
        (1,"Python Foundations & Data Types","""
<h2>Python Foundations</h2>
<p>Python is a <strong>high-level, interpreted, general-purpose</strong> programming language designed with code readability as its core principle. Created by <strong>Guido van Rossum</strong> and released in 1991, Python has grown into one of the world's most used languages, powering everything from Instagram's backend to NASA research pipelines and machine learning at Google.</p>

<h3>The Python Philosophy</h3>
<p>Python follows guiding principles called the <em>Zen of Python</em>. Run <code>import this</code> in any Python shell to see them. The most relevant for everyday coding:</p>
<ul>
  <li><strong>Readability counts</strong> — Code is read far more than it is written</li>
  <li><strong>Simple is better than complex</strong> — Avoid cleverness that obscures intent</li>
  <li><strong>Explicit is better than implicit</strong> — Say what you mean clearly</li>
  <li><strong>Errors should never pass silently</strong> — Handle exceptions, do not ignore them</li>
</ul>

<h3>How Python Executes Your Code</h3>
<p>When you run a <code>.py</code> file, the Python interpreter:</p>
<ol>
  <li><strong>Lexes & parses</strong> your source code into an Abstract Syntax Tree (AST)</li>
  <li><strong>Compiles</strong> the AST to bytecode (<code>.pyc</code> files stored in <code>__pycache__/</code>)</li>
  <li><strong>Executes</strong> the bytecode on the Python Virtual Machine (PVM)</li>
</ol>
<p>This bytecode is platform-independent — the same <code>.pyc</code> runs on Windows, macOS, or Linux as long as the Python version matches.</p>

<h3>Variables as References</h3>
<p>This is a critical distinction from languages like C or Java. In Python, a variable is a <strong>label pointing to an object in memory</strong>, not a container holding a value:</p>
<div class="code-block"><pre><code># Variables are references to objects
x = 42          # x points to integer object 42 in memory
y = x           # y points to the SAME object as x
x = 100         # x now points to a NEW object; y still points to 42
print(y)        # Output: 42

# id() returns the memory address of the object
print(id(x))    # e.g. 140234567890
print(id(y))    # Different — they now point to different objects

# Mutable objects — multiple references share state
list_a = [1, 2, 3]
list_b = list_a      # SAME object, not a copy!
list_b.append(4)
print(list_a)        # [1, 2, 3, 4] — both changed!

# Correct way to copy a list
list_c = list_a.copy()   # or list(list_a) or list_a[:]</code></pre></div>

<h3>Python's Built-in Data Types</h3>
<table class="lesson-table">
  <tr><th>Type</th><th>Example</th><th>Mutable?</th><th>Primary Use</th></tr>
  <tr><td><code>int</code></td><td><code>age = 25</code></td><td>No</td><td>Counters, IDs, whole numbers</td></tr>
  <tr><td><code>float</code></td><td><code>price = 9.99</code></td><td>No</td><td>Decimals, measurements, percentages</td></tr>
  <tr><td><code>str</code></td><td><code>name = "Alice"</code></td><td>No</td><td>Text, labels, messages</td></tr>
  <tr><td><code>bool</code></td><td><code>active = True</code></td><td>No</td><td>Flags, conditions, truth values</td></tr>
  <tr><td><code>list</code></td><td><code>[1, 2, 3]</code></td><td>Yes</td><td>Ordered, changeable collections</td></tr>
  <tr><td><code>dict</code></td><td><code>{"key": "val"}</code></td><td>Yes</td><td>Key-value mappings, JSON-like data</td></tr>
  <tr><td><code>tuple</code></td><td><code>(1, 2, 3)</code></td><td>No</td><td>Fixed collections, function returns</td></tr>
  <tr><td><code>set</code></td><td><code>{1, 2, 3}</code></td><td>Yes</td><td>Unique values, membership tests</td></tr>
  <tr><td><code>NoneType</code></td><td><code>None</code></td><td>No</td><td>Absence of value, default returns</td></tr>
</table>

<h3>Quick-Reference: Key Concepts</h3>
<p>Click each card to reveal the explanation:</p>
<div class="flip-grid">
  <div class="flip-card-wrap"><div class="flip-card">
    <div class="flip-front"><div class="flip-icon">🏷️</div><div class="flip-label">Dynamic Typing</div><div class="flip-hint">Click to learn</div></div>
    <div class="flip-back"><div class="flip-text">Variables hold references to objects, not values. Types are checked at runtime, not compile time. The same variable can hold any type at different times.</div></div>
  </div></div>
  <div class="flip-card-wrap"><div class="flip-card">
    <div class="flip-front"><div class="flip-icon">🧱</div><div class="flip-label">Mutability</div><div class="flip-hint">Click to learn</div></div>
    <div class="flip-back"><div class="flip-text">Lists, dicts, and sets are mutable — you can change them in place. Integers, strings, floats, and tuples are immutable — operations create new objects.</div></div>
  </div></div>
  <div class="flip-card-wrap"><div class="flip-card">
    <div class="flip-front"><div class="flip-icon">💾</div><div class="flip-label">Memory Model</div><div class="flip-hint">Click to learn</div></div>
    <div class="flip-back"><div class="flip-text">Variables are labels pointing to objects in memory. Assigning one variable to another copies the reference, not the object. Use .copy() for true copies.</div></div>
  </div></div>
  <div class="flip-card-wrap"><div class="flip-card">
    <div class="flip-front"><div class="flip-icon">🔄</div><div class="flip-label">Type Conversion</div><div class="flip-hint">Click to learn</div></div>
    <div class="flip-back"><div class="flip-text">Python never silently coerces types. You must explicitly convert: int("42"), str(100), float("3.14"), list((1,2,3)). This prevents subtle bugs.</div></div>
  </div></div>
</div>

<h3>Type System and Conversion</h3>
<div class="code-block"><pre><code># Python is DYNAMICALLY typed (types checked at runtime)
# but STRONGLY typed (no implicit coercion like JavaScript)
x = "5" + 3        # TypeError! Python won't auto-convert

# Explicit conversion (casting)
age_str = "25"
age_int = int(age_str)           # "25" -> 25
price   = float("9.99")          # "9.99" -> 9.99
label   = str(100)               # 100 -> "100"
is_on   = bool(1)                # 1 -> True (0 is False)

# Check types
print(type(age_int))             # <class 'int'>
print(isinstance(age_int, int))  # True
print(isinstance(age_int, (int, float)))  # True — check against multiple types

# Arithmetic coercion (int + float = float)
result = 5 + 2.0                 # 7.0 (float)
print(type(result))              # <class 'float'></code></pre></div>

<h3>Strings — Immutable Sequences</h3>
<div class="code-block"><pre><code>name = "iLEARN Platform"

# Indexing and slicing (0-indexed, negative from end)
print(name[0])          # 'i'
print(name[-1])         # 'm'
print(name[0:6])        # 'iLEARN'
print(name[7:])         # 'Platform'
print(name[::-1])       # Reversed: 'mroftalP NRAELi'

# String methods — strings are objects with rich methods
print(name.upper())                  # ILEARN PLATFORM
print(name.lower())                  # ilearn platform
print(name.title())                  # Ilearn Platform
print(name.replace("i", "e"))        # eLEARN Platform
print(name.split(" "))               # ['iLEARN', 'Platform']
print("  spaces  ".strip())          # 'spaces'
print(name.startswith("iL"))         # True
print(name.find("Platform"))         # 7 (index where it starts)
print(",".join(["a","b","c"]))        # 'a,b,c'

# f-strings (Python 3.6+) — preferred string formatting
user  = "Alice"
score = 98.567
print(f"Hello {user}, score: {score:.2f}%")  # Hello Alice, score: 98.57%
print(f"{user!r}")                            # 'Alice' (repr formatting)
print(f"{score:>10.1f}")                      # Right-aligned, width 10</code></pre></div>
        """,25),

        (2,"Control Flow, Loops & Comprehensions","""
<h2>Control Flow in Python</h2>
<p>Control flow determines the <strong>order in which statements execute</strong>. Python provides conditionals, loops, and powerful comprehension syntax that makes code both readable and efficient.</p>

<h3>Conditional Logic</h3>
<div class="code-block"><pre><code># Standard conditionals
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

# Ternary operator (conditional expression)
age = 20
status = "Adult" if age >= 18 else "Minor"

# Chained comparisons — unique to Python
x = 15
if 10 < x < 20:        # Equivalent to: x > 10 and x < 20
    print("In range")

# Truthiness — Python evaluates these as False:
# None, 0, 0.0, 0j, "", [], {}, set(), tuple()
data = []
if not data:
    print("No data found")   # This prints

# Match statement (Python 3.10+) — like switch/case
command = "quit"
match command:
    case "start":   print("Starting...")
    case "stop":    print("Stopping...")
    case "quit":    print("Quitting...")
    case _:         print("Unknown command")</code></pre></div>

<h3>For Loops — Idiomatic Iteration</h3>
<div class="code-block"><pre><code># Basic range-based loop
for i in range(1, 6):
    print(f"Step {i}")    # 1, 2, 3, 4, 5

# enumerate() — index and value together (avoid manual counters)
languages = ["Python", "Java", "JavaScript", "CSS"]
for index, lang in enumerate(languages, start=1):
    print(f"{index}. {lang}")

# zip() — iterate multiple iterables in parallel
names  = ["Alice", "Bob", "Carol"]
scores = [88, 92, 76]
grades = ["B", "A", "C"]
for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score} ({grade})")

# Iterating dictionaries
student = {"name": "Alice", "age": 22, "gpa": 3.9}
for key, value in student.items():
    print(f"  {key}: {value}")

# sorted(), reversed(), filter(), map()
numbers = [5, 2, 8, 1, 9, 3]
for n in sorted(numbers, reverse=True):
    print(n)    # 9, 8, 5, 3, 2, 1</code></pre></div>

<h3>While Loops and Loop Control</h3>
<div class="code-block"><pre><code># while with break and else
attempts = 0
while attempts < 3:
    password = input("Password: ")
    if password == "secret123":
        print("Access granted!")
        break
    attempts += 1
else:
    # Runs ONLY if loop finished WITHOUT hitting break
    print("Too many failed attempts. Account locked.")

# continue — skip rest of current iteration
for num in range(10):
    if num % 2 == 0:
        continue    # Skip even numbers
    print(num)      # Prints 1, 3, 5, 7, 9</code></pre></div>

<h3>Comprehensions — Pythonic One-liners</h3>
<p>Comprehensions are not just syntax sugar — they are <strong>optimised at the C level</strong> and run measurably faster than equivalent for loops.</p>
<div class="code-block"><pre><code># List comprehension: [expression for item in iterable if condition]
squares   = [x**2 for x in range(1, 11)]
evens     = [x for x in range(20) if x % 2 == 0]
cleaned   = [name.strip().title() for name in ["  alice", "BOB ", " carol"]]

# Nested comprehension — flatten a 2D matrix
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat   = [n for row in matrix for n in row]

# Dict comprehension
word_lengths = {word: len(word) for word in ["Python", "Java", "CSS"]}
# {'Python': 6, 'Java': 4, 'CSS': 3}

# Set comprehension — automatically removes duplicates
unique_initials = {name[0].upper() for name in ["alice", "bob", "anna", "carol"]}
# {'A', 'B', 'C'}

# Generator expression — memory-efficient, lazy evaluation
# Useful for large datasets — never stores the full result in memory
total = sum(x**2 for x in range(1_000_000))

# Conditional transformation in comprehension
labels = ["pass" if s >= 50 else "fail" for s in [70, 45, 88, 32]]
# ['pass', 'fail', 'pass', 'fail']</code></pre></div>
        """,25),

        (3,"Functions, Scope & Decorators","""
<h2>Functions in Python</h2>
<p>Functions are <strong>first-class objects</strong> in Python. They can be passed as arguments, returned from other functions, stored in data structures, and assigned to variables. This enables powerful patterns like decorators, callbacks, and higher-order programming.</p>

<h3>Parameter Types — All Variants</h3>
<div class="code-block"><pre><code># Python supports 5 parameter types in one function
def create_profile(
    name,                   # Positional (required)
    role,                   # Positional (required)
    *skills,                # *args — captures extra positional args as tuple
    active=True,            # Keyword-only with default (after *)
    **metadata              # **kwargs — captures extra keyword args as dict
):
    return {
        "name": name, "role": role,
        "skills": list(skills), "active": active,
        **metadata
    }

profile = create_profile(
    "Alice", "Engineer",
    "Python", "SQL", "Docker",   # Captured by *skills
    active=True,
    team="Backend", years=4      # Captured by **metadata
)
print(profile["skills"])   # ['Python', 'SQL', 'Docker']
print(profile["team"])     # Backend</code></pre></div>

<h3>Scope — The LEGB Rule</h3>
<p>Python resolves variable names by searching in this order: <strong>L</strong>ocal → <strong>E</strong>nclosing → <strong>G</strong>lobal → <strong>B</strong>uilt-in.</p>
<div class="code-block"><pre><code>x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)      # "local" — finds it immediately in Local scope
    
    inner()
    print(x)          # "enclosing" — inner's local x doesn't affect this

outer()
print(x)              # "global" — unchanged

# Modifying outer scopes
counter = 0
def increment():
    global counter    # Declare intent to modify global
    counter += 1

def make_counter():
    count = 0
    def inc():
        nonlocal count  # Modify enclosing (not global) scope
        count += 1
        return count
    return inc</code></pre></div>

<h3>Closures</h3>
<div class="code-block"><pre><code># Closure: inner function remembers enclosing scope after outer returns
def make_multiplier(factor):
    def multiply(number):
        return number * factor   # 'factor' is "closed over"
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))    # 10
print(triple(5))    # 15
print(double.__closure__[0].cell_contents)  # 2 — inspect the closure cell</code></pre></div>

<h3>Decorators — The Pattern Behind Frameworks</h3>
<p>A decorator is a function that takes another function and returns an enhanced version of it. Flask's <code>@app.route()</code>, Django's <code>@login_required</code>, and this project's <code>@login_required</code> are all decorators.</p>
<div class="code-block"><pre><code>import time
from functools import wraps

# Timer decorator
def timer(func):
    @wraps(func)   # Preserves __name__, __doc__ of original
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"{func.__name__} executed in {end-start:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)
# Output: slow_sum executed in 0.0287s

# Decorator with arguments (requires 3 levels of nesting)
def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url):
    # Will retry up to 3 times if it raises an exception
    pass</code></pre></div>
        """,30),

        (4,"Object-Oriented Programming (OOP)","""
<h2>OOP in Python</h2>
<p>Object-Oriented Programming organises code around <strong>objects</strong> — entities that combine <em>state (attributes)</em> and <em>behaviour (methods)</em>. Python supports all four OOP pillars: <strong>Encapsulation, Abstraction, Inheritance, and Polymorphism</strong>.</p>

<h3>Classes — Full Example</h3>
<div class="code-block"><pre><code>class BankAccount:
    bank_name    = "iLEARN Bank"     # Class variable (shared by all instances)
    _total_accts = 0

    def __init__(self, owner, initial_balance=0.0):
        self.owner    = owner
        self._balance = initial_balance   # _ prefix = convention for "private"
        BankAccount._total_accts += 1

    # Property decorator — controlled read access
    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        return self   # Return self enables method chaining

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Balance: {self._balance}")
        self._balance -= amount
        return self

    @classmethod
    def total_accounts(cls):
        return cls._total_accts

    @staticmethod
    def validate_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    def __repr__(self):
        return f"BankAccount(owner='{self.owner}', balance={self._balance:.2f})"

    def __str__(self):
        return f"Account [{self.owner}]: ${self._balance:,.2f}"

acc = BankAccount("Alice", 1000)
acc.deposit(500).withdraw(200)      # Method chaining
print(str(acc))                     # Account [Alice]: $1,300.00
print(BankAccount.total_accounts()) # 1</code></pre></div>

<h3>Inheritance and Polymorphism</h3>
<div class="code-block"><pre><code>class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0.0, rate=0.05):
        super().__init__(owner, balance)
        self.rate = rate

    def apply_interest(self):
        interest = self._balance * self.rate
        self._balance += interest
        return interest

    def __repr__(self):     # Polymorphism: overrides parent __repr__
        return f"SavingsAccount(owner='{self.owner}', balance={self._balance:.2f}, rate={self.rate:.0%})"

savings = SavingsAccount("Bob", 5000, rate=0.04)
earned  = savings.apply_interest()
print(f"Interest earned: ${earned:.2f}")   # $200.00

# Polymorphism in practice
accounts = [BankAccount("Alice", 1000), SavingsAccount("Bob", 5000)]
for acc in accounts:
    print(repr(acc))   # Each calls its OWN __repr__ method</code></pre></div>

<h3>Abstract Base Classes</h3>
<div class="code-block"><pre><code">from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: pass

    @abstractmethod
    def perimeter(self) -> float: pass

    def describe(self):
        print(f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}")

class Circle(Shape):
    def __init__(self, radius): self.radius = radius
    def area(self):      return math.pi * self.radius ** 2
    def perimeter(self): return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

# Shape() would raise TypeError — cannot instantiate abstract class
Circle(7).describe()       # Circle: area=153.94, perimeter=43.98
Rectangle(4, 6).describe() # Rectangle: area=24.00, perimeter=20.00</code></pre></div>
        """,35),

        (5,"File Handling, Exceptions & The Standard Library","""
<h2>File Handling</h2>
<p>Reading and writing files is fundamental to practically every real application. Python's <strong>context managers</strong> (the <code>with</code> statement) are the standard approach — they guarantee the file is closed even if an exception occurs mid-read.</p>

<div class="code-block"><pre><code># Writing text files
with open("students.txt", "w", encoding="utf-8") as f:
    f.write("Alice,22,3.9\\n")
    f.writelines(["Bob,24,3.5\\n", "Carol,21,3.7\\n"])

# Reading — whole file
with open("students.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Reading line by line (memory-efficient for large files)
with open("students.txt", "r", encoding="utf-8") as f:
    for line in f:
        name, age, gpa = line.strip().split(",")
        print(f"{name}: GPA {gpa}")

# File modes: "r" read | "w" write (overwrite) | "a" append | "b" binary

# JSON — the most common format for data exchange
import json

data = {
    "platform": "iLEARN",
    "courses": [
        {"id": 1, "title": "Python", "lessons": 5},
        {"id": 2, "title": "JavaScript", "lessons": 5}
    ]
}
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("data.json", "r") as f:
    loaded = json.load(f)
print(loaded["courses"][0]["title"])   # Python</code></pre></div>

<h3>Exception Handling — Professional Patterns</h3>
<div class="code-block"><pre><code"># Define custom exceptions for your domain
class LessonNotFoundError(Exception):
    def __init__(self, lesson_id):
        super().__init__(f"Lesson with ID {lesson_id} does not exist.")
        self.lesson_id = lesson_id

class QuizAlreadyCompletedError(Exception):
    pass

# Full try/except/else/finally pattern
def load_lesson(lesson_id):
    try:
        # Attempt the risky operation
        with open(f"lessons/{lesson_id}.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise LessonNotFoundError(lesson_id)
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted lesson file: {e}") from e
    except Exception as e:
        # Catch-all for unexpected errors — log, then re-raise
        print(f"Unexpected error loading lesson {lesson_id}: {e}")
        raise
    else:
        # Runs ONLY if no exception was raised
        print("Lesson loaded successfully")
    finally:
        # ALWAYS runs — use for cleanup
        print("Load attempt complete")</code></pre></div>

<h3>Key Standard Library Modules</h3>
<table class="lesson-table">
  <tr><th>Module</th><th>Purpose</th><th>Key Tools</th></tr>
  <tr><td><code>os / pathlib</code></td><td>File system operations</td><td>Path, os.listdir, os.makedirs</td></tr>
  <tr><td><code>datetime</code></td><td>Dates and times</td><td>datetime.now(), timedelta, strftime</td></tr>
  <tr><td><code>collections</code></td><td>Specialised containers</td><td>Counter, defaultdict, deque, namedtuple</td></tr>
  <tr><td><code>itertools</code></td><td>Efficient iteration</td><td>chain, product, combinations, islice</td></tr>
  <tr><td><code>functools</code></td><td>Higher-order functions</td><td>wraps, partial, lru_cache, reduce</td></tr>
  <tr><td><code>re</code></td><td>Regular expressions</td><td>match, findall, sub, compile</td></tr>
  <tr><td><code>logging</code></td><td>Application logging</td><td>basicConfig, getLogger, DEBUG/INFO/ERROR</td></tr>
  <tr><td><code>unittest</code></td><td>Testing framework</td><td>TestCase, assertEqual, mock</td></tr>
</table>
        """,30),
    ]

    quizzes = {
        1:[
            ("In Python, variables are best described as:","Containers that hold values directly","Labels (references) pointing to objects in memory","Static typed slots in a memory block","B","Python variables are references (pointers) to objects. Multiple variables can point to the same object, and reassigning a variable just moves the pointer without affecting the original object."),
            ("Which of these data types is IMMUTABLE in Python?","list","dict","tuple","C","Tuples are immutable — you cannot add, remove, or change their elements after creation. Lists and dicts are mutable and can be modified in place."),
            ("What does isinstance(3.14, (int, float)) return?","TypeError","False","True","C","isinstance() accepts a tuple of types. Since 3.14 is a float, and float is in the tuple, it returns True."),
        ],
        2:[
            ("What does the 'else' clause on a while loop do?","Runs if the condition was False from the start","Runs if the loop exits normally WITHOUT hitting 'break'","Runs after every iteration","B","The else clause on a loop is a Python-specific feature. It only runs if the loop completes without hitting a break statement."),
            ("Which is the most memory-efficient for large datasets?","[x for x in range(1000000)]","list(range(1000000))","(x for x in range(1000000))","C","Generator expressions use lazy evaluation — they yield values one at a time rather than building the entire list in memory. Essential for large datasets."),
            ("What does enumerate(['a','b'], start=1) produce first?","(0, 'a')","(1, 'a')","('a', 1)","B","With start=1, enumerate begins its counter at 1. The first yielded tuple is (index, value) = (1, 'a')."),
        ],
        3:[
            ("What does @wraps(func) from functools do?","Makes the function run faster","Preserves the original function's __name__ and __doc__ in the wrapper","Makes the function thread-safe","B","Without @wraps, the wrapper function would show its own name/docstring instead of the original's, breaking debugging, introspection, and documentation tools."),
            ("In the LEGB rule, 'E' stands for:","External scope","Enclosing scope","Exported scope","B","LEGB = Local, Enclosing, Global, Built-in. Enclosing refers to the scope of any surrounding function (relevant in nested/closure patterns)."),
        ],
        4:[
            ("What is the purpose of super().__init__() in a subclass?","Delete the parent class from memory","Call the parent class constructor to initialise inherited attributes","Create a copy of the parent class","B","super().__init__() delegates construction to the parent class. Without it, the parent's attributes would not be initialised, causing AttributeErrors when accessing them."),
            ("What does the @property decorator do?","Creates a static method","Turns a method into a computed attribute accessed like a variable","Creates a class variable","B","@property makes a method callable without parentheses, allowing controlled access to private attributes while keeping the interface clean (e.g., account.balance instead of account.get_balance())."),
        ],
        5:[
            ("Why use 'with open()' instead of open() followed by f.close()?","It's shorter to write","It automatically closes the file even if an exception occurs inside the block","It's the only way to read binary files","B","Context managers (with statement) guarantee cleanup. If an exception occurs inside the block, Python still calls __exit__() on the context manager, ensuring the file is properly closed."),
            ("When does the 'else' block in try/except execute?","Always, after any exception","Only when NO exception was raised in the try block","Only after a specific exception type","B","The else block in try/except executes only when the try block ran without raising any exception. It's useful for code that should only run when everything succeeded."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


# ═══════════════════════════════════════════════
# JAVASCRIPT COURSE
# ═══════════════════════════════════════════════


def extend_python(conn, c, cid):
    lessons = [
        (4, "Object-Oriented Programming", """
<h2>Object-Oriented Programming (OOP)</h2>
<p>OOP is a programming paradigm that organises code around <strong>objects</strong> — bundles of data (attributes) and behaviour (methods). Python is fully object-oriented: even integers and strings are objects.</p>

<div class="concept-box">
  <div class="cb-title">Core OOP Pillars</div>
  <p><strong>Encapsulation</strong> — bundle data and methods; hide internal details.<br>
  <strong>Inheritance</strong> — a child class reuses and extends a parent class.<br>
  <strong>Polymorphism</strong> — different objects respond to the same method call differently.<br>
  <strong>Abstraction</strong> — expose only what is necessary.</p>
</div>

<h3>How a Class Gets Built — Step by Step</h3>
<div class="step-animator">
  <div class="step-item">
    <div class="step-header"><div class="step-num">1</div><div class="step-title">Define the class and its attributes</div></div>
    <div class="step-body">Use the <code>class</code> keyword. The <code>__init__</code> method runs every time an object is created. <code>self</code> is the object itself — always the first parameter.</div>
  </div>
  <div class="step-item">
    <div class="step-header"><div class="step-num">2</div><div class="step-title">Add methods (behaviours)</div></div>
    <div class="step-body">Methods are functions inside a class. They always receive <code>self</code> as their first argument so they can access the object's own data. Return <code>self</code> to enable method chaining.</div>
  </div>
  <div class="step-item">
    <div class="step-header"><div class="step-num">3</div><div class="step-title">Create instances and call methods</div></div>
    <div class="step-body">Call the class like a function to create an object: <code>acc = BankAccount("Alice", 1000)</code>. Then call methods on it: <code>acc.deposit(500)</code>. Each object has its own copy of the attributes.</div>
  </div>
  <div class="step-item">
    <div class="step-header"><div class="step-num">4</div><div class="step-title">Extend with Inheritance</div></div>
    <div class="step-body">A child class puts the parent in parentheses: <code>class SavingsAccount(BankAccount)</code>. Call <code>super().__init__(...)</code> to run the parent setup, then add new attributes and override methods as needed.</div>
  </div>
  <div class="step-controls">
    <button class="btn btn-ghost btn-sm step-prev">← Previous</button>
    <span class="step-counter">1 / 4</span>
    <button class="btn btn-primary btn-sm step-next">Next →</button>
  </div>
</div>

<h3>Defining a Class</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="class BankAccount:
    # Class attribute — shared by ALL instances
    bank_name = &quot;iLearn Bank&quot;

    def __init__(self, owner, balance=0):
        # Instance attributes — unique per object
        self.owner   = owner
        self.balance = balance
        self._transactions = []   # _ prefix = convention for &quot;private&quot;

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(&quot;Deposit must be positive&quot;)
        self.balance += amount
        self._transactions.append(f&quot;+{amount}&quot;)
        return self

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(&quot;Insufficient funds&quot;)
        self.balance -= amount
        self._transactions.append(f&quot;-{amount}&quot;)
        return self

    def statement(self):
        return f&quot;{self.owner}: ${self.balance} | {self._transactions}&quot;

    def __repr__(self):
        return f&quot;BankAccount(owner={self.owner!r}, balance={self.balance})&quot;

# Create instances
acc1 = BankAccount(&quot;Alice&quot;, 1000)
acc1.deposit(500).withdraw(200)   # method chaining
print(acc1.statement())           # Alice: $1300 | [+500, -200]
print(acc1)                       # BankAccount(owner=&#39;Alice&#39;, balance=1300)"></code></pre></div>

<h3>Inheritance</h3>
<div class="code-block"><pre><code>class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.05):
        super().__init__(owner, balance)   # call parent __init__
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = round(self.balance * self.interest_rate, 2)
        self.deposit(interest)
        print(f"Interest applied: +${interest}")

savings = SavingsAccount("Bob", 2000)
savings.apply_interest()   # Interest applied: +$100.0
print(savings.balance)     # 2100.0</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Create a <code>Vehicle</code> class with attributes <code>make</code>, <code>model</code>, <code>year</code> and a method <code>describe()</code>.</li>
    <li>Create a <code>Car</code> class that inherits from <code>Vehicle</code> and adds a <code>num_doors</code> attribute.</li>
    <li>Override <code>describe()</code> in <code>Car</code> to include door count.</li>
    <li>Create three Car instances and store them in a list. Loop through and call <code>describe()</code> on each.</li>
  </ol>
</div>
""", 45),
        (5, "File Handling & Error Management", """
<h2>File Handling in Python</h2>
<p>Reading and writing files is fundamental to real-world Python. Python's built-in <code>open()</code> function gives you full control over files, and the <strong>context manager</strong> (<code>with</code> statement) ensures files are always properly closed.</p>

<h3>Reading Files</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="# Always use &quot;with&quot; — it auto-closes the file even if an error occurs
with open(&quot;data.txt&quot;, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
    content = f.read()         # Entire file as one string
    # OR
    lines = f.readlines()      # List of lines
    # OR
    for line in f:             # Memory-efficient for large files
        print(line.strip())

# Writing — &quot;w&quot; overwrites, &quot;a&quot; appends
with open(&quot;output.txt&quot;, &quot;w&quot;, encoding=&quot;utf-8&quot;) as f:
    f.write(&quot;Line 1\n&quot;)
    f.writelines([&quot;Line 2\n&quot;, &quot;Line 3\n&quot;])"></code></pre></div>

<h3>Working with JSON</h3>
<div class="code-block"><pre><code>import json

# Python dict -> JSON file
student = {"name": "Alice", "grade": "A", "scores": [88, 92, 95]}
with open("student.json", "w") as f:
    json.dump(student, f, indent=2)

# JSON file -> Python dict
with open("student.json", "r") as f:
    loaded = json.load(f)
print(loaded["name"])   # Alice</code></pre></div>

<h3>Exception Handling</h3>
<div class="code-block"><pre><code>def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError as e:
        print(f"Type error: {e}")
        return None
    else:
        # Runs only if NO exception was raised
        print(f"Result: {result}")
        return result
    finally:
        # ALWAYS runs — use for cleanup
        print("Division attempted.")

safe_divide(10, 2)   # Result: 5.0
safe_divide(10, 0)   # Error: Cannot divide by zero</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Write a program that reads a text file and counts how many times each word appears (use a dictionary).</li>
    <li>Write a student grade tracker that saves records to a JSON file and can load them back.</li>
    <li>Handle the <code>FileNotFoundError</code> gracefully when trying to open a file that doesn't exist.</li>
    <li>Create a log-writer function that appends timestamped messages to a <code>log.txt</code> file.</li>
  </ol>
</div>
""", 40),
        (6, "Python in Practice — APIs & Projects", """
<h2>Real-World Python: APIs, Data & Projects</h2>
<p>You now know enough Python to build real projects. This lesson covers the most important practical skills: working with web APIs, processing CSV data, and structuring a proper project.</p>

<h3>Calling a Web API with requests</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="import requests

# GET request — fetch data from a public API
response = requests.get(&quot;https://api.github.com/users/octocat&quot;)

# Always check the status code
if response.status_code == 200:
    data = response.json()     # Parse JSON automatically
    print(data[&quot;name&quot;])        # The Octocat
    print(data[&quot;public_repos&quot;]) # Number of repos
else:
    print(f&quot;Error: {response.status_code}&quot;)

# POST request — send data
payload = {&quot;title&quot;: &quot;New Post&quot;, &quot;body&quot;: &quot;Content here&quot;, &quot;userId&quot;: 1}
r = requests.post(&quot;https://jsonplaceholder.typicode.com/posts&quot;, json=payload)
print(r.json()[&quot;id&quot;])   # ID of newly created resource"></code></pre></div>

<h3>Processing CSV Data</h3>
<div class="code-block"><pre><code>import csv

# Reading CSV
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)   # Each row is a dict
    for row in reader:
        print(row["name"], row["grade"])

# Writing CSV
students = [
    {"name": "Alice", "grade": "A", "score": 92},
    {"name": "Bob",   "grade": "B", "score": 78},
]
with open("grades.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name","grade","score"])
    writer.writeheader()
    writer.writerows(students)</code></pre></div>

<h3>Project Structure — Best Practices</h3>
<div class="code-block"><pre><code>my_project/
├── main.py           # Entry point — keep it short
├── config.py         # Constants, settings, API keys
├── models/
│   ├── __init__.py
│   └── user.py       # Data classes and DB models
├── services/
│   ├── __init__.py
│   └── api_client.py # External API calls
├── utils/
│   └── helpers.py    # Small reusable functions
├── tests/
│   └── test_user.py  # Unit tests
└── requirements.txt  # pip freeze > requirements.txt</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Final Python Project Ideas</div>
  <ol>
    <li><strong>Weather App</strong> — Call the OpenWeatherMap free API, display temperature and conditions for any city.</li>
    <li><strong>Student Grade Tracker</strong> — Read/write CSV, calculate averages, output a report.</li>
    <li><strong>Quote of the Day Bot</strong> — Fetch a random quote from an API and save it to a daily log file.</li>
    <li><strong>Simple CLI To-Do App</strong> — Add, list, complete, and delete tasks stored in a JSON file.</li>
  </ol>
</div>
""", 50),
    ]
    quizzes = {
        4: [
            ("In Python OOP, which method is called automatically when a new object is created?", "__start__()", "__init__()", "__new__()", "B", "__init__ is the initialiser — it runs immediately after Python allocates memory for the new object, letting you set up instance attributes."),
            ("What does the `super()` function do in a child class?", "Deletes the parent class", "Calls a method from the parent class", "Creates a copy of the parent", "B", "super() gives you a proxy object that delegates method calls to the parent class, allowing you to reuse and extend parent behaviour without hard-coding the parent name."),
        ],
        5: [
            ("Which Python keyword ensures a file is always closed after use, even if an error occurs?", "try", "with", "finally", "B", "The `with` statement (context manager) calls __exit__ automatically, which closes the file. This is safer than manual f.close() because it runs even if an exception is raised."),
            ("Which exception is raised when you try to open a file that does not exist?", "FileError", "FileNotFoundError", "IOError", "B", "FileNotFoundError (a subclass of OSError) is raised when Python cannot find the specified file path."),
        ],
        6: [
            ("Which HTTP status code means a request was successful?", "404", "500", "200", "C", "200 OK is the standard success response. 404 = Not Found, 500 = Internal Server Error."),
            ("What does `csv.DictReader` return for each row in a CSV file?", "A list", "A dictionary", "A tuple", "B", "DictReader maps each row to a dict where keys come from the header row, making it much easier to access columns by name."),
        ],
    }
    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


