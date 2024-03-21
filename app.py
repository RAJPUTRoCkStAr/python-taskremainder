import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification
import datetime
from ttkbootstrap import Style

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, date, time, category):
        self.tasks.append({"title": title, "date": date, "time": time, "category": category})

    def delete_task(self, index):
        del self.tasks[index]

    def clear_tasks(self):
        self.tasks = []

    def get_tasks(self):
        return self.tasks

def set_notification():
    title = title_entry.get()
    date = date_combobox.get()
    time = time_combobox.get()
    category = category_combobox.get()

    # Validate date format
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        notification.notify(title="Error", message="Invalid date format. Please use YYYY-MM-DD format.")
        return

    # Validate time format
    try:
        time_obj = datetime.datetime.strptime(time, "%H:%M").time()
    except ValueError:
        notification.notify(title="Error", message="Invalid time format. Please use HH:MM format.")
        return

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    # Calculate time difference
    datetime_selected = datetime.datetime.combine(date_obj, time_obj)
    datetime_current = datetime.datetime.combine(current_date, current_time)
    time_diff = datetime_selected - datetime_current

    # Schedule notification
    if time_diff.total_seconds() <= 0:
        notification.notify(title="Error", message="Please select a future date and time.")
    else:
        root.after(int(time_diff.total_seconds() * 1000), lambda: notification.notify(title=title, message="It's time for your task: " + title))
        task_manager.add_task(title, date, time, category)
        update_task_listbox()

def delete_task():
    selected_index = task_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        task_manager.delete_task(index)
        update_task_listbox()
        task_listbox.selection_clear(0, tk.END)  # Clear the selection after deleting

def clear_tasks():
    task_manager.clear_tasks()
    update_task_listbox()

def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for idx, task in enumerate(task_manager.get_tasks(), start=1):
        task_listbox.insert(tk.END, f"{idx}. {task['time']} - {task['title']} - {task['category']}")

# Create tkinter window with ttkbootstrap style
root = tk.Tk()
root.title("Task Manager")
style = Style(theme='flatly')

task_manager = TaskManager()

# Title label
ttk.Label(root, text="Add Your Task", style="primary.TLabel").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Title entry
ttk.Label(root, text="Title:", style="primary.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="w")
title_entry = ttk.Entry(root, width=30)
title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Date selection
ttk.Label(root, text="Date:", style="primary.TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="w")
date_combobox = ttk.Combobox(root, width=15, values=[""])
date_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Time selection
ttk.Label(root, text="Time:", style="primary.TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="w")
time_combobox = ttk.Combobox(root, width=10, values=[""])
time_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Category selection
ttk.Label(root, text="Category:", style="primary.TLabel").grid(row=4, column=0, padx=5, pady=5, sticky="w")
category_combobox = ttk.Combobox(root, width=15, values=["Office Work", "Project", "Study", "Other"])
category_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Populate date dropdown with dates for the next 7 days
date_combobox["values"] = [(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

# Populate time dropdown with hourly intervals
time_combobox["values"] = [f"{hour:02d}:00" for hour in range(24)]
set_notification_btn = ttk.Button(root, text="Set Notification", style="success.TButton", command=set_notification)
set_notification_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Button to delete task
delete_task_btn = ttk.Button(root, text="Delete Task", style="danger.TButton", command=delete_task)
delete_task_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Button to clear tasks
clear_tasks_btn = ttk.Button(root, text="Clear All Tasks", style="warning.TButton", command=clear_tasks)
clear_tasks_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Title for showing tasks
ttk.Label(root, text="Task List", style="success.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Listbox to display tasks
task_listbox = tk.Listbox(root, width=60, bg="#f0f0f0", selectbackground="#add8e6")
task_listbox.grid(row=1, column=2, rowspan=7, padx=5, pady=5, sticky="nsew")

update_task_listbox()

root.mainloop()
