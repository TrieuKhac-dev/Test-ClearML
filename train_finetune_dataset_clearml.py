"""
train_finetune_dataset_clearml.py - Fine-tune a model using a dataset from ClearML

Usage:
    python train_finetune_dataset_clearml.py --dataset_id <dataset_id> --csv_file <csv_file_name>

- --dataset_id: ID của dataset đã upload lên ClearML
- --csv_file: Tên file CSV trong dataset (ví dụ: digits_dataset.csv)
"""
import os
import sys
import random
import argparse
from clearml import Task, Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
import joblib

# Redirect stdout/stderr to log file
class Tee:
    def __init__(self, filename, mode="w"):
        self.file = open(filename, mode, encoding="utf-8")
        self.stdout = sys.stdout
        self.closed = False
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
        self.stdout.flush()
    def close(self):
        self.file.close()
        self.closed = True
        
log_file = "run_stdout.log"
sys.stdout = Tee(log_file)
sys.stderr = sys.stdout

parser = argparse.ArgumentParser(description="Fine-tune model using dataset from ClearML")
parser.add_argument('--dataset_id', required=True, help='ClearML dataset id')
parser.add_argument('--csv_file', required=True, help='CSV file name inside dataset')
args = parser.parse_args()

# Get the current task if running via agent, otherwise create a new task
clearml_task = Task.current_task() or Task.init(
    project_name="test_workflows",
    task_name="finetune sklearn logistic regression (clearml dataset)",
    output_uri=True
)

clearml_task.connect({'model': 'LogisticRegression', 'dataset_id': args.dataset_id, 'csv_file': args.csv_file})

# Download dataset from ClearML
print(f"Downloading dataset {args.dataset_id} from ClearML...")
dataset = Dataset.get(dataset_id=args.dataset_id)
local_path = dataset.get_local_copy()
print(f"Dataset downloaded to: {local_path}")

# Load CSV
csv_path = os.path.join(local_path, args.csv_file)
print(f"Loading data from: {csv_path}")
data = pd.read_csv(csv_path)
X = data.drop("label", axis=1).values
y = data["label"].values

# Generate random seed for splitting data each run
seed = random.randint(999999, 1000000)
print(f"Random seed for split: {seed}")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

# Pre-trained model: fit on 50% of train, then fine-tune on the rest
X_pre, X_ft, y_pre, y_ft = train_test_split(X_train, y_train, test_size=0.5, random_state=seed)
model = LogisticRegression(max_iter=1000, solver='lbfgs')
model.fit(X_pre, y_pre)

# Fine-tune on the remaining data
model.fit(X_ft, y_ft)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)
accuracy = accuracy_score(y_test, y_pred)
logloss = log_loss(y_test, y_prob)

# Log metrics
print(f"Test accuracy: {accuracy:.4f}, log loss: {logloss:.4f}")
clearml_task.get_logger().report_scalar("accuracy", "test", value=accuracy, iteration=0)
clearml_task.get_logger().report_scalar("log_loss", "test", value=logloss, iteration=0)

# Save metrics and model weights
with open("finetune_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Test accuracy: {accuracy:.4f}\nLog loss: {logloss:.4f}\n")
joblib.dump(model, "finetuned_model.joblib")

# Upload artifacts
if os.path.exists("run_stdout.log"):
    clearml_task.upload_artifact("run_stdout", "run_stdout.log")
clearml_task.upload_artifact("finetune_metrics", "finetune_result.txt")
clearml_task.upload_artifact("finetuned_model", "finetuned_model.joblib")
print("Metrics and model have been saved and uploaded to ClearML.")

print("Current working directory:", os.getcwd())
print("Files in cwd:", os.listdir())
