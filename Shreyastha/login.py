import mysql.connector
import customtkinter as ctk
from tkinter import messagebox

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'banik2605',
    'database': 'AuctionDB'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connected")
    
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Login System")

def attempt_login():
    uname = username_entry.get()
    pword = password_entry.get()

    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    cursor.execute(query, (uname, pword))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", f"Welcome, {result[3]}!")  # First name
        log_login(uname, pword, result[0])  # Log attempt in Login table
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def log_login(username, password, user_id):
    insert_query = "INSERT INTO Login (username, password, user_id) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (username, password, user_id))
    conn.commit()
    
ctk.CTkLabel(app, text="Username").pack(pady=10)
username_entry = ctk.CTkEntry(app)
username_entry.pack()

ctk.CTkLabel(app, text="Password").pack(pady=10)
password_entry = ctk.CTkEntry(app, show="*")
password_entry.pack()

ctk.CTkButton(app, text="Login", command=attempt_login).pack(pady=20)

app.mainloop()
