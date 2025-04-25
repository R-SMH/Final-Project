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

class Dashboard(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.current_balance = current_balance 
        self.title("Dashboard")
        self.geometry("1200x600")
        self.fetch_total_spent()
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


        buttons = [
             "Silent Auction"
        ]
        
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
        
        mystery_auction_btn = ctk.CTkButton(
                master=scrollable_frame,
                text="Mystery Auction",
                width=130,
                anchor="w",
                command=self.load_mystery_auction_view  # Corrected function call
            )
        
        mystery_auction_btn.pack(pady=3, padx=(5, 5))
        
        for bt in buttons:
            ctk.CTkButton(
                master=scrollable_frame,
                text=bt,
                width=130,
                anchor="w"
            ).pack(pady=3, padx=(5, 5))


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
        self.summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        summary_data = self.get_summary_data(self.user_id)

        self.display_data = [
            ("Balance", f"$ {self.current_balance:.2f}"),
            ("Active Bids", f"{summary_data[1]}"),
            ("Auctions Won", f"{summary_data[2]}"),
            ("Total Spent", f"$ {self.total_spent:.2f}")
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

        sample_notifications = [
            "✅ You won the 'Smartwatch' auction!",
            "❌ You were outbid on 'Vintage Camera'.",
            "💸 You added $500 to your wallet.",
            "🔔 Someone bid on your 'Headphones' listing!"
        ]

        for note in sample_notifications:
            ctk.CTkLabel(master=self.notification_list, text=note, anchor="w", justify="left", wraplength=400).pack(anchor="w", pady=3)

        self.render_auction_cards()

    def fetch_user_balance(self):
        try:
            conn = mysql.connector.connect(
                host="138.47.140.139",
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
    def fetch_total_spent(self):
        try:
            conn = mysql.connector.connect(
                host="138.47.140.139",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = conn.cursor()
            query = "SELECT totalspent FROM wallet WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()

            if result:
                self.total_spent = float(result[0])  # Update the current balance
            else:
                self.total_spent = 0.00  # Default to 0 if no balance is found

            print(f"Fetched totalspent for user_id={self.user_id}: {self.current_balance}")  # Debugging

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching the balance: {e}")
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


        # Step 4: Load auction data

        my_auctions = self.load_auctions()
        all_auctions = self.load_all_auctions()

        ctk.CTkLabel(scroll_frame, text="My Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        self.render_cards(my_auctions, self.my_auction_grid, columns=5)


        # Separator
        ctk.CTkFrame(scroll_frame, height=2, fg_color="#666").pack(fill="x", pady=10)


        ctk.CTkLabel(scroll_frame, text="All Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        self.render_cards(all_auctions, self.my_auction_grid, columns=5)

        #all_auctions = self.load_all_auctions()

    def load_mystery_auction_view(self):
        # Step 1: Clear previous content on right side
        
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    info = child.grid_info()
                    if int(info.get("column", -1)) == 1 and int(info.get("row", -1)) >= 1:
                        child.grid_forget()
        

        # Step 2: Auction view container
        self.mystery_auction_view = ctk.CTkFrame(master = self.main_frame, fg_color="#2b2b2b", width=800)
        self.mystery_auction_view.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.mystery_auction_view.grid_columnconfigure(0, weight=1) 
        self.mystery_auction_view.grid_rowconfigure(0, weight=0)
        self.mystery_auction_view.grid_rowconfigure(1, weight=1)

        # Step 3: Scrollable canvas
        self.canvas = ctk.CTkCanvas(self.mystery_auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.mystery_auction_view, orientation="vertical", command=self.canvas.yview,)
        scroll_frame = ctk.CTkFrame(master=self.mystery_auction_view) # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew") 
        scrollbar.grid(row=1, column=1, sticky="ns")


        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))
        # self.canvas.itemconfig(self.auction_view, width=800)
        # self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * int(e.delta / 120), "units"))


        # Step 4: Load auction data

        all_mystery_auctions = self.load_all_mystery_auctions()


        ctk.CTkLabel(scroll_frame, text="All Mystery Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        my_mystery_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        my_mystery_auction_grid.pack(anchor="nw")
        self.mystery_render_cards(all_mystery_auctions, my_mystery_auction_grid, columns=5)

        # all_mystery_auctions = self.load_all_mystery_auctions()


#=========================================================================================================================
        

#=========================================================================================================================
        
    def open_add_item_window(self):
            from add_auction import Add_Auction_Window
            Add_Auction_Window(self, on_submit=self.render_auction_cards)
            
    def open_wallet_ui(self):
            Wallet = WalletWindow(self, user_id=self.user_id, current_balance=self.current_balance, on_balance_update=self.update_balance)
            Wallet.get_set()
            
    def get_summary_data(self, username):
        return [self.current_balance, 5, 3, 1500]  # Use instance variable!

    def update_balance(self, new_balance, added_amount=0):
        previous_balance = self.current_balance
        self.current_balance = new_balance

        if self.balance_summary_label:
            self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")

        if added_amount > 0:
            self.add_notification(f"💰 You added ${added_amount:.2f} to your wallet.")
        elif new_balance < previous_balance:
            self.add_notification(f"📉 You spent ${previous_balance - new_balance:.2f}.")




    def load_auctions(self):
        with open("sample_data.json", "r") as f:
            return json.load(f)

    def load_all_auctions(self):
        with open("all_auctions.json", "r") as f:
            return json.load(f)
    
    def load_all_mystery_auctions(self):
        with open("all_mystery_auctions.json", "r") as f:
            return json.load(f)
        
    def render_mystery_auction_cards(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        sample_auctions = self.load_mystery_auctions()
        columns = 3
        
        for index, auction in enumerate(sample_auctions):
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

            ctk.CTkLabel(card, text=f"Current: {auction['price']}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda: "bid now clicked").pack(pady=(5, 10))
    
    def mystery_render_cards(self, auctions, parent_frame, columns=4):
        
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        for i, auction in enumerate(auctions):
            row = i // columns
            col = i % columns

            card = ctk.CTkFrame(master=parent_frame, width=250, height=280, corner_radius=10, fg_color="#3b3b39")
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False) #
            try:
                if "image" in auction and os.path.exists(auction["image"]):
                    img = ctk.CTkImage(Image.open(auction["image"]), size=(200, 100))
                    image_label = ctk.CTkLabel(card, image=img, text="")
                    image_label.image = img
                    image_label.pack(pady=(10, 5))
            except:
                ctk.CTkLabel(card, text="[Image Here]", width=200, height=100, fg_color="#444").pack(pady=(10, 5))

            ctk.CTkLabel(card, text=f"Price: {auction['price']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 10)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda: "bid now clicked").pack(pady=(5, 10))

            
    def open_profile_window_func(self):
        try:
            conn = mysql.connector.connect(
                host="138.47.140.139",
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
                host="138.47.140.139",
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
    def render_auction_cards(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        sample_auctions = self.load_auctions()
        columns = 3
        
        for index, auction in enumerate(sample_auctions):
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

            ctk.CTkLabel(card, text=auction["Name"], font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Current: {auction['price']}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda a=auction: open_bid_popup(self, a, on_submit=lambda bid: self.add_notification(f"✅ You bid ${bid:.2f} on '{a['Name']}'"))).pack(pady=(5, 10))   #bid now button

# ------------------------------------------------------------------------
    def render_cards(self, auctions, parent_frame, columns=4):
        
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        for i, auction in enumerate(auctions):
            row = i // columns
            col = i % columns

            card = ctk.CTkFrame(master=parent_frame, width=250, height=280, corner_radius=10, fg_color="#3b3b39")
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False) #
            
            if "image" in auction and os.path.exists(auction["image"]):
                img = ctk.CTkImage(Image.open(auction["image"]), size=(200, 100))
                image_label = ctk.CTkLabel(card, image=img, text="")
                image_label.image = img
                image_label.pack(pady=(10, 5))
            else:
                ctk.CTkLabel(card, text="[Image Here]", width=200, height=100, fg_color="#444").pack(pady=(10, 5))

            ctk.CTkLabel(card, text=auction["Name"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Price: {auction['price']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 10)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda: "bid now clicked").pack(pady=(5, 10))
# ------------------------------------------------------------------------
    def perform_search(self, query):
        all_auctions = self.load_all_auctions()
        searched_with = query
        query = query.lower()

        if query == "":
            self.load_auction_view()
            return

        filtered_auctions = [
            auction for auction in all_auctions
            if query in auction["Name"].lower()
        ]

        self.canvas = ctk.CTkCanvas(self.auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.auction_view, orientation="vertical", command=self.canvas.yview,)
        scroll_frame = ctk.CTkFrame(master=self.auction_view) # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew") 
        scrollbar.grid(row=1, column=1, sticky="ns")

        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))

        ctk.CTkLabel(scroll_frame, text=f"Searching for {searched_with}", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        if filtered_auctions == []:
            ctk.CTkLabel(scroll_frame, text="No results found", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="center")
        else:
            self.render_cards(filtered_auctions, self.my_auction_grid, columns=5) 
        """
        for widget in self.canvas.winfo_children():
            widget.destroy()

        self.render_cards(filtered_auctions, self.my_auction_grid) if query != "" else self.load_self.auction_view()
        """
    def add_notification(self, message):
        if hasattr(self, 'notification_list'):
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
                command=notif_frame.destroy
            )
            delete_btn.pack(side="right", padx=2)
            print(f"[DEBUG] Adding notification: {message}")




if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
