import mysql.connector  # Import MySQL connector
from mysql.connector import Error
import customtkinter as ctk
from tkinter import messagebox


class WalletWindow(ctk.CTkToplevel):
    def __init__(self, master, user_id, current_balance=0, on_balance_update=None):
        super().__init__(master)
        self.title("Your Wallet")
        self.geometry("400x350")
        self.resizable(False, False)
        self.user_id = user_id
        self.current_balance = current_balance
        self.on_balance_update = on_balance_update


        # Ensure the window pops up on top
        self.lift()  # Bring the window to the front
        self.attributes("-topmost", True)  # Make it stay on top temporarily

        print(f"Initializing WalletWindow with user_id={self.user_id}")  # Debugging

        # Fetch the user's actual balance from the database
        try:
            conn = mysql.connector.connect(
                host= "138.47.140.139",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (self.user_id,))
                result = cursor.fetchone()
                print(f"Query result for user_id={self.user_id}: {result}")  # Debugging
                if result:
                    self.current_balance = result[0]  # Update the current balance
                else:
                    self.current_balance = 0  # Default to 0 if no balance is found
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                conn.close()

        print(f"Current balance for user_id={self.user_id}: {self.current_balance}")  # Debugging

        # UI setup
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
        card_number = self.card_entry.get()
        cvv = self.cvv_entry.get()
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid amount.")
            return

        # Validate card number and CVV (basic validation for demonstration)
        if not card_number.isdigit() or len(card_number) not in [15,16]:
            messagebox.showerror("Invalid Card", "Please enter a valid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showerror("Invalid CVV", "Please enter a valid CVV.")
            return

        # Update the database
        try:
            conn = mysql.connector.connect(
                host="138.47.140.139",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            if conn.is_connected():
                cursor = conn.cursor()

                # Query 1: Update the user's balance in the database
                cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, self.user_id))
                conn.commit()

                # Query 2: Check if a row exists for the user in the wallet table
                try:
                    cursor.execute("SELECT * FROM wallet WHERE user_id = %s", (self.user_id,))
                    wallet_row = cursor.fetchone()

                    if wallet_row:
                        # If a row exists, update the existing row
                        cursor.execute(
                            "UPDATE wallet SET Balance = Balance + %s, CreditCardNumber = %s, cvv = %s WHERE user_id = %s",
                            (amount, card_number, cvv, self.user_id)
                        )
                    else:
                        # If no row exists, insert a new row
                        cursor.execute(
                            "INSERT INTO wallet (user_id, Balance, CreditCardNumber, cvv) VALUES (%s, %s, %s, %s)",
                            (self.user_id, amount, card_number, cvv)
                        )
                    conn.commit()
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred while updating the wallet: {e}")
                    return
                
                # Query 3: Fetch the updated balance from the database
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (self.user_id,))
                result = cursor.fetchone()
                if result:
                    self.current_balance = result[0]  # Update the current balance
                else:
                    messagebox.showerror("Error", "Failed to fetch updated balance.")
                    return

                # Update the UI
                self.balance_label.configure(text=f"Balance: ${self.current_balance:.2f}")
                if self.on_balance_update:
                    self.on_balance_update(self.current_balance)

                # Success message and clear input fields
                messagebox.showinfo("Success", f"${amount:.2f} added to your wallet.")
                self.amount_entry.delete(0, "end")
                self.card_entry.delete(0, "end")
                self.cvv_entry.delete(0, "end")

                self.destroy()  # Close the wallet window after successful transaction
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                conn.close()
