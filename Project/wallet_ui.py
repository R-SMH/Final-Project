import customtkinter as ctk
from tkinter import messagebox


class WalletWindow(ctk.CTkToplevel):
    def __init__(self, master, current_balance=0, on_balance_update=None):
        super().__init__(master)
        self.title("Your Wallet")
        self.geometry("400x350")
        self.resizable(False, False)
        self.current_balance = current_balance
        self.on_balance_update = on_balance_update 
        ctk.CTkLabel(self, text="Your Wallet", font=("Arial", 20, "bold")).pack(pady=10)

        self.balance_label = ctk.CTkLabel(self, text=f"Balance: ${self.current_balance:.2f}", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        ctk.CTkLabel(self, text="Add Balance", font=("Arial", 14)).pack(pady=(10, 5))

        self.card_entry = ctk.CTkEntry(self, placeholder_text="Credit/Debit Card Number")
        self.card_entry.pack(pady=5)

        self.cvv_entry = ctk.CTkEntry(self, placeholder_text="CVV", show="*")
        self.cvv_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Amount")
        self.amount_entry.pack(pady=5)

        ctk.CTkButton(self, text="Add to Wallet", command=self.add_balance).pack(pady=15)

    def add_balance(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid amount.")
            return

        self.current_balance += amount
        self.balance_label.configure(text=f"Balance: ${self.current_balance:.2f}")
        if self.on_balance_update:
            self.on_balance_update(self.current_balance)
        
        messagebox.showinfo("Success", f"${amount:.2f} added to your wallet.")
        self.amount_entry.delete(0, "end")
        self.destroy()  # Close the wallet window after adding balance
        return self.current_balance

