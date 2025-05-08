import customtkinter as ctk
from PIL import Image
import os
import json
from wallet import *  # Assuming wallet_ui.py contains the WalletWindow class
from profile_window import ProfileWindow
from auction_button import create_auction_button
from bidpopup_ui import open_bid_popup


current_balance = 0  # Placeholder for current balance, replace with actual value
total_spent=1000
hosted_auctions = 0  # Placeholder for hosted auctions, replace with actual value
class Dashboard(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.current_balance = current_balance 
        self.hosted_auctions = hosted_auctions
        self.title("Dashboard")
        self.geometry("1200x600")
        self.fetch_user_balance()
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=0)   # Sidebar
        self.main_frame.grid_columnconfigure(1, weight=1)   # Main content
        self.main_frame.grid_rowconfigure(0, weight=0)  # Top bar
        self.main_frame.grid_rowconfigure(1, weight=0)  # Summary label
        self.main_frame.grid_rowconfigure(2, weight=0)  # Summary cards
        self.main_frame.grid_rowconfigure(3, weight=1)  # Auction section
        
        self.top_bar = ctk.CTkFrame(master=self.main_frame, height=70)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="new")
        self.top_bar.grid_propagate(False)
        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=0)
        
        platform_title = ctk.CTkLabel(self.top_bar, text="BidMasters", font=("Arial", 25, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="nsw")
        
        icon_path = "assets/user_icon.png"
        self.icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(32, 32))

        account_btn = ctk.CTkButton(
            master=self.top_bar,
            image=self.icon_image,
            text="",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=self.open_profile_window_func  # Corrected function call
        )
        account_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        # 
        sidebar_container = ctk.CTkFrame(master=self.main_frame)
        sidebar_container.grid(row=1, column=0, rowspan=3, sticky="ns")

        # 
        sidebar_canvas = ctk.CTkCanvas(sidebar_container, bg='#2b2b2b', highlightthickness=0, bd=0)
        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # 
        sidebar_canvas.configure(width=250)
        sidebar_canvas.pack(side="left", fill="y", expand=True)
        
        ctk.CTkButton(
                master=scrollable_frame,
                text="Home",
                width=130,
                anchor="w",
                command = self.load_home_view
            ).pack(pady=3, padx=(5, 5))
        
        auction_btn = ctk.CTkButton(
                master=scrollable_frame,
                text="Auction",
                width=130,
                anchor="w",
                command=self.load_auction_view  # Corrected function call
            )

            
        auction_btn.pack(pady=3, padx=(5, 5))

        wallet_button = ctk.CTkButton(
            master=scrollable_frame,
            text="Wallet",
            width=130,
            anchor="w",
            command=self.open_wallet_ui
        )
        wallet_button.pack(pady=3, padx=(5, 5))

        ctk.CTkButton(
            master=scrollable_frame,
            text="➕ Add Auction Item",
            width=130,
            anchor="w",
            command=self.open_add_item_window
        ).pack(pady=15, padx=0)

        self.load_home_view(user_id)
        
    def load_home_view(self, user_id=None):
        if user_id is not None:
            self.user_id = user_id

        self.fetch_hosted_auctions()

        # Clear any previously rendered widgets on the right
        for widget in self.main_frame.grid_slaves():
            info = widget.grid_info()
            if int(info["column"]) == 1 and int(info["row"]) >= 1:
                widget.destroy()

        self.summary_label = ctk.CTkLabel(master=self.main_frame, text="Summary", font=("Arial", 18, "bold"))
        self.summary_label.grid(row=1, column=1, sticky="nw", padx=10, pady=(10, 0))

        self.summary_frame = ctk.CTkFrame(master=self.main_frame, height=100)
        self.summary_frame.grid(row=2, column=1, sticky="new", padx=10, pady=(5, 0))
        self.summary_frame.grid_propagate(False)
        self.summary_frame.grid_columnconfigure((0, 1), weight=1)

        

        self.display_data = [
            ("Balance", f"$ {self.current_balance:.2f}"),
            ("Active Auctions", f"{self.hosted_auctions}"),
        ]

        self.balance_summary_label = None
        for i, (label, value) in enumerate(self.display_data):
            card = ctk.CTkFrame(master=self.summary_frame, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))
            if label == "Balance":
                self.balance_summary_label = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"))
                self.balance_summary_label.pack(expand=True)
            else:
                ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(expand=True)

        # Auction + Notification Section
        self.auction_section = ctk.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.auction_section.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        self.auction_section.grid_columnconfigure(0, weight=4)
        self.auction_section.grid_columnconfigure(1, weight=2)
        self.auction_section.grid_rowconfigure(1, weight=1)

        self.auction_label = ctk.CTkLabel(master=self.auction_section, text="My Auctions", font=("Arial", 18, "bold"))
        self.auction_label.grid(row=0, column=0, sticky="w", padx=5)

        self.add_auction_btn = ctk.CTkButton(
            master=self.auction_section,
            text="Add Auction",
            width=60,
            height=30,
            corner_radius=8,
            command=self.open_add_item_window
        )
        self.add_auction_btn.grid(row=0, column=1, sticky="e", padx=10)

        self.scroll_container = ctk.CTkFrame(master=self.auction_section)
        self.scroll_container.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.scroll_container.grid_rowconfigure(0, weight=1)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        self.auction_canvas = ctk.CTkCanvas(self.scroll_container, bg="#2b2b2b", highlightthickness=0)
        self.auction_scrollbar = ctk.CTkScrollbar(master=self.scroll_container, orientation="vertical", command=self.auction_canvas.yview)

        self.scrollable_list = ctk.CTkFrame(master=self.auction_canvas)
        self.scroll_window = self.auction_canvas.create_window((0, 0), window=self.scrollable_list, anchor="nw")

        self.scrollable_list.bind("<Configure>", lambda e: self.auction_canvas.configure(scrollregion=self.auction_canvas.bbox("all")))

        self.auction_canvas.configure(yscrollcommand=self.auction_scrollbar.set)
        self.auction_canvas.grid(row=0, column=0, sticky="nsew")
        self.auction_scrollbar.grid(row=0, column=1, sticky="ns")

        # NOTIFICATION PANEL
        self.notification_panel = ctk.CTkFrame(master=self.auction_section, fg_color="#3a3a3a", corner_radius=8)
        self.notification_panel.grid(row=1, column=1, sticky="nsew")
        self.notification_panel.grid_columnconfigure(0, weight=1)
        self.notification_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.notification_panel, text="Notifications", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.notification_list = ctk.CTkScrollableFrame(self.notification_panel, fg_color="#2b2b2b", corner_radius=5)
        self.notification_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Load notifications from the JSON file
        try:
            with open("notifications.json", "r") as file:
                notifications = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            notifications = []

        self.display_notifications()



        my_auctions = self.fetch_my_auctions()

        self.render_cards(my_auctions, self.scrollable_list, columns=3)

    def fetch_user_balance(self):
        try:
            conn = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = conn.cursor()
            query = "SELECT balance FROM Users WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()

            if result:
                self.current_balance = float(result[0])  # Update the current balance
            else:
                self.current_balance = 0.00  # Default to 0 if no balance is found

            print(f"Fetched balance for user_id={self.user_id}: {self.current_balance}")  # Debugging

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching the balance: {e}")
        finally:
            if conn.is_connected():
                conn.close()
    
    def fetch_auctions_from_db(self):
        """Fetch auction items from the NormalAuction table."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT auction_id, itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
            """
            cursor.execute(query)
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_my_auctions(self):
    #Fetch auctions created by the current user.
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT auction_id, itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
                WHERE User_ID = %s
            """
            cursor.execute(query, (self.user_id,))
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_my_bids(self):
        """Fetch auctions where the current user has placed bids."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT auction_id, itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
                WHERE bidder_id = %s
            """
            cursor.execute(query, (self.user_id,))
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def fetch_all_auctions(self):
        """Fetch all auctions."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT auction_id, itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
            """
            cursor.execute(query)
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def fetch_hosted_auctions(self):
        """Fetch the count of auctions hosted by the current user."""
        try:
            conn = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = conn.cursor()
            query = """
                SELECT COUNT(*) AS hosted_auctions
                FROM NormalAuction
                WHERE User_ID = %s
            """
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()

            if result:
                self.hosted_auctions = int(result[0])  # Update the hosted auctions count
            else:
                self.hosted_auctions = 0  # Default to 0 if no hosted auctions are found

      

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching hosted auctions: {e}")
        finally:
            if conn.is_connected():
                conn.close()


#=========================================================================================================================
    def load_auction_view(self):
        # Step 1: Clear previous content on right side
        
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    info = child.grid_info()
                    if int(info.get("column", -1)) == 1 and int(info.get("row", -1)) >= 1:
                        child.grid_forget()
        
        
        # Step 2: Auction view container
        self.auction_view = ctk.CTkFrame(master = self.main_frame, fg_color="#2b2b2b", width=800)
        self.auction_view.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.auction_view.grid_columnconfigure(0, weight=1) 
        self.auction_view.grid_rowconfigure(0, weight=0)
        self.auction_view.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.auction_view, height=28, fg_color = "transparent", width=800)
        search_frame.grid(row=0, column=0, columnspan=1, sticky="ne", pady=(2, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0)  # Button column
        search_frame.grid_propagate(True)  # Prevent resizing
        search_frame.configure(height=30)

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search auctions...", height=28, width=250, border_width=1, corner_radius=0)
        # search_entry.pack(side="left", padx=10)
        search_entry.grid(row=0, column=0, sticky="new", padx=(5, 0), pady=(5, 0))
        search_entry.grid_propagate(True)  # 

        search_button = ctk.CTkButton(search_frame, text="Search", height=28, width=60, corner_radius=0, command=lambda:  self.perform_search(search_entry.get(),))
        search_button.grid(row=0, column=0, sticky="ne" ,padx=(5, 0), pady=(5, 0))
        search_button.grid_propagate(True)  # Prevent resizing
        # search_button.pack(side="left", padx=5)


        # Step 3: Scrollable canvas
        self.canvas = ctk.CTkCanvas(self.auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.auction_view, orientation="vertical", command=self.canvas.yview,)
        scroll_frame = ctk.CTkFrame(master=self.auction_view) # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew") 
        scrollbar.grid(row=1, column=1, sticky="ns")


        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))
        # self.canvas.itemconfig(self.auction_view, width=800)
        # self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

         # Step 4: Fetch and render auction data
        for widget in scroll_frame.winfo_children():
            widget.destroy()  # Clear existing widgets in the scroll frame


        # Step 4: Load auction data
        my_bids = self.fetch_my_bids() ###Change to fetch_my_bids when bidding logic is working
        all_auctions = self.fetch_all_auctions()


        ctk.CTkLabel(scroll_frame, text="My Bids", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        self.render_cards(my_bids, self.my_auction_grid, columns=5)


        # Separator
        ctk.CTkFrame(scroll_frame, height=2, fg_color="#666").pack(fill="x", pady=10)

        ctk.CTkLabel(scroll_frame, text="All Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.all_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.all_auction_grid.pack(anchor="nw")
        self.render_cards(all_auctions, self.all_auction_grid, columns=5)

        #all_auctions = self.load_all_auctions()


#=========================================================================================================================
        

#=========================================================================================================================
        
    def open_add_item_window(self):
        from add_auction import Add_Auction_Window

        # Open the Add Auction Window
        def on_submit():
            self.load_auction_view()  # Refresh the auction view after adding an item

        Add_Auction_Window(self, user_id=self.user_id, on_submit=on_submit)
            
    def open_wallet_ui(self):
            Wallet = WalletWindow(self, user_id=self.user_id, current_balance=self.current_balance, on_balance_update=self.update_balance)
            Wallet.grab_set()
            
    def get_summary_data(self, username):
        return [self.current_balance, 5, 3, 1500]  # Use instance variable!

    def update_balance(self, new_balance, added_amount=0):
        previous_balance = self.current_balance
        self.current_balance = new_balance

        if self.balance_summary_label:
            self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")

        if added_amount > 0:
            self.add_notification(self.user_id, f"💰 You added ${added_amount:.2f} to your wallet.")
        elif new_balance < previous_balance:
            self.add_notification(self.user_id, f"📉 You spent ${previous_balance - new_balance:.2f}.")




    def load_all_auctions(self):
        """Fetch all auctions from the database."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
            """
            cursor.execute(query)
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_all_auctions(self):
        """Fetch all auctions from the database."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
            """
            ####### ADDD MORE QUERIES HERE ###########
            ####### ADDD MORE QUERIES HERE ###########
            ####### ADDD MORE QUERIES HERE ###########
            cursor.execute(query)
            auctions = cursor.fetchall()
            return auctions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            
    def open_profile_window_func(self):
        try:
            conn = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT username, user_id, first_name, last_name, dob, balance, imagelink
                FROM Users WHERE user_id = %s
            """
            cursor.execute(query, (self.user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                messagebox.showerror("Error", "User data not found.")
                return

            # Ensure the image path is included in the user_data dictionary
            user_data["profile_image_path"] = user_data.get("imagelink", "assets/profile.png")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return
        finally:
            if conn.is_connected():
                conn.close()

        # Pass the handle_profile_save method to ProfileWindow
        ProfileWindow(self, user_data, on_save=self.handle_profile_save).grab_set()

    def handle_profile_save(self, updated_data):
        try:
            print("Saving the following data to the database:", updated_data)  # Debugging
            conn = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = conn.cursor()
            update_query = """
                UPDATE Users
                SET username = %s, first_name = %s, last_name = %s, dob = %s, balance = %s, imagelink = %s
                WHERE user_id = %s
            """
            cursor.execute(update_query, (
                updated_data["username"],
                updated_data["first_name"],
                updated_data["last_name"],
                updated_data["dob"],
                updated_data["balance"],
                updated_data["profile_image_path"],  # Ensure this matches the key in updated_data
                self.user_id
            ))
            conn.commit()
            print("Profile updated successfully in the database.")  # Debugging
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")  # Debugging
            messagebox.showerror("Database Error", f"An error occurred while saving: {e}")
        finally:
            if conn.is_connected():
                conn.close()


    def refresh_ui(self):
        # Fetch the updated user balance
        self.fetch_user_balance()

        # Update the balance summary label
        if hasattr(self, "balance_summary_label") and self.balance_summary_label:
            self.balance_summary_label.configure(text=f"$ {self.current_balance:.2f}")
            print(f"[DEBUG] Balance summary label updated to: ${self.current_balance:.2f}")

        # Refresh other UI components (e.g., auction details)
        self.load_home_view(self.user_id)
        print("[DEBUG] UI refreshed successfully.")

    def render_auction_cards(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        my_auctions = self.fetch_my_auctions()
        columns = 3
        
        for index, auction in enumerate(my_auctions):
            row = index // columns
            col = index % columns

            card = ctk.CTkFrame(master=self.scrollable_list, width=250, height=280, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False)

            if "image" in auction and os.path.exists(auction["image"]):
                auction_image = ctk.CTkImage(Image.open(auction["image"]), size=(230, 120))
                image_label = ctk.CTkLabel(card, image=auction_image, text="")
                image_label.image = auction_image
            else:
                image_label = ctk.CTkLabel(card, text="[Image Here]", width=230, height=120, fg_color="#444")

            image_label.pack(pady=(10, 5), padx=10)

            ctk.CTkLabel(card, text=auction["itemName"], font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Current: {auction['StartingPrice']}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['Auctionlength']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkButton(
    card,
    text="Bid Now",
    command=lambda a=auction: open_bid_popup(
        self,
        a["auction_id"],  # Pass the auction_id instead of the entire auction dictionary
        user_id=self.user_id,
        refresh_ui=self.refresh_ui,
        add_notification=self.add_notification
    )
).pack(pady=(5, 10))
# ------------------------------------------------------------------------
    def render_cards(self, auctions, parent_frame, columns=4):

        # Clear existing widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Iterate over auctions and create cards
        for i, auction in enumerate(auctions):
            row = i // columns
            col = i % columns

            # Create a card for each auction
            card = ctk.CTkFrame(master=parent_frame, width=250, height=280, corner_radius=10, fg_color="#3b3b39")
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False)

            # Render image
            if auction["Imagelink"] and os.path.exists(auction["Imagelink"]):
                auction_image = ctk.CTkImage(Image.open(auction["Imagelink"]), size=(230, 120))
                image_label = ctk.CTkLabel(card, image=auction_image, text="")
                image_label.image = auction_image
                image_label.pack(pady=(10, 5))
            else:
                ctk.CTkLabel(card, text="[Image Here]", width=230, height=120, fg_color="#444").pack(pady=(10, 5))

            # Render auction details (move these inside the loop)
            ctk.CTkLabel(card, text=auction["itemName"], font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Current Price: ${auction['CurrentPrice']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Auction Length: {auction['Auctionlength']}", font=("Arial", 10)).pack(anchor="w", padx=10)
            ctk.CTkButton(
    card,
    text="Bid Now",
    command=lambda a=auction: open_bid_popup(
        self,
        a["auction_id"],  # Pass the auction_id instead of the entire auction dictionary
        user_id=self.user_id,
        refresh_ui=self.refresh_ui,
        add_notification=self.add_notification
    )
).pack(pady=(5, 10))
# ------------------------------------------------------------------------
    def perform_search(self, query):
        """Search auctions using SQL."""
        searched_with = query
        query = query.lower()

        if query == "":
            self.load_auction_view()
            return

        try:
            # Connect to the database and perform the search
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            search_query = """
                SELECT itemName, StartingPrice, CurrentPrice, itemDescription, Auctionlength, Imagelink
                FROM NormalAuction
                WHERE LOWER(itemName) LIKE %s
            """
            cursor.execute(search_query, (f"%{query}%",))
            filtered_auctions = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            filtered_auctions = []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # Render the search results
        self.canvas = ctk.CTkCanvas(self.auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.auction_view, orientation="vertical", command=self.canvas.yview)
        scroll_frame = ctk.CTkFrame(master=self.auction_view)  # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw")  # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))

        ctk.CTkLabel(scroll_frame, text=f"Searching for {searched_with}", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")

        if not filtered_auctions:
            ctk.CTkLabel(scroll_frame, text="No results found", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="center")
        else:
            self.render_cards(filtered_auctions, self.my_auction_grid, columns=5)

    def add_notification(self, user_id, message):
        """Add a notification to the database for the specified user."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor()

            # Insert the new notification into the Notifications table
            query = "INSERT INTO Notifications (user_id, message) VALUES (%s, %s)"
            cursor.execute(query, (user_id, message))
            connection.commit()

            # Refresh the notifications panel if the notification is for the current user
            if user_id == self.user_id:
                self.display_notifications()

            print(f"[DEBUG] Added notification for user_id {user_id}: {message}")

        except mysql.connector.Error as err:
            print(f"[ERROR] Database error while adding notification: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def display_notifications(self):
        """Display notifications from the database for the current user."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor()

            # Fetch notifications for the user
            query = "SELECT message FROM Notifications WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            notifications = [row[0] for row in cursor.fetchall()]

            if hasattr(self, 'notification_list'):
                # Clear existing notifications in the UI
                for widget in self.notification_list.winfo_children():
                    widget.destroy()

                # Display each notification
                for message in notifications:
                    # Create a container frame for the message + delete button
                    notif_frame = ctk.CTkFrame(self.notification_list, fg_color="transparent")
                    notif_frame.pack(fill="x", pady=2, padx=5)

                    # Message label
                    notif_label = ctk.CTkLabel(
                        master=notif_frame,
                        text=message,
                        anchor="w",
                        justify="left",
                        wraplength=350,
                        font=("Arial", 13)
                    )
                    notif_label.pack(side="left", fill="x", expand=True, padx=(0, 5))

                    # Delete button
                    delete_btn = ctk.CTkButton(
                        master=notif_frame,
                        text="❌",
                        width=28,
                        height=28,
                        font=("Arial", 12),
                        fg_color="#4a4a4a",
                        hover_color="#d13b3b",
                        command=lambda m=message: self.delete_notification(m)
                    )
                    delete_btn.pack(side="right", padx=2)

        except mysql.connector.Error as err:
            print(f"[ERROR] Database error while displaying notifications: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_notification(self, message):
        """Delete a notification from the database for the current user."""
        try:
            connection = mysql.connector.connect(
                host="138.47.138.4",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor()

            # Delete the notification from the Notifications table
            query = "DELETE FROM Notifications WHERE user_id = %s AND message = %s LIMIT 1"
            cursor.execute(query, (self.user_id, message))
            connection.commit()

            # Refresh the displayed notifications
            self.display_notifications()

            print(f"[DEBUG] Deleted notification: {message}")

        except mysql.connector.Error as err:
            print(f"[ERROR] Database error while deleting notification: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
