#import tkinter as tk
#from tkinter import ttk, simpledialog, messagebox
#import sqlite3

db = "company.db"

def get_cols(t):
    return [c[1] for c in sqlite3.connect(db).execute(f"PRAGMA table_info({t})")]

def load():
    t = table.get()
    cols = get_cols(t)
    tree.config(columns=cols, show="headings")
    for c in cols: tree.heading(c, text=c)
    for i in tree.get_children(): tree.delete(i)
    for r in sqlite3.connect(db).execute(f"SELECT * FROM {t}"): tree.insert("", "end", values=r)

def edit(e):
    i, c = tree.focus(), tree.identify_column(e.x)
    if not i: return
    col, idx = tree["columns"][int(c[1:])-1], int(c[1:])-1
    x, y, w, h = tree.bbox(i, c)
    old = tree.item(i)["values"]
    ent = tk.Entry(tree); ent.insert(0, old[idx]); ent.place(x=x, y=y, w=w, h=h); ent.focus()

    def save(_):
        val = ent.get(); ent.destroy()
        new = list(old); new[idx] = val; tree.item(i, values=new)
        with sqlite3.connect(db) as conn:
            conn.execute(f"UPDATE {table.get()} SET {col}=? WHERE id=?", (val, old[0]))
            conn.commit()

    ent.bind("<Return>", save)
    ent.bind("<FocusOut>", lambda _: ent.destroy())

def add():
    t, cols = table.get(), get_cols(table.get())[1:]
    vals = [simpledialog.askstring("Добавить", f"{c}:") for c in cols]
    if None in vals: return
    with sqlite3.connect(db) as conn:
        conn.execute(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join('?'*len(vals))})", vals)
        conn.commit()
    load()

def delete():
    i = tree.focus()
    if not i: return
    row = tree.item(i)["values"]
    with sqlite3.connect(db) as conn:
        conn.execute(f"DELETE FROM {table.get()} WHERE id=?", (row[0],))
        conn.commit()
    tree.delete(i)

root = tk.Tk(); root.title("SQLite GUI"); root.geometry("700x400")
table = tk.StringVar(value="users")
ttk.Combobox(root, textvariable=table, values=["users", "departments", "employees"]).pack()
f = tk.Frame(root); f.pack()
tk.Button(f, text="Загрузить", command=load).pack(side="left")
tk.Button(f, text="Добавить", command=add).pack(side="left")
tk.Button(f, text="Удалить", command=delete).pack(side="left")
tree = ttk.Treeview(root); tree.pack(fill="both", expand=True); tree.bind("<Double-1>", edit)
root.mainloop()