import mysql.connector  # Import MySQL connector
from mysql.connector import Error
import customtkinter as ctk
from tkinter import messagebox


class WalletWindow(ctk.CTkToplevel):
    def __init__(self, master, user_id, current_balance=0, on_balance_update=None):
        super().__init__(master)
        self.title("Your Wallet")
        self.geometry("400x400")
        self.resizable(False, False)
        self.user_id = user_id
        self.current_balance = current_balance
        self.on_balance_update = on_balance_update

        self.lift()
        self.attributes("-topmost", True)

        print(f"Initializing WalletWindow with user_id={self.user_id}")

        try:
            conn = mysql.connector.connect(
                host= "138.47.226.216",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (self.user_id,))
                result = cursor.fetchone()
                print(f"Query result for user_id={self.user_id}: {result}")
                if result:
                    self.current_balance = result[0]
                else:
                    self.current_balance = 0
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                conn.close()

        print(f"Current balance for user_id={self.user_id}: {self.current_balance}")

        # UI Design
        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="💰 Your Wallet", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10, 5))

        self.balance_label = ctk.CTkLabel(main_frame, text=f"Balance: ${self.current_balance:.2f}", font=ctk.CTkFont(size=18))
        self.balance_label.pack(pady=10)

        ctk.CTkLabel(main_frame, text="───────────────", text_color="gray").pack()

        ctk.CTkLabel(main_frame, text="➕ Add Balance", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        self.card_entry = ctk.CTkEntry(main_frame, placeholder_text="Credit/Debit Card Number", width=250)
        self.card_entry.pack(pady=5)

        self.cvv_entry = ctk.CTkEntry(main_frame, placeholder_text="CVV", show="*", width=250)
        self.cvv_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(main_frame, placeholder_text="Amount", width=250)
        self.amount_entry.pack(pady=5)

        ctk.CTkButton(main_frame, text="Add to Wallet", command=self.add_balance, fg_color="#2ecc71", hover_color="#27ae60").pack(pady=15)

    def add_balance(self):
        card_number = self.card_entry.get()
        cvv = self.cvv_entry.get()
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid amount.")
            return

        if not card_number.isdigit() or len(card_number) not in [15, 16]:
            messagebox.showerror("Invalid Card", "Please enter a valid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showerror("Invalid CVV", "Please enter a valid CVV.")
            return

        try:
            conn = mysql.connector.connect(
                host="138.47.226.216",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, self.user_id))
                conn.commit()

                cursor.execute("SELECT * FROM wallet WHERE user_id = %s", (self.user_id,))
                wallet_row = cursor.fetchone()

                if wallet_row:
                    cursor.execute(
                        "UPDATE wallet SET Balance = Balance + %s, CreditCardNumber = %s, cvv = %s WHERE user_id = %s",
                        (amount, card_number, cvv, self.user_id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO wallet (user_id, Balance, CreditCardNumber, cvv) VALUES (%s, %s, %s, %s)",
                        (self.user_id, amount, card_number, cvv)
                    )
                conn.commit()

                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (self.user_id,))
                result = cursor.fetchone()
                if result:
                    self.current_balance = result[0]
                else:
                    messagebox.showerror("Error", "Failed to fetch updated balance.")
                    return

                self.balance_label.configure(text=f"Balance: ${self.current_balance:.2f}")
                if self.on_balance_update:
                    self.after(100, lambda: self.on_balance_update(self.current_balance, amount))  # Pass both balance and added amount
  # Let UI settle

                messagebox.showinfo("Success", f"${amount:.2f} added to your wallet.")
                self.amount_entry.delete(0, "end")
                self.card_entry.delete(0, "end")
                self.cvv_entry.delete(0, "end")

                self.after(300, self.destroy)  # Delay to ensure notification is rendered

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                conn.close()
