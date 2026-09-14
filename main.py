# Expense Tracker DARK PRO v3.1 FIXED - Shruti Mishra
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, re, csv
from datetime import datetime
from collections import defaultdict

DB_NAME = "expense.db"
conn = sqlite3.connect(DB_NAME)
conn.execute('''CREATE TABLE IF NOT EXISTS expenses
            (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, note TEXT)''')
conn.commit(); conn.close()

def is_valid_date(d): return re.match(r"^\d{2}-\d{2}-\d{4}$", d) is not None

BG = "#0F0F10"
CARD = "#1C1C1E"
CARD_BORDER = "#2C2C2E"
ACCENT = "#7C5CFF"
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#8E8E93"
RED = "#FF453A"

def add_expense():
    d, c, a, n = date_entry.get().strip(), cat_combo.get(), amt_entry.get().strip(), note_entry.get().strip()
    if not is_valid_date(d):
        messagebox.showerror("Error", "Date DD-MM-YYYY enter this"); return
    try:
        amt = float(a)
        if amt <= 0: raise ValueError
    except: messagebox.showerror("Error", "Enter the Amount no."); return
    if not c: messagebox.showerror("Error", "Choose your Category"); return
    con = sqlite3.connect(DB_NAME)
    con.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?,?,?,?)", (d,c,amt,n))
    con.commit(); con.close()
    amt_entry.delete(0, tk.END); note_entry.delete(0, tk.END)
    refresh()

def refresh():
    for i in tree.get_children(): tree.delete(i)
    con = sqlite3.connect(DB_NAME)
    rows = con.execute("SELECT * FROM expenses ORDER BY id DESC").fetchall()
    con.close()
    total = sum(r[3] for r in rows)
    cat = defaultdict(float)
    for r in rows: cat[r[2]] += r[3]
    total_lbl.config(text=f"₹ {total:,.0f}")
    total_sub.config(text=f"{len(rows)} Transactions")
    food_lbl.config(text=f"₹ {cat.get('Food',0):,.0f}")
    shop_lbl.config(text=f"₹ {cat.get('Shopping',0):,.0f}")
    travel_lbl.config(text=f"₹ {cat.get('Travel',0):,.0f}")
    for r in rows:
        tree.insert("", tk.END, values=r)

def delete_exp():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Select", "Select a Row to delete"); return
    eid = tree.item(sel[0])['values'][0]
    con = sqlite3.connect(DB_NAME)
    con.execute("DELETE FROM expenses WHERE id=?", (eid,)); con.commit(); con.close()
    refresh()

def export_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
    if not path: return
    con = sqlite3.connect(DB_NAME)
    rows = con.execute("SELECT * FROM expenses").fetchall()
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(["ID","Date","Category","Amount","Note"]); w.writerows(rows)
    messagebox.showinfo("Done", "CSV Export ho gaya!")

# --- UI ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("980x700")
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT_MAIN,
                rowheight=38, font=("Segoe UI", 10), borderwidth=0)
style.configure("Treeview.Heading", background="#232326", foreground=TEXT_MUTED,
                font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[('selected', '#3A345E')])
style.configure("TCombobox", fieldbackground="#2C2C2E", background="#2C2C2E",
                foreground=TEXT_MAIN, arrowcolor=TEXT_MAIN)

