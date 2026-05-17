import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Имя файла для хранения истории
HISTORY_FILE = "task_history.json"

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x600")

        # 1. Список предопределённых задач
        self.predefined_tasks = [
            {"text": "Прочитать главу учебника", "type": "Учёба"},
            {"text": "Сделать 20 приседаний", "type": "Спорт"},
            {"text": "Разобрать почту", "type": "Работа"},
            {"text": "Выучить 10 новых слов", "type": "Учёба"},
            {"text": "Пробежка 15 минут", "type": "Спорт"},
            {"text": "Составить план на неделю", "type": "Работа"}
        ]

        # Загрузка истории из JSON
        self.history = self.load_history()

        # --- Интерфейс ---
        
        # Кнопка генерации
        self.gen_btn = tk.Button(root, text="Сгенерировать задачу", font=("Arial", 12, "bold"),
                                 command=self.generate_task, bg="#4CAF50", fg="white")
        self.gen_btn.pack(pady=20)

        # Поле для отображения текущей задачи
        self.current_task_label = tk.Label(root, text="Нажмите кнопку для выбора задачи", 
                                           font=("Arial", 10, "italic"), wraplength=400)
        self.current_task_label.pack(pady=10)

        # --- Секция добавления своей задачи ---
        add_frame = tk.LabelFrame(root, text="Добавить свою задачу в список доступных")
        add_frame.pack(fill="x", padx=20, pady=10)

        self.new_task_entry = tk.Entry(add_frame)
        self.new_task_entry.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        self.type_var = tk.StringVar(value="Учёба")
        self.type_menu = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                      values=["Учёба", "Спорт", "Работа"], width=10)
        self.type_menu.grid(row=0, column=1, padx=5)

        tk.Button(add_frame, text="+", command=self.add_custom_task).grid(row=0, column=2, padx=5)
        add_frame.columnconfigure(0, weight=1)

        # --- Секция истории и фильтрации ---
        tk.Label(root, text="История сгенерированных задач:", font=("Arial", 10, "bold")).pack()
        
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Фильтр:").grid(row=0, column=0)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                        values=["Все", "Учёба", "Спорт", "Работа"], width=10)
        self.filter_menu.grid(row=0, column=1, padx=5)
        self.filter_menu.bind("«ComboboxSelected»", lambda e: self.update_history_display())

        self.history_listbox = tk.Listbox(root, width=60, height=12)
        self.history_listbox.pack(padx=20, pady=5)

        self.update_history_display()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def generate_task(self):
        # 2. Выбор случайной задачи
        task = random.choice(self.predefined_tasks)
        self.current_task_label.config(text=f"ЗАДАЧА: {task['text']} ({task['type']})", font=("Arial", 10, "bold"))
        
        # 3. Добавление в историю
        self.history.insert(0, task)
        self.save_history()
        self.update_history_display()

    def add_custom_task(self):
        # 6. Проверка корректности ввода
        text = self.new_task_entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка", "Текст задачи не может быть пустым!")
            return
        
        self.predefined_tasks.append({"text": text, "type": self.type_var.get()})
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена в список возможных!")

    def update_history_display(self):
        # 4. Реализация фильтрации
        self.history_listbox.delete(0, tk.END)
        f_type = self.filter_var.get()
        
        for task in self.history:
            if f_type == "Все" or task['type'] == f_type:
                self.history_listbox.insert(tk.END, f"[{task['type']}] {task['text']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
