"""iLEARN — Data Science & Analytics course seed data."""
from .helpers import insert_lessons_and_quizzes

def seed_data_science(conn, c):
    c.execute("INSERT INTO courses (title,description,icon,level,language) VALUES (?,?,?,?,?)",
              ("Data Science & Analytics","From raw data to actionable insight. Learn the full workflow: NumPy, Pandas, data cleaning, exploratory analysis, visualisation, and a practical introduction to machine learning.","📊","Intermediate","python"))
    cid = c.lastrowid

    lessons = [
        (1,"NumPy & Pandas Fundamentals","""
<h2>NumPy — The Foundation of Scientific Python</h2>
<p>NumPy provides the <strong>ndarray</strong> — an N-dimensional array that is the backbone of the entire Python scientific computing ecosystem. Pandas, Matplotlib, Scikit-learn, TensorFlow, and PyTorch all use NumPy arrays under the hood. The key advantage: NumPy operations are <strong>vectorised</strong> — executed in compiled C code rather than interpreted Python, giving 10–100x speedups over pure Python loops.</p>

<div class="code-block"><pre><code">import numpy as np

# Creating arrays
arr1 = np.array([1, 2, 3, 4, 5])           # 1D from list
arr2 = np.array([[1,2,3],[4,5,6],[7,8,9]]) # 2D (matrix)

# Factory functions
zeros    = np.zeros((3, 4))          # 3x4 matrix of 0.0
ones     = np.ones((2, 3), dtype=int)# 2x3 matrix of 1
identity = np.eye(4)                  # 4x4 identity matrix
rng      = np.arange(0, 10, 2)        # [0 2 4 6 8]
lin      = np.linspace(0, 1, 5)       # [0. 0.25 0.5 0.75 1.]
rand     = np.random.rand(3, 3)       # 3x3 uniform random [0,1)
normal   = np.random.randn(100)       # 100 samples from N(0,1)

# Array inspection
print(arr2.shape)    # (3, 3) — rows, columns
print(arr2.ndim)     # 2 — number of dimensions
print(arr2.dtype)    # int64
print(arr2.size)     # 9 — total elements
print(arr2.nbytes)   # 72 — memory in bytes

# Indexing and slicing
print(arr2[0, 1])       # Row 0, Col 1: 2
print(arr2[1, :])        # All of row 1: [4 5 6]
print(arr2[:, 2])        # All of col 2: [3 6 9]
print(arr2[0:2, 1:3])   # Sub-matrix rows 0-1, cols 1-2</code></pre></div>

<div class="code-block"><pre><code"># Vectorised operations (no loops needed!)
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)          # [11 22 33 44]
print(a * b)          # [10 40 90 160]
print(a ** 2)         # [1 4 9 16]
print(np.sqrt(a))     # [1. 1.41 1.73 2.]
print(np.exp(a))      # [2.71 7.38 20.08 54.59]

# Boolean indexing — powerful filtering
scores = np.array([72, 88, 45, 91, 63, 77])
passing = scores[scores >= 70]   # [72 88 91 77]
high    = scores[(scores >= 80) & (scores < 90)]  # [88]

# Broadcasting — operations between different-shaped arrays
matrix = np.array([[1,2,3],[4,5,6]])  # (2,3)
row    = np.array([10, 20, 30])       # (3,)
result = matrix + row   # Each row gets row added: [[11,22,33],[14,25,36]]

# Aggregation
print(np.mean(scores))      # 72.67
print(np.median(scores))    # 74.5
print(np.std(scores))       # 15.76
print(np.percentile(scores, 75))  # 84.25</code></pre></div>

<h2>Pandas — DataFrames for Data Analysis</h2>
<div class="code-block"><pre><code>import pandas as pd

# Creating a DataFrame
df = pd.DataFrame({
    "name":       ["Alice", "Bob", "Carol", "Dan", "Eve"],
    "department": ["CS", "Math", "CS", "Physics", "Math"],
    "age":        [25, 30, 22, 28, 35],
    "score":      [88, 92, 76, 85, 91],
    "passed":     [True, True, False, True, True]
})

# Exploration — always start here
print(df.shape)          # (5, 5)
print(df.dtypes)         # Data types of each column
print(df.describe())     # Stats for numeric columns
print(df.info())         # Non-null counts, memory usage
print(df.head(3))        # First 3 rows
print(df.value_counts("department"))  # Frequency of each dept

# Selection
col  = df["score"]                     # Series
cols = df[["name", "score", "passed"]] # DataFrame
row  = df.iloc[2]                      # Row by integer position
val  = df.loc[2, "name"]               # Value by label: "Carol"

# Filtering
passing = df[df["passed"] == True]
cs_high = df[(df["department"] == "CS") & (df["score"] >= 85)]

# New columns
df["grade"]    = df["score"].apply(lambda s: "A" if s>=90 else "B" if s>=75 else "C")
df["score_sq"] = df["score"] ** 2    # Vectorised</code></pre></div>
        """,30),

        (2,"Data Cleaning & Exploratory Analysis","""
<h2>Data Cleaning</h2>
<p>Real-world datasets are always messy. Missing values, duplicates, wrong data types, inconsistent formatting, and outliers are the rule, not the exception. Professional data scientists estimate spending <strong>60–80% of project time on cleaning</strong>. Getting this step right determines the quality of everything downstream.</p>

<div class="code-block"><pre><code">import pandas as pd
import numpy as np

df = pd.read_csv("students.csv")

# ── Step 1: Understand the Mess ──
print("Shape:", df.shape)
print("\\nNull counts:\\n", df.isnull().sum())
print("\\nNull percentages:\\n", (df.isnull().sum() / len(df) * 100).round(2))
print("\\nDuplicates:", df.duplicated().sum())
print("\\nData types:\\n", df.dtypes)
print("\\nUnique values per column:")
for col in df.columns:
    print(f"  {col}: {df[col].nunique()} unique values")

# ── Step 2: Handle Missing Values ──
# Strategy A: Drop rows/columns
df_drop    = df.dropna()                          # Drop ANY null
df_partial = df.dropna(subset=["student_id", "name"])  # Only key columns
df.drop(columns=["irrelevant_col"], inplace=True)

# Strategy B: Fill nulls
df["score"].fillna(df["score"].mean(),     inplace=True)  # Mean imputation
df["score"].fillna(df["score"].median(),   inplace=True)  # Median (robust to outliers)
df["city"].fillna("Unknown",               inplace=True)  # Categorical fill
df["score"].fillna(method="ffill",         inplace=True)  # Forward fill (time series)
df["score"].fillna(method="bfill",         inplace=True)  # Backward fill

# ── Step 3: Fix Data Types ──
df["enrollment_date"] = pd.to_datetime(df["enrollment_date"], errors="coerce")
df["age"]             = pd.to_numeric(df["age"], errors="coerce").astype("Int64")
df["dept"]            = df["dept"].astype("category")    # Memory efficient

# ── Step 4: Clean String Columns ──
df["name"] = df["name"].str.strip().str.title()
df["email"] = df["email"].str.lower().str.strip()
df["phone"] = df["phone"].str.replace(r"[^0-9]", "", regex=True)

# ── Step 5: Remove Duplicates ──
df.drop_duplicates(inplace=True)
df.drop_duplicates(subset=["student_id"], keep="first", inplace=True)</code></pre></div>

<h3>Outlier Detection</h3>
<div class="code-block"><pre><code"># IQR Method (robust to extreme values)
Q1  = df["score"].quantile(0.25)
Q3  = df["score"].quantile(0.75)
IQR = Q3 - Q1
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

outliers   = df[(df["score"] < lower_fence) | (df["score"] > upper_fence)]
df_clean   = df[(df["score"] >= lower_fence) & (df["score"] <= upper_fence)]
print(f"Removed {len(outliers)} outliers")

# Z-Score Method (assumes normal distribution)
from scipy import stats
z_scores      = np.abs(stats.zscore(df["score"]))
df_no_outlier = df[z_scores < 3]   # Keep within 3 standard deviations</code></pre></div>

<h3>GroupBy and Aggregation</h3>
<div class="code-block"><pre><code">
# GroupBy — split by group, apply function, combine results
summary = df.groupby("department")["score"].agg(
    count  ="count",
    mean   ="mean",
    median ="median",
    std    ="std",
    min    ="min",
    max    ="max"
).round(2)

# Multiple columns
trend = df.groupby(["department", "year"])["score"].mean().reset_index()

# Pivot table — reshape data
pivot = pd.pivot_table(
    df,
    values    ="score",
    index     ="department",
    columns   ="grade",
    aggfunc   ="count",
    fill_value=0,
    margins   =True    # Add row/column totals
)</code></pre></div>
        """,30),

        (3,"Visualisation & Machine Learning Intro","""
<h2>Data Visualisation</h2>
<p>Visualisation serves two purposes: <em>exploration</em> (understanding your data) and <em>communication</em> (presenting findings to stakeholders). The right chart type depends on what relationship you want to show.</p>

<table class="lesson-table">
  <tr><th>Chart Type</th><th>Use For</th><th>Matplotlib/Seaborn</th></tr>
  <tr><td>Histogram</td><td>Distribution of one numeric variable</td><td>ax.hist() / sns.histplot()</td></tr>
  <tr><td>Bar Chart</td><td>Comparing categories</td><td>ax.bar() / sns.barplot()</td></tr>
  <tr><td>Box Plot</td><td>Distribution + outliers by group</td><td>ax.boxplot() / sns.boxplot()</td></tr>
  <tr><td>Scatter Plot</td><td>Relationship between two numerics</td><td>ax.scatter() / sns.scatterplot()</td></tr>
  <tr><td>Line Chart</td><td>Trends over time</td><td>ax.plot() / sns.lineplot()</td></tr>
  <tr><td>Heatmap</td><td>Correlation matrix</td><td>sns.heatmap()</td></tr>
</table>

<div class="code-block"><pre><code>import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid", palette="husl", font_scale=1.1)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Student Performance Dashboard", fontsize=16, fontweight="bold")

# 1. Score distribution
sns.histplot(df["score"], bins=20, kde=True, ax=axes[0,0], color="#00d4b4")
axes[0,0].set_title("Score Distribution with KDE")
axes[0,0].axvline(df["score"].mean(), color="red", linestyle="--", label="Mean")
axes[0,0].legend()

# 2. Average by department
dept_avg = df.groupby("dept")["score"].mean().sort_values()
sns.barplot(x=dept_avg.values, y=dept_avg.index, ax=axes[0,1], palette="viridis")
axes[0,1].set_title("Average Score by Department")

# 3. Score vs Age scatter with regression line
sns.regplot(data=df, x="age", y="score", ax=axes[1,0], color="#f5a623")
axes[1,0].set_title("Score vs Age")

# 4. Correlation heatmap
corr = df[["age", "score", "hours_studied", "previous_score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=axes[1,1])
axes[1,1].set_title("Correlation Matrix")

plt.tight_layout()
plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
plt.show()</code></pre></div>

<h2>Introduction to Machine Learning</h2>
<div class="code-block"><pre><code">from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing   import StandardScaler, LabelEncoder
from sklearn.linear_model    import LogisticRegression
from sklearn.ensemble        import RandomForestClassifier
from sklearn.metrics         import (accuracy_score, classification_report,
                                      confusion_matrix)

# 1. Feature Engineering
df["study_efficiency"] = df["score"] / (df["hours_studied"] + 1)
df["age_group"]        = pd.cut(df["age"], bins=[0,22,26,100],
                                labels=["young","mid","mature"])

# 2. Encode categorical features
le = LabelEncoder()
df["dept_encoded"] = le.fit_transform(df["department"])

# 3. Prepare features and target
X = df[["age", "hours_studied", "previous_score", "dept_encoded",
        "study_efficiency"]]
y = df["passed"]

# 4. Train/test split (stratify preserves class ratio)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Scale features (ONLY fit on training data — prevents data leakage)
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)   # Apply SAME transform

# 6. Train and evaluate
model  = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred    = model.predict(X_test)
accuracy  = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2%}")
print("\\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
importance = pd.Series(model.feature_importances_, index=X.columns)
print("\\nTop Features:\\n", importance.sort_values(ascending=False))</code></pre></div>
        """,35),
    ]

    quizzes = {
        1:[
            ("What makes NumPy vectorised operations faster than Python for-loops?","They use multiple CPU cores by default","Operations run as compiled C code, bypassing Python's interpreter overhead","They use GPU acceleration","B","NumPy operations are implemented in compiled C/Fortran code. By operating on entire arrays without Python's interpreter, they avoid the overhead of Python bytecode execution per element — achieving 10-100x speedups."),
            ("What does df.describe() return?","The first 5 rows of the DataFrame","Statistical summary (count, mean, std, min, quartiles, max) for numeric columns","Column types and null counts","B","df.describe() generates descriptive statistics for numeric columns. For a quick overview of the data's distribution, range, and central tendency."),
        ],
        2:[
            ("Why should you use median imputation instead of mean for a skewed column?","Median is faster to compute","The median is robust to outliers and better represents the 'typical' value in a skewed distribution","Mean imputation is not supported in Pandas","B","In skewed distributions, a few extreme values pull the mean away from the typical value. The median (50th percentile) is not affected by extreme values, making it a more representative fill value."),
            ("What does df.groupby('dept')['score'].agg(['mean','std']) do?","Filters rows by department","Computes mean and standard deviation of score for each department group","Sorts scores within each department","B","groupby().agg() is the split-apply-combine pattern: split data into groups, apply aggregation functions to each group, then combine results into a summary DataFrame."),
        ],
        3:[
            ("Why do we call scaler.fit_transform(X_train) but only scaler.transform(X_test)?","To run faster on smaller data","To prevent data leakage — test set statistics must not influence the scaler fitted on training data","The test set doesn't need scaling","B","Data leakage corrupts model evaluation. The scaler must ONLY learn statistics (mean, std) from training data. Applying those SAME parameters to the test set simulates real deployment, where you wouldn't have access to future data when computing scaling parameters."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid



# ═══════════════════════════════════════════════
# EXTENDED LESSONS — added to each course
# ═══════════════════════════════════════════════


def extend_data_science(conn, c, cid):
    lessons = [
        (4, "Data Visualisation with Matplotlib & Seaborn", """
<h2>Data Visualisation</h2>
<p>A data scientist who cannot visualise data effectively cannot communicate insights. Matplotlib gives you control; Seaborn gives you beauty with less code.</p>

<h3>Matplotlib Fundamentals</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle(&quot;Common Plot Types&quot;, fontsize=16, fontweight=&quot;bold&quot;)

# Line chart
x = np.linspace(0, 10, 100)
axes[0,0].plot(x, np.sin(x), color=&quot;#4facfe&quot;, linewidth=2, label=&quot;sin(x)&quot;)
axes[0,0].plot(x, np.cos(x), color=&quot;#f5a623&quot;, linewidth=2, label=&quot;cos(x)&quot;)
axes[0,0].legend(); axes[0,0].set_title(&quot;Line Chart&quot;)

# Bar chart
categories = [&quot;Python&quot;, &quot;JavaScript&quot;, &quot;Java&quot;, &quot;CSS&quot;]
values     = [85, 72, 68, 91]
bars = axes[0,1].bar(categories, values, color=[&quot;#4facfe&quot;,&quot;#f5a623&quot;,&quot;#a78bfa&quot;,&quot;#34d399&quot;])
axes[0,1].bar_label(bars); axes[0,1].set_title(&quot;Bar Chart&quot;)

# Histogram
data = np.random.normal(70, 15, 1000)   # exam scores
axes[1,0].hist(data, bins=30, color=&quot;#4facfe&quot;, edgecolor=&quot;white&quot;, alpha=0.8)
axes[1,0].set_title(&quot;Histogram&quot;)

# Scatter plot
x = np.random.randn(100); y = x * 2 + np.random.randn(100)
axes[1,1].scatter(x, y, alpha=0.6, color=&quot;#a78bfa&quot;)
axes[1,1].set_title(&quot;Scatter Plot&quot;)

plt.tight_layout()
plt.savefig(&quot;plots.png&quot;, dpi=150, bbox_inches=&quot;tight&quot;)
plt.show()"></code></pre></div>

<h3>Seaborn for Statistical Plots</h3>
<div class="code-block"><pre><code>import seaborn as sns
import pandas as pd

df = sns.load_dataset("titanic")

# Countplot — frequency of a categorical variable
sns.countplot(data=df, x="class", hue="survived", palette="Set2")

# Heatmap — correlation matrix
corr = df.select_dtypes("number").corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues")

# Box plot — distribution and outliers
sns.boxplot(data=df, x="class", y="age", hue="sex")</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Load the Iris dataset (<code>sns.load_dataset("iris")</code>) and create a scatter plot matrix (<code>sns.pairplot</code>) coloured by species.</li>
    <li>Generate 1000 random exam scores (normal distribution) and visualise their distribution with both a histogram and a KDE curve.</li>
    <li>Create a bar chart showing the top 10 most popular programming languages from your own survey data.</li>
  </ol>
</div>
""", 45),
        (5, "Machine Learning Fundamentals with scikit-learn", """
<h2>Machine Learning with scikit-learn</h2>
<p>Machine learning lets computers learn from data rather than being explicitly programmed. scikit-learn provides consistent, well-documented implementations of the most important algorithms.</p>

<div class="concept-box">
  <div class="cb-title">ML Workflow — Always in This Order</div>
  <p>1. Collect & explore data &nbsp;→&nbsp; 2. Clean & preprocess &nbsp;→&nbsp; 3. Split train/test &nbsp;→&nbsp; 4. Choose & train model &nbsp;→&nbsp; 5. Evaluate &nbsp;→&nbsp; 6. Tune &nbsp;→&nbsp; 7. Deploy</p>
</div>

<h3>Classification — Predicting Categories</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="from sklearn.datasets       import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing  import StandardScaler
from sklearn.ensemble       import RandomForestClassifier
from sklearn.metrics        import classification_report, accuracy_score

# 1. Load data
iris = load_iris()
X, y = iris.data, iris.target

# 2. Split BEFORE scaling (critical — prevents data leakage)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Scale: fit on TRAIN only, transform both
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)     # do NOT fit_transform here!

# 4. Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
print(f&quot;Accuracy: {accuracy_score(y_test, y_pred):.2%}&quot;)
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# Feature importance — which features matter most?
import pandas as pd
importance = pd.Series(model.feature_importances_, index=iris.feature_names)
print(importance.sort_values(ascending=False))"></code></pre></div>

<h3>Regression — Predicting Numbers</h3>
<div class="code-block"><pre><code>from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Predict house price from square footage
X = np.array([[500],[750],[1000],[1250],[1500],[1750],[2000]])
y = np.array([150000,200000,280000,330000,400000,460000,520000])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"R² Score: {r2_score(y_test, y_pred):.3f}")   # 1.0 = perfect
print(f"RMSE: ${np.sqrt(mean_squared_error(y_test, y_pred)):,.0f}")
print(f"Predicted price for 1,100 sqft: ${model.predict([[1100]])[0]:,.0f}")</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Practical Exercises</div>
  <ol>
    <li>Train a classifier on the breast cancer dataset (<code>load_breast_cancer()</code>). Compare the accuracy of Logistic Regression vs Random Forest.</li>
    <li>Use the Titanic dataset to predict survival. Engineer at least one new feature (e.g., family size = SibSp + Parch + 1).</li>
    <li>Visualise a confusion matrix using <code>ConfusionMatrixDisplay</code> from sklearn.</li>
  </ol>
</div>
""", 55),
        (6, "Data Science Project — End to End", """
<h2>End-to-End Data Science Project</h2>
<p>This lesson walks you through a complete, real-world data science project from raw data to insights — the kind of workflow you would present to a supervisor or employer.</p>

<h3>Step 1: Define the Problem</h3>
<div class="concept-box success">
  <div class="cb-title">Project Brief</div>
  <p>Analyse student performance data to identify which factors most strongly predict final exam scores, and build a model to flag at-risk students early.</p>
</div>

<h3>Step 2: Exploratory Data Analysis (EDA)</h3>
<div class="typewriter-block"><pre><code class="typewriter-code" data-code="import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(&quot;student_performance.csv&quot;)

# ── First pass: understand the data ──
print(df.shape)          # (395, 33)
print(df.dtypes)
print(df.isnull().sum()) # Any missing values?
print(df.describe())     # Statistical summary

# ── Distribution of target variable ──
plt.figure(figsize=(8, 4))
sns.histplot(df[&quot;G3&quot;], bins=20, kde=True)
plt.title(&quot;Distribution of Final Grades (G3)&quot;)
plt.xlabel(&quot;Grade (0-20)&quot;)
plt.show()

# ── Correlation with target ──
numeric_cols = df.select_dtypes(include=&quot;number&quot;)
corr = numeric_cols.corr()[&quot;G3&quot;].sort_values(ascending=False)
print(corr.head(10))   # Top predictors"></code></pre></div>

<h3>Step 3: Feature Engineering & Modelling</h3>
<div class="code-block"><pre><code>from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

# Separate feature types
num_features = ["age","absences","G1","G2","studytime","failures"]
cat_features = ["school","sex","address","famsize","Pstatus"]

# Build a preprocessing pipeline
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
])

# Full pipeline: preprocess + model
pipeline = Pipeline([
    ("prep",   preprocessor),
    ("model",  GradientBoostingRegressor(n_estimators=200, random_state=42)),
])

X = df[num_features + cat_features]
y = df["G3"]

# Cross-validation gives a reliable estimate of real-world performance
scores = cross_val_score(pipeline, X, y, cv=5, scoring="r2")
print(f"R² (5-fold CV): {scores.mean():.3f} ± {scores.std():.3f}")</code></pre></div>

<div class="practice-box">
  <div class="pb-title">🛠 Final Project Checklist</div>
  <ol>
    <li>Download a real dataset from Kaggle or UCI ML Repository.</li>
    <li>Write a Jupyter notebook with sections: Problem Definition, EDA, Preprocessing, Modelling, Evaluation, Conclusions.</li>
    <li>Use at least two different model types and compare their performance with cross-validation.</li>
    <li>Create a minimum of 5 meaningful visualisations that tell a story about the data.</li>
    <li>Write a 200-word executive summary as if presenting findings to a non-technical manager.</li>
  </ol>
</div>
""", 60),
    ]
    quizzes = {
        4: [
            ("Which Seaborn plot is best for showing the distribution AND outliers of a numerical variable across categories?", "sns.barplot()", "sns.boxplot()", "sns.lineplot()", "B", "Box plots show the median, interquartile range (IQR), and outliers simultaneously. They are ideal for comparing distributions across multiple categories."),
            ("What does a correlation heatmap show?", "The frequency of each value", "The strength of linear relationships between pairs of variables", "The sum of each column", "B", "A correlation heatmap displays the Pearson correlation coefficient (-1 to +1) between every pair of numerical variables. Values near 1 or -1 indicate strong relationships; near 0 indicates weak/no linear relationship."),
        ],
        5: [
            ("Why must you call `fit_transform()` on training data but only `transform()` on test data?", "To make the code run faster", "To prevent data leakage — test statistics must not influence the scaler", "The scaler does not work on test data", "B", "fit() computes statistics (mean, std) from the training data. Applying fit() to test data would leak information about the test set into the model, giving an unrealistically optimistic evaluation."),
            ("What does the R² (R-squared) metric measure in regression?", "The number of errors", "The proportion of variance in the target explained by the model", "The average prediction error", "B", "R² ranges from 0 to 1 (and can be negative for very bad models). An R² of 0.85 means the model explains 85% of the variance in the target variable. Higher is better."),
        ],
        6: [
            ("What is the advantage of using a scikit-learn Pipeline over applying transformations manually?", "It is slower but more accurate", "It prevents data leakage and makes the workflow reproducible and deployable", "It automatically selects the best model", "B", "A Pipeline chains preprocessing and modelling steps together. This ensures transformations are always applied consistently, prevents leakage during cross-validation, and makes the model easy to serialise and deploy."),
            ("What does k-fold cross-validation do that a single train/test split does not?", "Uses less data", "Gives a more reliable performance estimate by testing on k different held-out subsets", "Always uses more features", "B", "A single split can be lucky or unlucky. k-fold CV rotates the held-out set k times, giving k performance scores. Averaging them yields a much more reliable estimate of how the model will perform on unseen data."),
        ],
    }
    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid


# ═══════════════════════════════════════════════
# AUTH DECORATOR
# ═══════════════════════════════════════════════

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════
# ROUTES — AUTH
# ═══════════════════════════════════════════════

