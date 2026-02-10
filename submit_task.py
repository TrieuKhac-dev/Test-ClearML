from clearml import Task
from clearml.task import Task as TaskType

# This script is only used to submit and enqueue a task for the agent. It does NOT run training locally.


# script_name = "main.py"
# if len(sys.argv) > 1:
#     script_name = sys.argv[1]

task: TaskType = Task.create(
    project_name="test_workflows",
    task_name="train on colab agent: train_finetune.py",
    script="train_finetune.py"
)
task.enqueue(task=task, queue_name="default")
print("Task has been enqueued to the 'default' queue with script train_finetune.py. The Colab agent will pick it up and execute it.")