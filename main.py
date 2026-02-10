# main.py - chi chua code training, khong enqueue, khong submit task
# -*- coding: utf-8 -*-
import time
import numpy as np
from clearml import Task

# Lấy task hiện tại nếu đang chạy qua agent, nếu không sẽ tạo task mới
task: Task = Task.current_task() or Task.init(
    project_name="test_workflows",
    task_name="main.py run on colab via clearml",
    output_uri=True
)

task.connect({'learning_rate': 0.09, 'batch_size': 64})
with open("result.txt", "w", encoding="utf-8") as f:
    for epoch in range(5):
        acc = np.random.uniform(0.1, 1)
        loss = np.random.uniform(0.1, 1)
        log_line = f"Epoch {epoch+1}: acc={acc:.3f}, loss={loss:.3f}\n"
        print(log_line.strip())
        task.get_logger().report_scalar("accuracy", "train", value=acc, iteration=epoch)
        task.get_logger().report_scalar("loss", "train", value=loss, iteration=epoch)
        f.write(log_line)
        time.sleep(1)
    f.write("Training completed!\n")
task.upload_artifact("result_file", "result.txt")
print("Da upload artifact va log xong.")
