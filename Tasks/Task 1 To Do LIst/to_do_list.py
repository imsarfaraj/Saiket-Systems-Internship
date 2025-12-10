import json
import os
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass, asdict

DATA_FILE = 'tasks.json'


@dataclass
class Task:
    description: str
    completed: bool = False


class TaskManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.tasks = []
        self.load()

    def add(self, description):
        if not description.strip():
            return
        self.tasks.append(Task(description=description.strip()))
        self.save()

    def remove(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save()

    def toggle_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed
            self.save()

    def clear_all(self):
        self.tasks = []
        self.save()

    def save(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print('Error saving tasks:', e)

    def load(self):
        if not os.path.exists(self.data_file):
            self.tasks = []
            return
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task(**item) for item in data]
        except Exception as e:
            print('Error loading tasks:', e)
            self.tasks = []


class SimpleTodoApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()

        # Color scheme
        self.colors = {
            'primary': '#4A6FA5',
            'accent': '#FF6B6B',
            'success': '#51A851',
            'background': '#2C3E50',
            'surface': 'white',
            'text': 'white',
            'text_dark': '#2C3E50'
        }

        self.title('Simple To-Do List')
        self.geometry('400x500')
        self.resizable(False, False)
        self.manager = manager

        # Configure root window background
        self.configure(bg=self.colors['background'])

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_container, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = tk.Label(
            header_frame,
            text="My Tasks",
            font=('Arial', 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['background']
        )
        title_label.pack()

        # Simple stats
        self.stats_label = tk.Label(
            header_frame,
            text="0 tasks",
            font=('Arial', 10),
            fg='#BDC3C7',
            bg=self.colors['background']
        )
        self.stats_label.pack()

        # Input area
        input_frame = tk.Frame(main_container, bg=self.colors['background'])
        input_frame.pack(fill=tk.X, pady=(0, 15))

        self.entry = tk.Entry(
            input_frame,
            font=('Arial', 11),
            bg='white',
            relief='solid',
            borderwidth=1,
            width=25
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind('<Return>', lambda e: self.add_task())

        add_btn = tk.Button(
            input_frame,
            text='Add',
            command=self.add_task,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            borderwidth=0,
            padx=15,
            cursor='hand2'
        )
        add_btn.pack(side=tk.RIGHT)

        # Tasks list with scrollbar
        list_frame = tk.Frame(main_container, bg=self.colors['background'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='white',
            fg=self.colors['text_dark'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            borderwidth=1,
            relief='solid',
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons
        actions_frame = tk.Frame(main_container, bg=self.colors['background'])
        actions_frame.pack(fill=tk.X)

        btn1 = tk.Button(
            actions_frame,
            text='Task Done',
            command=self.toggle_completed,
            bg=self.colors['success'],
            fg='black',
            font=('Arial', 9, 'bold'),
            borderwidth=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        btn1.pack(side=tk.LEFT, padx=(0, 5))

        btn2 = tk.Button(
            actions_frame,
            text='Delete',
            command=self.delete_task,
            bg=self.colors['accent'],
            fg='black',
            font=('Arial', 9, 'bold'),
            borderwidth=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        btn2.pack(side=tk.LEFT, padx=5)

        btn3 = tk.Button(
            actions_frame,
            text='Clear All',
            command=self.clear_all,
            bg='#E74C3C',
            fg='black',
            font=('Arial', 9, 'bold'),
            borderwidth=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        btn3.pack(side=tk.LEFT, padx=(5, 0))

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            mark = '✓' if task.completed else '○'
            display = f" {mark} {task.description}"
            self.listbox.insert(tk.END, display)

        self.update_stats()

    def update_stats(self):
        total = len(self.manager.tasks)
        completed = sum(1 for t in self.manager.tasks if t.completed)

        if total == 0:
            self.stats_label.config(text="No tasks")
        else:
            self.stats_label.config(text=f"{completed}/{total} completed")

    def add_task(self):
        desc = self.entry.get().strip()
        if not desc:
            messagebox.showinfo('Empty', 'Please enter a task.')
            return
        self.manager.add(desc)
        self.entry.delete(0, tk.END)
        self.refresh_list()

    def get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo('No Selection', 'Please select a task first.')
            return None
        return sel[0]

    def toggle_completed(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        self.manager.toggle_completed(idx)
        self.refresh_list()

    def delete_task(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        confirm = messagebox.askyesno('Confirm', 'Delete this task?')
        if confirm:
            self.manager.remove(idx)
            self.refresh_list()

    def clear_all(self):
        if not self.manager.tasks:
            messagebox.showinfo('Info', 'No tasks to clear!')
            return

        confirm = messagebox.askyesno('Confirm', 'Delete ALL tasks?')
        if confirm:
            self.manager.clear_all()
            self.refresh_list()


if __name__ == '__main__':
    manager = TaskManager()
    app = SimpleTodoApp(manager)
    app.mainloop()
