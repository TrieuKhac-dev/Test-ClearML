from clearml import Task

# Xóa tất cả các task theo trạng thái hoặc theo project


# Hàm chuẩn hóa kết quả trả về từ _query_tasks thành list dict {'id', 'name'}
def normalize_tasks(tasks):
    # Nếu là dict có key 'tasks' thì lấy ra list
    if isinstance(tasks, dict) and 'tasks' in tasks:
        return tasks['tasks']
    # Nếu là list object Task thì chuyển thành dict
    if isinstance(tasks, list):
        return [
            {'id': t.id, 'name': getattr(t, 'name', None)} if hasattr(t, 'id') else t
            for t in tasks
        ]
    return []

# Hàm lọc task theo tên (exact hoặc chứa tên)
def filter_tasks_by_name(task_list, task_name, exact_match):
    if not task_name:
        return task_list
    if exact_match:
        return [t for t in task_list if t.get('name') == task_name]
    return [t for t in task_list if task_name in (t.get('name') or '')]

# Hàm xóa task theo id
def delete_task_by_id(task_id):
    try:
        task = Task.get_task(task_id=task_id)
        task.delete()
        print(f"Deleted task: {task_id}")
    except Exception as e:
        print(f"Failed to delete task {task_id}: {e}")

# Hàm chính để xóa task theo các tiêu chí
def delete_tasks(project_name=None, status=None, task_name=None, exact_match=False):
    """
    Xóa các task trong ClearML theo project, trạng thái, hoặc tên task.
    Args:
        project_name (str): Tên project (None để lấy tất cả project)
        status (str): Trạng thái task (None để lấy tất cả trạng thái)
        task_name (str): Tên task (None để lấy tất cả tên)
        exact_match (bool): True để chỉ xóa task có tên chính xác, False để xóa task chứa tên
    """
    # Tạo filter cho truy vấn
    task_filter = {}
    if project_name:
        task_filter['project_name'] = project_name
    if status:
        task_filter['status'] = status
    # Nếu exact_match, filter theo name luôn từ API, còn nếu không thì lấy hết rồi lọc lại
    if task_name and exact_match:
        task_filter['name'] = task_name

    # Lấy danh sách task
    tasks = Task._query_tasks(**task_filter)
    task_list = normalize_tasks(tasks)
    # Lọc lại theo tên nếu cần
    task_list = filter_tasks_by_name(task_list, task_name, exact_match)
    task_ids = [t['id'] for t in task_list]
    if not task_ids:
        print("No matching tasks found to delete.")
        return
    print(f"Found {len(task_ids)} tasks to delete.")
    for tid in task_ids:
        delete_task_by_id(tid)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Xóa task trong ClearML theo project, trạng thái, hoặc tên task.")
    parser.add_argument('--project', type=str, default=None, help='Tên project (tùy chọn)')
    parser.add_argument('--status', type=str, default=None, help='Trạng thái task (tùy chọn, ví dụ: completed, failed, published, draft, in_progress, stopped, queued, closed)')
    parser.add_argument('--task_id', type=str, default=None, help='ID task cần xóa (tùy chọn)')
    parser.add_argument('--task_name', type=str, default=None, help='Tên task cần xóa (tùy chọn, xóa tất cả task trùng tên)')
    parser.add_argument('--exact', action='store_true', help='Chỉ xóa task có tên chính xác (bật cờ này để so khớp chính xác)')
    args = parser.parse_args()
    if args.task_id:
        try:
            task = Task.get_task(task_id=args.task_id)
            task.delete()
            print(f"Đã xóa task: {args.task_id}")
        except Exception as e:
            print(f"Không thể xóa task {args.task_id}: {e}")
    else:
        delete_tasks(project_name=args.project, status=args.status, task_name=args.task_name, exact_match=args.exact)
