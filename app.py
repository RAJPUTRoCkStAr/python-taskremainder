import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification
import datetime
from ttkbootstrap import Style

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title,desc ,date, time, category):
        self.tasks.append({"title": title, "description":desc,"date": date, "time": time, "category": category})

    def delete_task(self, index):
        del self.tasks[index]

    def clear_tasks(self):
        self.tasks = []

    def get_tasks(self):
        return self.tasks

def set_notification():
    title = title_entry.get()
    desc = desc_entry.get()
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
        root.after(int(time_diff.total_seconds() * 1000), lambda: notification.notify(title=title, message=desc))
        task_manager.add_task(title,desc ,date, time, category)
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
        task_listbox.insert(tk.END, f"{idx} -- {task['time']} -- {task['title']}-- {task['desc']} -- {task['category']}")

# Create tkinter window with ttkbootstrap style
root = tk.Tk()
root.title("Task Manager")
icon_path = "./paper.png"

# Use the iconbitmap method to set the icon
root.iconbitmap(icon_path)
style = Style(theme='cyborg')

task_manager = TaskManager()


ttk.Label(root, text="Add Your Task", style="light.TLabel",font=("Arial",16)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)


ttk.Label(root, text="Title:", style="warning.TLabel",font=("arial",10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
title_entry = ttk.Entry(root, width=50)
title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Detail :", style="warning.TLabel",font=("arial",10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
desc_entry = ttk.Entry(root, width=50)
desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


ttk.Label(root, text="Date:", style="warning.TLabel",font=("arial",10)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
date_combobox = ttk.Combobox(root, width=30, values=[""])
date_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")


ttk.Label(root, text="Time:", style="warning.TLabel",font=("arial",10)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
time_combobox = ttk.Combobox(root, width=30, values=[""])
time_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")


ttk.Label(root, text="Category:", style="warning.TLabel",font=("arial",10)).grid(row=5, column=0, padx=5, pady=5, sticky="w")
category_combobox = ttk.Combobox(root, width=26,font=("arial",10), values=["Office Work","Project", "Study","Class Work","Important","Eat","Other"])
category_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")


date_combobox["values"] = [(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]


time_combobox["values"] = [f"{hour:02d}:00" for hour in range(24)]
set_notification_btn = ttk.Button(root, text="Set Notification", style="success.TButton", command=set_notification)
set_notification_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


delete_task_btn = ttk.Button(root, text="Delete Task", style="danger.TButton", command=delete_task)
delete_task_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

clear_tasks_btn = ttk.Button(root, text="Clear All Tasks", style="warning.TButton", command=clear_tasks)
clear_tasks_btn.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


ttk.Label(root, text="Task List", style="success.TLabel",font=("arial",16)).grid(row=0, column=2, padx=5, pady=5, sticky="w")


task_listbox = tk.Listbox(root, width=80, bg="#f0f0f0", selectbackground="#add8e6")
task_listbox.grid(row=1, column=2, rowspan=7, padx=5, pady=5, sticky="nsew")

update_task_listbox()

root.mainloop()
