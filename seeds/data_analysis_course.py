"""iLEARN — Data Analysis course seed."""
from .helpers import insert_lessons_and_quizzes


def seed_data_analysis(conn, c):
    c.execute(
        "INSERT INTO courses (title, description, icon, level, language) VALUES (?,?,?,?,?)",
        (
            "Data Analysis",
            "Master data analysis from foundations to advanced techniques. Learn to collect, clean, analyse, and visualise data using Python, Pandas, and real-world datasets.",
            "chart-bar",
            "Beginner to Intermediate",
            "data_analysis",
        ),
    )
    cid = c.lastrowid

    # ── Module 1: Foundations ────────────────────────────────────────
    c.execute(
        "INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
        (cid, "Foundations of Data Analysis", 1),
    )
    mod1 = c.lastrowid

    # ── Module 2: Data Wrangling ─────────────────────────────────────
    c.execute(
        "INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
        (cid, "Data Wrangling with Pandas", 2),
    )
    mod2 = c.lastrowid

    # ── Module 3: Visualisation ──────────────────────────────────────
    c.execute(
        "INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
        (cid, "Data Visualisation", 3),
    )
    mod3 = c.lastrowid

    # ── Module 4: Statistical Analysis ──────────────────────────────
    c.execute(
        "INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
        (cid, "Statistical Analysis", 4),
    )
    mod4 = c.lastrowid

    lessons = [
        # Module 1
        (1, "What is Data Analysis?", mod1, """
<h2>What is Data Analysis?</h2>
<p>Data analysis is the process of collecting, cleaning, transforming, and modelling data to discover useful information, draw conclusions, and support decision-making. It is the foundation of every data-driven organisation.</p>

<h3>The Data Analysis Workflow</h3>
<div class="concept-box">
  <div class="cb-title">Five Stages</div>
  <ol>
    <li><strong>Define</strong> — What question are you trying to answer?</li>
    <li><strong>Collect</strong> — Gather data from sources (CSV, databases, APIs)</li>
    <li><strong>Clean</strong> — Handle missing values, fix errors, remove duplicates</li>
    <li><strong>Analyse</strong> — Apply statistical methods, spot patterns</li>
    <li><strong>Communicate</strong> — Visualise and present findings clearly</li>
  </ol>
</div>

<h3>Types of Analysis</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0;">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Type</th><th style="padding:8px;text-align:left">Question it answers</th><th style="padding:8px;text-align:left">Example</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Descriptive</td><td style="padding:8px">What happened?</td><td style="padding:8px">Monthly sales totals</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Diagnostic</td><td style="padding:8px">Why did it happen?</td><td style="padding:8px">Why did sales drop in Q3?</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Predictive</td><td style="padding:8px">What will happen?</td><td style="padding:8px">Next month's revenue forecast</td></tr>
  <tr><td style="padding:8px">Prescriptive</td><td style="padding:8px">What should we do?</td><td style="padding:8px">Which customers to target?</td></tr>
</table>

<h3>Tools of the Trade</h3>
<pre><code># The core Python data stack
import pandas as pd        # data manipulation
import numpy as np         # numerical computing
import matplotlib.pyplot as plt  # plotting
import seaborn as sns      # statistical visualisation</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Write down a real-world question that could be answered with data (e.g. "Which day of the week do students perform best?")</li>
    <li>Identify what data you would need to answer it</li>
    <li>Identify which type of analysis (descriptive, diagnostic, predictive, prescriptive) it falls under</li>
  </ol>
</div>
""", 20),
        (2, "Python for Data Analysis — NumPy & Pandas", mod1, """
<h2>Python for Data Analysis</h2>
<p>NumPy and Pandas are the two most important libraries in the Python data ecosystem. Almost every data analysis task uses them.</p>

<h3>NumPy — Numerical Computing</h3>
<pre><code>import numpy as np

# Create arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4], [5, 6]])

# Vectorised operations (much faster than Python loops)
print(arr * 2)          # [2 4 6 8 10]
print(arr.mean())       # 3.0
print(arr.std())        # 1.41
print(np.sqrt(arr))     # [1. 1.41 1.73 2. 2.23]

# Useful array creation
zeros = np.zeros((3, 3))
ones  = np.ones((2, 4))
rng   = np.arange(0, 10, 2)   # [0 2 4 6 8]</code></pre>

<h3>Pandas — Data Manipulation</h3>
<pre><code>import pandas as pd

# Create a DataFrame (the core Pandas structure)
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "David"],
    "score":  [88, 72, 95, 61],
    "grade":  ["B", "C", "A", "D"],
    "passed": [True, True, True, False],
})

# Always inspect new data first
print(df.shape)       # (4, 4)
print(df.dtypes)      # column types
print(df.describe())  # statistics for numeric columns
print(df.head(3))     # first 3 rows</code></pre>

<h3>Selecting & Filtering</h3>
<pre><code># Select columns
print(df["name"])              # single column (Series)
print(df[["name", "score"]])   # multiple columns (DataFrame)

# Filter rows
passed = df[df["passed"] == True]
high   = df[df["score"] >= 80]
top    = df[(df["score"] >= 80) & (df["passed"] == True)]</code></pre>

<div class="concept-box warning">
  <div class="cb-title">Important</div>
  <p>Always run <code>df.info()</code> and <code>df.describe()</code> as your very first step on any new dataset. They tell you about nulls, data types, and basic statistics.</p>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a DataFrame of 5 students with columns: name, age, mark, subject</li>
    <li>Filter to show only students with marks above 70</li>
    <li>Use <code>df.describe()</code> to see the statistics</li>
    <li>Find the student with the highest mark using <code>df.nlargest(1, "mark")</code></li>
  </ol>
</div>
""", 30),
        # Module 2
        (3, "Data Cleaning — Handling Real-World Data", mod2, """
<h2>Data Cleaning</h2>
<p>Real-world data is messy. Studies show data scientists spend 60–80% of their time cleaning data. Mastering this step is what separates professional analysts from beginners.</p>

<h3>Loading Data</h3>
<pre><code>import pandas as pd

# From a CSV file
df = pd.read_csv("students.csv")

# From a URL
df = pd.read_csv("https://example.com/data.csv")

# From Excel
df = pd.read_excel("report.xlsx", sheet_name="Sheet1")</code></pre>

<h3>Identifying Problems</h3>
<pre><code># Check for missing values
print(df.isnull().sum())        # count nulls per column
print(df.isnull().sum() / len(df) * 100)  # as percentage

# Check for duplicates
print(df.duplicated().sum())

# Check data types
print(df.dtypes)

# Check unique values in a column
print(df["grade"].value_counts())</code></pre>

<h3>Fixing Missing Values</h3>
<pre><code># Drop rows where ANY column is null
df_clean = df.dropna()

# Drop rows where a SPECIFIC column is null
df_clean = df.dropna(subset=["score"])

# Fill nulls with a fixed value
df["score"] = df["score"].fillna(0)

# Fill nulls with the column mean (better approach)
df["score"] = df["score"].fillna(df["score"].mean())

# Fill nulls with forward fill (for time series)
df["price"] = df["price"].ffill()</code></pre>

<h3>Fixing Data Types</h3>
<pre><code># Convert a column to numeric (coerce errors to NaN)
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# Convert a string column to datetime
df["date"] = pd.to_datetime(df["date"])

# Convert a column to categorical
df["grade"] = df["grade"].astype("category")</code></pre>

<h3>Removing Duplicates & Outliers</h3>
<pre><code># Remove duplicate rows
df = df.drop_duplicates()

# Remove duplicates based on specific columns
df = df.drop_duplicates(subset=["student_id"])

# Detect outliers using IQR
Q1  = df["score"].quantile(0.25)
Q3  = df["score"].quantile(0.75)
IQR = Q3 - Q1
df_clean = df[(df["score"] >= Q1 - 1.5*IQR) & (df["score"] <= Q3 + 1.5*IQR)]</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a DataFrame with some deliberately missing values (use <code>None</code> or <code>np.nan</code>)</li>
    <li>Use <code>df.isnull().sum()</code> to find them</li>
    <li>Fill numeric nulls with the column mean</li>
    <li>Remove any duplicate rows</li>
    <li>Use <code>df.describe()</code> to verify the cleaned data looks right</li>
  </ol>
</div>
""", 35),
        (4, "Exploratory Data Analysis (EDA)", mod2, """
<h2>Exploratory Data Analysis</h2>
<p>EDA is the process of investigating a dataset to understand its structure, patterns, and relationships before formal analysis. It is arguably the most important step in any data project.</p>

<h3>Aggregation & Grouping</h3>
<pre><code>import pandas as pd

df = pd.read_csv("sales.csv")

# Group by one column
by_region = df.groupby("region")["revenue"].sum()

# Group by multiple columns
by_region_year = df.groupby(["region", "year"])["revenue"].agg(["sum", "mean", "count"])

# Pivot table (like Excel pivot)
pivot = df.pivot_table(
    values="revenue",
    index="region",
    columns="quarter",
    aggfunc="sum",
    fill_value=0
)</code></pre>

<h3>Correlation Analysis</h3>
<pre><code># Correlation matrix — values from -1 to +1
corr = df[["score", "study_hours", "attendance"]].corr()
print(corr)

# Strong positive correlation (close to 1): variables move together
# Strong negative correlation (close to -1): variables move opposite
# Near zero: no linear relationship</code></pre>

<h3>Distribution Analysis</h3>
<pre><code># Basic statistics
print(df["score"].mean())     # average
print(df["score"].median())   # middle value
print(df["score"].mode())     # most common value
print(df["score"].std())      # spread
print(df["score"].skew())     # asymmetry

# Count unique values
print(df["grade"].value_counts())
print(df["grade"].value_counts(normalize=True))  # as proportions</code></pre>

<div class="concept-box">
  <div class="cb-title">EDA Checklist</div>
  <ol>
    <li>How many rows and columns? (<code>df.shape</code>)</li>
    <li>What are the data types? (<code>df.dtypes</code>)</li>
    <li>Are there missing values? (<code>df.isnull().sum()</code>)</li>
    <li>What does the distribution look like? (<code>df.describe()</code>)</li>
    <li>Are there outliers?</li>
    <li>What correlations exist?</li>
    <li>Are there surprising values?</li>
  </ol>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Load any CSV dataset (try <code>df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")</code>)</li>
    <li>Run the full EDA checklist on it</li>
    <li>Use <code>groupby</code> to find the average survival rate by passenger class</li>
    <li>Find the top 3 most correlated numeric columns</li>
  </ol>
</div>
""", 30),
        # Module 3
        (5, "Data Visualisation with Matplotlib & Seaborn", mod3, """
<h2>Data Visualisation</h2>
<p>A chart communicates a pattern in seconds that a table of numbers would take minutes to reveal. Good visualisation is a core analyst skill.</p>

<h3>Matplotlib — The Foundation</h3>
<pre><code>import matplotlib.pyplot as plt
import numpy as np

# Line chart
x = [1, 2, 3, 4, 5]
y = [10, 24, 18, 35, 42]
plt.figure(figsize=(10, 5))
plt.plot(x, y, color="#4facfe", linewidth=2, marker="o")
plt.title("Monthly Revenue", fontsize=14, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Bar chart
categories = ["Python", "JavaScript", "Java", "CSS"]
counts     = [45, 38, 22, 31]
plt.bar(categories, counts, color=["#4facfe","#a78bfa","#34d399","#fbbf24"])
plt.title("Course Enrolment")
plt.show()</code></pre>

<h3>Seaborn — Statistical Visualisation</h3>
<pre><code>import seaborn as sns
import pandas as pd

df = pd.read_csv("students.csv")

# Distribution plot
sns.histplot(df["score"], bins=20, kde=True, color="#4facfe")

# Box plot — shows median, quartiles, outliers
sns.boxplot(x="course", y="score", data=df, palette="husl")

# Scatter plot with regression line
sns.regplot(x="study_hours", y="score", data=df)

# Heatmap — perfect for correlation matrices
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")</code></pre>

<h3>Subplots — Multiple Charts</h3>
<pre><code>fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df["score"], bins=15, color="#4facfe")
axes[0].set_title("Score Distribution")

axes[1].scatter(df["study_hours"], df["score"], alpha=0.6, color="#a78bfa")
axes[1].set_title("Study Hours vs Score")

plt.tight_layout()
plt.show()</code></pre>

<div class="concept-box">
  <div class="cb-title">Choosing the Right Chart</div>
  <table style="width:100%;border-collapse:collapse">
    <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Goal</th><th style="padding:8px;text-align:left">Chart type</th></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Show distribution</td><td style="padding:8px">Histogram, Box plot</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Compare categories</td><td style="padding:8px">Bar chart</td></tr>
    <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Show trend over time</td><td style="padding:8px">Line chart</td></tr>
    <tr><td style="padding:8px">Show relationship</td><td style="padding:8px">Scatter plot</td></tr>
  </table>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Create a bar chart of your weekly study hours across 5 days</li>
    <li>Create a histogram showing a distribution of 100 random numbers</li>
    <li>Build a 2x2 subplot grid showing four different chart types</li>
    <li>Create a heatmap of a correlation matrix</li>
  </ol>
</div>
""", 35),
        # Module 4
        (6, "Statistical Analysis & Reporting", mod4, """
<h2>Statistical Analysis</h2>
<p>Statistics gives us the tools to move from raw observations to reliable conclusions. This lesson covers the essential techniques every data analyst must know.</p>

<h3>Descriptive Statistics</h3>
<pre><code>import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("students.csv")

# Central tendency
mean   = df["score"].mean()
median = df["score"].median()
mode   = df["score"].mode()[0]

# Spread
std_dev  = df["score"].std()
variance = df["score"].var()
iqr      = df["score"].quantile(0.75) - df["score"].quantile(0.25)

# Full summary
print(df["score"].describe())
# count, mean, std, min, 25%, 50%, 75%, max</code></pre>

<h3>Hypothesis Testing</h3>
<pre><code>from scipy import stats

# T-test: Are two groups significantly different?
group_a = df[df["course"] == "Python"]["score"]
group_b = df[df["course"] == "JavaScript"]["score"]

t_stat, p_value = stats.ttest_ind(group_a, group_b)

if p_value < 0.05:
    print(f"Significant difference (p={p_value:.3f})")
else:
    print(f"No significant difference (p={p_value:.3f})")</code></pre>

<h3>Correlation & Linear Regression</h3>
<pre><code># Pearson correlation
r, p = stats.pearsonr(df["study_hours"], df["score"])
print(f"r = {r:.2f}, p = {p:.4f}")

# Linear regression
from scipy.stats import linregress
slope, intercept, r2, p, se = linregress(df["study_hours"], df["score"])
print(f"score = {slope:.2f} * hours + {intercept:.2f}")
print(f"R² = {r2**2:.2f}")  # R² tells you how much variance is explained</code></pre>

<h3>Creating a Data Report</h3>
<pre><code># A professional summary function
def summarise(df, column):
    s = df[column]
    return {
        "n":      len(s),
        "mean":   round(s.mean(), 2),
        "median": round(s.median(), 2),
        "std":    round(s.std(), 2),
        "min":    s.min(),
        "max":    s.max(),
        "nulls":  s.isnull().sum(),
    }

print(summarise(df, "score"))</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Load a dataset and compute descriptive statistics for at least 2 numeric columns</li>
    <li>Run a t-test comparing two groups in your data</li>
    <li>Calculate the correlation between two variables</li>
    <li>Write a Python function that generates a complete summary report for a DataFrame</li>
  </ol>
</div>
""", 35),
    ]

    quizzes = {
        1: [
            ("What is the correct order of the data analysis workflow?",
             "Analyse, collect, define, clean, communicate",
             "Define, collect, clean, analyse, communicate",
             "Collect, define, analyse, clean, communicate",
             "B",
             "A good analysis starts with a clear question (Define), then gathers data, cleans it, analyses it, and finally communicates findings."),
            ("Which type of analysis answers 'What will happen?'",
             "Descriptive", "Diagnostic", "Predictive", "C",
             "Predictive analysis uses historical data to forecast future outcomes."),
        ],
        2: [
            ("Which Pandas method shows column types and null counts?",
             "df.describe()", "df.info()", "df.head()", "B",
             "df.info() shows dtypes, non-null counts, and memory usage — essential for understanding a new dataset."),
            ("What does df.describe() show?",
             "Only the first 5 rows",
             "Statistical summary including mean, std, min, max for numeric columns",
             "The data types of each column", "B",
             "df.describe() computes count, mean, standard deviation, min, quartiles, and max for numeric columns."),
        ],
        3: [
            ("Which method fills missing values with the column mean?",
             "df.dropna()", "df['col'].fillna(df['col'].mean())", "df.replace(None, 0)", "B",
             "fillna() with the column mean is better than dropping rows or using zero, as it preserves the dataset size without distorting the distribution."),
            ("What does drop_duplicates() do?",
             "Removes columns with duplicate names",
             "Removes rows that are identical across all columns",
             "Sorts the DataFrame", "B",
             "drop_duplicates() removes rows where every value is identical, or you can specify subset columns."),
        ],
        4: [
            ("What does groupby().agg() do?",
             "Merges two DataFrames",
             "Groups rows by a column then applies aggregate functions to each group",
             "Filters rows by a condition", "B",
             "groupby() splits the data into groups, and agg() applies functions like sum, mean, count to each group."),
            ("A correlation of -0.85 between two variables means:",
             "They have no relationship",
             "When one increases, the other tends to strongly decrease",
             "They are identical", "B",
             "Negative correlation means the variables move in opposite directions. -0.85 is a strong negative correlation."),
        ],
        5: [
            ("Which chart type is best for showing a distribution of values?",
             "Line chart", "Histogram", "Pie chart", "B",
             "Histograms show the frequency distribution of a continuous variable, making it easy to see the shape, spread, and skew of data."),
            ("What does seaborn's heatmap typically visualise?",
             "Time series data",
             "A correlation matrix, showing the strength of relationships between variables",
             "Geographic data", "B",
             "Heatmaps with annotation are the standard way to display correlation matrices, using colour intensity to show the strength of each correlation."),
        ],
        6: [
            ("In a t-test, what does a p-value below 0.05 tell you?",
             "The result is definitely correct",
             "The difference between groups is statistically significant",
             "The data has no outliers", "B",
             "p < 0.05 means there is less than a 5% chance the difference occurred by random chance — the standard threshold for statistical significance."),
            ("What does R² (R-squared) measure in regression?",
             "The slope of the regression line",
             "The proportion of variance in the outcome explained by the predictor",
             "The number of data points", "B",
             "R² ranges from 0 to 1. An R² of 0.72 means 72% of the variation in the outcome is explained by the model."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid
