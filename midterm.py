import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

COLOR_BG = "grey"         
COLOR_PRIMARY = "#2C3E50"    
COLOR_SECONDARY = "#16A085"  
COLOR_ACCENT = "#27AE60"     
COLOR_DANGER = "#C0392B"     
COLOR_WHITE = "#FFFFFF"

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")
conn.commit()


def add_employee():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    phone = phone_entry.get().strip()
    city = city_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not age or not phone or not city or not email:
        messagebox.showwarning("Warning", "Please fill in all blank fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    cursor.execute(
        "INSERT INTO employees(name, age, phone, city, email) VALUES (?, ?, ?, ?, ?)",
        (name, age, phone, city, email)
    )
    conn.commit()
    messagebox.showinfo("Success", "Employee added successfully.")

    clear_fields()
    display_employees()


def display_employees(search_query=""):
    for item in tree.get_children():
        tree.delete(item)

    if search_query:
        cursor.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR city LIKE ? OR email LIKE ?",
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        )
    else:
        cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    for employee in employees:
        # employee[0] is id (used as iid), values are name(1), age(2), phone(3), city(4), email(5)
        tree.insert("", tk.END, iid=employee[0],
                    values=(employee[1], employee[2], employee[3], employee[4], employee[5]))


def search_employees(*args):
    query = search_entry.get().strip()
    display_employees(query)


def update_employee():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an employee to update.")
        return

    employee_id = selected[0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    phone = phone_entry.get().strip()
    city = city_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not age or not phone or not city or not email:
        messagebox.showwarning("Warning", "Please fill in all blank fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    cursor.execute("""
        UPDATE employees
        SET name = ?, age = ?, phone = ?, city = ?, email = ?
        WHERE id = ?
    """, (name, age, phone, city, email, employee_id))

    conn.commit()
    messagebox.showinfo("Success", "Employee updated successfully.")

    clear_fields()
    display_employees()


def delete_employee():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Click the employee to delete.")
        return

    employee_id = selected[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Do you want to delete this employee?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )
        conn.commit()
        messagebox.showinfo("Success", "Employee deleted successfully.")

        clear_fields()
        display_employees()


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def exit_program():
    confirm = messagebox.askyesno(
        "Exit",
        "Do you want to exit the program?"
    )
    if confirm:
        conn.close()
        root.destroy()


def select_employee(event):
    selected = tree.selection()

    if selected:
        employee = tree.item(selected[0])["values"]

        clear_fields()
        name_entry.insert(0, employee[0])
        age_entry.insert(0, employee[1])
        phone_entry.insert(0, employee[2])
        city_entry.insert(0, employee[3])
        email_entry.insert(0, employee[4])


root = tk.Tk()
root.title("Employee Management System")
root.geometry("1100x540")  # Expanded width to comfortably fit fields in one row
root.configure(bg=COLOR_BG)

title_label = tk.Label(
    root,
    text="Employee Management System",
    font=("Arial", 16, "bold"),
    bg=COLOR_BG,
    fg=COLOR_PRIMARY
)
title_label.pack(pady=15)

# Input Frame - Fields arranged in a single horizontal row
input_frame = tk.Frame(root, bd=2, relief="groove", bg=COLOR_WHITE)
input_frame.pack(pady=5, padx=20, ipadx=10, ipady=10)

# Name
tk.Label(input_frame, text="Name:", font=("Arial", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).grid(row=0, column=0, padx=4, pady=6, sticky="e")
name_entry = tk.Entry(input_frame, width=15, font=("Arial", 9), bd=1, relief="solid")
name_entry.grid(row=0, column=1, padx=4, pady=6)

# Age
tk.Label(input_frame, text="Age:", font=("Arial", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).grid(row=0, column=2, padx=4, pady=6, sticky="e")
age_entry = tk.Entry(input_frame, width=6, font=("Arial", 9), bd=1, relief="solid")
age_entry.grid(row=0, column=3, padx=4, pady=6)

# Phone Number
tk.Label(input_frame, text="Phone:", font=("Arial", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).grid(row=0, column=4, padx=4, pady=6, sticky="e")
phone_entry = tk.Entry(input_frame, width=15, font=("Arial", 9), bd=1, relief="solid")
phone_entry.grid(row=0, column=5, padx=4, pady=6)

# City
tk.Label(input_frame, text="City:", font=("Arial", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).grid(row=0, column=6, padx=4, pady=6, sticky="e")
city_entry = tk.Entry(input_frame, width=12, font=("Arial", 9), bd=1, relief="solid")
city_entry.grid(row=0, column=7, padx=4, pady=6)

# Email
tk.Label(input_frame, text="Email:", font=("Arial", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).grid(row=0, column=8, padx=4, pady=6, sticky="e")
email_entry = tk.Entry(input_frame, width=20, font=("Arial", 9), bd=1, relief="solid")
email_entry.grid(row=0, column=9, padx=4, pady=6)

search_frame = tk.Frame(root, bg=COLOR_BG)
search_frame.pack(pady=5)

tk.Label(
    search_frame, text="Search (Name/City/Email):",
    font=("Arial", 10, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY
).pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10), bd=1, relief="solid")
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<KeyRelease>", search_employees)

button_frame = tk.Frame(root, bg=COLOR_BG)
button_frame.pack(pady=10)

tk.Button(
    button_frame, text="Add", width=10,
    font=("Arial", 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_WHITE,
    activebackground="#219653", activeforeground=COLOR_WHITE, relief="flat",
    command=add_employee
).grid(row=0, column=0, padx=6)

tk.Button(
    button_frame, text="Update", width=10,
    font=("Arial", 10, "bold"), bg=COLOR_SECONDARY, fg=COLOR_WHITE,
    activebackground="#117A65", activeforeground=COLOR_WHITE, relief="flat",
    command=update_employee
).grid(row=0, column=1, padx=6)

tk.Button(
    button_frame, text="Delete", width=10,
    font=("Arial", 10, "bold"), bg=COLOR_DANGER, fg=COLOR_WHITE,
    activebackground="#A93226", activeforeground=COLOR_WHITE, relief="flat",
    command=delete_employee
).grid(row=0, column=2, padx=6)

tk.Button(
    button_frame, text="Clear", width=10,
    font=("Arial", 10, "bold"), bg="#7F8C8D", fg=COLOR_WHITE,
    activebackground="#626868", activeforeground=COLOR_WHITE, relief="flat",
    command=clear_fields
).grid(row=0, column=3, padx=6)

tk.Button(
    button_frame, text="Exit", width=10,
    font=("Arial", 10, "bold"), bg="#34495E", fg=COLOR_WHITE,
    activebackground="#2C3E50", activeforeground=COLOR_WHITE, relief="flat",
    command=exit_program
).grid(row=0, column=4, padx=6)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold"),
    background=COLOR_PRIMARY,
    foreground=COLOR_WHITE
)
style.map("Treeview.Heading", background=[('active', COLOR_SECONDARY)])

style.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=28,
    fieldbackground=COLOR_WHITE
)

tree = ttk.Treeview(
    root,
    columns=("Name", "Age", "Phone", "City", "Email"),
    show="headings"
)

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Phone", text="Phone")
tree.heading("City", text="City")
tree.heading("Email", text="Email")

tree.column("Name", width=150)
tree.column("Age", width=60, anchor="center")
tree.column("Phone", width=120)
tree.column("City", width=120)
tree.column("Email", width=200)

tree.pack(padx=20, pady=10, fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", select_employee)

display_employees()

root.mainloop()
