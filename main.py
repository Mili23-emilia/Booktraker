import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Путь к файлу базы данных
DATA_FILE = "books_data.json"

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Твой список книг")
        self.root.geometry("750x600")

        # Основной список книг
        self.books = self.load_data()

        # --- ПОЛЯ ВВОДА ---
        input_frame = tk.LabelFrame(root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w")
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2, sticky="w")
        self.pages_entry = tk.Entry(input_frame, width=30)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=2)

        self.add_button = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white")
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        # --- ФИЛЬТРАЦИЯ ---
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame, width=20)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").grid(row=0, column=2)
        self.filter_pages = tk.Entry(filter_frame, width=10)
        self.filter_pages.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=5, padx=5)

        # --- ТАБЛИЦА ВЫВОДА ---
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        
        self.tree.column("pages", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_table(self.books)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not (title and author and genre and pages):
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка на число в поле страниц
        if not pages.isdigit():
            messagebox.showwarning("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(new_book)
        self.save_data()
        self.refresh_table(self.books)
        
        # Очистка полей
        for entry in (self.title_entry, self.author_entry, self.genre_entry, self.pages_entry):
            entry.delete(0, tk.END)

    def refresh_table(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in data_list:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_q = self.filter_genre.get().strip().lower()
        pages_q = self.filter_pages.get().strip()

        filtered = self.books

        if genre_q:
            filtered = [b for b in filtered if genre_q in b["genre"].lower()]
        
        if pages_q.isdigit():
            filtered = [b for b in filtered if b["pages"] >= int(pages_q)]

        self.refresh_table(filtered)

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.refresh_table(self.books)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
