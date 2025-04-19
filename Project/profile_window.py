import customtkinter as ctk
from tkinter import messagebox

class ProfileWindow(ctk.CTkToplevel):
    def __init__(self, master, user_data, on_save=None):
        super().__init__(master)
        self.title("User Profile")
        self.geometry("400x500")
        self.resizable(False, False)

        self.on_save = on_save
        self.user_data = user_data

        ctk.CTkLabel(self, text="Profile", font=("Arial", 20, "bold")).pack(pady=15)

        self.entries = {}
        fields = [
            ("Username", "username"),
            ("User ID", "user_id"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Date of Birth", "dob"),
            ("Balance", "balance")
        ]

        for label_text, key in fields:
            ctk.CTkLabel(self, text=label_text, font=("Arial", 14)).pack(pady=(10, 2))
            entry = ctk.CTkEntry(self)
            entry.insert(0, str(user_data.get(key, "")))
            entry.pack(pady=2)
            self.entries[key] = entry

        ctk.CTkButton(self, text="Save Changes", command=self.save_profile).pack(pady=20)

    def save_profile(self):
        updated_data = {}
        try:
            for key, entry in self.entries.items():
                val = entry.get()
                if key == "balance":
                    val = float(val)
                updated_data[key] = val

            if self.on_save:
                self.on_save(updated_data)

            messagebox.showinfo("Success", "Profile updated successfully!")
            self.destroy()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for balance.")


