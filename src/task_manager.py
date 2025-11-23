from .storage import load_tasks, save_tasks
from .task import Task
from dataclasses import asdict

def add_task(title: str, due_to=None):
    tasks_list = load_tasks()
    new_id = max([task['id'] for task in tasks_list] if tasks_list else [0]) + 1

    tasks_list.append(asdict(Task(id=new_id, 
                                  title=title, 
                                  due_to=due_to)))
    save_tasks(tasks_list)

def list_tasks(status_filter=None) -> list:
    tasks_list = load_tasks()
    if status_filter:
        tasks_list =  [task for task in tasks_list if task['status'] == status_filter]

    tasks_list.sort(key=lambda x: x['due_to'] or '9999-12-31')
    return tasks_list

def update_task(task_id: int, new_status: str = None, title: str = None) -> bool: 
    tasks_list = load_tasks()

    upt_task = next((task for task in tasks_list if task['id'] == task_id), None)
    if upt_task: 
        if new_status:
            upt_task['status'] = new_status
        if title:
            upt_task['title'] = title
        save_tasks(tasks_list)
        return True
    return False

def delete_task(task_id: int) -> bool:
    tasks_list = load_tasks()
    del_task = next((task for task in tasks_list if task['id'] == task_id), None)
    if del_task:
        tasks_list.remove(del_task)
        save_tasks(tasks_list)
        return True
    return False