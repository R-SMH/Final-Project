import customtkinter as ctk
from tkinter import messagebox, simpledialog
import socket
import threading
import json

class Dashboard(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Auction Dashboard")
        self.geometry("600x500")
        self.resizable(False, False)

        # Connect to server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("127.0.0.1", 5555))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
            self.destroy()
            return

        # UI Components
        ctk.CTkLabel(self, text=f"Welcome {self.username}!", font=("Arial", 20, "bold")).pack(pady=10)

        self.auction_box = ctk.CTkTextbox(self, width=550, height=300)
        self.auction_box.pack(pady=10)

        self.bid_button = ctk.CTkButton(self, text="Place Bid", command=self.place_bid)
        self.bid_button.pack(pady=5)

        self.add_item_button = ctk.CTkButton(self, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.auctions = {}

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                message = json.loads(data)
                if message['type'] == 'update':
                    self.auctions = message['auctions']
                    self.refresh_auctions()
                elif message['type'] == 'error':
                    messagebox.showerror("Error", message['message'])
            except Exception as e:
                print("Receive error:", e)
                break

    def refresh_auctions(self):
        self.auction_box.delete("1.0", "end")
        for item_id, info in self.auctions.items():
            line = f"ID: {item_id} | {info['name']} | Highest Bid: ${info['highest_bid']} by {info['bidder'] or 'None'}\n"
            self.auction_box.insert("end", line)

    def place_bid(self):
        try:
            item_id = simpledialog.askinteger("Place Bid", "Enter Item ID:")
            bid = simpledialog.askinteger("Place Bid", "Enter Your Bid Amount:")
            if item_id is not None and bid is not None:
                payload = json.dumps({
                    "type": "bid",
                    "item_id": item_id,
                    "amount": bid,
                    "user": self.username
                })
                self.socket.sendall(payload.encode())
        except Exception as e:
            messagebox.showerror("Error", f"Bid failed: {e}")

    def add_item(self):
        try:
            item_name = simpledialog.askstring("Add Item", "Enter Item Name:")
            if item_name:
                payload = json.dumps({
                    "type": "new_item",
                    "name": item_name
                })
                self.socket.sendall(payload.encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")

    def on_close(self):
        try:
            self.socket.close()
        except:
            pass
        self.destroy()

# For testing independently:
if __name__ == "__main__":
    app = Dashboard("test_user@example.com")
    app.mainloop()

