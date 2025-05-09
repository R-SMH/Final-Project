import customtkinter as ctk
from tkinter import filedialog
import mysql.connector
import json
from PIL import Image, ImageTk

class Add_Mystery_Auction_Window(ctk.CTkToplevel):
    def __init__(self, master=None, on_submit=None):
        super().__init__(master)
        self.on_submit = on_submit
        self.title("Add Mystery Auction Item")
        self.geometry("320x300")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set()

        price_entry = ctk.CTkEntry(self, placeholder_text="Starting Price")
        price_entry.pack(pady=10)

        auction_duration_entry = ctk.CTkEntry(self, placeholder_text="Auction Duration (in hours)")
        auction_duration_entry.pack(pady=10)


        def add_item():
            price = price_entry.get()
            auction_duration = auction_duration_entry.get()
            img_path = open_image = Image.open("assets/QuestionMark.png")()


            # ========== Database Connection Using JSON - For Testing Purposes ==========
            def save_auction_to_database(data):
                # === Placeholder for MySQL INSERT ===
                # Caden: Remove everything below and write something that would 
                # save the 'data' dictionary into your database  

                try:
                    with open("sample_data.json", "r") as f:
                        auctions = json.load(f)
                except FileNotFoundError:
                    auctions = []

                auctions.append(data)

                with open("sample_data.json", "w") as f:
                    json.dump(auctions, f, indent=4)
            # ========== Database Connection Using JSON - For Testing Purposes ==========


            if  price and auction_duration_entry:
                # Save the auction item to the database
                # current_auctions = load_auctions()
                save_auction_to_database({"price": price, "time_left": auction_duration, "image": img_path})
                # current_auctions.append(new_auction)
                # save_auctions(current_auctions)
                if self.on_submit:
                    self.on_submit()  # Tell dashboard to refresh
                self.destroy()

        ctk.CTkButton(self, text="Add Item", command=add_item).pack(pady=20)

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x500")
    Add_Mystery_Auction_Window(app)
    app.mainloop()