import customtkinter as ctk
from tkinter import messagebox

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Register")
        self.geometry("400x500")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set()

        self.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self, text="Register", font=("Arial", 22, "bold")).pack(pady=(20, 10))

        self.entry_first = ctk.CTkEntry(self, placeholder_text="First Name")
        self.entry_first.pack(pady=8, padx=40)

        self.entry_last = ctk.CTkEntry(self, placeholder_text="Last Name")
        self.entry_last.pack(pady=8, padx=40)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email")
        self.entry_email.pack(pady=8, padx=40)
        
        self.entry_dob = ctk.CTkEntry(self, placeholder_text="DOB (MM/DD/YYYY)")
        self.entry_dob.pack(pady=8, padx=40)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=8, padx=40)

        self.entry_confirm = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.entry_confirm.pack(pady=8, padx=40)

        self.terms_checkbox = ctk.CTkCheckBox(self,text="I agree to the Terms and Conditions",command=self.toggle_register_button)
        self.terms_checkbox.pack(pady=(10, 20))

        # Register button
        self.register_btn = ctk.CTkButton(self, text="Register", command=self.submit_form, state="disabled")
        self.register_btn.pack(pady=5)

    def toggle_register_button(self):
        if self.terms_checkbox.get():
            self.register_btn.configure(state="normal")
        else:
            self.register_btn.configure(state="disabled")

    def submit_form(self):
        # Collect input values
        first = self.entry_first.get().strip()
        last = self.entry_last.get().strip()
        email = self.entry_email.get().strip()
        dob = self.entry_dob.get().strip()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()

        # Validate fields
        if not all([first, last, email, dob, password, confirm]):
            messagebox.showerror("Error", "All fields are required.")
            return
        
        # Comparison of password and confirm password fields
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Success placeholder
        messagebox.showinfo("Success", "Registration submitted! (DB pending)")
        self.destroy()
