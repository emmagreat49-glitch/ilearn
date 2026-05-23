"""iLEARN — Java Programming course seed data."""
from .helpers import insert_lessons_and_quizzes

def seed_java(conn, c):
    c.execute("INSERT INTO courses (title,description,icon,level,language) VALUES (?,?,?,?,?)",
              ("Java Programming","Learn Java — the language powering Android apps, enterprise banking systems, and large-scale backends. Covers the type system, OOP, collections framework, and robust exception handling.","☕","Intermediate","java"))
    cid = c.lastrowid

    lessons = [
        (1,"Java Fundamentals & the Type System","""
<h2>Java: Compiled, Statically Typed, Platform-Independent</h2>
<p>Java was created by James Gosling at Sun Microsystems in 1995 under the philosophy <strong>"Write Once, Run Anywhere"</strong>. Java source code compiles to <em>bytecode</em> (not machine code), which runs on the <strong>Java Virtual Machine (JVM)</strong>. This means the same compiled Java program runs on Windows, macOS, Linux, and any other platform that has a JVM.</p>

<h3>Java vs Python vs JavaScript — Key Differences</h3>
<table class="lesson-table">
  <tr><th>Feature</th><th>Java</th><th>Python</th><th>JavaScript</th></tr>
  <tr><td>Typing</td><td>Static (compile-time)</td><td>Dynamic (runtime)</td><td>Dynamic (runtime)</td></tr>
  <tr><td>Compilation</td><td>Compiled to JVM bytecode</td><td>Interpreted</td><td>JIT-compiled in browser</td></tr>
  <tr><td>OOP</td><td>Mandatory — everything in a class</td><td>Optional but supported</td><td>Prototype-based</td></tr>
  <tr><td>Concurrency</td><td>Threads built-in</td><td>GIL limits threading</td><td>Event loop (single thread)</td></tr>
  <tr><td>Primary uses</td><td>Android, enterprise, big data</td><td>AI/ML, data, scripting</td><td>Web (frontend + Node backend)</td></tr>
</table>

<h3>Primitive Types — Java's 8 Built-ins</h3>
<div class="code-block"><pre><code>// Java requires you to declare types explicitly
byte    b  = 127;             // 8-bit: -128 to 127
short   s  = 32_000;          // 16-bit: -32,768 to 32,767
int     i  = 2_147_483_647;   // 32-bit: most common integer type
long    l  = 9_999_999_999L;  // 64-bit: note the L suffix!
float   f  = 3.14f;           // 32-bit decimal: note the f suffix!
double  d  = 3.14159265358;   // 64-bit decimal: default for decimals
char    c  = 'A';             // Single UTF-16 character (note single quotes)
boolean flag = true;          // Only true or false

// Underscores in numeric literals (Java 7+) — improve readability
long creditCard = 1234_5678_9012_3456L;
int  hexColor   = 0xFF_AA_33;

// Casting between numeric types
double pi       = 3.14159;
int truncated   = (int) pi;       // Explicit narrowing cast: 3
int smallInt    = 100;
double exact    = smallInt;       // Implicit widening: 100.0</code></pre></div>

<h3>Wrapper Classes and Autoboxing</h3>
<div class="code-block"><pre><code">// Every primitive has an Object wrapper class
// Needed for generics (List<Integer> not List<int>)
Integer   num     = 42;          // Autoboxing: int → Integer
Double    price   = 9.99;
Boolean   active  = true;
Character letter  = 'Z';

// Autoboxing and unboxing happen automatically
List<Integer> numbers = new ArrayList<>();
numbers.add(42);          // Autoboxes int to Integer
int first = numbers.get(0); // Unboxes Integer to int

// Useful wrapper class utilities
int     parsed   = Integer.parseInt("123");       // String → int
String  str      = Integer.toBinaryString(255);   // "11111111"
int     max      = Integer.MAX_VALUE;             // 2,147,483,647
int     min      = Integer.MIN_VALUE;             // -2,147,483,648
boolean isNum    = Character.isDigit('5');         // true

// Null danger with wrappers
Integer box = null;
int val = box;   // NullPointerException! Cannot unbox null</code></pre></div>

<h3>Strings in Java</h3>
<div class="code-block"><pre><code">// Strings are immutable objects in Java (like Python)
String name = "iLEARN";

// String operations
System.out.println(name.length());         // 6
System.out.println(name.charAt(0));        // 'i'
System.out.println(name.substring(1, 4)); // "LEA"
System.out.println(name.toLowerCase());   // "ilearn"
System.out.println(name.contains("LEARN")); // true
System.out.println(name.replace("i", "e")); // "eLEARN"
System.out.println(name.startsWith("iL")); // true
String[] parts = "a,b,c".split(",");       // ["a", "b", "c"]

// String comparison — ALWAYS use .equals(), never ==
String a = new String("hello");
String b = new String("hello");
System.out.println(a == b);        // false — different objects!
System.out.println(a.equals(b));   // true — same content

// String formatting
String msg = String.format("Hello %s, score: %.2f%%", "Alice", 98.567);
// "Hello Alice, score: 98.57%"

// StringBuilder — for building strings in loops (much faster)
StringBuilder sb = new StringBuilder();
for (int i = 1; i <= 5; i++) {
    sb.append("Item ").append(i).append("\\n");
}
String result = sb.toString();</code></pre></div>
        """,20),

        (2,"OOP — Classes, Inheritance & Interfaces","""
<h2>Object-Oriented Programming in Java</h2>
<p>Java enforces OOP — you cannot write code outside of a class. Every Java program consists of classes interacting through well-defined interfaces. This enforced structure is what makes Java suitable for <strong>large teams building complex, long-lived systems</strong>.</p>

<h3>Access Modifiers — Encapsulation</h3>
<table class="lesson-table">
  <tr><th>Modifier</th><th>Class</th><th>Package</th><th>Subclass</th><th>World</th></tr>
  <tr><td><code>public</code></td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
  <tr><td><code>protected</code></td><td>✓</td><td>✓</td><td>✓</td><td>✗</td></tr>
  <tr><td>(default)</td><td>✓</td><td>✓</td><td>✗</td><td>✗</td></tr>
  <tr><td><code>private</code></td><td>✓</td><td>✗</td><td>✗</td><td>✗</td></tr>
</table>

<div class="code-block"><pre><code">public class Student {
    // Fields — usually private (encapsulation)
    private final int id;      // final = cannot change after construction
    private String name;
    private double gpa;

    // Constructor — same name as class, no return type
    public Student(int id, String name, double gpa) {
        this.id   = id;        // 'this' disambiguates field vs parameter
        this.name = name;
        setGpa(gpa);           // Use setter for validation
    }

    // Getter — read-only access
    public int    getId()   { return id; }
    public String getName() { return name; }
    public double getGpa()  { return gpa; }

    // Setter with validation
    public void setGpa(double gpa) {
        if (gpa < 0.0 || gpa > 4.0)
            throw new IllegalArgumentException("GPA must be 0.0 to 4.0");
        this.gpa = gpa;
    }

    // Override Object methods
    @Override
    public String toString() {
        return String.format("Student{id=%d, name='%s', gpa=%.2f}", id, name, gpa);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Student)) return false;
        return this.id == ((Student) obj).id;
    }

    @Override
    public int hashCode() { return Integer.hashCode(id); }
}</code></pre></div>

<h3>Inheritance</h3>
<div class="code-block"><pre><code">// Java supports single inheritance — extends one class only
public class GraduateStudent extends Student {
    private String thesisTitle;
    private String supervisor;

    public GraduateStudent(int id, String name, double gpa,
                            String thesis, String supervisor) {
        super(id, name, gpa);   // Must call parent constructor first
        this.thesisTitle = thesis;
        this.supervisor  = supervisor;
    }

    // Method overriding with @Override annotation
    @Override
    public String toString() {
        return super.toString()
             + String.format(", thesis='%s', supervisor='%s'",
                             thesisTitle, supervisor);
    }

    // New method only in GraduateStudent
    public String getResearchSummary() {
        return getName() + " researching: " + thesisTitle;
    }
}

// Polymorphism — parent type reference, child object
Student s = new GraduateStudent(1, "Alice", 3.9, "AI in EdTech", "Dr. Smith");
System.out.println(s);             // Calls GraduateStudent.toString()
System.out.println(s instanceof Student);         // true
System.out.println(s instanceof GraduateStudent); // true

// Downcast when you need child-specific methods
GraduateStudent gs = (GraduateStudent) s;
System.out.println(gs.getResearchSummary());</code></pre></div>

<h3>Interfaces vs Abstract Classes</h3>
<div class="code-block"><pre><code">// INTERFACE — pure contract, no instance variables
// A class can implement MULTIPLE interfaces
public interface Assessable {
    double calculateFinalScore();                  // Abstract by default
    default String getGrade() {                   // Default method (Java 8+)
        double score = calculateFinalScore();
        if (score >= 90) return "A";
        if (score >= 75) return "B";
        return "C";
    }
}

// ABSTRACT CLASS — partial implementation, one inheritance slot
public abstract class Course {
    protected final String title;
    protected final int    creditHours;

    public Course(String title, int credits) {
        this.title       = title;
        this.creditHours = credits;
    }
    public abstract double calculateFinalScore();  // Subclass must implement
    public String getTitle() { return title; }     // Concrete — inherited
}

// Concrete class — implements interface AND extends abstract class
public class PythonCourse extends Course implements Assessable {
    private double examScore, projectScore;

    public PythonCourse(String title, int credits, double exam, double project) {
        super(title, credits);
        this.examScore    = exam;
        this.projectScore = project;
    }

    @Override
    public double calculateFinalScore() {
        return examScore * 0.6 + projectScore * 0.4;
    }
    // getGrade() is inherited from Assessable default method
}</code></pre></div>
        """,30),

        (3,"Collections Framework","""
<h2>Java Collections Framework</h2>
<p>The Collections Framework provides battle-tested data structures. Choosing the right one for your use case is a key Java competency and common interview topic.</p>

<h3>List — Ordered, Indexed, Allows Duplicates</h3>
<div class="code-block"><pre><code">import java.util.*;

// ArrayList — backed by a dynamic array
// O(1) random access, O(n) insert/delete in middle
List<String> courses = new ArrayList<>();
courses.add("Python");
courses.add("Java");
courses.add("CSS");
courses.add(1, "JavaScript");    // Insert at index 1

// Access and search
String first  = courses.get(0);              // O(1)
int    idx    = courses.indexOf("Java");     // O(n) linear search
boolean has   = courses.contains("CSS");     // O(n)

// Sorting
Collections.sort(courses);                          // Natural order
courses.sort(Comparator.comparingInt(String::length)); // By length
courses.sort(Comparator.reverseOrder());             // Reverse

// Iteration options
for (String course : courses) { /* enhanced for */ }
courses.forEach(c -> System.out.println(c));        // Lambda
courses.stream().filter(c -> c.length() > 4).forEach(System.out::println);

// LinkedList — backed by doubly-linked list
// O(n) random access, O(1) insert/delete at head/tail
Deque<String> queue = new LinkedList<>();
queue.offerFirst("first");  // Add to front
queue.offerLast("last");    // Add to back
queue.pollFirst();           // Remove and return front</code></pre></div>

<h3>Map — Key-Value Pairs</h3>
<div class="code-block"><pre><code">// HashMap — unordered, O(1) average get/put
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob",   87);
scores.put("Alice", 98);   // Overwrites previous value

// Reading
int aliceScore = scores.get("Alice");                  // 98
int danScore   = scores.getOrDefault("Dan", 0);        // 0 — key absent
scores.putIfAbsent("Carol", 92);                        // Only if key not present

// Conditional update (Java 8+)
scores.merge("Alice", 5, Integer::sum);  // Alice: 98 + 5 = 103
scores.computeIfAbsent("Eve", k -> 0);  // Add with computed value

// Iteration
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.printf("%-10s: %d%n", entry.getKey(), entry.getValue());
}
scores.forEach((name, score) ->  // Lambda form
    System.out.printf("%-10s: %d%n", name, score));

// LinkedHashMap — maintains insertion order
// TreeMap      — sorted by key (natural or Comparator)</code></pre></div>

<h3>Set — Unique Elements</h3>
<div class="code-block"><pre><code">// HashSet — unordered unique elements, O(1) add/contains/remove
Set<String> tags = new HashSet<>();
tags.add("python"); tags.add("web"); tags.add("python"); // Duplicate ignored
System.out.println(tags.size());     // 2
System.out.println(tags.contains("web"));  // true

// Set operations
Set<String> a = new HashSet<>(Arrays.asList("A","B","C"));
Set<String> b = new HashSet<>(Arrays.asList("B","C","D"));

Set<String> union     = new HashSet<>(a); union.addAll(b);      // A,B,C,D
Set<String> intersect = new HashSet<>(a); intersect.retainAll(b); // B,C
Set<String> diff      = new HashSet<>(a); diff.removeAll(b);     // A

// TreeSet — sorted order
Set<Integer> sorted = new TreeSet<>(Arrays.asList(5,3,8,1,4));
System.out.println(sorted);  // [1, 3, 4, 5, 8]</code></pre></div>
        """,25),

        (4,"Exception Handling & Java I/O","""
<h2>Java's Exception Handling System</h2>
<p>Java has a <strong>mandatory, compile-time checked exception system</strong>. Certain exceptions <em>must</em> be handled or declared — the compiler rejects your code otherwise. This forces developers to think about failure scenarios upfront, making Java code more robust but more verbose.</p>

<h3>The Exception Hierarchy</h3>
<table class="lesson-table">
  <tr><th>Type</th><th>Extends</th><th>Must Handle?</th><th>Examples</th></tr>
  <tr><td>Checked Exception</td><td>Exception</td><td>Yes — compiler enforces</td><td>IOException, SQLException, ParseException</td></tr>
  <tr><td>Unchecked (Runtime)</td><td>RuntimeException</td><td>No — optional</td><td>NullPointerException, IllegalArgumentException, ArrayIndexOutOfBoundsException</td></tr>
  <tr><td>Error</td><td>Error</td><td>No — usually fatal</td><td>OutOfMemoryError, StackOverflowError</td></tr>
</table>

<div class="code-block"><pre><code">// Custom exception — extend appropriate base
public class InsufficientFundsException extends Exception {
    private final double requested;
    private final double available;

    public InsufficientFundsException(double requested, double available) {
        super(String.format("Requested %.2f but only %.2f available",
                            requested, available));
        this.requested = requested;
        this.available = available;
    }
    public double getShortfall() { return requested - available; }
}

// Throwing and catching
public void withdraw(double amount) throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException(amount, balance);
    }
    balance -= amount;
}

// Full try-catch-finally
try {
    account.withdraw(1000);
    System.out.println("Withdrawal successful");
} catch (InsufficientFundsException e) {
    System.err.println("Failed: " + e.getMessage());
    System.err.println("Shortfall: " + e.getShortfall());
} catch (IllegalArgumentException e) {
    System.err.println("Invalid amount: " + e.getMessage());
} finally {
    auditLog.record(transaction);   // ALWAYS executes
}</code></pre></div>

<h3>Try-With-Resources (Java 7+)</h3>
<div class="code-block"><pre><code">// Any class implementing AutoCloseable can be used in try-with-resources
// The resource is AUTOMATICALLY closed when the block exits (success or exception)

public List<String> readCSV(String path) throws IOException {
    List<String> records = new ArrayList<>();

    // Both reader and parser are closed automatically
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.isBlank()) {
                records.add(line.trim());
            }
        }
    }
    // reader.close() called automatically here

    return records;
}

// Multiple resources in one try
try (
    Connection conn = dataSource.getConnection();
    PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
) {
    stmt.setInt(1, userId);
    ResultSet rs = stmt.executeQuery();
    while (rs.next()) {
        System.out.println(rs.getString("username"));
    }
}
// conn and stmt both closed automatically</code></pre></div>
        """,25),
    ]

    quizzes = {
        1:[
            ("What suffix is required for a long literal in Java?","d or D","f or F","L or l","C","Long literals need an L suffix (e.g., 9999999999L). Without it, Java treats the literal as int and throws a compile error if the value exceeds Integer.MAX_VALUE."),
            ("What is autoboxing in Java?","Automatically packaging code into a JAR","Automatic conversion between primitives and their wrapper classes","Converting one primitive type to another","B","Autoboxing is Java's automatic wrapping of primitives into their object wrappers (int → Integer) and unboxing is the reverse. Required when working with generics and collections."),
            ("What is the correct way to compare two String values in Java?","str1 == str2","str1.compareTo(str2)","str1.equals(str2)","C","== compares object references (memory addresses), not content. Two String objects with identical content are different objects. Always use .equals() for content comparison."),
        ],
        2:[
            ("What is the main reason a class can implement multiple interfaces but only extend one class?","Java limitation that will be removed soon","Prevents the diamond inheritance ambiguity problem for method implementations","Interfaces use less memory","B","Multiple inheritance of classes creates the diamond problem — ambiguity about which parent's method implementation to use. Interfaces (pre-Java 8) had no implementations, so multiple implementation was safe."),
            ("When must you call super() in a subclass constructor?","Never — Java calls it automatically","Only if the parent has no default constructor","It must be the FIRST statement if called explicitly","C","If you call super(), it must be the very first statement in the subclass constructor. Java automatically calls super() with no arguments if you don't — which fails if the parent has no no-arg constructor."),
        ],
        3:[
            ("What type of Map maintains insertion order in Java?","HashMap","TreeMap","LinkedHashMap","C","LinkedHashMap maintains the order keys were inserted. HashMap has no ordering guarantee. TreeMap sorts keys by natural order or a Comparator."),
            ("What is the time complexity of get() on a HashMap?","O(n) linear","O(log n)","O(1) average","C","HashMap uses hashing — computing the bucket from the key's hash code gives O(1) average time. In the worst case (all keys hash to same bucket) it degrades to O(n), but good hash functions and Java's tree-ification of long buckets (Java 8+) make this rare."),
        ],
        4:[
            ("What is a checked exception in Java?","Any exception from java.lang package","An exception the compiler forces you to handle or declare with throws","An exception caught inside a catch block","B","Checked exceptions are enforced at COMPILE TIME. If a method can throw one, you must either surround the call with try/catch or declare 'throws ExceptionType' in your method signature."),
            ("What is the advantage of try-with-resources over manually calling close()?","It runs faster","It automatically closes resources even when an exception occurs","It only works with files","B","try-with-resources calls close() on AutoCloseable resources automatically when the block exits — whether normally or due to an exception. This eliminates the common bug of forgetting to close resources in error paths."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


# ═══════════════════════════════════════════════
# DATA SCIENCE COURSE
# ═══════════════════════════════════════════════


def extend_java(conn, c, cid):
    lessons = [
        (4, "Collections, Generics & Streams", """
<h2>Java Collections, Generics & Streams</h2>
<p>The Collections Framework and the Stream API (Java 8+) are what you use in almost every real Java application. Mastering these is essential for backend and Android development.</p>

<h3>Core Collection Types</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="import java.util.*;

// ArrayList — dynamic array, fast random access
List&lt;String&gt; names = new ArrayList&lt;&gt;();
names.add(&quot;Alice&quot;);
names.add(&quot;Bob&quot;);
names.add(&quot;Charlie&quot;);
System.out.println(names.get(1));   // Bob
names.remove(&quot;Bob&quot;);

// HashMap — key-value pairs, O(1) lookup
Map&lt;String, Integer&gt; scores = new HashMap&lt;&gt;();
scores.put(&quot;Alice&quot;, 95);
scores.put(&quot;Bob&quot;,   82);
scores.getOrDefault(&quot;Carol&quot;, 0);   // returns 0 if not found

// HashSet — unique elements only, O(1) contains
Set&lt;String&gt; unique = new HashSet&lt;&gt;(names);
unique.add(&quot;Alice&quot;);   // ignored — already present
System.out.println(unique.contains(&quot;Alice&quot;));  // true

// LinkedList — fast insert/delete at ends (use as queue/deque)
Queue&lt;String&gt; queue = new LinkedList&lt;&gt;();
queue.offer(&quot;first&quot;);
queue.poll();   // removes and returns head"></code></pre></div>

<h3>The Stream API — Functional Data Processing</h3>
<div class="code-block"><pre><code>import java.util.stream.*;

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// filter + map + collect — the most common pipeline
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)          // keep even numbers
    .map(n -> n * n)                   // square them
    .collect(Collectors.toList());     // [4, 16, 36, 64, 100]

// reduce — aggregate to a single value
int sum = numbers.stream()
    .reduce(0, Integer::sum);          // 55

// Sorting and finding
Optional<String> first = names.stream()
    .filter(s -> s.startsWith("A"))
    .sorted()
    .findFirst();

first.ifPresent(System.out::println);  // Alice (no NullPointerException!)</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Build a word frequency counter: read a sentence, split it into words, and use a <code>HashMap</code> to count occurrences of each word.</li>
    <li>Given a list of student objects, use Streams to find the average score of students who passed (score >= 50).</li>
    <li>Remove duplicates from a list of integers using a <code>HashSet</code>, then sort the remaining elements.</li>
  </ol>
</div>
""", 45),
        (5, "Exception Handling & File I/O", """
<h2>Java Exception Handling & File I/O</h2>
<p>Robust applications handle failures gracefully. Java's checked exceptions enforce that you think about error cases at compile time — a design philosophy that prevents many production bugs.</p>

<h3>Checked vs Unchecked Exceptions</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="// Checked exceptions — compiler FORCES you to handle them (extend Exception)
// Unchecked exceptions — programming errors (extend RuntimeException)

public class FileProcessor {

    // Method that declares a checked exception
    public String readConfig(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            // try-with-resources: auto-closes the reader
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append(&quot;\n&quot;);
            }
            return sb.toString();

        } catch (FileNotFoundException e) {
            System.err.println(&quot;Config file not found: &quot; + path);
            return &quot;&quot;;   // return safe default

        } catch (IOException e) {
            System.err.println(&quot;Error reading file: &quot; + e.getMessage());
            throw e;     // re-throw — let caller handle it
        }
    }

    // Custom exception — gives callers specific information
    public void validateAge(int age) {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException(
                &quot;Invalid age: &quot; + age + &quot;. Must be between 0 and 150.&quot;
            );
        }
    }
}"></code></pre></div>

<h3>Writing Files with NIO</h3>
<div class="code-block"><pre><code>import java.nio.file.*;
import java.nio.charset.StandardCharsets;

Path path = Paths.get("students.txt");

// Write all lines at once
List<String> lines = Arrays.asList("Alice,95", "Bob,82", "Carol,78");
Files.write(path, lines, StandardCharsets.UTF_8,
    StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);

// Read all lines
List<String> read = Files.readAllLines(path, StandardCharsets.UTF_8);
read.forEach(System.out::println);

// Append to file
Files.write(path, List.of("Diana,88"), StandardCharsets.UTF_8,
    StandardOpenOption.APPEND);</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Write a program that reads a CSV file of students and their scores, then outputs a formatted grade report.</li>
    <li>Create a custom exception <code>InsufficientFundsException</code> and use it in a banking class.</li>
    <li>Build a simple logger class that writes timestamped messages to a <code>.log</code> file using <code>try-with-resources</code>.</li>
  </ol>
</div>
""", 40),
        (6, "Java in Practice — REST APIs & Design Patterns", """
<h2>Java in Practice — REST APIs & Design Patterns</h2>
<p>This lesson bridges academic Java with industry practice. Understanding these patterns will make your code immediately recognisable as professional to any senior engineer or NUC assessor.</p>

<h3>The Builder Pattern</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="// Builder pattern: construct complex objects step by step
public class HttpRequest {
    private final String url;
    private final String method;
    private final Map&lt;String, String&gt; headers;
    private final String body;

    private HttpRequest(Builder b) {
        this.url     = b.url;
        this.method  = b.method;
        this.headers = Collections.unmodifiableMap(b.headers);
        this.body    = b.body;
    }

    public static class Builder {
        private String url;
        private String method = &quot;GET&quot;;
        private Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
        private String body;

        public Builder url(String url)              { this.url = url; return this; }
        public Builder method(String m)             { this.method = m; return this; }
        public Builder header(String k, String v)   { headers.put(k, v); return this; }
        public Builder body(String body)            { this.body = body; return this; }
        public HttpRequest build()                  { return new HttpRequest(this); }
    }
}

// Usage — reads like natural language
HttpRequest request = new HttpRequest.Builder()
    .url(&quot;https://api.example.com/users&quot;)
    .method(&quot;POST&quot;)
    .header(&quot;Content-Type&quot;, &quot;application/json&quot;)
    .header(&quot;Authorization&quot;, &quot;Bearer &quot; + token)
    .body(&quot;{\&quot;name\&quot;: \&quot;Alice\&quot;}&quot;)
    .build();"></code></pre></div>

<h3>The Singleton Pattern & Dependency Injection</h3>
<div class="code-block"><pre><code>// Singleton — one instance shared across the application
public class DatabaseConnection {
    private static volatile DatabaseConnection instance;

    private DatabaseConnection() {}   // private constructor

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}

// Dependency Injection — pass dependencies in, don't create them inside
// BAD (tightly coupled):
class UserService { private DB db = new DB(); }

// GOOD (loosely coupled, testable):
class UserService {
    private final DB db;
    public UserService(DB db) { this.db = db; }   // inject it
}</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Project Ideas</div>
  <ol>
    <li><strong>Library System</strong> — Books, Members, and Loans. Implement with ArrayList, HashMap, and proper exception handling for overdue books.</li>
    <li><strong>Student Grade System</strong> — Read student records from a file, compute GPA, and output a ranked report.</li>
    <li><strong>Simple Bank</strong> — Account, SavingsAccount, CurrentAccount with the Builder pattern for account creation.</li>
    <li><strong>HTTP Client</strong> — Use Java's <code>HttpClient</code> (Java 11+) to call a public REST API and parse the JSON response.</li>
  </ol>
</div>
""", 50),
    ]
    quizzes = {
        4: [
            ("Which Java collection allows only unique elements and provides O(1) lookup?", "ArrayList", "LinkedList", "HashSet", "C", "HashSet uses a hash table internally, giving O(1) average-case contains() and add(). It automatically rejects duplicates."),
            ("What does the Stream `.filter()` method return?", "The first matching element", "A new Stream with only matching elements", "A boolean", "B", "filter() is an intermediate Stream operation. It returns a new Stream containing only the elements that match the predicate. The original Stream is unchanged."),
        ],
        5: [
            ("What is the advantage of try-with-resources over a regular try-finally block?", "It is faster", "It automatically closes resources even if an exception occurs", "It catches more exception types", "B", "try-with-resources (introduced in Java 7) calls close() on any AutoCloseable resource automatically, even if an exception is thrown — preventing resource leaks."),
            ("What is the difference between checked and unchecked exceptions in Java?", "Checked are faster", "Checked must be handled or declared; unchecked need not be", "Unchecked are more serious", "B", "Checked exceptions (subclasses of Exception) must be either caught or declared with throws. Unchecked exceptions (subclasses of RuntimeException) represent programming errors and do not require explicit handling."),
        ],
        6: [
            ("What problem does the Builder pattern solve?", "Speeds up object creation", "Makes constructors with many parameters readable and safe", "Prevents subclassing", "B", "When a class has many optional parameters, a constructor becomes unreadable and error-prone. The Builder pattern uses method chaining to build up the object step-by-step with named parameters."),
            ("In Dependency Injection, how are dependencies provided to a class?", "Created inside the class with `new`", "Passed in through the constructor or a setter", "Fetched from a global variable", "B", "DI passes dependencies from outside, making classes loosely coupled and testable. You can inject a mock object during testing without changing the class itself."),
        ],
    }
    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


