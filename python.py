import json
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"

# Load existing tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def task_manager():
    tasks = load_tasks()
    history = []
    print("\033[1;34m***** WELCOME TO YOUR TASK MANAGEMENT APP *****\033[0m")
    
    while True:
        operation = input('''\nChoose an option:
1: ADD TASK
2: UPDATE TASK
3: DELETE TASK
4: VIEW TASKS
5: VIEW HISTORY
6: EXIT
Enter your choice: ''')
        
        if operation == '1':  # Add Task
            day = input("Enter the day (Monday-Sunday) for the task: ").capitalize()
            task_name = input("Enter task: ")
            priority = input("Enter priority (High/Medium/Low): ").capitalize()
            recurring = input("Is this a recurring task? (Yes/No): ").lower()
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if day not in tasks:
                tasks[day] = []
            
            task_entry = {"task": task_name, "priority": priority, "recurring": recurring, "time": time}
            tasks[day].append(task_entry)
            save_tasks(tasks)
            print(f"Task '{task_name}' (Priority: {priority}) added under {day}.")
        
        elif operation == '2':  # Update Task
            day = input("Enter the day of the task to update: ").capitalize()
            if day in tasks:
                print("Tasks:")
                for idx, t in enumerate(tasks[day]):
                    print(f"{idx+1}: {t['task']} (Priority: {t['priority']})")
                
                index = int(input("Enter task number to update: ")) - 1
                if 0 <= index < len(tasks[day]):
                    new_task = input("Enter new task: ")
                    new_priority = input("Enter new priority (High/Medium/Low): ").capitalize()
                    tasks[day][index]["task"] = new_task
                    tasks[day][index]["priority"] = new_priority
                    tasks[day][index]["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_tasks(tasks)
                    print("Task updated successfully.")
            else:
                print("No tasks found for this day.")
        
        elif operation == '3':  # Delete Task
            day = input("Enter the day of the task to delete: ").capitalize()
            if day in tasks:
                print("Tasks:")
                for idx, t in enumerate(tasks[day]):
                    print(f"{idx+1}: {t['task']} (Priority: {t['priority']})")
                
                index = int(input("Enter task number to delete: ")) - 1
                if 0 <= index < len(tasks[day]):
                    removed_task = tasks[day].pop(index)
                    history.append({"task": removed_task['task'], "deleted_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    save_tasks(tasks)
                    print(f"Task '{removed_task['task']}' deleted.")
            else:
                print("No tasks found for this day.")
        
        elif operation == '4':  # View Tasks (Sorted by Priority)
            if tasks:
                for day, task_list in tasks.items():
                    print(f"\n\033[1;33m{day}:\033[0m")
                    sorted_tasks = sorted(task_list, key=lambda x: ["Low", "Medium", "High"].index(x["priority"]))
                    for t in sorted_tasks:
                        print(f"  - {t['task']} (Priority: {t['priority']}, Added on {t['time']})")
            else:
                print("No tasks available.")
        
        elif operation == '5':  # View History
            if history:
                print("Task History:")
                for h in history:
                    print(f"- {h['task']} (Deleted on {h['deleted_on']})")
            else:
                print("No task history available.")
        
        elif operation == '6':  # Exit
            print("\033[1;31mExiting task manager. Have a productive day!\033[0m")
            break
        
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    task_manager()
