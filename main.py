# main.py
from dotenv import load_dotenv
import os
from clearml import Task
from clearml import Task as ClearMLTask

load_dotenv()

# Thiết lập ClearML credentials từ .env
os.environ["CLEARML_API_ACCESS_KEY"] = os.getenv("CLEARML_API_ACCESS_KEY") or ""
os.environ["CLEARML_API_SECRET_KEY"] = os.getenv("CLEARML_API_SECRET_KEY") or ""
os.environ["CLEARML_SERVER_HOST"] = os.getenv("CLEARML_SERVER_HOST") or ""

# Khởi tạo ClearML Task
task: ClearMLTask = Task.init(
	project_name="test_workflows",
	task_name="main.py run on colab via clearml"
)

print("ClearML Task initialized. Ready to run remotely.")
