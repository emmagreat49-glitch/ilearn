"""iLEARN — AI Fundamentals course seed."""
from .helpers import insert_lessons_and_quizzes


def seed_ai_fundamentals(conn, c):
    c.execute(
        "INSERT INTO courses (title, description, icon, level, language) VALUES (?,?,?,?,?)",
        (
            "AI Fundamentals",
            "Understand artificial intelligence from the ground up. Learn how machine learning works, build your first models, and understand the real-world applications and limitations of AI.",
            "cpu",
            "Beginner to Intermediate",
            "ai",
        ),
    )
    cid = c.lastrowid

    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Understanding AI & Machine Learning", 1))
    mod1 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Machine Learning in Practice", 2))
    mod2 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "Deep Learning & Neural Networks", 3))
    mod3 = c.lastrowid
    c.execute("INSERT INTO modules (course_id, module_title, module_order) VALUES (?,?,?)",
              (cid, "AI Ethics & Real-World Applications", 4))
    mod4 = c.lastrowid

    lessons = [
        (1, "What is AI? From Rules to Learning", mod1, """
<h2>What is Artificial Intelligence?</h2>
<p>Artificial Intelligence is the field of computer science focused on building systems that can perform tasks that normally require human intelligence — things like recognising images, understanding language, making decisions, and learning from experience.</p>

<h3>The Three Levels</h3>
<div class="concept-box">
  <div class="cb-title">AI vs Machine Learning vs Deep Learning</div>
  <p><strong>AI (broad)</strong> — Any technique that allows computers to mimic human intelligence</p>
  <p><strong>Machine Learning (subset)</strong> — Systems that learn from data without being explicitly programmed</p>
  <p><strong>Deep Learning (subset of ML)</strong> — Multi-layered neural networks that learn complex patterns</p>
</div>

<h3>Types of Machine Learning</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Type</th><th style="padding:8px;text-align:left">How it works</th><th style="padding:8px;text-align:left">Example</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Supervised</td><td style="padding:8px">Learns from labelled examples</td><td style="padding:8px">Spam detection, image classification</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Unsupervised</td><td style="padding:8px">Finds patterns in unlabelled data</td><td style="padding:8px">Customer segmentation, anomaly detection</td></tr>
  <tr><td style="padding:8px">Reinforcement</td><td style="padding:8px">Learns by trial and error with rewards</td><td style="padding:8px">Game AI, robotics</td></tr>
</table>

<h3>How a Machine "Learns"</h3>
<pre><code># Conceptual view of supervised learning

# 1. You have labelled training data
emails = [
    {"text": "Buy cheap pills now!", "label": "spam"},
    {"text": "Meeting at 3pm tomorrow", "label": "not spam"},
]

# 2. The model learns a function: features -> label
# 3. It makes predictions on new, unseen data
new_email = "Congratulations! You won a prize!"
prediction = model.predict(new_email)  # -> "spam"</code></pre>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>List 5 AI applications you use daily (e.g. Netflix recommendations, Google Maps)</li>
    <li>For each, identify whether it is supervised, unsupervised, or reinforcement learning</li>
    <li>Describe in plain English how you think spam detection works</li>
  </ol>
</div>
""", 25),
        (2, "Machine Learning with scikit-learn", mod2, """
<h2>Machine Learning with scikit-learn</h2>
<p>scikit-learn is the most widely used Python library for machine learning. It provides consistent, simple APIs for dozens of algorithms.</p>

<h3>The ML Workflow</h3>
<pre><code>import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. Load data
df = pd.read_csv("students.csv")
X  = df[["study_hours", "attendance", "prev_score"]]  # features
y  = df["passed"]                                      # target

# 2. Split BEFORE scaling (prevent data leakage)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Scale features (fit on train, transform both)
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)   # learn mean/std from training set
X_test  = scaler.transform(X_test)        # apply same scale to test set

# 4. Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. Evaluate
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
print(classification_report(y_test, predictions))</code></pre>

<h3>Classification vs Regression</h3>
<pre><code># Classification — predicts a CATEGORY
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Regression — predicts a NUMBER
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train, y_train)

from sklearn.metrics import r2_score, mean_squared_error
preds = reg.predict(X_test)
print(f"R²: {r2_score(y_test, preds):.2f}")</code></pre>

<div class="concept-box warning">
  <div class="cb-title">Data Leakage</div>
  <p>Always split your data BEFORE scaling or any preprocessing. If you fit the scaler on the full dataset, your model "sees" the test data during training — making performance metrics unrealistically good.</p>
</div>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Load the iris dataset: <code>from sklearn.datasets import load_iris</code></li>
    <li>Split it 80/20 into train and test sets</li>
    <li>Train a <code>RandomForestClassifier</code> on it</li>
    <li>Print the accuracy score and classification report</li>
  </ol>
</div>
""", 35),
        (3, "Neural Networks & Deep Learning Explained", mod3, """
<h2>Neural Networks</h2>
<p>Neural networks are the foundation of deep learning and the technology behind ChatGPT, image recognition, and speech recognition. Understanding how they work is essential for any AI practitioner.</p>

<h3>How a Neuron Works</h3>
<pre><code># A single artificial neuron
def neuron(inputs, weights, bias):
    # Weighted sum
    z = sum(w * x for w, x in zip(weights, inputs)) + bias
    # Activation function (ReLU)
    return max(0, z)

# Example: predicting if a student will pass
inputs  = [8, 90, 75]   # study_hours, attendance%, prev_score
weights = [0.5, 0.3, 0.2]
bias    = -10

output = neuron(inputs, weights, bias)
print(f"Pass probability input: {output}")</code></pre>

<h3>Building a Neural Network with Keras</h3>
<pre><code>import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Build the network
model = keras.Sequential([
    keras.layers.Dense(64, activation="relu",    input_shape=(3,)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1,  activation="sigmoid")  # binary output
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train
history = model.fit(X_train, y_train, epochs=50, validation_split=0.2, verbose=0)

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {acc:.2f}")</code></pre>

<h3>Key Concepts</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Term</th><th style="padding:8px;text-align:left">Meaning</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Epoch</td><td style="padding:8px">One full pass through the training data</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Loss</td><td style="padding:8px">How wrong the model's predictions are</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Backpropagation</td><td style="padding:8px">Algorithm that adjusts weights to reduce loss</td></tr>
  <tr><td style="padding:8px">Overfitting</td><td style="padding:8px">Model memorises training data but fails on new data</td></tr>
</table>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Manually trace through the neuron function above with different inputs</li>
    <li>Draw a diagram of a 3-layer neural network (input, hidden, output)</li>
    <li>Explain in your own words what backpropagation does</li>
    <li>Describe the difference between overfitting and underfitting</li>
  </ol>
</div>
""", 35),
        (4, "AI Ethics, Bias & Real-World Impact", mod4, """
<h2>AI Ethics & Responsible AI</h2>
<p>AI systems are making decisions that affect people's lives — loan approvals, medical diagnoses, criminal sentencing. Understanding the ethical challenges is as important as understanding the technology.</p>

<h3>Bias in AI Systems</h3>
<pre><code># Where bias comes from

# 1. Biased training data
# If historical hiring data shows men were hired more,
# a model trained on it will discriminate against women.

# 2. Proxy variables
# Zip codes can be proxies for race.
# Even "neutral" features can encode discrimination.

# 3. Feedback loops
# Predictive policing: model predicts crime -> police patrol area ->
# more arrests -> model gets reinforced -> cycle continues</code></pre>

<h3>Measuring Fairness</h3>
<pre><code">from sklearn.metrics import confusion_matrix

# Check model performance separately for each group
for group in df["gender"].unique():
    subset = df[df["gender"] == group]
    X_sub  = subset[features]
    y_sub  = subset["target"]
    preds  = model.predict(X_sub)
    acc    = accuracy_score(y_sub, preds)
    print(f"{group}: accuracy = {acc:.2f}")

# If accuracy differs significantly between groups,
# the model may be discriminatory</code></pre>

<h3>Key Principles of Responsible AI</h3>
<div class="concept-box">
  <div class="cb-title">The Five Principles</div>
  <ol>
    <li><strong>Transparency</strong> — People should know when AI is making decisions about them</li>
    <li><strong>Fairness</strong> — Models should not discriminate against protected groups</li>
    <li><strong>Privacy</strong> — Training data must be collected and stored responsibly</li>
    <li><strong>Accountability</strong> — Humans must remain responsible for AI decisions</li>
    <li><strong>Safety</strong> — AI systems must be tested rigorously before deployment</li>
  </ol>
</div>

<h3>Real-World Applications</h3>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
  <tr style="background:var(--surface-2)"><th style="padding:8px;text-align:left">Field</th><th style="padding:8px;text-align:left">Application</th><th style="padding:8px;text-align:left">Concern</th></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Healthcare</td><td style="padding:8px">Diagnosis assistance</td><td style="padding:8px">Must not replace doctor judgement</td></tr>
  <tr style="border-bottom:1px solid var(--border)"><td style="padding:8px">Finance</td><td style="padding:8px">Credit scoring</td><td style="padding:8px">Cannot discriminate by protected class</td></tr>
  <tr><td style="padding:8px">Criminal Justice</td><td style="padding:8px">Recidivism prediction</td><td style="padding:8px">Has shown racial bias in practice</td></tr>
</table>

<div class="practice-box">
  <div class="pb-title">Practice Exercise</div>
  <ol>
    <li>Find a real news story about AI bias and summarise it in 5 sentences</li>
    <li>For each of the 5 responsible AI principles, give one real-world example of what happens when it is violated</li>
    <li>If you were building an AI hiring tool, what steps would you take to ensure it is fair?</li>
  </ol>
</div>
""", 30),
    ]

    quizzes = {
        1: [
            ("What is the relationship between AI, Machine Learning, and Deep Learning?",
             "They are three completely unrelated fields",
             "Machine Learning is a subset of AI, and Deep Learning is a subset of Machine Learning",
             "Deep Learning is broader than AI", "B",
             "AI is the broadest field. ML is a subset that uses data to learn. Deep Learning is a subset of ML using neural networks."),
            ("In supervised learning, what does 'labelled data' mean?",
             "Data that has been sorted alphabetically",
             "Training examples where the correct answer is already known",
             "Data that has been encrypted", "B",
             "Supervised learning requires training examples paired with correct answers (labels), so the model can learn the mapping from input to output."),
        ],
        2: [
            ("Why must you split data BEFORE scaling?",
             "Splitting after scaling is faster",
             "Scaling before splitting leaks test set statistics into training, causing inflated performance metrics",
             "The order does not matter", "B",
             "If you fit the scaler on the full dataset, the model indirectly 'sees' the test data during training. Split first, fit scaler on train only."),
            ("What is the difference between classification and regression?",
             "Classification is for small datasets; regression is for large ones",
             "Classification predicts categories; regression predicts continuous numbers",
             "They are the same thing", "B",
             "Classification outputs a class (spam/not spam). Regression outputs a number (house price, temperature)."),
        ],
        3: [
            ("What does an epoch represent in neural network training?",
             "The learning rate of the model",
             "One complete pass through the entire training dataset",
             "The number of neurons in the network", "B",
             "An epoch means the model has seen every training example once. Training typically runs for multiple epochs."),
            ("What is overfitting?",
             "When a model is too simple to learn the training data",
             "When a model memorises the training data but performs poorly on new data",
             "When the learning rate is too low", "B",
             "Overfitting occurs when a model learns the training data too well — including its noise — making it fail to generalise."),
        ],
        4: [
            ("How can bias enter an AI system?",
             "Only through coding errors",
             "Through biased training data, proxy variables, or feedback loops",
             "AI systems cannot be biased", "B",
             "Bias enters through historical data that reflects past discrimination, features that act as proxies for protected attributes, and self-reinforcing feedback loops."),
            ("What does the principle of AI transparency require?",
             "That AI source code must be publicly available",
             "That people should know when AI is making decisions that affect them",
             "That all AI models must be explainable in detail", "B",
             "Transparency means affected individuals should be informed when automated decision-making is involved, even if the technical details remain proprietary."),
        ],
    }

    insert_lessons_and_quizzes(c, cid, lessons, quizzes)
    return cid
