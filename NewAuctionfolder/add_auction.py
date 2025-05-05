import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import mysql.connector

class Add_Auction_Window(ctk.CTkToplevel):
    def __init__(self, master=None, on_submit=None, user_id=None):
        super().__init__(master)
        self.on_submit = on_submit
        self.user_id = user_id
        self.title("Add Auction Item")
        self.geometry("320x400")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set()

        name_entry = ctk.CTkEntry(self, placeholder_text="Item Name")
        name_entry.pack(pady=10)

        price_entry = ctk.CTkEntry(self, placeholder_text="Starting Price")
        price_entry.pack(pady=10)

        auction_duration_entry = ctk.CTkEntry(self, placeholder_text="Auction Duration (in hours)")
        auction_duration_entry.pack(pady=10)

        description_entry = ctk.CTkEntry(self, placeholder_text="Item Description")
        description_entry.pack(pady=10)

        image_path_var = ctk.StringVar()

        
        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        ctk.CTkButton(self, text="📁 Upload Image", command=upload_image).pack(pady=10)
        image_label = ctk.CTkLabel(self, textvariable=image_path_var, font=("Arial", 10), wraplength=250)
        image_label.pack(pady=5)

        def add_item():
            name = name_entry.get()
            price = price_entry.get()
            auction_duration = auction_duration_entry.get()
            description = description_entry.get()
            img_path = image_path_var.get()


            # ========== Database Connection Using JSON - For Testing Purposes ==========
            def save_auction_to_database(data):
                try:
                    # Establish a connection to the MySQL database
                    connection = mysql.connector.connect(
                        host= "138.47.137.36",
                        user="otheruser",
                        passwd="GroupProjectPassword",
                        database="AuctionDB"  # Replace with your MySQL database name
                    )
                    cursor = connection.cursor()

                    # Insert the auction data into the NormalAuction table
                    insert_query = """
                    INSERT INTO NormalAuction (itemName, User_ID, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        data["itemName"],
                        data["user_id"],
                        data["startingprice"],
                        data["currentprice"],
                        data["itemdescription"],
                        data["auctionlength"],
                        data["imagelink"]
                    ))

                    # Commit the transaction
                    connection.commit()

                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
            # ========== Database Connection Using JSON - For Testing Purposes ==========


            if name and price and auction_duration and description:
              
                save_auction_to_database({
                    "itemName": name,
                    "user_id": self.user_id,  # Use the passed user_id
                    "startingprice": price,
                    "currentprice": price,  # Current price matches starting price at creation
                    "itemdescription": description,
                    "auctionlength": auction_duration,
                    "imagelink": img_path
                })
                if self.on_submit:
                    self.on_submit()  # Tell dashboard to refresh
                self.destroy()

        print("Creating Add Item button...")
        ctk.CTkButton(self, text="Add Item", command=add_item).pack(pady=20)
        print("Add Item button created.")
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x500")
    Add_Auction_Window(app)
    app.mainloop()