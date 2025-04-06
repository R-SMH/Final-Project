import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from dashboard_ui import Dashboard
from register_window import RegisterWindow


themeColor = "green"
open_image = Image.open("assets/RandomPhoto.png")
cover_image = ctk.CTkImage(light_image = open_image, dark_image = open_image, size = (950, 600))

# Main Application Window (to open after login)
def open_main_window():
    Dashboard()

# Login Logic
def login():
    user_id = entry_id.get()
    password = entry_password.
    if user_id and password:
        # login_status = Caden_will_Pass_them(user_id, password)
        '''
        if login_status:
            # app.withdraw()  # Hide login window
            app.destroy()
            Dashboard(user_id).mainloop()
            # open_main_window()

        else :
            messagebox.showerror("Login Failed", "Please check your login credentials")
        '''
    else:
        messagebox.showerror("Login Failed", "Please enter both ID and password.")

# Register Logic
def register():
    RegisterWindow(app)

# Forgot Password Logic
def forgot_password():
    messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")

# Root Login Window
ctk.set_appearance_mode("system")  # Options: "light", "dark", "system"
ctk.set_default_color_theme(themeColor)

app = ctk.CTk()
app.title("Login")
app.geometry("1200x600")

main_frame = ctk.CTkFrame(master=app)
main_frame.pack(fill="both", expand=True)
main_frame.grid_columnconfigure((0, 1, 2), weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Placeholder for cover image on the left (spanning column 0 and 1)
cover_label = ctk.CTkLabel(master=main_frame,image = cover_image,text="", width=800)
cover_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Login block on the right (column 2), centered and shaded
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