header = tk.Frame(root, bg=BG); header.pack(fill="x", padx=25, pady=(20,10))
tk.Label(header, text="EXPENSE TRACKER", bg=BG, fg=TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
tk.Label(header, text="SHRUTI MISHRA", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(side="left", padx=15, pady=5)

dash = tk.Frame(root, bg=BG); dash.pack(fill="x", padx=20, pady=10)
def card(parent, title, amount, sub, accent_color):
    c = tk.Frame(parent, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, bd=0)
    c.pack(side="left", expand=True, fill="both", padx=8)
    tk.Frame(c, bg=accent_color, height=3).pack(fill="x")
    inner = tk.Frame(c, bg=CARD); inner.pack(fill="both", padx=18, pady=14)
    tk.Label(inner, text=title, bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
    lbl = tk.Label(inner, text=amount, bg=CARD, fg=TEXT_MAIN, font=("Segoe UI", 20, "bold"))
    lbl.pack(anchor="w", pady=(6,2))
    sub_lbl = tk.Label(inner, text=sub, bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9))
    sub_lbl.pack(anchor="w")
    return lbl, sub_lbl

total_lbl, total_sub = card(dash, "TOTAL SPENT", "₹ 0", "0 Transactions", ACCENT)
food_lbl, _ = card(dash, "FOOD & DINING", "₹ 0", "32% of total", "#FF9F0A")
shop_lbl, _ = card(dash, "SHOPPING", "₹ 0", "18% of total", "#FF375F")
travel_lbl, _ = card(dash, "TRAVEL", "₹ 0", "12% of total", "#00D1FF")

inp = tk.Frame(root, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1)
inp.pack(fill="x", padx=20, pady=15)

tk.Label(inp, text="Add new transaction", bg=CARD, fg=TEXT_MAIN, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=5, sticky="w", padx=18, pady=(14,6))

# Labels
tk.Label(inp, text="DATE", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).grid(row=1, column=0, padx=18, sticky="w")
tk.Label(inp, text="CATEGORY", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).grid(row=1, column=1, padx=10, sticky="w")
tk.Label(inp, text="AMOUNT", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).grid(row=1, column=2, padx=10, sticky="w")
tk.Label(inp, text="NOTE", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).grid(row=1, column=3, padx=10, sticky="w")

# FIXED ENTRIES - Ab safed text ke saath clear dikhega
entry_style = {"font":("Segoe UI", 10), "bg":"#2C2C2E", "fg":"white", "insertbackground":"white", "bd":0, "relief":"flat", "highlightthickness":1, "highlightbackground":CARD_BORDER, "highlightcolor":ACCENT}

date_entry = tk.Entry(inp, width=14, **entry_style); date_entry.grid(row=2, column=0, padx=18, pady=(2,16), ipady=9)
date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))

cat_combo = ttk.Combobox(inp, values=["Food","Travel","Shopping","Study","Other"], width=15, font=("Segoe UI", 10))
cat_combo.grid(row=2, column=1, padx=10, pady=(2,16), ipady=5)

amt_entry = tk.Entry(inp, width=14, **entry_style); amt_entry.grid(row=2, column=2, padx=10, pady=(2,16), ipady=9)
note_entry = tk.Entry(inp, width=22, **entry_style); note_entry.grid(row=2, column=3, padx=10, pady=(2,16), ipady=9)

# FIXED BUTTON - Ab white box nahi ayega
add_btn = tk.Button(inp, text="ADD EXPENSE →", bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
          bd=0, padx=22, pady=9, activebackground="#6A4FE0", activeforeground="white",
          cursor="hand2", command=add_expense)
add_btn.grid(row=2, column=4, padx=20, pady=(2,16))

tf = tk.Frame(root, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1)
tf.pack(fill="both", expand=True, padx=20, pady=(0,20))

th = tk.Frame(tf, bg=CARD); th.pack(fill="x", padx=18, pady=(15,10))
tk.Label(th, text="Recent Transactions", bg=CARD, fg=TEXT_MAIN, font=("Segoe UI", 12, "bold")).pack(side="left")
tk.Button(th, text="Export CSV", bg="#2C2C2E", fg=TEXT_MAIN, font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=6, command=export_csv).pack(side="right", padx=5)
tk.Button(th, text="Delete", bg="#2C2C2E", fg=RED, font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=6, command=delete_exp).pack(side="right")

tree = ttk.Treeview(tf, columns=("ID","Date","Category","Amount","Note"), show="headings", height=13)
for c in ("ID","Date","Category","Amount","Note"): tree.heading(c, text=c.upper())
tree.column("ID", width=60, anchor="center"); tree.column("Date", width=120, anchor="center")
tree.column("Category", width=120, anchor="center"); tree.column("Amount", width=120, anchor="center")
tree.column("Note", width=320)
tree.pack(fill="both", expand=True, padx=2, pady=2)

refresh()
root.mainloop()