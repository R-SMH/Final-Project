import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from dashboard_ui import Dashboard

themeColor = "green"
open_image = Image.open("assets/RandomPhoto.png")
cover_image = ctk.CTkImage(light_image = open_image, dark_image = open_image, size = (950, 600))

def open_main_window():
    Dashboard()

def login():
    user_id = entry_id.get()
    password = entry_password.get()
    if user_id and password:
        app.destroy()
        Dashboard().mainloop()

    else:
        messagebox.showerror("Login Failed", "Please enter both ID and password.")

def register():
    messagebox.showinfo("Register", "Registration functionality coming soon!")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme(themeColor)

app = ctk.CTk()
app.title("Login")
app.geometry("1200x600")

main_frame = ctk.CTkFrame(master=app)
main_frame.pack(fill="both", expand=True)
main_frame.grid_columnconfigure((0, 1, 2), weight=1)
main_frame.grid_rowconfigure(0, weight=1)

cover_label = ctk.CTkLabel(master=main_frame,image = cover_image,text="", width=800)
cover_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

login_frame = ctk.CTkFrame(master=main_frame, corner_radius=10)
login_frame.grid(row=0, column=2, padx=40, pady=30, sticky="nsew")
login_frame.grid_propagate(False)
login_frame.configure(width=300, height=350)

ctk.CTkLabel(master=login_frame, text="Login", font=("Arial", 20)).pack(pady=10)

entry_id = ctk.CTkEntry(master=login_frame, placeholder_text="User ID")
entry_id.pack(pady=10)

entry_password = ctk.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
entry_password.pack(pady=(0, 5))

ctk.CTkButton(
    master=login_frame,
    text="Forgot Password?",
    command=forgot_password,
    fg_color="transparent",
    text_color=themeColor,
    hover=False
).pack(pady=(0, 10))

ctk.CTkButton(master=login_frame, text="Login", command=login).pack(pady=5)
ctk.CTkButton(master=login_frame, text="Register", command=register).pack()

app.mainloop()
