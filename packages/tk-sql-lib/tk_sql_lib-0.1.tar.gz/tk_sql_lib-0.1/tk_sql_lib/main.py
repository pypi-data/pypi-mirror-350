#import sqlite3
#import tkinter as tk
#from tkinter import messagebox
#import subprocess

def db_query(query, params=(), fetch=False):
    with sqlite3.connect("company.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone() if fetch else conn.commit()

def login():
    user = db_query("SELECT role FROM users WHERE login = ? AND password = ?",
                    (login_entry.get(), pass_entry.get()), fetch=True)
    if user:
        messagebox.showinfo("Успешно", f"Добро пожаловать! Роль: {user[0]}")
        subprocess.Popen(["python", "dashboard.py"])
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

def register():
    login_text = login_entry.get()
    password_text = pass_entry.get()
    if not login_text or not password_text:
        return messagebox.showwarning("Ошибка", "Заполните оба поля")
    if len(password_text) < 8:
        return messagebox.showwarning("Ошибка", "Пароль должен быть минимум 8 символов")
    try:
        db_query("INSERT INTO users (login, password, role) VALUES (?, ?, 'user')",
                 (login_text, password_text))
        messagebox.showinfo("Успешно", "Регистрация завершена")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Логин уже существует")

def reset_password():
    login_text = login_entry.get()
    password_text = pass_entry.get()
    if not login_text or not password_text:
        return messagebox.showwarning("Ошибка", "Заполните оба поля")
    if len(password_text) < 8:
        return messagebox.showwarning("Ошибка", "Пароль должен быть минимум 8 символов")
    user = db_query("SELECT 1 FROM users WHERE login = ?", (login_text,), fetch=True)
    if user:
        db_query("UPDATE users SET password = ? WHERE login = ?",
                 (password_text, login_text))
        messagebox.showinfo("Успешно", "Пароль обновлён")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")

# Интерфейс
root = tk.Tk()
root.title("Авторизация")
root.geometry("300x250")

for text, var in [("Логин:", None), ("Пароль:", "*")]:
    tk.Label(root, text=text).pack()
    e = tk.Entry(root, show=var) if var else tk.Entry(root)
    e.pack()
    if not var: login_entry = e
    else: pass_entry = e

for text, cmd in [("Войти", login), ("Регистрация", register), ("Сброс пароля", reset_password)]:
    tk.Button(root, text=text, command=cmd).pack(pady=5)

root.mainloop()