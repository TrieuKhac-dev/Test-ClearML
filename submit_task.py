
from clearml import Task
import time
import requests
import shutil

def wait_for_task(task):
    print(f"Waiting for task {task.id} to finish...")
    while task.status not in ("completed", "failed", "closed", "stopped"):
        print(f"Current status: {task.status}")
        time.sleep(10)
        task.reload()
    print(f"Task finished with status: {task.status}")

def download_artifact(task, artifact_name, output_path):
    artifact = task.artifacts.get(artifact_name)
    if not artifact:
        print(f"Artifact '{artifact_name}' not found!")
        return False
    url = artifact.get('url')
    if not url:
        print(f"Artifact '{artifact_name}' has no URL!")
        return False
    url_str = str(url)
    if url_str.startswith("http://") or url_str.startswith("https://"):
        print(f"Downloading artifact '{artifact_name}' from {url_str}")
        r = requests.get(url_str)
        if r.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded to {output_path}")
            return True
        else:
            print(f"Failed to download artifact: HTTP {r.status_code}")
            return False
    else:
        # Local file path
        print(f"Copying local artifact '{artifact_name}' from {url_str}")
        shutil.copy(url_str, output_path)
        print(f"Copied to {output_path}")
        return True

def print_log_file(log_file):
    print("\n--- Log from run_stdout.log ---")
    with open(log_file, encoding="utf-8") as f:
        print(f.read())
    print("--- End of log ---\n")

if __name__ == "__main__":
    # Submit and enqueue task
    # task = Task.create(
    #     project_name="test_workflows",
    #     task_name="train on colab agent: train_finetune.py",
    #     script="train_finetune_clean.py"
    # )

    task = Task.create(
        project_name="test_workflows",
        task_name="train on agent: train_finetune_dataset_clearml.py",
        script="train_finetune_dataset_clearml.py"
    )
    task.enqueue(task=task, queue_name="default")
    print("Task has been enqueued to the 'default' queue with script train_finetune_dataset_clearml.py. The agent will pick it up and execute it.")

    # Wait for task to complete
    wait_for_task(task)

    # Download and print log artifact
    log_file = "run_stdout.log"
    if download_artifact(task, "run_stdout", log_file):
        print_log_file(log_file)