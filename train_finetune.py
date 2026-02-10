# -*- coding: utf-8 -*-
# train_finetune.py - Fine-tune a pre-trained model, log metrics and upload weights to ClearML

import os
import random
import sys
from clearml import Task
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
import joblib

# Get the current task if running via agent, otherwise create a new task
task: Task = Task.current_task() or Task.init(
    project_name="test_workflows",
    task_name="finetune sklearn logistic regression",
    output_uri=True
)

task.connect({'model': 'LogisticRegression', 'dataset': 'digits'})


# Load dataset
X, y = load_digits(return_X_y=True)

# Sinh seed ngẫu nhiên mỗi lần chạy để chia dữ liệu khác nhau
seed = random.randint(999999, 1000000)
print(f"Random seed for split: {seed}")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

# "Pre-trained" model: fit on 50% of train, then fine-tune on the rest
X_pre, X_ft, y_pre, y_ft = train_test_split(X_train, y_train, test_size=0.5, random_state=seed)
model = LogisticRegression(max_iter=1000, solver='lbfgs')
model.fit(X_pre, y_pre)

# Fine-tune
model.fit(X_ft, y_ft)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)
acc = accuracy_score(y_test, y_pred)
loss = log_loss(y_test, y_prob)

# Log metrics
print(f"Test accuracy: {acc:.4f}, log loss: {loss:.4f}")
task.get_logger().report_scalar("accuracy", "test", value=acc, iteration=0)
task.get_logger().report_scalar("log_loss", "test", value=loss, iteration=0)

# Save metrics and weights
with open("finetune_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Test accuracy: {acc:.4f}\nLog loss: {loss:.4f}\n")
joblib.dump(model, "finetuned_model.joblib")

# Cuối script, upload log file lên ClearML nếu tồn tại
if os.path.exists("run_stdout.log"):
    task.upload_artifact("run_stdout", "run_stdout.log")

task.upload_artifact("finetune_metrics", "finetune_result.txt")
task.upload_artifact("finetuned_model", "finetuned_model.joblib")
print("Metrics and model have been saved and uploaded to ClearML.")

print("Current working directory:", os.getcwd())
print("Files in cwd:", os.listdir())
